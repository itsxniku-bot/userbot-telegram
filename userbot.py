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
        
        # ULTIMATE KEEP-ALIVE - HAR 2 MINUTE MEIN
        def ultimate_ping():
            ping_count = 0
            while True:
                try:
                    response = requests.get("http://localhost:10000/ping", timeout=5)
                    ping_count += 1
                    print(f"🔁 Internal Ping #{ping_count} - Status: {response.status_code}")
                except:
                    print("⚠️ Internal ping failed")
                time.sleep(120)
        
        ping_thread = threading.Thread(target=ultimate_ping, daemon=True)
        ping_thread.start()
        print("✅ Internal ping service started!")
        
        # 🚀 INSTANT PORT OPENING
        print("🚀 ULTIMATE: Instantly opening port 10000...")
        app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Flask Error: {e}")

# 🚨 SABSE PEHLE FLASK START KARO
print("🔥 STEP 1: INSTANT Flask starting FIRST...")
flask_process = multiprocessing.Process(target=run_flask)
flask_process.daemon = True
flask_process.start()

time.sleep(3)
print("✅ STEP 1: Flask started on port 10000!")

# 🚨 EXTERNAL PING SERVICE
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
        time.sleep(180)

print("🔥 STEP 2: Starting external ping service...")
external_ping_thread = threading.Thread(target=external_ping_service, daemon=True)
external_ping_thread.start()
print("✅ STEP 2: External ping service started!")

# 🔥 ULTIMATE TELEGRAM BOT WITH STRICT ADMIN CONTROL
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
        
        # 🔒 STRICT ADMIN CHECK - SIRF ADMIN KO HI REPLY
        @app.on_message(filters.command(["start", "ping", "status", "allow", "safe", "delay", "remove", "help", "alive", "nleep", "test"]))
        async def command_handler(client, message: Message):
            # STRICT ADMIN CHECK - Agar admin nahi hai to kuch nahi karo
            if not is_admin(message.from_user.id):
                print(f"🚫 Unauthorized access attempt from: {message.from_user.id}")
                return  # Kuch bhi reply nahi karenge
            
            command = message.command[0]
            print(f"✅ Admin command: {command} from {message.from_user.first_name}")
            
            if command == "start":
                await message.reply("🚀 **ULTIMATE NO-SLEEP BOT STARTED!**\nUse /help for commands.")
            
            elif command == "ping":
                await message.reply("🏓 **Pong!** ULTIMATE BOT Active 🚫💤")
            
            elif command == "alive":
                await message.reply("🟢 **BOT ZINDA HAI!** 24/7 Active - No Sleep!")
            
            elif command == "nleep":
                await message.reply("🚫 **SLEEP NAHI HOGAA!** Ultimate Protection Active!")
            
            elif command == "status":
                me = await app.get_me()
                status_text = f"""
🤖 **ULTIMATE NO-SLEEP BOT STATUS**

**Bot Info:**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Username:** @{me.username}

**Protection Status:**
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {len(safe_bots)}
├─ **Delayed Bots:** {len(delayed_bots)}
├─ **Sleep Protection:** 🛡️ ACTIVATED
├─ **Message Deletion:** 🗑️ ACTIVE
├─ **Admin Only:** ✅ STRICT
└─ **Uptime:** 24/7 PERMANENT

**Use /test to check deletion functionality**
                """
                await message.reply(status_text)
            
            elif command == "allow":
                if len(message.command) > 1:
                    group_id = message.command[1]
                    allowed_groups.add(group_id)
                    await message.reply(f"✅ **Group Added!**\n`{group_id}` ko allow kar diya gaya!")
                    print(f"✅ Group allowed: {group_id}")
                else:
                    await message.reply("❌ Usage: `/allow <group_id>`")
            
            elif command == "safe":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    safe_bots.add(bot_username)
                    await message.reply(f"✅ **Safe Bot Added!**\n@{bot_username} ko safe list mein add kar diya!")
                    print(f"✅ Safe bot: @{bot_username}")
                else:
                    await message.reply("❌ Usage: `/safe @botusername`")
            
            elif command == "delay":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    delayed_bots.add(bot_username)
                    await message.reply(f"⏰ **Delayed Bot Added!**\n@{bot_username} ko delayed list mein add kar diya!")
                    print(f"⏰ Delayed bot: @{bot_username}")
                else:
                    await message.reply("❌ Usage: `/delay @botusername`")
            
            elif command == "remove":
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    safe_bots.discard(bot_username)
                    delayed_bots.discard(bot_username)
                    await message.reply(f"🗑️ **Bot Removed!**\n@{bot_username} ko sabhi lists se remove kar diya!")
                    print(f"🗑️ Removed bot: @{bot_username}")
                else:
                    await message.reply("❌ Usage: `/remove @botusername`")
            
            elif command == "test":
                # Test message deletion
                test_msg = await message.reply("🧪 **Testing Message Deletion...**\nYe message 10 second mein delete ho jana chahiye!")
                await asyncio.sleep(10)
                await test_msg.delete()
                await message.reply("✅ **Test Successful!** Message deletion kaam kar raha hai!")
            
            elif command == "help":
                help_text = """
🤖 **ULTIMATE NO-SLEEP BOT COMMANDS**

**Basic Commands:**
├─ /start - Bot start karein
├─ /ping - Bot response check karein
├─ /alive - Bot zinda hai ya nahi
├─ /nleep - Sleep protection status
├─ /status - Complete bot status
├─ /test - Message deletion test karein

**Management Commands:**
├─ /allow <group_id> - Group ko allow karein
├─ /safe @bot - Bot ko safe list mein add karein  
├─ /delay @bot - Bot ko delayed list mein add karein
├─ /remove @bot - Bot ko sabhi lists se remove karein

**Example:**
`/allow -1001234567890`
`/safe @example_bot`
`/delay @spam_bot`

🔒 **ADMIN ONLY:** ✅ STRICT
🚫 **SLEEP PROTECTION:** ACTIVATED
🗑️ **MESSAGE DELETION:** ACTIVE
                """
                await message.reply(help_text)
        
        # SIMPLE & EFFECTIVE BOT DETECTION
        def contains_bot_mention(text):
            if not text:
                return False
            mentions = re.findall(r'@(\w+)', text)
            return any(mention.lower() not in safe_bots for mention in mentions)
        
        # 🔥 ULTIMATE MESSAGE DELETION HANDLER
        @app.on_message(filters.group & ~filters.service)
        async def handle_group_messages(client, message: Message):
            try:
                # Group ID check
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return
                
                # Self messages ignore
                me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                # Get message info
                sender_name = message.from_user.first_name if message.from_user else "Unknown"
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                
                print(f"\n📨 NEW MESSAGE:")
                print(f"   Group: {message.chat.title}")
                print(f"   Sender: {sender_name} (Bot: {is_bot})")
                print(f"   Username: @{username}")
                print(f"   Text: {message_text[:50]}...")
                
                # CASE 1: BOT MESSAGES
                if is_bot:
                    print(f"   🤖 BOT MESSAGE DETECTED!")
                    
                    # Safe bot check
                    if username in safe_bots:
                        print("   ✅ Safe bot - No action")
                        return
                    
                    # Delayed bot check
                    elif username in delayed_bots:
                        print("   ⏰ Delayed bot - Will delete in 30s")
                        await asyncio.sleep(30)
                        try:
                            await message.delete()
                            print("   🗑️ Delayed bot message deleted!")
                        except Exception as e:
                            print(f"   ❌ Delete failed: {e}")
                    
                    # Unsafe bot - immediate delete
                    else:
                        print("   🚫 Unsafe bot - Immediate delete")
                        try:
                            await message.delete()
                            print("   🗑️ Bot message deleted successfully!")
                        except Exception as e:
                            print(f"   ❌ Delete failed: {e}")
                
                # CASE 2: USER MESSAGES WITH BOT MENTIONS
                elif not is_bot and contains_bot_mention(message_text):
                    print("   👤 User message with bot mention - Deleting")
                    try:
                        await message.delete()
                        print("   🗑️ User message with bot mention deleted!")
                    except Exception as e:
                        print(f"   ❌ Delete failed: {e}")
                
                else:
                    print("   ✅ No action needed")
                    
            except Exception as e:
                print(f"❌ Error in message handler: {e}")
        
        # Bot start
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        print(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Auto-add some test groups for quick testing
        test_groups = ["-1002129045974"]  # Replace with your actual group IDs
        for group in test_groups:
            allowed_groups.add(group)
        
        print(f"✅ Auto-allowed {len(allowed_groups)} groups")
        print("🔒 ADMIN RESTRICTION: STRICT MODE")
        print("🗑️ MESSAGE DELETION SYSTEM: ACTIVE")
        print("🚫 SLEEP PROTECTION: ACTIVATED")
        
        # Startup message
        await app.send_message("me", """
✅ **ULTIMATE BOT STARTED SUCCESSFULLY!**

🤖 **Bot Ready with Strict Admin Control**

🔒 **Admin Features:**
• Commands: Only you can use
• Management: Only you can manage
• Security: No unauthorized access

🗑️ **Deletion Features:**
• Bot messages - Auto delete
• Unsafe mentions - Auto delete  
• Delayed bots - Delete after 30s

🛡️ **Protection Active:**
• Sleep protection
• 24/7 uptime
• Strict admin only

**Quick Start:**
1. Use `/allow -100groupid` to allow your group
2. Use `/test` to check deletion
3. Use `/status` to see bot status

**🔒 Bot commands are now ADMIN ONLY!**
        """)
        
        # Permanent run
        await asyncio.Future()  # Never ending
        
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    print("🔧 STEP 3: Starting Telegram bot...")
    await start_telegram()

if __name__ == "__main__":
    print("🚀 ULTIMATE NO-SLEEP BOT STARTING...")
    asyncio.run(main())
