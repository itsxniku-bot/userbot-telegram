print("🎯 BOT SCRIPT STARTING...")

import asyncio
import multiprocessing
from flask import Flask

# Flask Server
def start_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 Bot Server Running!"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong!"
    
    @app.route('/status')
    def status():
        return "✅ Bot Status: Starting..."
    
    print("🌐 Flask starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask in background
print("🚀 Starting Flask server...")
flask_process = multiprocessing.Process(target=start_flask)
flask_process.daemon = True
flask_process.start()
print("✅ Flask server started!")

# Telegram Bot
async def start_telegram():
    print("🔗 Attempting Telegram connection...")
    
    try:
        from pyrogram import Client, filters
        
        print("✅ Pyrogram imported successfully")
        
        app = Client(
            "render_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        print("✅ Client created")
        
        @app.on_message(filters.command("start"))
        async def start_handler(client, message):
            await message.reply("🤖 Bot is alive!")
        
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message):
            await message.reply("🏓 Pong! Working!")
            print("✅ Ping command executed")
        
        print("🚀 Starting Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 BOT CONNECTED SUCCESSFULLY: {me.first_name} ({me.id})")
        
        # Send startup message
        try:
            await app.send_message("me", "✅ Bot started on Render!")
            print("✅ Startup message sent")
        except:
            print("⚠️ Could not send startup message")
        
        print("🤖 Bot is now running and ready!")
        
        # Keep alive
        while True:
            await asyncio.sleep(10)
            
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        import traceback
        traceback.print_exc()

# Main execution
async def main():
    print("🔧 Starting main function...")
    await start_telegram()

if __name__ == "__main__":
    print("⭐ Script entry point reached")
    asyncio.run(main())
