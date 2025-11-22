"""
Telegram Bot Test Script
This script helps you test your Telegram bot configuration
"""

import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 60)
print("TELEGRAM BOT CONFIGURATION TEST")
print("=" * 60)

# Test 1: Check if credentials are loaded
print("\n1. Checking environment variables...")
if not TELEGRAM_BOT_TOKEN:
    print("   ❌ TELEGRAM_BOT_TOKEN is not set in .env file!")
    exit(1)
else:
    print(f"   ✅ Bot Token found: {TELEGRAM_BOT_TOKEN[:20]}...")

if not TELEGRAM_CHAT_ID:
    print("   ❌ TELEGRAM_CHAT_ID is not set in .env file!")
    exit(1)
else:
    print(f"   ✅ Chat ID found: {TELEGRAM_CHAT_ID}")
    if TELEGRAM_CHAT_ID.startswith('-'):
        print("   ✅ Chat ID is negative (looks like a group ID)")
    else:
        print("   ⚠️  Chat ID is positive (this is a personal chat ID, not a group!)")

# Test 2: Test bot token
print("\n2. Testing bot token validity...")
try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    response = requests.get(url)
    data = response.json()
    
    if data.get('ok'):
        bot_info = data.get('result', {})
        print(f"   ✅ Bot token is valid!")
        print(f"   Bot name: {bot_info.get('first_name')}")
        print(f"   Bot username: @{bot_info.get('username')}")
    else:
        print(f"   ❌ Bot token is invalid: {data}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error testing bot token: {e}")
    exit(1)

# Test 3: Get chat info
print("\n3. Getting chat information...")
try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat"
    params = {"chat_id": TELEGRAM_CHAT_ID}
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get('ok'):
        chat_info = data.get('result', {})
        print(f"   ✅ Chat found!")
        print(f"   Chat type: {chat_info.get('type')}")
        print(f"   Chat title: {chat_info.get('title', 'N/A')}")
        
        if chat_info.get('type') == 'private':
            print("\n   ⚠️  WARNING: This is a PRIVATE chat (personal messages)!")
            print("   You need to use a GROUP chat ID for group messages!")
        elif chat_info.get('type') in ['group', 'supergroup']:
            print(f"   ✅ This is a {chat_info.get('type').upper()} - perfect!")
    else:
        error_desc = data.get('description', 'Unknown error')
        print(f"   ❌ Error getting chat info: {error_desc}")
        if 'bot was kicked' in error_desc.lower():
            print("   💡 Solution: Add the bot back to the group!")
        elif 'chat not found' in error_desc.lower():
            print("   💡 Solution: Make sure the chat ID is correct!")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 4: Send test message
print("\n4. Sending test message...")
try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "🧪 <b>Test Message</b>\n\nIf you see this, your Telegram bot is configured correctly! ✅",
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data.get('ok'):
        print("   ✅ Test message sent successfully!")
        print("   📱 Check your Telegram group/chat for the message!")
    else:
        error_desc = data.get('description', 'Unknown error')
        print(f"   ❌ Failed to send message: {error_desc}")
        
        if 'bot was blocked' in error_desc.lower():
            print("   💡 Solution: Unblock the bot in Telegram!")
        elif 'chat not found' in error_desc.lower():
            print("   💡 Solution: Double-check the chat ID!")
        elif 'bot is not a member' in error_desc.lower():
            print("   💡 Solution: Add the bot to the group!")
        elif "have no rights to send" in error_desc.lower():
            print("   💡 Solution: Make the bot an admin or enable 'All Members Can Send Messages'!")
        
        exit(1)
except Exception as e:
    print(f"   ❌ Error sending message: {e}")
    exit(1)

# Success!
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("Your Telegram bot is configured correctly!")
print("=" * 60)
