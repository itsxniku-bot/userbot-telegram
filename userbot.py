print("🎯 ADVANCED BOT STARTING...")

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
        return "🤖 Advanced Bot Server Running!"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong! Bot is alive"
    
    @app.route('/status')
    def status():
        return f"✅ Bot Status: Running | Groups: {len(allowed_groups)} | Safe Bots: {len(safe_bots)}"
    
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
    print("🔗 Starting Advanced Telegram Bot...")
    
    try:
        from pyrogram import Client, filters
        
        app = Client(
            "advanced_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # COMMAND HANDLERS
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message: Message):
            await message.reply("🏓 Pong! Advanced Bot Working!")
        
        @app.on_message(filters.command("status"))
        async def status_handler(client, message: Message):
            me = await app.get_me()
            status_text = f"""
🤖 **Advanced Bot Status**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {len(safe_bots)}
└─ **Delayed Bots:** {len(delayed_bots)}

**Commands:**
!allow <group_id> - Add group
!safe @bot - Add safe bot  
!delay @bot - Add delayed bot
!remove @bot - Remove bot
!status - Show status
!ping - Test bot
            """
            await message.reply(status_text)
        
        @app.on_message(filters.command("allow") & filters.private)
        async def allow_handler(client, message: Message):
            if len(message.command) > 1:
                group_id = message.command[1]
                allowed_groups.add(group_id)
                await message.reply(f"✅ Group `{group_id}` allowed!")
                print(f"✅ Group added: {group_id}")
            else:
                await message.reply("❌ Usage: !allow <group_id>")
        
        @app.on_message(filters.command("safe") & filters.private)
        async def safe_handler(client, message: Message):
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                safe_bots.add(bot_username)
                if bot_username in delayed_bots:
                    delayed_bots.remove(bot_username)
                await message.reply(f"✅ @{bot_username} added to safe list!")
                print(f"✅ Safe bot added: {bot_username}")
            else:
                await message.reply("❌ Usage: !safe @botusername")
        
        @app.on_message(filters.command("delay") & filters.private)
        async def delay_handler(client, message: Message):
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                delayed_bots.add(bot_username)
                if bot_username in safe_bots:
                    safe_bots.remove(bot_username)
                await message.reply(f"⏰ @{bot_username} added to delayed list!")
                print(f"✅ Delayed bot added: {bot_username}")
            else:
                await message.reply("❌ Usage: !delay @botusername")
        
        @app.on_message(filters.command("remove") & filters.private)
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
                await message.reply("❌ Usage: !remove @botusername")
        
        # MESSAGE FILTERING
        @app.on_message(filters.group)
        async def message_handler(client, message: Message):
            try:
                # Check if group is allowed
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return
                
                # Don't process own messages
                me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                message_text = message.text or message.caption or ""
                
                # Handle bot messages
                if message.from_user and message.from_user.is_bot:
                    sender_username = message.from_user.username or ""
                    if sender_username:
                        sender_username_lower = sender_username.lower()
                        
                        # Safe bots are allowed
                        if sender_username_lower in safe_bots:
                            return
                        
                        # Delayed bots - delete only links
                        if sender_username_lower in delayed_bots:
                            if message_text and ('t.me/' in message_text.lower() or '@' in message_text):
                                try:
                                    await message.delete()
                                    print(f"🗑️ Deleted link from delayed bot: {sender_username}")
                                except Exception as e:
                                    print(f"❌ Failed to delete from delayed bot: {e}")
                            return
                        else:
                            # Regular bots - delete immediately
                            try:
                                await message.delete()
                                print(f"🗑️ Deleted bot: {sender_username}")
                            except Exception as e:
                                print(f"❌ Failed to delete bot: {e}")
                            return
                
                # Delete messages with t.me links or @ mentions from users
                if message_text and ('t.me/' in message_text.lower() or '@' in message_text):
                    try:
                        await message.delete()
                        print(f"🗑️ Deleted link message from user in group {group_id}")
                    except Exception as e:
                        print(f"❌ Delete failed: {e}")
                        
            except Exception as e:
                print(f"❌ Error in handler: {e}")
        
        print("🚀 Starting Advanced Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 ADVANCED BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send startup message
        try:
            await app.send_message("me", "✅ Advanced Bot Started on Render!\nUse !status to see commands.")
            print("✅ Startup message sent")
        except:
            print("⚠️ Could not send startup message")
        
        print("🤖 Advanced Bot is now running with ALL FEATURES!")
        
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
    print("⭐ Advanced Bot Script Starting...")
    asyncio.run(main())
