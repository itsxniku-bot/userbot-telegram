print("🎯 24/7 BOT STARTING - PERMANENT NO SLEEP...")

import asyncio
import multiprocessing
import re
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import requests
import time

# Bot data storage
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

# YOUR USER ID
ADMIN_USER_ID = 8368838212

# ULTIMATE FLASK SERVER WITH MULTIPLE PORTS
def run_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 24/7 Bot - Permanent Active!"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong! 24/7 Active"
    
    @app.route('/health')
    def health():
        return "✅ Health: Perfect - No Sleep"
    
    @app.route('/status')
    def status():
        return "🟢 Status: 24/7 Running"
    
    @app.route('/keepalive')
    def keepalive():
        return "🔁 Keep Alive Active"
    
    # ULTIMATE KEEP-ALIVE SERVICE
    def ultimate_keep_alive():
        urls = [
            "https://userbot-telegram-1.onrender.com/",
            "https://userbot-telegram-1.onrender.com/ping", 
            "https://userbot-telegram-1.onrender.com/health",
            "https://userbot-telegram-1.onrender.com/status"
        ]
        
        while True:
            for url in urls:
                try:
                    response = requests.get(url, timeout=10)
                    print(f"🔁 Auto-ping: {url} - Status: {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Ping failed: {url} - {e}")
            
            # Har 4 minute mein ping
            time.sleep(240)
    
    # Start ultimate keep-alive
    keep_alive_thread = threading.Thread(target=ultimate_keep_alive, daemon=True)
    keep_alive_thread.start()
    print("✅ Ultimate keep-alive started!")
    
    # MULTIPLE PORTS - Double protection
    def start_on_port(port):
        try:
            app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)
        except:
            pass
    
    # Try multiple ports
    print("🌐 Starting Flask on multiple ports...")
    port_thread_10000 = threading.Thread(target=start_on_port, args=(10000,), daemon=True)
    port_thread_8080 = threading.Thread(target=start_on_port, args=(8080,), daemon=True)
    port_thread_5000 = threading.Thread(target=start_on_port, args=(5000,), daemon=True)
    
    port_thread_10000.start()
    port_thread_8080.start() 
    port_thread_5000.start()
    
    print("✅ Flask running on ports: 10000, 8080, 5000")

# Start Flask in separate process
print("🚀 Starting ULTIMATE 24/7 Flask server...")
flask_process = multiprocessing.Process(target=run_flask)
flask_process.daemon = True
flask_process.start()
print("✅ ULTIMATE Flask server started!")

# Telegram Bot
async def start_telegram():
    print("🔗 Starting PERMANENT Telegram Bot...")
    
    try:
        from pyrogram import Client, filters
        
        app = Client(
            "permanent_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # Function to check if user is admin
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # COMMAND HANDLER - SIRF ADMIN KE LIYE
        @app.on_message(filters.command(["ping", "status", "allow", "safe", "delay", "remove", "help", "alive"]))
        async def command_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            command = message.command[0]
            print(f"✅ Admin command: {command}")
            
            if command == "ping":
                await message.reply("🏓 Pong! **PERMANENT 24/7 ACTIVE** - No Sleep Ever!")
            
            elif command == "alive":
                await message.reply("🟢 **BOT IS ALIVE!**\n24/7 Running - No Sleep Issues!")
            
            elif command == "status":
                me = await app.get_me()
                safe_list = ", ".join([f"@{bot}" for bot in safe_bots]) if safe_bots else "None"
                delayed_list = ", ".join([f"@{bot}" for bot in delayed_bots]) if delayed_bots else "None"
                groups_list = ", ".join(allowed_groups) if allowed_groups else "None"
                
                status_text = f"""
🤖 **PERMANENT 24/7 BOT STATUS**
├─ **Owner:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {groups_list}
├─ **Safe Bots:** {safe_list}
├─ **Delayed Bots:** {delayed_list}
├─ **Status:** 🟢 PERMANENT ACTIVE
├─ **Sleep:** ❌ NEVER
└─ **Uptime:** 24/7 FOREVER

**🔒 Normal users ignored**
**🕒 Multiple keep-alive methods**
**🌐 Multiple ports running**
                """
                await message.reply(status_text)
            
            elif command == "allow":
                if len(message.command) > 1:
                    group_id = message.command[1]
                    allowed_groups.add(group_id)
                    await message.reply(f"✅ Group `{group_id}` allowed!")
                    print(f"✅ Group added: {group_id}")
                else:
                    await message.reply("❌ Usage: /allow <group_id>")
            
            elif command == "safe":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    safe_bots.add(bot_username)
                    if bot_username in delayed_bots:
                        delayed_bots.remove(bot_username)
                    await message.reply(f"✅ @{bot_username} added to safe list!")
                    print(f"✅ Safe bot added: {bot_username}")
                else:
                    await message.reply("❌ Usage: /safe @botusername")
            
            elif command == "delay":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    delayed_bots.add(bot_username)
                    if bot_username in safe_bots:
                        safe_bots.remove(bot_username)
                    await message.reply(f"⏰ @{bot_username} added to delayed list!")
                    print(f"✅ Delayed bot added: {bot_username}")
                else:
                    await message.reply("❌ Usage: /delay @botusername")
            
            elif command == "remove":
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
            
            elif command == "help":
                help_text = """
🤖 **PERMANENT 24/7 BOT HELP**

**Admin Commands:**
/status - Full bot status  
/allow <group_id> - Allow group
/safe @bot - Add safe bot
/delay @bot - Add delayed bot
/remove @bot - Remove bot
/ping - Test bot
/alive - Check if alive

**🔒 Normal users completely ignored**
**🕒 24/7 Active - No Sleep Guaranteed**
                """
                await message.reply(help_text)
        
        # MESSAGE FILTERING
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
        
        print("🚀 Starting PERMANENT Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 PERMANENT BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send permanent confirmation
        try:
            await app.send_message("me", """
✅ **PERMANENT 24/7 BOT STARTED!**

**🛡️ ULTIMATE NO-SLEEP PROTECTION:**
• Multiple ports: 10000, 8080, 5000
• Auto-ping every 4 minutes  
• Multiple endpoints: /, /ping, /health, /status
• Web service properly detected
• 24/7 permanent active

**Normal users completely ignored**
**Bot will NEVER sleep!** 🚀
            """)
        except:
            pass
        
        print("🤖 PERMANENT 24/7 BOT IS NOW RUNNING!")
        print("💤 SLEEP PROTECTION: ACTIVATED")
        
        # PERMANENT RUN
        while True:
            await asyncio.sleep(60)
            
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        import traceback
        traceback.print_exc()

# Main execution
async def main():
    print("🔧 Starting PERMANENT main function...")
    await start_telegram()

if __name__ == "__main__":
    print("⭐ PERMANENT 24/7 BOT STARTING...")
    asyncio.run(main())
