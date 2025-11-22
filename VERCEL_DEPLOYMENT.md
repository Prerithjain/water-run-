# 🚀 Deploying to Vercel with Telegram

## Why isn't Telegram working on Vercel?

Your `.env` file is **local only** - it's not uploaded to Vercel (it's in `.gitignore`). You need to add the environment variables directly to Vercel.

---

## ✅ Step-by-Step: Add Environment Variables to Vercel

### Option 1: Through Vercel Dashboard (Easiest)

1. **Go to your Vercel dashboard:** https://vercel.com/dashboard

2. **Click on your project** (water-run or whatever you named it)

3. **Go to Settings** (top menu)

4. **Click "Environment Variables"** (left sidebar)

5. **Add these variables ONE BY ONE:**

   **Variable 1:**
   - Name: `ENABLE_TELEGRAM_ALERTS`
   - Value: `true`
   - Environment: Production, Preview, Development (check all three)
   - Click "Save"

   **Variable 2:**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: `8337036186:AAG_2mwnxznFqwYXGP7lR6wT_SH6nM4genl|updates` (your actual token)
   - Environment: Production, Preview, Development (check all three)
   - Click "Save"

   **Variable 3:**
   - Name: `TELEGRAM_CHAT_ID`
   - Value: `-5052917269` (your actual chat ID)
   - Environment: Production, Preview, Development (check all three)
   - Click "Save"

6. **Redeploy your app:**
   - Go to "Deployments" tab
   - Click the ⋮ (three dots) on the latest deployment
   - Click "Redeploy"
   - OR: Just push a new commit to GitHub and it will auto-deploy

---

### Option 2: Through Vercel CLI (Advanced)

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Set environment variables
vercel env add ENABLE_TELEGRAM_ALERTS
# Enter: true
# Select: Production, Preview, Development

vercel env add TELEGRAM_BOT_TOKEN
# Enter: 8337036186:AAG_2mwnxznFqwYXGP7lR6wT_SH6nM4genl|updates
# Select: Production, Preview, Development

vercel env add TELEGRAM_CHAT_ID
# Enter: -5052917269
# Select: Production, Preview, Development

# Redeploy
vercel --prod
```

---

## 🧪 Testing Your Vercel Deployment

After adding the environment variables and redeploying:

1. **Open your Vercel URL** (e.g., `https://your-app.vercel.app`)

2. **Log in as admin** (password: `water123`)

3. **Click "Send Telegram Alert"**

4. **Check your Telegram group** - you should get a message!

---

## 🔍 Troubleshooting

### Issue: Still not working after adding env vars

**Solution:** You MUST redeploy after adding environment variables!
- Go to Vercel Dashboard → Your Project → Deployments
- Click ⋮ on latest deployment → "Redeploy"

### Issue: "Failed to send alert" error

**Possible causes:**
1. Environment variables not added correctly
2. Didn't redeploy after adding variables
3. Typo in the values

**Solution:**
- Check Vercel Dashboard → Settings → Environment Variables
- Make sure all 3 variables are there
- Make sure no extra spaces in the values
- Redeploy

### Issue: How to check if env vars are loaded on Vercel?

Add a status endpoint to check (optional):

```python
# Already exists in your code!
# Just visit: https://your-app.vercel.app/api/telegram-status
```

This will show:
```json
{
  "enabled": true,
  "service": "Telegram Bot API (FREE)"
}
```

---

## 📝 Quick Checklist

- [ ] Added `ENABLE_TELEGRAM_ALERTS` to Vercel (value: `true`)
- [ ] Added `TELEGRAM_BOT_TOKEN` to Vercel (value: your bot token)
- [ ] Added `TELEGRAM_CHAT_ID` to Vercel (value: `-5052917269`)
- [ ] Selected all environments (Production, Preview, Development)
- [ ] Redeployed the app
- [ ] Tested by clicking "Send Telegram Alert"
- [ ] Received message in Telegram group ✅

---

## 🎯 Quick Reference

**Your Credentials** (for copy-paste):
```
ENABLE_TELEGRAM_ALERTS=true
TELEGRAM_BOT_TOKEN=8337036186:AAG_2mwnxznFqwYXGP7lR6wT_SH6nM4genl|updates
TELEGRAM_CHAT_ID=-5052917269
```

**Vercel Environment Variables Page:**
1. Go to: https://vercel.com/dashboard
2. Click your project
3. Settings → Environment Variables
4. Add the three variables above
5. Redeploy!

---

That's it! After adding these environment variables and redeploying, Telegram will work on Vercel! 🚀
