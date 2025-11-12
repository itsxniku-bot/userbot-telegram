import asyncio
import multiprocessing
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

print("🤖 PYROGRAM BOT STARTING...")

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

# Pyrogram Bot
async def main():
    print("🔗 Connecting to Telegram...")
    
    app = Client(
        "my_bot",
        api_id=22294121,
        api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
        session_string="1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc="
    )
    
    @app.on_message(filters.command("ping"))
    async def ping_handler(client, message: Message):
        await message.reply("🏓 Pong! Pyrogram Bot Working!")
        print("✅ Ping command received")
    
    @app.on_message(filters.command("test"))
    async def test_handler(client, message: Message):
        await message.reply("✅ Test successful! Bot is alive!")
    
    print("🚀 Starting Pyrogram bot...")
    await app.start()
    me = await app.get_me()
    print(f"✅ BOT CONNECTED: {me.first_name} ({me.id})")
    print("🤖 Bot is now running...")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
