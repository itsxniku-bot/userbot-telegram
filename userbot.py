print("🎯 BOT STARTING WITH ALL COMMANDS...")

import asyncio
import multiprocessing
import re
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot data storage
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

# Flask Server
def start_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 Bot Server Running!"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong! Bot is alive"
    
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
    print("🔗 Starting Telegram Bot...")
    
    try:
        from pyrogram import Client, filters
        
        app = Client(
            "full_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # TEST COMMAND - Both / and ! prefixes
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message: Message):
            await message.reply("🏓 Pong! All commands working!")
            print("✅ Ping command executed")
        
        # STATUS COMMAND
        @app.on_message(filters.command("status"))
        async def status_handler(client, message: Message):
            me = await app.get_me()
            status_text = f"""
🤖 **Bot Status**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {len(safe_bots)}
└─ **Delayed Bots:** {len(delayed_bots)}

**Available Commands:**
/status - Show this status
/ping - Test bot
/allow <group_id> - Add group
/safe @bot - Add safe bot  
/delay @bot - Add delayed bot
/remove @bot - Remove bot
            """
            await message.reply(status_text)
            print("✅ Status command executed")
        
        # ALLOW COMMAND
        @app.on_message(filters.command("allow"))
        async def allow_handler(client, message: Message):
            if len(message.command) > 1:
                group_id = message.command[1]
                allowed_groups.add(group_id)
                await message.reply(f"✅ Group `{group_id}` allowed!")
                print(f"✅ Group added: {group_id}")
            else:
                await message.reply("❌ Usage: /allow <group_id>")
        
        # SAFE COMMAND
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
        
        # DELAY COMMAND
        @app.on_message(filters.command("delay"))
        async def delay_handler(client, message: Message):
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                delayed_bots.add(bot_username)
                if bot_username in safe_bots:
                    safe_bots.remove(bot_username)
                await message.reply(f"⏰ @{bot_username} added to delayed list!")
                print(f"✅ Delayed bot added: {bot_username}")
            else:
                await message.reply("❌ Usage: /delay @botusername")
        
        # REMOVE COMMAND
        @app.on_message(filters.command("remove"))
        async def remove_handler(client, message: Message):
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                removed_from = []
                
                if bot_username in safe_bots:
                    safe_bots.remove(bot_username)
                    removed_from.append('safe')
                
                if bot_username in delayed_bots:
                    delayed_bots.remove(bot_username)
                    removed_from.append('delayed')
                
                if removed_from:
                    await message.reply(f"✅ @{bot_username} removed from: {', '.join(removed_from)}")
                else:
                    await message.reply(f"❌ @{bot_username} not found in any list!")
            else:
                await message.reply("❌ Usage: /remove @botusername")
        
        # HELP COMMAND
        @app.on_message(filters.command("help"))
        async def help_handler(client, message: Message):
            help_text = """
🤖 **Bot Help Guide**

**Basic Commands:**
/start - Start the bot
/ping - Test if bot is alive
/status - Show bot status
/help - This help message

**Management Commands:**
/allow <group_id> - Allow group for filtering
/safe @bot - Add bot to safe list (won't be deleted)
/delay @bot - Add bot to delayed list (only links deleted)
/remove @bot - Remove bot from lists

**How to Use:**
1. First use /allow to add your group
2. Bot will automatically delete links and bots
3. Use /safe for important bots you want to keep
            """
            await message.reply(help_text)
            print("✅ Help command executed")
        
        # START COMMAND
        @app.on_message(filters.command("start"))
        async def start_handler(client, message: Message):
            welcome_text = """
🎉 **Welcome to Advanced Telegram Bot!**

I can help you manage your groups by:
• Deleting spam links automatically
• Managing bot messages
• Keeping your group clean

**Quick Start:**
1. Add me to your group as admin
2. Use `/allow <group_id>` to enable filtering
3. Use `/help` to see all commands

Bot is now 24/7 active! 🚀
            """
            await message.reply(welcome_text)
            print("✅ Start command executed")
        
        print("🚀 Starting Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send startup message
        try:
            await app.send_message("me", "✅ Bot Started with ALL COMMANDS!\nUse /help to see available commands.")
            print("✅ Startup message sent")
        except:
            print("⚠️ Could not send startup message")
        
        print("🤖 Bot is now running with ALL COMMANDS!")
        print("📋 Available commands: /start, /ping, /status, /help, /allow, /safe, /delay, /remove")
        
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
    print("⭐ Bot Script Starting...")
    asyncio.run(main())
