print("🎯 PRODUCTION BOT STARTING...")

import asyncio
import multiprocessing
import re
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import requests

# Bot data storage
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

# PROPER FLASK SERVER with Ping Service
def run_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 Bot Server Running - 24/7 Active!"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong! Bot is alive and running"
    
    @app.route('/health')
    def health():
        return "✅ Bot Health: Perfect"
    
    # Auto-ping to keep service alive
    def keep_alive():
        while True:
            try:
                requests.get("https://userbot-telegram-1.onrender.com/ping", timeout=10)
                print("🔁 Auto-ping sent to keep service alive")
            except:
                print("⚠️ Auto-ping failed")
            threading.Event().wait(300)  # Ping every 5 minutes
    
    # Start keep-alive in background
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    print("🌐 PRODUCTION Flask starting on port 10000...")
    # Render uses port 10000 by default
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

# Start Flask in separate process
print("🚀 Starting PRODUCTION Flask server...")
flask_process = multiprocessing.Process(target=run_flask)
flask_process.daemon = True
flask_process.start()
print("✅ PRODUCTION Flask server started on port 10000!")

# Telegram Bot
async def start_telegram():
    print("🔗 Starting Telegram Bot...")
    
    try:
        from pyrogram import Client, filters
        
        app = Client(
            "production_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # COMMANDS
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message: Message):
            await message.reply("🏓 Pong! Bot is 24/7 Active!")
        
        @app.on_message(filters.command("status"))
        async def status_handler(client, message: Message):
            me = await app.get_me()
            safe_list = ", ".join([f"@{bot}" for bot in safe_bots]) if safe_bots else "None"
            delayed_list = ", ".join([f"@{bot}" for bot in delayed_bots]) if delayed_bots else "None"
            
            status_text = f"""
🤖 **24/7 Production Bot**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {safe_list}
├─ **Delayed Bots:** {delayed_list}
├─ **Status:** 🟢 24/7 ACTIVE
└─ **Uptime:** Permanent

**No more sleep issues!** 🎉
            """
            await message.reply(status_text)
        
        # ... (rest of your command handlers same as before)
        @app.on_message(filters.command("allow"))
        async def allow_handler(client, message: Message):
            if len(message.command) > 1:
                group_id = message.command[1]
                allowed_groups.add(group_id)
                await message.reply(f"✅ Group `{group_id}` allowed!")
                print(f"✅ Group added: {group_id}")
            else:
                await message.reply("❌ Usage: /allow <group_id>")
        
        @app.on_message(filters.command("safe"))
        async def safe_handler(client, message: Message):
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                safe_bots.add(bot_username)
                if bot_username in delayed_bots:
                    delayed_bots.remove(bot_username)
                await message.reply(f"✅ @{bot_username} added to safe list!")
                print(f"✅ Safe bot added: {bot_username}")
            else:
                await message.reply("❌ Usage: /safe @botusername")
        
        # ... (other commands same as before)

        # ADVANCED MESSAGE HANDLER
        @app.on_message(filters.group)
        async def message_handler(client, message: Message):
            try:
                group_id = str(message.chat.id)
                
                if group_id not in allowed_groups:
                    return
                
                me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                message_text = message.text or message.caption or ""
                
                # Handle BOT messages
                if message.from_user and message.from_user.is_bot:
                    sender_username = message.from_user.username or ""
                    
                    if sender_username:
                        sender_username_lower = sender_username.lower()
                        
                        if sender_username_lower in safe_bots:
                            return
                        
                        if sender_username_lower in delayed_bots:
                            if 't.me/' in message_text.lower() or '@' in message_text:
                                try:
                                    await message.delete()
                                    print(f"🗑️ Deleted link from delayed bot: {sender_username}")
                                except Exception as e:
                                    print(f"❌ Failed to delete: {e}")
                            else:
                                async def delete_after_delay():
                                    await asyncio.sleep(30)
                                    try:
                                        await message.delete()
                                        print(f"⏰ Deleted normal message after 30s: {sender_username}")
                                    except:
                                        pass
                                asyncio.create_task(delete_after_delay())
                            return
                        else:
                            try:
                                await message.delete()
                                print(f"🗑️ Deleted bot: {sender_username}")
                            except Exception as e:
                                print(f"❌ Failed to delete bot: {e}")
                            return
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("🚀 Starting PRODUCTION Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 PRODUCTION BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send permanent online message
        try:
            await app.send_message("me", "✅ **24/7 Production Bot Started!**\n\nNo more sleep issues! Bot will run permanently! 🚀")
        except:
            pass
        
        print("🤖 24/7 PRODUCTION BOT IS NOW RUNNING!")
        
        # Permanent run
        while True:
            await asyncio.sleep(60)  # Keep alive
            
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        import traceback
        traceback.print_exc()

# Main execution
async def main():
    print("🔧 Starting 24/7 Production Bot...")
    await start_telegram()

if __name__ == "__main__":
    print("⭐ 24/7 PRODUCTION BOT STARTING...")
    asyncio.run(main())
