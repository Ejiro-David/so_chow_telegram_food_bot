"""
SOCHOW Telegram Food Ordering Bot - Python Version
Lightweight implementation using python-telegram-bot + Flask + SQLite

Dependencies (install via pip):
    pip install python-telegram-bot==20.7 flask flask-cors

Environment variables (.env file):
    BOT_TOKEN=your_telegram_bot_token
    ADMIN_CHAT_ID=your_telegram_user_id
    PAYMENT_BANK=First Bank
    PAYMENT_ACCOUNT=1234567890
    PAYMENT_NAME=SOCHOW
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
from threading import Thread
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', 'YOUR_ADMIN_ID')
PORT = int(os.getenv('PORT', 3000))

# ============================================================================
# DATABASE SETUP
# ============================================================================

def init_db():
    """Initialize SQLite database with all tables"""
    conn = sqlite3.connect('sochow.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE NOT NULL,
        name TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Menu items
    c.execute('''CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price_naira INTEGER NOT NULL,
        available INTEGER DEFAULT 1,
        image_url TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Carts
    c.execute('''CREATE TABLE IF NOT EXISTS carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Cart items
    c.execute('''CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER NOT NULL,
        menu_item_id INTEGER NOT NULL,
        qty INTEGER DEFAULT 1,
        unit_price INTEGER NOT NULL,
        FOREIGN KEY (cart_id) REFERENCES carts(id),
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    )''')
    
    # Orders
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        cart_id INTEGER NOT NULL,
        order_id TEXT UNIQUE NOT NULL,
        total_naira INTEGER NOT NULL,
        delivery_address TEXT,
        contact_number TEXT,
        payment_status TEXT DEFAULT 'pending',
        order_status TEXT DEFAULT 'processing',
        rider_contact TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (cart_id) REFERENCES carts(id)
    )''')
    
    # Receipts
    c.execute('''CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        admin_verified INTEGER DEFAULT 0,
        admin_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Menu config (single row for menu image)
    c.execute('''CREATE TABLE IF NOT EXISTS menu_config (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        menu_image_url TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Admin actions log
    c.execute('''CREATE TABLE IF NOT EXISTS admin_actions_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id TEXT,
        order_id INTEGER,
        action TEXT NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()
    print('✅ Database initialized')

# Initialize database on startup
init_db()

def seed_menu_items():
    """Populate database with SOCHOW menu items if empty"""
    db = get_db()
    existing = db.execute('SELECT COUNT(*) as count FROM menu_items').fetchone()
    
    if existing['count'] == 0:
        print('📝 Seeding menu items...')
        menu_data = [
            ('Assorted Pepper Sauce', 15000, 'Spicy mixed-protein pepper sauce with onions & herbs'),
            ('Egusi Soup (Family Bowl)', 37000, 'Rich melon seed soup with assorted meat & vegetables'),
            ('Okro/Ilasa Soup (Family Bowl)', 35000, 'Thick okro-based soup with meats & leafy vegetables'),
            ('Boiled Plantain & Pepper Mix', 9500, 'Soft ripe plantain with spicy peppered fish/meat'),
            ('White Rice & Chicken Curry Sauce', 9000, 'Steamed rice served with aromatic Nigerian curry chicken sauce'),
            ('Native Palm Oil Jollof (Fisherman Style)', 9000, 'Palm-oil infused jollof with smoked fish, ponmo & egg'),
            ('Breakfast Platter', 6000, 'Scrambled eggs, sausages, croissant, strawberries & grapes'),
            ('Fresh Fruit Bowl', 6000, 'Strawberries, blueberries, mango & apples'),
            ('Beans, Fried Plantain & Peppered Fish', 9000, 'Nigerian beans porridge served with spicy fish & plantain'),
            ('White Rice with Fried Plantain & Stew', 9000, 'Boiled rice with crispy plantain and rich tomato stew')
        ]
        
        for name, price, description in menu_data:
            db.execute('''INSERT INTO menu_items (name, price_naira, description, available)
                          VALUES (?, ?, ?, 1)''', (name, price, description))
        
        db.commit()
        db.close()
        print('✅ Menu items seeded successfully')
    else:
        print(f'✅ Menu already has {existing["count"]} items')

def link_menu_photos():
    """Link uploaded food photos to menu items in database - Using exact filenames"""
    
    # Direct mapping of menu item ID to your actual filenames
    photo_mapping = {
        1: 'Assorted Pepper Sauce\t.jpeg',
        2: '02-egusi-soup.jpeg',
        3: 'Ilasa Soup (Family Bowl)\t.jpeg',
        4: 'Boiled Plantain & Pepper Mix.jpeg',
        5: 'Steamed rice served with aromatic Nigerian curry chicken sauce.jpeg',
        6: 'Palm-oil infused jollof with smoked fish, ponmo & egg.jpeg',
        7: 'Scrambled eggs, sausages, croissant, strawberries & grapes.jpeg',
        8: 'Fresh Fruit Bowl.jpeg',
        9: 'Beans, Fried Plantain & Peppered Fish.jpeg',
        10: 'White Rice with Fried Plantain & Stew.jpeg'
    }
    
    db = get_db()
    updated_count = 0
    
    for item_id, filename in photo_mapping.items():
        filepath = f'uploads/{filename}'
        
        # Check if file exists before updating database
        if os.path.exists(filepath):
            db.execute('UPDATE menu_items SET image_url = ? WHERE id = ?', 
                      (f'/uploads/{filename}', item_id))
            updated_count += 1
            print(f'✅ Item {item_id} → {filename}')
        else:
            print(f'⚠️  Item {item_id} → File not found: {filename}')
    
    db.commit()
    db.close()
    
    if updated_count > 0:
        print(f'✅ Linked {updated_count}/10 photos to menu items')
    else:
        print('❌ No photos were linked - check uploads folder!')

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('sochow.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_or_create_user(telegram_id, name):
    """Get or create user from Telegram data"""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE telegram_id = ?', (str(telegram_id),)).fetchone()
    
    if not user:
        db.execute('INSERT INTO users (telegram_id, name) VALUES (?, ?)', (str(telegram_id), name))
        db.commit()
        user = db.execute('SELECT * FROM users WHERE telegram_id = ?', (str(telegram_id),)).fetchone()
        print(f'📝 New user: {name} ({telegram_id})')
    
    db.close()
    return dict(user)

def get_or_create_cart(user_id):
    """Get or create active cart for user"""
    db = get_db()
    cart = db.execute('SELECT * FROM carts WHERE user_id = ? AND status = ?', (user_id, 'active')).fetchone()
    
    if not cart:
        db.execute('INSERT INTO carts (user_id, status) VALUES (?, ?)', (user_id, 'active'))
        db.commit()
        cart = db.execute('SELECT * FROM carts WHERE user_id = ? AND status = ?', (user_id, 'active')).fetchone()
    
    db.close()
    return dict(cart)

def calc_cart_total(cart_id):
    """Calculate cart total"""
    db = get_db()
    result = db.execute('SELECT SUM(qty * unit_price) as total FROM cart_items WHERE cart_id = ?', (cart_id,)).fetchone()
    db.close()
    return result['total'] or 0

def generate_order_id():
    """Generate unique order ID: SOCHOW-YYYYMMDD-XXXX"""
    date_str = datetime.now().strftime('%Y%m%d')
    db = get_db()
    count = db.execute("SELECT COUNT(*) as cnt FROM orders WHERE DATE(created_at) = DATE('now')").fetchone()['cnt']
    db.close()
    sequence = str(count + 1).zfill(4)
    return f'SOCHOW-{date_str}-{sequence}'

# Call seeding functions
seed_menu_items()
link_menu_photos()

print('✅ SOCHOW Bot Ready')

# ============================================================================
# TELEGRAM BOT HANDLERS
# ============================================================================

# Store user states for checkout flow
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    get_or_create_user(user.id, user.first_name)
    
    keyboard = [
        [InlineKeyboardButton("🍽️ View Menu", callback_data="view_menu"),
         InlineKeyboardButton("🛒 My Cart", callback_data="view_cart")],
        [InlineKeyboardButton("📦 Track Order", callback_data="track_order"),
         InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    
    await update.message.reply_text(
        "Welcome to SOCHOW! 👋\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = get_or_create_user(query.from_user.id, query.from_user.first_name)
    data = query.data.split(':')
    action = data[0]
    
    if action == 'view_menu':
        await show_menu(query, user['id'])
    elif action == 'view_cart':
        await show_cart(query, user['id'])
    elif action == 'add_to_cart':
        await add_to_cart(query, user['id'], int(data[1]))
    elif action == 'increase_qty':
        await update_qty(query, user['id'], int(data[1]), 1)
    elif action == 'decrease_qty':
        await update_qty(query, user['id'], int(data[1]), -1)
    elif action == 'clear_cart':
        await clear_cart(query, user['id'])
    elif action == 'checkout':
        await start_checkout(query, user['id'])
    elif action == 'track_order':
        await track_order(query, user['id'])
    elif action == 'help':
        await show_help(query)

async def show_menu(query, user_id):
    """Show menu with items and photos"""
    db = get_db()
    items = db.execute('SELECT * FROM menu_items WHERE available = 1 ORDER BY id').fetchall()
    db.close()
    
    if not items:
        await query.edit_message_text('❌ Menu is currently empty.')
        return
    
    await query.message.reply_text('🍽️ *SOCHOW Menu*\n\nBrowse our delicious dishes below:', 
                                   parse_mode='Markdown')
    
    for item in items:
        caption = f"*{item['name']}* — ₦{item['price_naira']:,}\n\n"
        if item['description']:
            caption += f"_{item['description']}_"
        
        keyboard = [[InlineKeyboardButton(f"➕ Add to Cart", 
                                          callback_data=f"add_to_cart:{item['id']}")]]
        
        if item['image_url']:
            try:
                photo_path = f"uploads/{os.path.basename(item['image_url'])}"
                if os.path.exists(photo_path):
                    with open(photo_path, 'rb') as photo_file:
                        await query.message.reply_photo(
                            photo=photo_file,
                            caption=caption,
                            parse_mode='Markdown',
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
                else:
                    await query.message.reply_text(caption, parse_mode='Markdown', 
                                                  reply_markup=InlineKeyboardMarkup(keyboard))
            except Exception as e:
                print(f'⚠️  Error sending photo for {item["name"]}: {e}')
                await query.message.reply_text(caption, parse_mode='Markdown', 
                                              reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text(caption, parse_mode='Markdown', 
                                          reply_markup=InlineKeyboardMarkup(keyboard))
    
    footer_keyboard = [[InlineKeyboardButton("🛒 View Cart", callback_data="view_cart")]]
    await query.message.reply_text("👆 Add items to cart, then checkout when ready!",
                                   reply_markup=InlineKeyboardMarkup(footer_keyboard))

async def add_to_cart(query, user_id, menu_item_id):
    """Add item to cart"""
    cart = get_or_create_cart(user_id)
    db = get_db()
    
    menu_item = db.execute('SELECT * FROM menu_items WHERE id = ?', (menu_item_id,)).fetchone()
    existing = db.execute('SELECT * FROM cart_items WHERE cart_id = ? AND menu_item_id = ?', 
                          (cart['id'], menu_item_id)).fetchone()
    
    if existing:
        db.execute('UPDATE cart_items SET qty = qty + 1 WHERE id = ?', (existing['id'],))
    else:
        db.execute('INSERT INTO cart_items (cart_id, menu_item_id, qty, unit_price) VALUES (?, ?, 1, ?)',
                   (cart['id'], menu_item_id, menu_item['price_naira']))
    
    db.commit()
    db.close()
    
    await query.message.reply_text(f"✅ {menu_item['name']} added to cart!")
    await show_cart(query, user_id)

async def show_cart(query, user_id):
    """Show cart contents"""
    cart = get_or_create_cart(user_id)
    db = get_db()
    
    items = db.execute('''SELECT ci.*, mi.name, mi.price_naira 
                          FROM cart_items ci 
                          JOIN menu_items mi ON ci.menu_item_id = mi.id 
                          WHERE ci.cart_id = ?''', (cart['id'],)).fetchall()
    db.close()
    
    if not items:
        keyboard = [[InlineKeyboardButton("🍽️ View Menu", callback_data="view_menu")]]
        await query.message.reply_text('🛒 Your cart is empty.', reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    text = '🛒 *Your Cart*\n\n'
    keyboard = []
    
    for item in items:
        total = item['qty'] * item['unit_price']
        text += f"{item['qty']}x {item['name']} — ₦{total:,}\n"
        keyboard.append([
            InlineKeyboardButton(f"➖ {item['name']}", callback_data=f"decrease_qty:{item['id']}"),
            InlineKeyboardButton(f"➕ {item['name']}", callback_data=f"increase_qty:{item['id']}")
        ])
    
    total = calc_cart_total(cart['id'])
    text += f"\n*Subtotal:* ₦{total:,}"
    
    keyboard.extend([
        [InlineKeyboardButton("🧹 Clear Cart", callback_data="clear_cart"),
         InlineKeyboardButton("🍽️ Add More", callback_data="view_menu")],
        [InlineKeyboardButton("✅ Checkout", callback_data="checkout")]
    ])
    
    await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def update_qty(query, user_id, cart_item_id, delta):
    """Update item quantity"""
    db = get_db()
    item = db.execute('SELECT * FROM cart_items WHERE id = ?', (cart_item_id,)).fetchone()
    
    new_qty = item['qty'] + delta
    
    if new_qty <= 0:
        db.execute('DELETE FROM cart_items WHERE id = ?', (cart_item_id,))
        await query.message.reply_text('🗑️ Item removed from cart.')
    else:
        db.execute('UPDATE cart_items SET qty = ? WHERE id = ?', (new_qty, cart_item_id))
    
    db.commit()
    db.close()
    await show_cart(query, user_id)

async def clear_cart(query, user_id):
    """Clear cart"""
    cart = get_or_create_cart(user_id)
    db = get_db()
    db.execute('DELETE FROM cart_items WHERE cart_id = ?', (cart['id'],))
    db.commit()
    db.close()
    
    keyboard = [[InlineKeyboardButton("🍽️ View Menu", callback_data="view_menu")]]
    await query.message.reply_text('🧹 Cart cleared.', reply_markup=InlineKeyboardMarkup(keyboard))

async def start_checkout(query, user_id):
    """Start checkout process"""
    cart = get_or_create_cart(user_id)
    db = get_db()
    items = db.execute('SELECT * FROM cart_items WHERE cart_id = ?', (cart['id'],)).fetchall()
    db.close()
    
    if not items:
        await query.message.reply_text('❌ Your cart is empty.')
        return
    
    user_states[user_id] = {'step': 'awaiting_address', 'cart_id': cart['id']}
    await query.message.reply_text('✅ *Checkout*\n\n🏠 Please enter your delivery address:', parse_mode='Markdown')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages during checkout"""
    user = get_or_create_user(update.effective_user.id, update.effective_user.first_name)
    state = user_states.get(user['id'])
    
    if not state:
        return
    
    if state['step'] == 'awaiting_address':
        state['address'] = update.message.text
        state['step'] = 'awaiting_phone'
        user_states[user['id']] = state
        await update.message.reply_text('📞 Please enter your contact number:')
    
    elif state['step'] == 'awaiting_phone':
        state['phone'] = update.message.text
        await create_order(update, user, state)
        del user_states[user['id']]

async def create_order(update, user, state):
    """Create order and show summary"""
    db = get_db()
    
    items = db.execute('''SELECT ci.*, mi.name FROM cart_items ci 
                          JOIN menu_items mi ON ci.menu_item_id = mi.id 
                          WHERE ci.cart_id = ?''', (state['cart_id'],)).fetchall()
    
    total = calc_cart_total(state['cart_id'])
    order_id = generate_order_id()
    
    db.execute('''INSERT INTO orders (user_id, cart_id, order_id, total_naira, delivery_address, contact_number)
                  VALUES (?, ?, ?, ?, ?, ?)''',
               (user['id'], state['cart_id'], order_id, total, state['address'], state['phone']))
    
    db.execute('UPDATE carts SET status = ? WHERE id = ?', ('checked_out', state['cart_id']))
    db.commit()
    db.close()
    
    text = f'✅ *Order Summary*\n\n*Order ID:* {order_id}\n\n*Items:*\n'
    
    for item in items:
        text += f"• {item['name']} x{item['qty']} — ₦{item['qty'] * item['unit_price']:,}\n"
    
    text += f"\n*Total:* ₦{total:,}\n"
    text += f"*Delivery:* {state['address']}\n"
    text += f"*Contact:* {state['phone']}\n\n"
    text += f"*Payment:*\n"
    text += f"Bank: {os.getenv('PAYMENT_BANK', 'First Bank')}\n"
    text += f"Account: {os.getenv('PAYMENT_ACCOUNT', '1234567890')}\n"
    text += f"Name: {os.getenv('PAYMENT_NAME', 'SOCHOW')}\n\n"
    text += "📤 After payment, send your receipt image to this chat."
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle receipt photo uploads"""
    user = get_or_create_user(update.effective_user.id, update.effective_user.first_name)
    
    db = get_db()
    order = db.execute('''SELECT * FROM orders 
                          WHERE user_id = ? AND payment_status = 'pending' 
                          ORDER BY created_at DESC LIMIT 1''', (user['id'],)).fetchone()
    db.close()
    
    if not order:
        await update.message.reply_text('❌ No pending order found.')
        return
    
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"receipt_{order['id']}_{datetime.now().timestamp()}.jpg"
    
    await file.download_to_drive(f"uploads/{file_path}")
    
    db = get_db()
    db.execute('INSERT INTO receipts (order_id, user_id, image_url) VALUES (?, ?, ?)',
               (order['id'], user['id'], f'/uploads/{file_path}'))
    db.commit()
    db.close()
    
    await update.message.reply_text('✅ Receipt received. Forwarding to admin for verification…')
    
    try:
        await context.bot.send_message(ADMIN_CHAT_ID, 
                                       f"💳 Payment receipt for {order['order_id']}\nAmount: ₦{order['total_naira']:,}")
        await context.bot.send_photo(ADMIN_CHAT_ID, photo.file_id)
    except:
        pass

async def track_order(query, user_id):
    """Show order tracking"""
    db = get_db()
    orders = db.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', 
                        (user_id,)).fetchall()
    db.close()
    
    if not orders:
        keyboard = [[InlineKeyboardButton("🍽️ View Menu", callback_data="view_menu")]]
        await query.message.reply_text('📦 No orders found.', reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    text = '📦 *Your Orders*\n\n'
    
    for order in orders:
        emoji = {'processing': '⏳', 'prepared': '🍴', 'out-for-delivery': '🚚', 'delivered': '✅'}.get(order['order_status'], '📦')
        text += f"*{order['order_id']}*\n"
        text += f"Status: {emoji} {order['order_status']}\n"
        text += f"Total: ₦{order['total_naira']:,}\n\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="view_menu")]]
    await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def show_help(query):
    """Show help"""
    text = """ℹ️ *SOCHOW Help*

*How to order:*
1. View Menu
2. Add to Cart
3. Checkout
4. Pay & Upload Receipt
5. Track Order

*Commands:*
/start — Show main menu"""
    
    keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="view_menu")]]
    await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

# ============================================================================
# FLASK API (for admin dashboard)
# ============================================================================

app = Flask(__name__)
CORS(app)

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory('uploads', filename)

@app.route('/api/menu/items', methods=['GET'])
def get_menu_items():
    db = get_db()
    items = db.execute('SELECT * FROM menu_items ORDER BY id').fetchall()
    db.close()
    return jsonify([dict(item) for item in items])

@app.route('/api/menu/items', methods=['POST'])
def add_menu_item():
    data = request.json
    db = get_db()
    cursor = db.execute('''INSERT INTO menu_items (name, price_naira, description, available) 
                           VALUES (?, ?, ?, ?)''',
                        (data['name'], data['price_naira'], data.get('description'), 
                         1 if data.get('available', True) else 0))
    db.commit()
    item = db.execute('SELECT * FROM menu_items WHERE id = ?', (cursor.lastrowid,)).fetchone()
    db.close()
    return jsonify(dict(item))

@app.route('/api/menu/items', methods=['PATCH'])
def update_menu_item(item_id):
    data = request.json
    db = get_db()
    if 'available' in data:
        db.execute('UPDATE menu_items SET available = ? WHERE id = ?', 
                   (1 if data['available'] else 0, item_id))
    
    db.commit()
    item = db.execute('SELECT * FROM menu_items WHERE id = ?', (item_id,)).fetchone()
    db.close()
    return jsonify(dict(item))

@app.route('/api/menu/items/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    db = get_db()
    db.execute('DELETE FROM menu_items WHERE id = ?', (item_id,))
    db.commit()
    return jsonify({'success': True})

@app.route('/api/menu/upload', methods=['POST'])
def upload_menu():
    if 'menu_image' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['menu_image']
    filename = f"menu_{datetime.now().timestamp()}.jpg"
    file.save(f"uploads/{filename}")
    
    image_url = f"/uploads/{filename}"
    db = get_db()
    db.execute('''INSERT OR REPLACE INTO menu_config (id, menu_image_url, updated_at) 
                  VALUES (1, ?, CURRENT_TIMESTAMP)''', (image_url,))
    db.commit()
    db.close()
    
    return jsonify({'imageUrl': image_url})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    db = get_db()
    orders = db.execute('''SELECT o.*, u.name as customer_name, u.telegram_id as customer_telegram,
                                  r.image_url as receipt_url
                           FROM orders o
                           JOIN users u ON o.user_id = u.id
                           LEFT JOIN receipts r ON o.id = r.order_id
                           ORDER BY o.created_at DESC''').fetchall()
    
    result = []
    for order in orders:
        order_dict = dict(order)
        items = db.execute('''SELECT ci.qty, mi.name, mi.price_naira
                              FROM cart_items ci
                              JOIN menu_items mi ON ci.menu_item_id = mi.id
                              WHERE ci.cart_id = ?''', (order['cart_id'],)).fetchall()
        
        order_dict['items'] = [dict(item) for item in items]
        order_dict['customer'] = {'name': order['customer_name'], 'telegram_id': order['customer_telegram']}
        result.append(order_dict)
    
    db.close()
    return jsonify(result)

@app.route('/api/orders/<int:order_id>/verify', methods=['POST'])
def verify_payment(order_id):
    data = request.json
    db = get_db()
    
    if data.get('verified'):
        db.execute('''UPDATE orders SET payment_status = 'verified', order_status = 'processing', 
                      updated_at = CURRENT_TIMESTAMP WHERE id = ?''', (order_id,))
        db.execute('UPDATE receipts SET admin_verified = 1 WHERE order_id = ?', (order_id,))
        
        # Notify customer
        order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        user = db.execute('SELECT * FROM users WHERE id = ?', (order['user_id'],)).fetchone()
        
        asyncio.run(telegram_app.bot.send_message(
            user['telegram_id'],
            f"✅ Payment confirmed for {order['order_id']}\nTotal: ₦{order['total_naira']:,}\nYour order is being prepared."
        ))
    else:
        db.execute('''UPDATE orders SET payment_status = 'denied', updated_at = CURRENT_TIMESTAMP 
                      WHERE id = ?''', (order_id,))
    
    db.commit()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    db.close()
    return jsonify(dict(order))

@app.route('/api/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    data = request.json
    db = get_db()
    
    db.execute('''UPDATE orders SET order_status = ?, rider_contact = ?, updated_at = CURRENT_TIMESTAMP 
                  WHERE id = ?''', (data['status'], data.get('rider_contact'), order_id))
    db.commit()    
    
    # Notify customer
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    user = db.execute('SELECT * FROM users WHERE id = ?', (order['user_id'],)).fetchone()
    
    status_emoji = {'processing': '⏳', 'prepared': '🍴', 'out-for-delivery': '🚚', 'delivered': '✅'}
    emoji = status_emoji.get(data['status'], '📦')
    text = f"{emoji} Order {order['order_id']} status updated: {data['status']}"
    if data.get('rider_contact'):
        text += f"\nRider contact: {data['rider_contact']}"
    
    try:
        asyncio.run(telegram_app.bot.send_message(user['telegram_id'], text))
    except:
        pass
    
    db.close()
    return jsonify(dict(order))

@app.route('/api/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    db = get_db()
    db.execute('''UPDATE orders SET order_status = 'cancelled', updated_at = CURRENT_TIMESTAMP 
                  WHERE id = ?''', (order_id,))
    db.commit()
    
    # Notify customer
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    user = db.execute('SELECT * FROM users WHERE id = ?', (order['user_id'],)).fetchone()
    
    text = f"❌ Order {order['order_id']} has been cancelled. Please contact us if you have any questions."
    
    try:
        asyncio.run(telegram_app.bot.send_message(user['telegram_id'], text))
    except:
        pass
    
    db.close()
    return jsonify(dict(order))

@app.route('/api/orders/<int:order_id>/query', methods=['POST'])
def query_customer(order_id):
    data = request.json
    db = get_db()
    
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    user = db.execute('SELECT * FROM users WHERE id = ?', (order['user_id'],)).fetchone()
    
    # Send query to admin
    asyncio.run(telegram_app.bot.send_message(
        ADMIN_CHAT_ID,
        f"❓ Query about {order['order_id']}:\n\n{data['message']}"
    ))
    
    db.close()
    return jsonify({'success': True})

# ============================================================================
# START SERVERS
# ============================================================================

def run_flask():
    """Run Flask in separate thread"""
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# Global telegram app reference
telegram_app = None

if __name__ == '__main__':
    print('✅ SOCHOW Bot Starting...')
    os.makedirs('uploads', exist_ok=True)
    
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print(f'📡 API Server running on http://localhost:{PORT}')
    
    telegram_app = Application.builder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler('start', start))
    telegram_app.add_handler(CallbackQueryHandler(button_handler))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print('🤖 Telegram bot starting...')
    telegram_app.run_polling()
