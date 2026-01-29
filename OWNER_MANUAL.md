# 📖 SOCHOW BOT - OWNER'S MANUAL

**Complete setup and operations guide for non-technical users**

---

## 📑 **TABLE OF CONTENTS**

1. [First Time Setup](#1-first-time-setup)
2. [Daily Operations](#2-daily-operations)
3. [Admin Dashboard Guide](#3-admin-dashboard-guide)
4. [Managing Orders](#4-managing-orders)
5. [Troubleshooting](#5-troubleshooting)
6. [Cloud Deployment (24/7 Access)](#6-cloud-deployment)
7. [Backup & Maintenance](#7-backup--maintenance)

---

## 1️⃣ **FIRST TIME SETUP**

### **Step 1: Check Python Installation**

**On Mac:**
```bash
python3 --version
```

**On Windows:**
```bash
python --version
```

You should see `Python 3.8` or higher. If not, [download Python here](https://www.python.org/downloads/).

---

### **Step 2: Get Your Telegram Admin ID**

1. Open Telegram app
2. Search for: **@userinfobot**
3. Start chat with the bot
4. It will reply with your ID (example: `123456789`)
5. **Write this number down!** You'll need it in Step 4

---

### **Step 3: Install Required Software**

Open **Terminal** (Mac) or **Command Prompt** (Windows):

**Navigate to SOCHOW folder:**
```bash
cd /path/to/sochow
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

You should see:
```
Successfully installed flask-3.0.0 flask-cors-4.0.0 python-telegram-bot-20.7 python-dotenv-1.0.0
```

---

### **Step 4: Create Configuration File**

In the SOCHOW folder, create a file named **`.env`** (include the dot!)

**Copy this template and fill in YOUR details:**

```bash
# Telegram Bot Configuration
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_CHAT_ID=YOUR_TELEGRAM_ID_FROM_STEP_2

# Payment Information (shown to customers)
PAYMENT_BANK=First Bank
PAYMENT_ACCOUNT=1234567890
PAYMENT_NAME=SOCHOW Restaurant

# Server Port (leave as 3000)
PORT=3000
```

**Where to get BOT_TOKEN:**
1. Open Telegram → search **@BotFather**
2. Send `/newbot` command
3. Follow prompts to create your bot
4. BotFather will give you a token like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Copy this token into `.env` file

**Save the file and close it.**

---

### **Step 5: First Run Test**

```bash
python bot.py
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

**⚠️ IMPORTANT:** Keep this terminal window open. Closing it stops the bot!

---

## 2️⃣ **DAILY OPERATIONS**

### **Starting the Bot**

Every time you want to run the restaurant bot:

**1. Open Terminal/Command Prompt**

**2. Navigate to folder:**
```bash
cd /path/to/sochow
```

**3. Run:**
```bash
python bot.py
```

**4. Leave window open!**

---

### **Opening Admin Dashboard**

**Option A:** Double-click `index.html` file

**Option B:** Open browser → type `http://localhost:3000`

You should see the SOCHOW Admin Dashboard with:
- Menu Management tab
- Orders Queue tab
- Payment Verification section

---

### **Stopping the Bot**

When you're done for the day:

1. Go to terminal window running `bot.py`
2. Press **Ctrl+C** (Mac/Windows)
3. Bot stops gracefully

```
^C
🛑 Shutting down...
Bot stopped.
```

---

## 3️⃣ **ADMIN DASHBOARD GUIDE**

### **Managing Menu Items**

#### **Add New Dish:**
1. Click **"Menu Management"** tab
2. Fill in form:
   - **Name:** e.g., "Jollof Rice Special"
   - **Price (₦):** e.g., 5000
   - **Description:** e.g., "Spicy jollof rice with chicken"
3. Click **"Upload Photo"** → select food image
4. Click **"Add Item"**
5. ✅ Item appears in menu list immediately

#### **Edit Existing Dish:**
1. Find item in menu list
2. Click **"Edit"** button
3. Change name/price/description
4. Click **"Save"**

#### **Mark Item as Unavailable (Sold Out):**
1. Find item in menu list
2. Toggle **"Available"** switch to OFF
3. ⚠️ Customers won't see this item until you turn it back on

#### **Delete Dish:**
1. Click **"Delete"** button
2. Confirm deletion
3. ⚠️ This is permanent!

---

### **Upload Full Menu Image**

If you have a designed menu poster/image:

1. Click **"Upload Menu Image"** button
2. Select your menu image file
3. Preview appears
4. Customers will see this when they open bot

---

## 4️⃣ **MANAGING ORDERS**

### **New Order Arrives**

When customer places order, you'll see:
1. **Telegram notification** (sent to your admin account)
2. **Red badge** on Orders tab in dashboard
3. Order appears in **"Pending Payment"** section

---

### **Verify Payment Receipt**

1. Click **"Orders"** tab
2. Find order with **"Pending"** status (orange badge)
3. Review order details:
   - Customer name
   - Items ordered
   - Total amount
   - Delivery address
4. Click **"View Receipt"** → receipt photo opens
5. Check if payment matches order total

**If payment is correct:**
- Click **"✅ Verify Payment"**
- Customer receives instant confirmation
- Order moves to **"Processing"**

**If payment is incorrect/fake:**
- Click **"❌ Deny Payment"**
- Add note explaining why
- Customer receives denial message

---

### **Update Order Status**

As you prepare and deliver the order:

**Order Status Flow:**
```
Pending → Processing → Prepared → Out for Delivery → Delivered
```

**To update:**
1. Find order in dashboard
2. Click **"Update Status"** dropdown
3. Select new status:
   - **Processing:** You're cooking the food
   - **Prepared:** Food is ready, waiting for rider
   - **Out for Delivery:** Rider picked up, on the way
   - **Delivered:** Customer received order
4. (Optional) Add rider contact number
5. Click **"Update"**
6. ✅ Customer receives automatic Telegram notification

---

### **Send Message to Customer**

Need to ask customer something?

1. Find their order
2. Click **"Send Message"** button
3. Type your message
4. Click **"Send"**
5. Message delivered via Telegram bot

---

### **Cancel Order**

If needed:
1. Click **"Cancel Order"** button
2. Confirm cancellation
3. Customer notified automatically

---

## 5️⃣ **TROUBLESHOOTING**

### **Problem: Bot Not Responding to Customers**

**Solutions:**
1. Check terminal → Is `bot.py` running?
2. Verify `.env` file → Is `BOT_TOKEN` correct?
3. Restart bot: Press Ctrl+C → run `python bot.py` again
4. Test by sending `/start` to your bot in Telegram

---

### **Problem: Admin Dashboard Shows Empty**

**Solutions:**
1. Check `bot.py` is running (terminal window open)
2. Refresh browser (press F5)
3. Check browser console (right-click → Inspect → Console tab)
4. Look for errors mentioning `localhost:3000`
5. Verify API_BASE in `index.html` says `http://localhost:3000/api`

---

### **Problem: Images Not Displaying**

**Solutions:**
1. Check `uploads/menu/` folder → Are image files there?
2. Verify file names don't have special characters
3. Restart `bot.py`
4. Re-upload images via dashboard

---

### **Problem: "CORS Error" in Browser**

**Solution:**
- Bot must be running on `http://localhost:3000`
- Don't change the port in `.env` unless necessary
- Restart browser and bot

---

### **Problem: Customer Says Receipt Upload Failed**

**Solutions:**
1. Check `uploads/receipts/` folder exists
2. Check folder permissions (should be writable)
3. Ask customer to try smaller image file
4. Restart bot

---

## 6️⃣ **CLOUD DEPLOYMENT (24/7 Access)**

### **Why Deploy to Cloud?**

**Benefits:**
- ✅ Bot runs 24/7 without your computer
- ✅ Access admin dashboard from anywhere (phone, tablet, any computer)
- ✅ No need to keep terminal window open
- ✅ Professional, reliable operation
- ✅ Multiple team members can access admin panel

**When to Deploy:**
- You want hands-free operation
- Restaurant operates outside your working hours
- You have multiple admins who need access

---

### **Recommended Platform: Render.com (FREE)**

**Why Render:**
- ✅ Completely free tier
- ✅ Easy setup (no credit card required initially)
- ✅ Auto-deploys from your code
- ✅ Provides HTTPS (secure) URL

---

### **Deployment Steps:**

#### **1. Create Render Account**
1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Sign up with GitHub or Email

#### **2. Create New Web Service**
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub (upload SOCHOW folder to GitHub first)
3. OR use "Public Git Repository" if code is already online

#### **3. Configure Service**

**Build Settings:**
- **Name:** `sochow-bot`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python bot.py`

**Environment Variables (click "Advanced"):**
Add each variable from your `.env` file:
```
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_CHAT_ID=YOUR_TELEGRAM_ID
PAYMENT_BANK=First Bank
PAYMENT_ACCOUNT=1234567890
PAYMENT_NAME=SOCHOW
PORT=3000
```

#### **4. Deploy**
1. Click **"Create Web Service"**
2. Wait 2-5 minutes for deployment
3. You'll get a URL like: `https://sochow-bot.onrender.com`

#### **5. Update Admin Dashboard**
1. Open `index.html` in text editor
2. Find line: `const API_BASE = 'http://localhost:3000/api';`
3. Change to: `const API_BASE = 'https://sochow-bot.onrender.com/api';`
4. Save file
5. Now you can open `index.html` from anywhere!

---

### **After Deployment:**

**Testing:**
1. Send `/start` to your Telegram bot
2. Try ordering something
3. Check admin dashboard at your Render URL
4. Verify everything works

**⚠️ Free Tier Note:**
- Render free tier "sleeps" after 15 minutes of inactivity
- First customer message will wake it up (takes ~30 seconds)
- Totally normal, doesn't affect functionality

**Upgrading:**
- If you need faster response, upgrade to $7/month plan
- Bot will never sleep

---

## 7️⃣ **BACKUP & MAINTENANCE**

### **What to Backup**

Back up these files weekly:

1. **sochow.db** - All your data (orders, customers, menu)
2. **uploads/** folder - All images (receipts, menu photos)
3. **.env** file - Your configuration (passwords, tokens)

---

### **How to Backup**

**Easy Method:**
1. Create folder: `SOCHOW_Backup_2026-01-28`
2. Copy `sochow.db` to this folder
3. Copy `uploads/` folder to this folder
4. Copy `.env` file to this folder
5. Store on external drive or cloud (Google Drive, Dropbox)

**Automated Backup (Mac/Linux):**
```bash
# Run this weekly
cp sochow.db backups/sochow_$(date +%Y%m%d).db
cp -r uploads backups/uploads_$(date +%Y%m%d)
```

---

### **Restore from Backup**

If something breaks:

1. Stop the bot (Ctrl+C)
2. Rename current `sochow.db` to `sochow.db.old`
3. Copy backup `sochow.db` to main folder
4. Restart bot: `python bot.py`
5. ✅ All orders/data restored

---

### **Database Maintenance**

**Monthly Tasks:**
1. Check database size: `ls -lh sochow.db`
2. If over 100MB, consider archiving old orders
3. Delete very old receipt images (keep last 3 months)

**Clean old receipts:**
```bash
# Delete receipts older than 90 days
find uploads/receipts -name "receipt_*" -mtime +90 -delete
```

---

## 📞 **GETTING HELP**

### **Common Questions**

**Q: Can I use this on multiple computers?**  
A: Yes! Copy the entire SOCHOW folder. Just make sure only ONE instance of `bot.py` runs at a time.

**Q: Can I have multiple admins?**  
A: Yes! Share the admin dashboard URL (or `index.html` file if local). All admins see same data in real-time.

**Q: What if I lose my bot token?**  
A: Contact @BotFather on Telegram → Send `/mybots` → Select your bot → Get token

**Q: Can customers pay with card instead of bank transfer?**  
A: This version uses manual bank transfer. Payment gateway integration requires additional coding.

**Q: How many orders can the system handle?**  
A: SQLite easily handles 100,000+ orders. If you grow beyond that, consider upgrading to PostgreSQL.

---

## ✅ **DAILY CHECKLIST**

**Morning Routine:**
- [ ] Start bot: `python bot.py`
- [ ] Open admin dashboard
- [ ] Check for overnight orders
- [ ] Verify menu items are all available

**During Operation:**
- [ ] Monitor orders queue
- [ ] Verify payment receipts promptly
- [ ] Update order statuses as you cook/deliver
- [ ] Respond to customer queries

**End of Day:**
- [ ] Complete all pending orders
- [ ] Stop bot (Ctrl+C)
- [ ] (Optional) Backup database if it was a busy day

---

**🎉 You're all set! Happy selling!**

**Welcome!** This guide will help you run and manage your SOCHOW food ordering bot. Everything is explained in simple steps - no technical experience needed!

---

## 📑 TABLE OF CONTENTS

1. [What is SOCHOW Bot?](#what-is-sochow-bot)
2. [First-Time Setup](#first-time-setup)
3. [Daily Operations](#daily-operations)
4. [Admin Dashboard Guide](#admin-dashboard-guide)
5. [Understanding Orders](#understanding-orders)
6. [Customer Experience](#customer-experience)
7. [Troubleshooting](#troubleshooting)
8. [Data Backup](#data-backup)
9. [Getting Help](#getting-help)

---

## 🤖 WHAT IS SOCHOW BOT?

SOCHOW is a Telegram bot that lets customers:
- Browse your food menu with photos
- Add items to cart
- Place orders
- Upload payment receipts
- Track order status

You (the admin) can:
- Manage menu items
- Verify payments
- Update order statuses
- Communicate with customers

**Components:**
- **Telegram Bot** - Customers interact here
- **Admin Dashboard** - You manage everything here (webpage)
- **Database** - Stores all data automatically

---

## 🚀 FIRST-TIME SETUP

### ✅ Prerequisites

**You need:**
- A computer (Mac or Windows)
- Python 3.8 or newer
- Telegram account
- Internet connection

**Check if you have Python:**

**On Mac:**
```bash
python3 --version
```

**On Windows:**
```bash
python --version
```

If you see a version number (like `Python 3.10.5`), you're good! If not, download Python from [python.org](https://www.python.org/downloads/).

---

### 📝 STEP 1: Get Your Telegram Bot Token

1. Open Telegram on your phone or computer
2. Search for **@BotFather**
3. Start a chat and send `/newbot`
4. Follow instructions:
   - Give your bot a name (e.g., "SOCHOW Food Bot")
   - Give it a username ending in "bot" (e.g., "sochow_food_bot")
5. **BotFather will give you a token** - looks like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. **SAVE THIS TOKEN!** You'll need it in Step 3.

---

### 👤 STEP 2: Get Your Telegram User ID

1. Open Telegram
2. Search for **@userinfobot**
3. Start the chat
4. It will show your ID (example: `123456789`)
5. **SAVE THIS NUMBER!** You'll need it in Step 3.

---

### ⚙️ STEP 3: Configure the Bot

1. Open the `sochow` folder on your computer
2. Find the file named `.env.example`
3. Make a copy and rename it to `.env` (just `.env`, remove the `.example`)
4. Open `.env` with a text editor (Notepad on Windows, TextEdit on Mac)
5. Fill in your information:

```env
BOT_TOKEN=paste_your_token_from_step_1
ADMIN_CHAT_ID=paste_your_id_from_step_2
PAYMENT_BANK=Your Bank Name
PAYMENT_ACCOUNT=Your Account Number
PAYMENT_NAME=Your Account Name
PORT=3000
```

6. Save and close

---

### 📦 STEP 4: Install Dependencies

**On Mac:**
```bash
cd /path/to/sochow
python3 -m pip install -r requirements.txt
```

**On Windows:**
```bash
cd C:\path\to\sochow
python -m pip install -r requirements.txt
```

Replace `/path/to/sochow` with the actual folder location.

**This installs:**
- Telegram bot framework
- Web server
- Database tools

---

## 🏃 DAILY OPERATIONS

### ▶️ Starting the Bot

**Every day before taking orders:**

**On Mac:**
```bash
cd /path/to/sochow
python3 bot.py
```

**On Windows:**
```bash
cd C:\path\to\sochow
python bot.py
```

**What you should see:**
```
✅ Database initialized
✅ Menu items seeded
✅ Linked 10/10 photos to menu items
✅ SOCHOW Bot Ready
📡 API Server running on http://localhost:3000
🤖 Telegram bot starting...
```

**IMPORTANT:**
- **Keep this window open!** Closing it stops the bot.
- Your bot is now live - customers can order!
- Leave it running as long as you want to accept orders

---

### 🖥️ Opening the Admin Dashboard

**While the bot is running:**

1. Open your web browser (Chrome, Safari, Firefox, etc.)
2. **Method 1:** Double-click the `index.html` file in the `sochow` folder
3. **Method 2:** In browser, go to `http://localhost:3000`

**You should see:**
- SOCHOW logo and title
- Menu Management section
- Orders Queue section
- Payment Receipts section

**If the dashboard is empty**, make sure `bot.py` is running!

---

### ⏹️ Stopping the Bot

**At end of day:**

1. Go to the window/terminal where `bot.py` is running
2. Press `Ctrl + C` (on both Mac and Windows)
3. Wait for it to say "Stopped"
4. You can close the window

---

## 🎛️ ADMIN DASHBOARD GUIDE

### 🍽️ Menu Management

#### **Adding a New Menu Item**

1. In the dashboard, find "Add New Menu Item" section
2. Fill in:
   - **Item Name** - e.g., "Jollof Rice Special"
   - **Price (₦)** - e.g., `5000` (numbers only, no commas)
   - **Description** (optional) - e.g., "Spicy jollof with chicken"
3. Click **"Add Item"**
4. Item appears in your menu list
5. To add a photo later, see "Uploading Menu Photos" below

#### **Making an Item Unavailable** (Sold Out)

1. Find the item in your menu list
2. Click **"Toggle Availability"** button
3. Item turns gray - customers won't see it
4. Click again to make it available again

#### **Deleting an Item**

1. Find the item in your menu list
2. Click **"Delete"** button
3. Confirm deletion
4. Item is permanently removed

#### **Uploading Menu Photos**

**For individual items:**
- Currently items use pre-loaded photos
- To change: Edit item and upload new photo (coming soon)

**For full menu image:**
1. Find "Menu Image Upload" section
2. Click "Choose File"
3. Select your menu image (JPG or PNG)
4. Click "Upload Menu Image"
5. Preview appears below

---

### 📦 Managing Orders

#### **Understanding Order Statuses**

Orders move through these stages:

1. **Pending** (Orange) - New order, waiting for payment
2. **Processing** (Red) - Payment verified, preparing food
3. **Prepared** (Green) - Food ready, waiting for delivery
4. **Out for Delivery** (Blue) - Rider on the way
5. **Delivered** (Green) - Order completed!

#### **Viewing Order Details**

Each order card shows:
- **Order ID** - Unique identifier (e.g., SOCHOW-20260128-0001)
- **Customer name** and contact
- **Items ordered** with quantities
- **Total amount**
- **Delivery address**
- **Order status**
- **Payment receipt** (if uploaded)

#### **Verifying Payments**

**When a customer uploads a payment receipt:**

1. Find the order in "Payment Receipts" section
2. Click **"View Receipt"** to see full size image
3. Check if amount matches the order total
4. Verify payment details
5. **If payment is correct:**
   - Click **"Approve Payment"**
   - Order status changes to "Processing"
   - Customer gets notification
6. **If payment is wrong:**
   - Click **"Deny Payment"**
   - Add reason in notes
   - Customer gets notified to fix it

#### **Updating Order Status**

1. Find the order in "Orders Queue"
2. Click the **status dropdown**
3. Select new status:
   - Processing → Prepared → Out for Delivery → Delivered
4. **(Optional)** If "Out for Delivery", enter rider's phone number
5. Click **"Update Status"**
6. Customer gets automatic notification!

#### **Sending Messages to Customers**

**To communicate with a customer:**

1. Find their order
2. Click **"Send Message"** button
3. Type your message
4. Click **"Send"**
5. Customer gets it in Telegram

**Use cases:**
- "Your meal will be ready in 20 minutes"
- "We're out of Coke, can we substitute with Sprite?"
- "Please provide clearer address details"

#### **Canceling an Order**

1. Find the order
2. Click **"Cancel Order"**
3. Confirm cancellation
4. Customer gets notified

---

## 📱 CUSTOMER EXPERIENCE

**Understanding what customers see helps you manage better:**

### **Customer Order Flow:**

1. **Customer starts bot** - `/start` in Telegram
2. **Views menu** - Sees photos, prices, descriptions
3. **Adds to cart** - Can add multiple items
4. **Views cart** - See total, can adjust quantities
5. **Checkout** - Enters delivery address and phone
6. **Sees payment details** - Your bank account info
7. **Uploads receipt** - Takes photo of bank transfer
8. **Waits for verification** - You approve/deny
9. **Gets updates** - Automatic notifications as you update status
10. **Tracks order** - Can check status anytime

### **What Customers Can Do:**

- `/start` - Main menu
- View menu with photos
- Add/remove items from cart
- Track their orders
- Upload payment receipts
- Get notifications

---

## 🆘 TROUBLESHOOTING

### **Problem: Bot not responding on Telegram**

**Solutions:**
1. Check if `bot.py` is running
2. Verify `BOT_TOKEN` in `.env` file is correct
3. Restart the bot (stop with Ctrl+C, start again)
4. Check your internet connection

---

### **Problem: Admin dashboard is empty**

**Solutions:**
1. Make sure `bot.py` is running
2. Refresh the webpage (F5 or Cmd+R)
3. Check browser console for errors (F12)
4. Try opening in different browser

---

### **Problem: Menu photos not showing**

**Solutions:**
1. Check if `uploads/menu/` folder has the photos
2. Verify bot is running (serves the photos)
3. Clear browser cache
4. Check file names match exactly (case-sensitive)

---

### **Problem: "CORS error" in browser**

**Solutions:**
1. Make sure you're using `http://localhost:3000`
2. Don't use `file://` URLs
3. Bot must be running

---

### **Problem: Customer can't upload receipt**

**Solutions:**
1. Check `uploads/receipts/` folder exists
2. Verify folder has write permissions
3. Ask customer to try smaller image size
4. They can also send receipt via regular message

---

### **Problem: Can't see new orders**

**Solutions:**
1. Refresh dashboard (F5)
2. Check "Auto-refresh" is working (updates every 30 seconds)
3. Manually click "Refresh Orders"

---

## 💾 DATA BACKUP

**What to back up:**

Your important data is in these locations:

1. **Database:** `sochow.db` - Contains all orders, menu items, customer info
2. **Uploads:** `uploads/` folder - Payment receipts and menu photos
3. **Configuration:** `.env` file - Your bot credentials

**How to back up:**

**Weekly (Recommended):**
1. Copy the entire `sochow` folder
2. Paste it to:
   - External hard drive
   - Cloud storage (Google Drive, Dropbox)
   - Another location on your computer
3. Name it with date: `sochow-backup-2026-01-28`

**Before major changes:**
- Always back up before updating code
- Before deleting many items
- Before changing settings

**Restoring from backup:**
1. Close the bot (Ctrl+C)
2. Copy backed-up files over current ones
3. Restart bot

---

## 💡 TIPS FOR SUCCESS

### **For Smooth Operations:**

1. **Start bot before opening hours** - Give it 2-3 minutes to fully start
2. **Keep dashboard open** - Monitor orders in real-time
3. **Verify payments quickly** - Customers wait for confirmation
4. **Update statuses promptly** - Keeps customers informed
5. **Check uploads folder size** - Delete old receipts monthly

### **For Better Customer Experience:**

1. **Use clear menu photos** - Well-lit, appetizing
2. **Write good descriptions** - Mention key ingredients
3. **Respond to messages** - Be friendly and helpful
4. **Update out-of-stock items** - Toggle availability daily
5. **Keep realistic preparation times** - Don't overpromise

### **Security Best Practices:**

1. **Never share your `.env` file** - Contains secrets!
2. **Don't post BOT_TOKEN publicly** - Anyone can control your bot
3. **Back up regularly** - Prevent data loss
4. **Keep only one admin** - Or share carefully with team

---

## 🌐 ACCESSING FROM ANYWHERE (Optional)

**Currently:** Bot runs on your computer only

**To make it available 24/7:**
- See `DEPLOYMENT.md` for hosting on Render.com (free!)
- Once deployed, bot works even when computer is off
- Access admin dashboard from any device
- Recommended for professional operation

---

## 📞 GETTING HELP

**If something goes wrong:**

1. Check this manual first (Troubleshooting section)
2. Check the error message in terminal window
3. Try restarting the bot
4. Contact your developer

**Information to provide when asking for help:**
- What you were trying to do
- Error message (exact text)
- Screenshot if possible
- Which step in this manual you're on

---

## 📋 QUICK REFERENCE

### **Daily Checklist:**

- [ ] Start bot: `python3 bot.py` (Mac) or `python bot.py` (Windows)
- [ ] Open dashboard: Double-click `index.html`
- [ ] Check menu items are available
- [ ] Monitor orders throughout day
- [ ] Verify payments as they come in
- [ ] Update order statuses
- [ ] Stop bot at end of day: `Ctrl + C`

### **Important Files:**

- `bot.py` - Main bot program (don't edit)
- `index.html` - Admin dashboard (don't edit)
- `.env` - Your configuration (keep secret!)
- `sochow.db` - Database (back up regularly!)
- `uploads/` - Photos and receipts

### **Important Folders:**

- `uploads/menu/` - Food photos
- `uploads/receipts/` - Payment receipts

---

## 🎉 YOU'RE READY!

You now know everything to run your SOCHOW bot successfully!

**Remember:**
- Keep bot running during business hours
- Monitor dashboard for new orders
- Verify payments quickly
- Keep customers updated
- Back up your data weekly

**Good luck with your food business! 🍽️**
