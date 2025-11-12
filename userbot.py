# IMGHDR FIX - Python 3.13 Compatibility
import sys
import types
try:
    import imghdr
except ImportError:
    imghdr = types.ModuleType('imghdr')
    def what(file, h=None): return None
    imghdr.what = what
    sys.modules['imghdr'] = imghdr

import os
import asyncio
import multiprocessing
from flask import Flask

print("🚀 Starting UserBot...")

# Flask function for separate process
def run_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 Telegram Bot is Running on Render!"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong! Bot is alive"
    
    print("🌐 Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask in separate process
flask_process = multiprocessing.Process(target=run_flask, daemon=True)
flask_process.start()
print("🌐 Flask server started in separate process")

# Telegram Bot Part
async def test_telegram():
    from telethon import TelegramClient
    from telethon.sessions import StringSession
    
    api_id = 22294121
    api_hash = "0f7fa7216b26e3f52699dc3c5a560d2a"
    session_string = "1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc="
    
    try:
        print("🔗 Connecting to Telegram...")
        client = TelegramClient(StringSession(session_string), api_id, api_hash)
        await client.start()
        
        me = await client.get_me()
        print(f"✅ SUCCESS! Bot connected: {me.first_name} (ID: {me.id})")
        
        # Keep running
        print("🚀 Bot is now running...")
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"❌ Telegram connection failed: {e}")
        print("ℹ️ Possible issues: Invalid session, API credentials, or network")

# Run the bot
if __name__ == '__main__':
    asyncio.run(test_telegram())
