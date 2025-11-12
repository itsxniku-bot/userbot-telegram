import asyncio
import multiprocessing
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

print("🤖 SIMPLE DEBUG BOT STARTING...")

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
    print("🔗 STEP 1: Starting Telegram connection...")
    
    try:
        app = Client(
            "my_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        print("🔗 STEP 2: Client created")
        
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message: Message):
            print("✅ Ping command received!")
            await message.reply("🏓 PONG! Bot is working!")
        
        print("🚀 STEP 3: Starting app...")
        await app.start()
        
        me = await app.get_me()
        print(f"✅ STEP 4: BOT CONNECTED: {me.first_name} ({me.id})")
        
        print("🎯 BOT FULLY READY! Waiting for messages...")
        
        # Keep running
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())
