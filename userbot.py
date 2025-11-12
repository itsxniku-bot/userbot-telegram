print("🎯 BOT STARTING WITH ADMIN-ONLY COMMANDS...")

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

# YOUR USER ID - YAHAN APNA USER ID DALNA
ADMIN_USER_ID = 8368838212  # Tumhara User ID yahan dalo

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
            "admin_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # Function to check if user is admin
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # PUBLIC COMMANDS - Har koi use kar sakta hai
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message: Message):
            await message.reply("🏓 Pong! Bot is active!")
        
        @app.on_message(filters.command("help"))
        async def help_handler(client, message: Message):
            help_text = """
🤖 **Bot Help**

**Public Commands:**
/ping - Check if bot is alive
/help - Show this help

**Admin Commands:** (Only bot owner can use)
/status - Bot status
/allow <group_id> - Allow group
/safe @bot - Add safe bot
/delay @bot - Add delayed bot  
/remove @bot - Remove bot
            """
            await message.reply(help_text)
        
        # ADMIN-ONLY COMMANDS - Sirf tum use kar sakte ho
        @app.on_message(filters.command("status"))
        async def status_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                await message.reply("❌ This command is for bot owner only!")
                return
                
            me = await app.get_me()
            safe_list = ", ".join([f"@{bot}" for bot in safe_bots]) if safe_bots else "None"
            delayed_list = ", ".join([f"@{bot}" for bot in delayed_bots]) if delayed_bots else "None"
            groups_list = ", ".join(allowed_groups) if allowed_groups else "None"
            
            status_text = f"""
🤖 **Admin Bot Status**
├─ **Owner:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {groups_list}
├─ **Safe Bots:** {safe_list}
├─ **Delayed Bots:** {delayed_list}

**Commands working perfectly!** ✅
            """
            await message.reply(status_text)
            print("✅ Status command executed by admin")
        
        @app.on_message(filters.command("allow"))
        async def allow_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                await message.reply("❌ This command is for bot owner only!")
                return
                
            if len(message.command) > 1:
                group_id = message.command[1]
                allowed_groups.add(group_id)
                await message.reply(f"✅ Group `{group_id}` allowed!")
                print(f"✅ Group added by admin: {group_id}")
            else:
                await message.reply("❌ Usage: /allow <group_id>")
        
        @app.on_message(filters.command("safe"))
        async def safe_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                await message.reply("❌ This command is for bot owner only!")
                return
                
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                safe_bots.add(bot_username)
                if bot_username in delayed_bots:
                    delayed_bots.remove(bot_username)
                await message.reply(f"✅ @{bot_username} added to safe list!")
                print(f"✅ Safe bot added by admin: {bot_username}")
            else:
                await message.reply("❌ Usage: /safe @botusername")
        
        @app.on_message(filters.command("delay"))
        async def delay_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                await message.reply("❌ This command is for bot owner only!")
                return
                
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                delayed_bots.add(bot_username)
                if bot_username in safe_bots:
                    safe_bots.remove(bot_username)
                await message.reply(f"⏰ @{bot_username} added to delayed list!")
                print(f"✅ Delayed bot added by admin: {bot_username}")
            else:
                await message.reply("❌ Usage: /delay @botusername")
        
        @app.on_message(filters.command("remove"))
        async def remove_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                await message.reply("❌ This command is for bot owner only!")
                return
                
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
        
        # MESSAGE FILTERING (Working as before)
        async def contains_unsafe_bot_mention(client, text):
            if not text:
                return False
            
            mentions = re.findall(r'@(\w+)', text)
            
            for mention in mentions:
                mention_lower = mention.lower()
                if mention_lower in safe_bots:
                    continue
                if mention_lower in delayed_bots:
                    return True
                try:
                    user = await client.get_users(mention)
                    if user.is_bot and mention_lower not in safe_bots:
                        return True
                except:
                    if mention_lower not in safe_bots:
                        return True
            return False
        
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
                has_links = 't.me/' in message_text.lower() or 'http' in message_text.lower()
                has_unsafe_bot_mention = await contains_unsafe_bot_mention(client, message_text)
                
                # Handle BOT messages
                if message.from_user and message.from_user.is_bot:
                    sender_username = message.from_user.username or ""
                    
                    if sender_username:
                        sender_username_lower = sender_username.lower()
                        
                        if sender_username_lower in safe_bots:
                            return
                        
                        if sender_username_lower in delayed_bots:
                            if has_links or has_unsafe_bot_mention:
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
                
                # Handle NORMAL USER messages
                elif message.from_user:
                    if has_unsafe_bot_mention:
                        try:
                            await message.delete()
                            print(f"🗑️ Deleted user message with unsafe bot mention")
                        except Exception as e:
                            print(f"❌ Failed to delete user message: {e}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("🚀 Starting Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send admin info
        try:
            await app.send_message("me", f"""
✅ **Admin-Only Bot Started!**

**🔐 Admin Protection Enabled:**
• Only you (ID: {ADMIN_USER_ID}) can use management commands
• Others will get "command for owner only" message
• Public commands: /ping, /help

**Bot is ready with admin protection!** 🛡️
            """)
        except:
            pass
        
        print("🤖 Admin-Only Bot is now running!")
        
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
    print("⭐ Admin-Only Bot Starting...")
    asyncio.run(main())
