# WhatsApp Alert Setup Guide - **100% FREE!** 🎉

## Overview
The Water Run app supports automatic WhatsApp notifications using **CallMeBot** - a completely FREE WhatsApp API service!

✅ **NO credit card required**  
✅ **NO registration needed**  
✅ **Forever FREE**  
✅ **5-minute setup per person**

## Features
- 🚰 **Automatic alerts** after each water run
- 📱 **Manual alerts** via admin button
- 🎯 **Smart detection** of whose turn it is
- 🔒 **Admin-only** sending

---

## Step-by-Step Setup (5 minutes per person)

### Step 1: Get CallMeBot API Key (FREE!)

**Each team member needs to do this ONCE:**

1. **Add CallMeBot to WhatsApp contacts**:
   - Save this number: **+34 644 51 98 89**
   - Name it: "CallMeBot" or anything you like

2. **Send activation message**:
   - Open WhatsApp
   - Send this EXACT message to CallMeBot:
     ```
     I allow callmebot to send me messages
     ```

3. **Get your API key**:
   - CallMeBot will reply instantly with your FREE API key
   - Example reply: "*Your APIkey is 123456*"
   - **Save this API key** - you'll need it in Step 3

### Step 2: Get Phone Numbers

You need each person's phone number in **international format**:

**Format**: `+` + country code + number (NO spaces, dashes, or parentheses)

Examples:
- India: `+919876543210`
- USA: `+14155551234`
- UK: `+44 7911123456`

### Step 3: Create `.env` File

Create a file named `.env` in the watertracker folder with this format:

```env
# WhatsApp Configuration using CallMeBot (FREE!)
ENABLE_WHATSAPP_ALERTS=true

# Vishwas
WHATSAPP_VISHWAS_PHONE=+919876543210
WHATSAPP_VISHWAS_APIKEY=123456

# Prerith
WHATSAPP_PRERITH_PHONE=+919876543211
WHATSAPP_PRERITH_APIKEY=234567

# Prashanth
WHATSAPP_PRASHANTH_PHONE=+919876543212
WHATSAPP_PRASHANTH_APIKEY=345678

# Bhuvan Gumma
WHATSAPP_BHUVAN_GUMMA_PHONE=+919876543213
WHATSAPP_BHUVAN_GUMMA_APIKEY=456789

# Vikas Reddy
WHATSAPP_VIKAS_REDDY_PHONE=+919876543214
WHATSAPP_VIKAS_REDDY_APIKEY=567890
```

**Replace**:
- `+919876543210` → Real phone numbers
- `123456` → API keys from Step 1

### Step 4: Update Phone Numbers in Code (Optional)

The app already has placeholder phone numbers. You can update them in `api/index.py` around line 158-164 if you want:

```python
target_people = [
    {"name": "Vishwas", "score": 7, "phone": "+919876543210"},
    {"name": "Prerith", "score": 5, "phone": "+919876543211"},
    # ... etc
]
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - for making HTTP calls to CallMeBot
- `python-dotenv` - for reading .env file
  
### Step 6: Test It!

1. **Start the server**:
   ```bash
   npm run dev
   ```

2. **Record a water run** (as admin):
   - Log in with password: `water123`
   - Select someone and click "Go Alone" or "Go Together"
   - The next person should get a WhatsApp message instantly!

3. **Manual test**:
   - Click the green "**Send WhatsApp Alert**" button
   - Check if the message arrives

---

## Message Examples

**Automatic (after someone completes a run)**:
> 🚰 Hi Prerith! Great news - it's your turn for the water run! 💧
> 
> Your teammates are counting on you! 🙌

**Manual (admin button)**:
> 🚰 Hey Prerith! This is a reminder that it's your turn for the water run! 💧

---

## Troubleshooting

### "No WhatsApp config for [name]"
**Fix**:
1. Check `.env` file exists in the watertracker folder
2. Verify the environment variable names match EXACTLY:
   - `WHATSAPP_VISHWAS_PHONE` (not `WHATSAPP_Vishwas_PHONE`)
   - Must be ALL CAPS
   - Underscores, not spaces (`BHUVAN_GUMMA`, not `BHUVAN GUMMA`)
3. Restart the server after changing .env

### Message not received
**Fix**:
1. Verify the person sent the activation message to CallMeBot (+34 644 51 98 89)
2. Check API key is correct (no spaces)
3. Verify phone number format: `+919876543210` (no spaces/dashes)
4. Look at server console for error messages

### "WhatsApp alerts disabled"
**Fix**:
- Make sure `.env` has `ENABLE_WHATSAPP_ALERTS=true`
- Restart the server

### API Key not working
**Fix**:
1. Send the activation message again to CallMeBot
2. Wait for the reply with APIkey
3. Copy the number EXACTLY (no extra characters)
4. Update `.env` file
5. Restart server

---

## Advantages of CallMeBot vs Twilio

| Feature | CallMeBot | Twilio |
|---------|-----------|--------|
| **Cost** | FREE forever | ~$0.005 per message |
| **Setup** | 5 min | 30+ min |
| **Credit Card** | Not needed | Required |
| **Trial Period** | No limit | Limited credits |
| **Best For** | Small teams | Enterprise |

---

## Limitations

### CallMeBot Limitations:
- ⚠️ **Rate limit**: ~5 messages per minute per person
- ⚠️ **Delivery**: Usually instant, but can take up to 1 minute
- ⚠️ **No delivery confirmation**: You won't know if message failed to deliver
- ✅ **Free forever**: No hidden costs!

For your use case (5 people, occasional water runs), Call MeBot is perfect!

---

## Disabling WhatsApp Alerts

**Temporarily disable** (no code changes):
```env
ENABLE_WHATSAPP_ALERTS=false
```

**Permanently disable** remove or rename the `.env` file

---

## Alternative: Manual WhatsApp Links (Even Simpler!)

If CallMeBot doesn't work, I can implement **wa.me links** that open WhatsApp with a pre-filled message. Admin just clicks a link and presses send. Would you like me to implement this as a backup?

---

## Need Help?

- **CallMeBot Setup**: https://www.callmebot.com/blog/free-api-whatsapp-messages/
- **Test your setup**: Send `I allow callmebot to send me messages` to +34 644 51 98 89

---

**Enjoy FREE WhatsApp notifications! 💧📱**
