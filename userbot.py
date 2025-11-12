import asyncio
import multiprocessing
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import sys
import types

# FIX FOR PYTHON 3.13 - imghdr replacement
try:
    import imghdr
except ImportError:
    imghdr = types.ModuleType('imghdr')
    def what(file, h=None): 
        return None
    imghdr.what = what
    sys.modules['imghdr'] = imghdr

print("🤖 BOT STARTING WITH IMGHDR FIX...")

# Flask in background
def run_flask():
    app = Flask(__name__)
    @app.route('/')
    def home(): return "🤖 Bot Alive!"
    @app.route('/ping')  
    def ping(): return "🏓 Pong!"
    print("✅ Flask running on 5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask
p = multiprocessing.Process(target=run_flask)
p.daemon = True
p.start()

# Telegram Bot
async def telegram_bot():
    print("🔗 STEP 1: Starting Telegram connection...")
    
    try:
        client = TelegramClient(
            StringSession("1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc="),
            22294121,
            "0f7fa7216b26e3f52699dc3c5a560d2a"
        )
        
        print("🔗 STEP 2: Client created, starting...")
        await client.start()
        
        me = await client.get_me()
        print(f"✅ BOT CONNECTED: {me.first_name} ({me.id})")
        
        @client.on(events.NewMessage(pattern='!ping'))
        async def handler(event):
            await event.reply('🏓 PONG! Bot is working!')
            print("✅ Ping command worked!")
        
        @client.on(events.NewMessage(pattern='!test'))
        async def test_handler(event):
            await event.reply('✅ Test successful! Bot is alive!')
        
        print("🚀 BOT READY! Waiting for messages...")
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

# Start everything
if __name__ == '__main__':
    print("🎯 MAIN SCRIPT STARTING")
    asyncio.run(telegram_bot())
