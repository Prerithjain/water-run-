# 🚀 WhatsApp Group Alerts - Quick Setup Guide

## 📱 How It Works

After each water run, **everyone in the WhatsApp group** will receive a notification like this:

**Example 1 - Someone went alone:**
```
🚰 Water Run Update! 💧

✅ Prerith just went

👉 Vishwas - you're up next!

Thanks team! 🙌
```

**Example 2 - Two people went together:**
```
🚰 Water Run Update! 💧

✅ Prerith, Vishwas just went together

👉 Prashanth - you're up next!

Thanks team! 🙌
```

---

## ✅ Setup (5 Minutes Total!)

### Step 1: Create WhatsApp Group
1. Open WhatsApp
2. Create a new group with all team members (Vishwas, Prerith, Prashanth, Bhuvan Gumma, Vikas Reddy)
3. Name it something like "💧 Water Run Team"

### Step 2: Group Admin Gets CallMeBot API Key
**Only the GROUP ADMIN needs to do this:**

1. **Add CallMeBot** to your personal contacts: `+34 644 51 98 89`
2. **Send this message** to CallMeBot (in your personal chat, NOT the group):
   ```
   I allow callmebot to send me messages
   ```
3. **Copy your API key** from CallMeBot's reply (e.g., "123456")
4. **Note down your phone number** with country code (e.g., "+919876543210")

### Step 3: Configure the App
1. **Create a `.env` file** in the watertracker folder (copy from `env.example`)
2. **Update these two lines** with the group admin's details:
   ```env
   WHATSAPP_GROUP_PHONE=+919876543210  # Admin's phone (with country code)
   WHATSAPP_GROUP_APIKEY=123456         # Admin's API key from CallMeBot
   ```

### Step 4: Test It!
1. **Start the server**:
   ```bash
   npm run dev
   ```
2. **Log in as admin** (password: `water123`)
3. **Click "Send WhatsApp Alert"** button to test
4. **Check your WhatsApp group** - you should see the message!

---

## 📝 Important Notes

✅ **Only ONE person** (the group admin) needs to set up CallMeBot  
✅ **All team members** will see the messages in the group  
✅ **100% FREE** - no credit card required!  
✅ **Automatic** - sends after every water run  
✅ **Shows who went** + **who's next**  

---

## 🎯 Message Types

### Automatic (after recording a run)
Shows:
- ✅ Who just completed the run
- 👉 Who should go next

### Manual (when admin clicks the button)
Shows:
- 🚰 Reminder for whose turn it is

---

## 🔧 Troubleshooting

**Message not appearing?**
1. Make sure the group admin added CallMeBot correctly
2. Verify the phone number has a `+` and country code
3. Check the API key is correct (no spaces)
4. Ensure `ENABLE_WHATSAPP_ALERTS=true` in `.env`

**Wrong person getting notified?**
- The system calculates based on lowest score + oldest visit time

**Want to test without recording a run?**
- Click the "Send WhatsApp Alert" button (admin only)

---

## 🌟 Benefits

| Feature | Individual Messages | **Group Messages** ✨ |
|---------|-------------------|---------------------|
| Everyone sees updates | ❌ | ✅ |
| Setup complexity | High (5 setups) | Low (1 setup) |
| Transparency | Low | High |
| Team coordination | Difficult | Easy |

---

## 📚 Next Steps

- **Record your first run** and watch the magic happen! 🚰
- **Customize messages** by editing `api/index.py` (search for "Water Run Update")
- **Disable alerts** by setting `ENABLE_WHATSAPP_ALERTS=false` in `.env`

---

**Happy Water Running! 💧🚰📱**
