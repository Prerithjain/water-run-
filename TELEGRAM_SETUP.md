# 🎉 Telegram Bot Setup Guide

## Why Telegram Instead of CallMeBot/WhatsApp?

✅ **100% Reliable** - No registration issues  
✅ **100% Free** - Always free, no limits  
✅ **Easy Setup** - 5 minutes, works every time  
✅ **Official API** - Backed by Telegram  
✅ **Better Features** - Rich formatting, buttons, inline messages  

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Your Bot

1. **Open Telegram** on your phone or computer
2. **Search for @BotFather** (official bot with verified checkmark)
3. **Send** `/newbot`
4. **Choose a name** for your bot (e.g., "Water Run Bot")
5. **Choose a username** for your bot (must end in 'bot', e.g., "waterrun_tracker_bot")
6. **@BotFather will send you a token** - SAVE THIS! It looks like:
   ```
   1234567890:ABCdefGhIJKlmNoPQRstuVWXyz1234567890
   ```

### Step 2: Create Your Group

1. **Create a new group** in Telegram
2. **Add all team members** (Vishwas, Prerith, Prashanth, Bhuvan Gumma, Vikas Reddy)
3. **Add your bot** to the group (search for the username you created)
4. **Send a test message** in the group (anything, just to activate it)

### Step 3: Get Your GROUP Chat ID ⚠️ IMPORTANT!

**IMPORTANT:** You need the **GROUP** chat ID (negative number), NOT your personal chat ID!

1. **Make sure you sent a message IN THE GROUP** (not to the bot directly)
2. **Open your browser** and go to:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   **Replace `<YOUR_BOT_TOKEN>`** with the token from Step 1

3. **Look for the GROUP message** in the response:
   ```json
   {
     "ok": true,
     "result": [
       {
         "message": {
           "chat": {
             "id": -1001234567890,  <-- GROUP ID (NEGATIVE!)
             "title": "Water Run Team",
             "type": "group"  <-- Must say "group"!
           }
         }
       }
     ]
   }
   ```

4. **Find the chat with `"type": "group"`** and copy its **negative ID**
   - ✅ **GROUP chat IDs:** Start with **-100** (e.g., `-1001234567890`)
   - ❌ **Personal chat IDs:** Positive numbers (e.g., `123456789`)
   
5. **Common mistake:** If messages go to your personal chat instead of the group:
   - You used your PERSONAL chat ID (positive number)
   - You need the GROUP chat ID (negative number starting with -100)

### Step 4: Update Your `.env` File

1. **Create or edit** `.env` in your project root
2. **Add these lines** (with your actual values):
   ```env
   ENABLE_TELEGRAM_ALERTS=true
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRstuVWXyz1234567890
   TELEGRAM_CHAT_ID=-1001234567890
   ```

### Step 5: Test It!

1. **Start your app:**
   ```bash
   npm run dev
   ```

2. **Open** `http://localhost:3000`
3. **Log in as admin** (password: `water123`)
4. **Click "Send Telegram Alert"** button
5. **Check your Telegram group** - you should see a message! 🎉

---

## 📱 Example Messages

### After someone goes alone:
```
🚰 Water Run Update! 💧

✅ Prerith just went

👉 Vishwas - you're up next!

Thanks team! 🙌
```

### After people go together:
```
🚰 Water Run Update! 💧

✅ Prerith, Vishwas just went together

👉 Prashanth - you're up next!

Thanks team! 🙌
```

### Manual reminder:
```
🚰 Reminder!

Vishwas - it's your turn for the water run! 💧
```

---

## 🔧 Troubleshooting

### Bot not sending messages?

**Check 1:** Make sure bot token is correct
- Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe`
- Should show your bot info
- If error: token is wrong

**Check 2:** Make sure chat ID is correct
- Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
- Look for recent messages
- Chat ID must include minus sign if it's negative

**Check 3:** Make sure bot is in the group
- Go to your Telegram group
- Tap group name → view members
- Your bot should be listed

**Check 4:** Give bot admin permissions (optional but recommended)
- Go to your Telegram group
- Tap group name → "Administrators"
- Add your bot as admin (gives it permission to always send messages)

### Can't find chat ID?

**Option 1:** Use this helpful bot
1. Add @RawDataBot to your group
2. It will send you the chat ID immediately
3. Remove @RawDataBot after getting the ID

**Option 2:** Send a message and check
1. Send any message in your group
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for most recent message
4. Copy the `"chat":{"id":...}` value

---

## 🎯 Differences from WhatsApp

| Feature | Telegram ✅ | CallMeBot WhatsApp ❌ |
|---------|-------------|----------------------|
| **Reliability** | 100% | Unreliable |
| **Setup** | 5 minutes | Often fails |
| **API** | Official | Third-party |
| **Cost** | Free forever | Free but limited |
| **Message Limits** | None | May have limits |
| **Rich Formatting** | Yes (bold, italic, etc) | Limited |
| **Buttons** | Yes | No |
| **Group Support** | Native | Workaround |

---

## 💡 Pro Tips

✅ **Name your bot clearly** (e.g., "Water Run Tracker Bot")  
✅ **Set a bot profile picture** (makes it look professional)  
✅ **Make bot an admin** in the group (prevents permission issues)  
✅ **Test the /getUpdates URL** before starting  
✅ **Save your bot token** somewhere safe  

---

## 🔒 Security Note

- **Never share your bot token** (it's like a password)
- **Keep your `.env` file private** (add to `.gitignore`)
- If token is compromised, talk to @BotFather to revoke and get a new one

---

## ✨ What's Changed in Code

- ✅ **Removed:** CallMeBot/WhatsApp integration
- ✅ **Added:** Telegram Bot API integration
- ✅ **Fixed:** Date issue (now shows actual last water run date, not today)
- ✅ **Updated:** Environment variables
- ✅ **Improved:** Error handling and logging

---

**Ready to go! 🚀 Follow the steps above and you'll have Telegram alerts running in 5 minutes!**
