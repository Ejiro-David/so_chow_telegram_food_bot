# SOCHOW - Telegram Food Ordering Bot 🍽️

Lightweight Python implementation with Flask API + SQLite

## 📦 Installation

```bash
# Install Python dependencies (only 4!)
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Create `.env` file from template:
```bash
cp .env.example .env
```

2. Get your Telegram bot token from [@BotFather](https://t.me/botfather)

3. Get your Telegram user ID from [@userinfobot](https://t.me/userinfobot)

4. Edit `.env` and add your tokens

## 🚀 Running

```bash
python bot.py
```

This starts:
- ✅ Telegram bot (polling for messages)
- ✅ Flask API server on port 3000
- ✅ SQLite database (auto-created)

## 🖥️ Admin Dashboard

Open `index.html` in your browser (double-click the file)

Dashboard connects to `http://localhost:3000/api`

## 📊 File Structure

```
sochow/
├── bot.py              # Main bot + API server (Python)
├── index.html          # Admin dashboard (vanilla JS)
├── sochow.db           # SQLite database (auto-created)
├── uploads/            # Receipt & menu images
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Development

- **Python**: 3.8+ required
- **No Node.js needed!**
- **Dependencies**: Only 4 packages (~5MB total vs 100MB+ for Node)

## 📱 Customer Flow

1. `/start` → Main menu
2. View menu → Add items to cart
3. Checkout → Enter address & phone
4. Upload payment receipt
5. Admin verifies → Order confirmed
6. Track order status

## 👨‍💼 Admin Flow

1. Open `index.html` in browser
2. Add menu items
3. Upload menu image
4. Verify payments (approve/deny)
5. Update order status
6. Send messages to customers

## 🐛 Troubleshooting

- **Bot not responding**: Check BOT_TOKEN in .env
- **Admin dashboard empty**: Make sure bot.py is running
- **CORS errors**: API must be on http://localhost:3000

## 🎯 Production Deployment

**Recommended:** PythonAnywhere, Railway, or Render

All support Python + Flask out of the box!
# so_chow_telegram_food_bot
