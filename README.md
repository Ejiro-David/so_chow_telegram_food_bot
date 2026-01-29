# SOCHOW - Telegram Food Ordering Bot 🍽️

A complete Telegram-based food ordering system where customers browse menus, place orders, and upload payment receipts. Admins manage everything through a web dashboard.

---

## 📋 **What This Is**

**Technology Stack:**
- **Backend:** Python (Flask + python-telegram-bot)
- **Database:** SQLite (single file database)
- **Admin Panel:** HTML/CSS/JavaScript (no framework, just open the file)
- **Bot Platform:** Telegram

**What It Does:**
1. Customers interact with Telegram bot to browse menu and order food
2. Customers upload payment receipts after ordering
3. Admin verifies payments and manages orders via web dashboard
4. Admin updates order status (processing → prepared → out for delivery → delivered)
5. All data stored in local SQLite database

---

## 📂 **Project Structure**

```
sochow/
├── bot.py                      # Main application (Telegram bot + Flask API server)
├── index.html                  # Admin dashboard (open in browser)
├── sochow.db                   # SQLite database (auto-created on first run)
├── requirements.txt            # Python dependencies (only 4 packages)
├── .env                        # Environment variables (YOU CREATE THIS)
├── .env.example                # Template for .env file
├── uploads/
│   ├── menu/                   # Food photos for menu items
│   ├── receipts/               # Customer payment receipts
│   ├── sochow-logo.png         # Logo used in admin panel
│   └── brand.jpeg              # Brand assets
├── README.md                   # This file (project overview)
└── OWNER_MANUAL.md             # Complete setup & usage guide
```

---

## 🔄 **How It Works**

### **Customer Journey:**
1. Customer opens Telegram → searches for your bot
2. Sends `/start` → sees menu with photos and prices
3. Adds items to cart → proceeds to checkout
4. Enters delivery address and phone number
5. Bot shows payment details (bank account info)
6. Customer pays via bank transfer → uploads receipt photo to bot
7. Waits for admin to verify payment
8. Receives order confirmation and tracking updates

### **Admin Journey:**
1. Admin runs `python bot.py` in terminal (starts bot + API server)
2. Opens `index.html` in browser (admin dashboard)
3. Dashboard shows:
   - **Menu Management:** Add/edit dishes, upload photos, set prices
   - **Orders Queue:** All pending orders with customer details
   - **Payment Verification:** Review receipt photos, approve/deny
   - **Order Tracking:** Update status as order progresses
4. Admin clicks "Verify Payment" on receipts → customer gets notified
5. Admin updates order status → customer receives real-time Telegram updates
6. All actions logged in database

### **Data Flow:**
```
Telegram Bot ←→ bot.py (Flask API) ←→ sochow.db (SQLite)
                    ↕
            index.html (Admin Dashboard)
```

---

## ⚙️ **Technical Details**

### **Dependencies:**
```
python-telegram-bot==20.7    # Telegram bot framework
flask==3.0.0                 # Web server for API + admin dashboard
flask-cors==4.0.0            # Allow browser to access API
python-dotenv==1.0.0         # Load environment variables from .env
```

### **Database Tables:**
- `users` - Customer information from Telegram
- `menu_items` - Restaurant menu with photos and prices
- `carts` - Active shopping carts
- `cart_items` - Items in each cart
- `orders` - Placed orders with delivery info
- `receipts` - Payment receipt uploads
- `menu_config` - Full menu image
- `admin_actions_log` - Audit trail

### **API Endpoints:**
```
GET    /api/menu/items         - Fetch all menu items
POST   /api/menu/items         - Add new menu item
PATCH  /api/menu/items/:id     - Update menu item
DELETE /api/menu/items/:id     - Delete menu item
POST   /api/menu/upload        - Upload menu image

GET    /api/orders             - Fetch all orders
POST   /api/orders/:id/verify  - Verify payment (approve/deny)
PATCH  /api/orders/:id/status  - Update order status
POST   /api/orders/:id/query   - Send message to customer
POST   /api/orders/:id/cancel  - Cancel order

GET    /uploads/<path>         - Serve uploaded images
```

---

## 🚀 **Quick Start**

### **Prerequisites:**
- Python 3.8 or higher
- Telegram account
- Bot token from @BotFather

### **Installation:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file from template
cp .env.example .env

# 3. Edit .env and add your bot token + admin ID
# (See OWNER_MANUAL.md for detailed instructions)

# 4. Run the bot
python bot.py

# 5. Open index.html in browser
# Double-click the file or open with your browser
```

**Success looks like:**
```
✅ Database initialized
✅ Menu items seeded
✅ Linked 10/10 photos to menu items
✅ SOCHOW Bot Ready
📡 API Server running on http://localhost:3000
🤖 Telegram bot starting...
```

---

## 🌐 **Deployment Options**

**Local (Current Setup):**
- Run on your computer
- Dashboard accessible at `http://localhost:3000`
- Must keep terminal window open
- Good for: Testing, small operations, limited hours

**Cloud Hosting (Recommended for 24/7):**
- **Render.com** - Free tier, auto-sleeps when idle
- **Railway.app** - $5/month free credit
- **PythonAnywhere** - Free tier available

See `OWNER_MANUAL.md` for deployment instructions.

---

## 📚 **Documentation**

- **OWNER_MANUAL.md** - Complete setup guide, daily operations, troubleshooting
- **README.md** (this file) - Project overview and technical reference

---

## 🔧 **Troubleshooting**

| Problem | Solution |
|---------|----------|
| Bot not responding | Check `BOT_TOKEN` in `.env`, ensure bot is running |
| Admin dashboard empty | Verify `bot.py` is running, check browser console |
| Images not showing | Check `uploads/menu/` folder, verify file paths in database |
| CORS errors | API must be on `http://localhost:3000` |
| Database locked | Close any other programs accessing `sochow.db` |

---

## 📞 **Support**

For detailed setup instructions, see **OWNER_MANUAL.md**

**Common Questions:**
- How to get bot token? → See OWNER_MANUAL.md Section 1
- How to add menu items? → See OWNER_MANUAL.md Section 3
- How to verify payments? → See OWNER_MANUAL.md Section 4
- How to deploy to cloud? → See OWNER_MANUAL.md Section 6
