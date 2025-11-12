print("🎯 BOT STARTING WITH ADVANCED FILTERING...")

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
            "advanced_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # COMMANDS
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message: Message):
            await message.reply("🏓 Pong! Advanced filtering active!")
        
        @app.on_message(filters.command("status"))
        async def status_handler(client, message: Message):
            me = await app.get_me()
            safe_list = ", ".join([f"@{bot}" for bot in safe_bots]) if safe_bots else "None"
            delayed_list = ", ".join([f"@{bot}" for bot in delayed_bots]) if delayed_bots else "None"
            
            status_text = f"""
🤖 **Advanced Filter Bot**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {safe_list}
├─ **Delayed Bots:** {delayed_list}

**🔧 Filter Rules:**
• Normal users: Delete unsafe bot links
• Regular bots: Delete all messages
• Delayed bots: Delete links immediately, normal messages after 30s
• Safe bots: No deletion
            """
            await message.reply(status_text)
        
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
        
        # Function to check if message contains unsafe bot mention
        def contains_unsafe_bot_mention(text):
            if not text:
                return False
            
            # Find all @mentions in the message
            mentions = re.findall(r'@(\w+)', text)
            
            for mention in mentions:
                mention_lower = mention.lower()
                # If mentioned bot is NOT in safe list, it's unsafe
                if mention_lower not in safe_bots:
                    return True
            
            return False
        
        # ADVANCED MESSAGE HANDLER
        @app.on_message(filters.group)
        async def advanced_handler(client, message: Message):
            try:
                group_id = str(message.chat.id)
                
                # Check if group is allowed
                if group_id not in allowed_groups:
                    return
                
                # Don't process own messages
                me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                message_text = message.text or message.caption or ""
                has_links = 't.me/' in message_text.lower() or 'http' in message_text.lower()
                has_unsafe_mention = contains_unsafe_bot_mention(message_text)
                
                # Handle BOT messages
                if message.from_user and message.from_user.is_bot:
                    sender_username = message.from_user.username or ""
                    print(f"🤖 Bot message: {sender_username}")
                    
                    if sender_username:
                        sender_username_lower = sender_username.lower()
                        
                        # Safe bots - NO DELETE
                        if sender_username_lower in safe_bots:
                            print(f"✅ Safe bot allowed: {sender_username}")
                            return
                        
                        # Delayed bots - Delete links immediately, normal messages after 30s
                        if sender_username_lower in delayed_bots:
                            if has_links or has_unsafe_mention:
                                try:
                                    await message.delete()
                                    print(f"🗑️ Immediately deleted link from delayed bot: {sender_username}")
                                except Exception as e:
                                    print(f"❌ Failed to delete from delayed bot: {e}")
                            else:
                                # Normal message - delete after 30 seconds
                                async def delete_after_delay():
                                    await asyncio.sleep(30)
                                    try:
                                        await message.delete()
                                        print(f"⏰ Deleted normal message from delayed bot after 30s: {sender_username}")
                                    except:
                                        pass
                                
                                asyncio.create_task(delete_after_delay())
                            return
                        else:
                            # Regular bots - DELETE ALL MESSAGES IMMEDIATELY
                            try:
                                await message.delete()
                                print(f"🗑️ Deleted all messages from regular bot: {sender_username}")
                            except Exception as e:
                                print(f"❌ Failed to delete bot: {e}")
                            return
                
                # Handle NORMAL USER messages
                elif message.from_user:
                    print(f"👤 Normal user: {message.from_user.first_name}")
                    
                    # Delete if contains unsafe bot mention or links to unsafe bots
                    if has_unsafe_mention:
                        try:
                            await message.delete()
                            print(f"🗑️ Deleted user message with unsafe bot mention")
                        except Exception as e:
                            print(f"❌ Failed to delete user message: {e}")
                
            except Exception as e:
                print(f"❌ Error in handler: {e}")
        
        print("🚀 Starting Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send startup message
        try:
            await app.send_message("me", """
✅ **Advanced Filter Bot Started!**

**🎯 Filter Rules:**
• 👤 Normal users: Delete unsafe bot mentions
• 🤖 Regular bots: Delete all messages immediately  
• ⏰ Delayed bots: Delete links immediately, normal messages after 30s
• ✅ Safe bots: No deletion

**Use /safe @bot to protect important bots!** 🛡️
            """)
        except:
            pass
        
        print("🤖 Advanced Filter Bot is now running!")
        
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
