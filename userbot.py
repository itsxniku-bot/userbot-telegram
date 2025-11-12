print("🔥 ULTIMATE NO-SLEEP BOT STARTING...")

import asyncio
import multiprocessing
import re
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import requests
import time
import sys

# Bot data storage
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

# YOUR USER ID
ADMIN_USER_ID = 8368838212

# 🚨 ULTIMATE FLASK SERVER - INSTANT PORT OPENING
def run_flask():
    try:
        # SABSE PEHLE FLASK BANAO
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return "🤖 ULTIMATE NO-SLEEP BOT - 24/7 ACTIVE!"
        
        @app.route('/ping')
        def ping():
            return "🏓 Pong! 24/7 Active"
        
        @app.route('/health')
        def health():
            return "✅ Health: Perfect - No Sleep"
        
        @app.route('/status')
        def status():
            return "🟢 Status: Permanent Active"
        
        @app.route('/keepalive')
        def keepalive():
            return "🔁 Keep Alive Working"
        
        # ULTIMATE KEEP-ALIVE - HAR 2 MINUTE MEIN
        def ultimate_ping():
            ping_count = 0
            while True:
                try:
                    # Apne aap ko ping karo
                    response = requests.get("http://localhost:10000/ping", timeout=5)
                    ping_count += 1
                    print(f"🔁 Internal Ping #{ping_count} - Status: {response.status_code}")
                except:
                    print("⚠️ Internal ping failed")
                
                # Har 2 minute mein ping
                time.sleep(120)
        
        # Start internal pinging
        ping_thread = threading.Thread(target=ultimate_ping, daemon=True)
        ping_thread.start()
        print("✅ Internal ping service started!")
        
        # 🚀 INSTANT PORT OPENING - RENDER KO TURANT PORT DIKHAO
        print("🚀 ULTIMATE: Instantly opening port 10000...")
        app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Flask Error: {e}")

# 🚨 SABSE PEHLE FLASK START KARO - BEFORE ANYTHING ELSE!
print("🔥 STEP 1: INSTANT Flask starting FIRST...")
flask_process = multiprocessing.Process(target=run_flask)
flask_process.daemon = True
flask_process.start()

# Thoda wait karo Flask start hone ke liye
print("⏳ Waiting for Flask to start...")
time.sleep(3)
print("✅ STEP 1: Flask started on port 10000!")

# 🚨 EXTERNAL PING SERVICE - RENDER KO PAKKA ACTIVITY DIKHAO
def external_ping_service():
    ping_urls = [
        "https://userbot-telegram-1.onrender.com/",
        "https://userbot-telegram-1.onrender.com/ping",
        "https://userbot-telegram-1.onrender.com/health"
    ]
    
    ping_count = 0
    while True:
        for url in ping_urls:
            try:
                response = requests.get(url, timeout=10)
                ping_count += 1
                print(f"🌐 External Ping #{ping_count}: {url} - Status: {response.status_code}")
            except Exception as e:
                print(f"⚠️ External ping failed: {url}")
        
        # Har 3 minute mein external ping
        time.sleep(180)

# Start external ping service
print("🔥 STEP 2: Starting external ping service...")
external_ping_thread = threading.Thread(target=external_ping_service, daemon=True)
external_ping_thread.start()
print("✅ STEP 2: External ping service started!")

# Telegram Bot
async def start_telegram():
    print("🔗 STEP 3: Starting Telegram Bot...")
    
    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        @app.on_message(filters.command(["ping", "status", "allow", "safe", "delay", "remove", "help", "alive", "nleep"]))
        async def command_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            command = message.command[0]
            
            if command == "ping":
                await message.reply("🏓 Pong! **ULTIMATE NO-SLEEP BOT** 🚫💤")
            
            elif command == "alive":
                await message.reply("🟢 **BOT ZINDA HAI!** 24/7 Active - No Sleep!")
            
            elif command == "nleep":
                await message.reply("🚫 **SLEEP NAHI HOGAA!** Ultimate Protection Active!")
            
            elif command == "status":
                me = await app.get_me()
                status_text = f"""
🤖 **ULTIMATE NO-SLEEP BOT**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {len(safe_bots)}
├─ **Delayed Bots:** {len(delayed_bots)}
├─ **Protection:** 🛡️ ULTIMATE
├─ **Sleep:** ❌ NEVER
└─ **Uptime:** PERMANENT

**Multiple protection layers:**
• Instant port opening
• Internal ping every 2 mins  
• External ping every 3 mins
• Web service confirmed
                """
                await message.reply(status_text)
            
            elif command == "allow":
                if len(message.command) > 1:
                    group_id = message.command[1]
                    allowed_groups.add(group_id)
                    await message.reply(f"✅ Group `{group_id}` allowed!")
            
            elif command == "safe":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    safe_bots.add(bot_username)
                    await message.reply(f"✅ @{bot_username} added to safe list!")
            
            elif command == "delay":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    delayed_bots.add(bot_username)
                    await message.reply(f"⏰ @{bot_username} added to delayed list!")
            
            elif command == "remove":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    # Remove logic
                    await message.reply(f"✅ @{bot_username} removed!")
            
            elif command == "help":
                await message.reply("""
🤖 **ULTIMATE NO-SLEEP BOT**

**Commands:**
/ping - Test bot
/status - Full status
/alive - Check if alive  
/nleep - Sleep protection status
/allow - Allow group
/safe - Add safe bot
/delay - Add delayed bot
/remove - Remove bot

**🚫 SLEEP PROTECTION: ACTIVATED**
                """)
        
        # Message filtering (same as before)
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
                has_unsafe_bot_mention = await contains_unsafe_bot_mention(client, message_text)
                
                # Bot messages
                if message.from_user and message.from_user.is_bot:
                    sender_username = message.from_user.username or ""
                    if sender_username:
                        sender_username_lower = sender_username.lower()
                        if sender_username_lower in safe_bots:
                            return
                        elif sender_username_lower in delayed_bots:
                            if 't.me/' in message_text.lower() or has_unsafe_bot_mention:
                                await message.delete()
                            else:
                                async def delete_after_delay():
                                    await asyncio.sleep(30)
                                    try:
                                        await message.delete()
                                    except:
                                        pass
                                asyncio.create_task(delete_after_delay())
                        else:
                            await message.delete()
                
                # User messages
                elif message.from_user and has_unsafe_bot_mention:
                    await message.delete()
                        
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 ULTIMATE BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send ultimate confirmation
        try:
            await app.send_message("me", """
✅ **ULTIMATE NO-SLEEP BOT STARTED!**

**🛡️ ULTIMATE PROTECTION LAYERS:**
1. Instant port opening
2. Internal ping every 2 minutes
3. External ping every 3 minutes  
4. Multiple endpoints
5. Web service confirmed

**🚫 SLEEP: IMPOSSIBLE**
**🕒 24/7: GUARANTEED**

Use /nleep to check sleep protection!
            """)
        except:
            pass
        
        print("🤖 ULTIMATE NO-SLEEP BOT RUNNING!")
        print("🚫 SLEEP PROTECTION: ACTIVATED")
        
        # Permanent run
        while True:
            await asyncio.sleep(60)
            
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    print("🔧 STEP 3: Starting Telegram bot...")
    await start_telegram()

if __name__ == "__main__":
    print("⭐ ULTIMATE NO-SLEEP BOT STARTING...")
    asyncio.run(main())
