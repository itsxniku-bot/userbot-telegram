print("🔥 ULTIMATE BOT STARTING - DELETE & SLEEP PROTECTION...")

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

# YOUR USER ID
ADMIN_USER_ID = 8368838212

# 🛡️ SLEEP PROTECTION SYSTEM
class SleepProtection:
    def __init__(self):
        self.ping_count = 0
        self.start_time = time.time()
        
    def start_protection(self):
        """Start all sleep protection layers"""
        print("🛡️ Starting Sleep Protection...")
        
        # Layer 1: Flask Server
        self.start_flask()
        
        # Layer 2: External Pings
        self.start_external_pings()
        
        print("✅ SLEEP PROTECTION: 2 LAYERS ACTIVATED")
    
    def start_flask(self):
        """Layer 1: Flask Server"""
        def run_flask():
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                self.ping_count += 1
                return "🤖 BOT ACTIVE"
            
            @app.route('/ping')
            def ping():
                self.ping_count += 1
                return "🏓 Pong"
            
            # Auto-ping every 1 minute
            def auto_ping():
                while True:
                    try:
                        requests.get("http://localhost:10000/ping", timeout=5)
                    except:
                        pass
                    time.sleep(60)
            
            threading.Thread(target=auto_ping, daemon=True).start()
            app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
        
        multiprocessing.Process(target=run_flask, daemon=True).start()
        time.sleep(3)
        print("✅ Layer 1: Flask Server RUNNING")
    
    def start_external_pings(self):
        """Layer 2: External Ping Service"""
        def external_pinger():
            urls = [
                "https://userbot-telegram-1.onrender.com/",
                "https://userbot-telegram-1.onrender.com/ping"
            ]
            
            while True:
                for url in urls:
                    try:
                        requests.get(url, timeout=10)
                    except:
                        pass
                time.sleep(120)
        
        threading.Thread(target=external_pinger, daemon=True).start()
        print("✅ Layer 2: External Pings RUNNING")

# 🚀 INITIALIZE SLEEP PROTECTION
print("🛡️ Initializing Sleep Protection System...")
sleep_protection = SleepProtection()
sleep_protection.start_protection()

# 🔥 TELEGRAM BOT WITH SMART MESSAGE DELETION
async def start_telegram():
    print("🔗 Starting Telegram Bot...")
    
    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # 🔒 ADMIN COMMANDS
        @app.on_message(filters.command(["start", "status", "allow", "safe", "remove", "test"]))
        async def command_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            command = message.command[0]
            
            if command == "start":
                await message.reply("🚀 **BOT STARTED!**")
            
            elif command == "status":
                me = await app.get_me()
                status_text = f"""
🤖 **BOT STATUS**

**Features:**
├─ Message Deletion: 🗑️ ACTIVE
├─ Sleep Protection: 🛡️ ACTIVE
├─ Groups: {len(allowed_groups)}
└─ Safe Bots: {len(safe_bots)}

**Deletion Rules:**
• Bot messages → DELETE
• User messages with @bot mentions → DELETE
• User messages with @user mentions → ❌ NOT DELETE
• Normal user messages → ❌ NOT DELETE
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
            
            elif command == "test":
                test_msg = await message.reply("🧪 Testing...")
                await asyncio.sleep(3)
                await test_msg.delete()
                await message.reply("✅ Test passed!")
        
        # 🗑️ SMART MESSAGE DELETION SYSTEM
        @app.on_message(filters.group)
        async def handle_messages(client, message: Message):
            try:
                # Check group permission
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return
                
                # Ignore self messages
                me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                # Get message info
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                
                print(f"\n📨 Message in {message.chat.title}:")
                print(f"   From: {message.from_user.first_name}")
                print(f"   Is Bot: {is_bot}")
                print(f"   Text: {message_text}")
                
                # 🗑️ CASE 1: DELETE BOT MESSAGES
                if is_bot:
                    print(f"   🤖 BOT MESSAGE DETECTED")
                    
                    # Check if safe bot
                    if username in safe_bots:
                        print("   ✅ Safe bot - No action")
                        return
                    
                    # DELETE BOT MESSAGE
                    try:
                        await message.delete()
                        print("   🗑️ Bot message DELETED!")
                        return
                    except Exception as e:
                        print(f"   ❌ Delete failed: {e}")
                        return
                
                # 🗑️ CASE 2: CHECK FOR BOT MENTIONS IN USER MESSAGES
                if message_text:
                    # Find all @mentions
                    mentions = re.findall(r'@(\w+)', message_text)
                    
                    if mentions:
                        print(f"   🔍 Found mentions: {mentions}")
                        
                        for mention in mentions:
                            mention_lower = mention.lower()
                            
                            # 🚨 CRITICAL CHECK: Only delete if mentioned username is a BOT
                            # Normal user mentions will NOT be deleted
                            try:
                                # Try to get user info to check if it's a bot
                                user = await client.get_users(mention)
                                if user.is_bot:
                                    # Mentioned user is a BOT - DELETE message
                                    if mention_lower not in safe_bots:
                                        print(f"   🚫 Bot mention detected: @{mention_lower}")
                                        try:
                                            await message.delete()
                                            print("   🗑️ User message with bot mention DELETED!")
                                            return
                                        except Exception as e:
                                            print(f"   ❌ Delete failed: {e}")
                                            return
                                    else:
                                        print(f"   ✅ Safe bot mention: @{mention_lower}")
                                else:
                                    # Mentioned user is a NORMAL USER - DON'T DELETE
                                    print(f"   👤 Normal user mention: @{mention_lower} - NO DELETE")
                                    
                            except Exception as e:
                                # If we can't get user info, assume it's unsafe and delete
                                print(f"   ⚠️ Could not verify @{mention_lower}, deleting for safety")
                                if mention_lower not in safe_bots:
                                    try:
                                        await message.delete()
                                        print("   🗑️ Message with unverified mention DELETED!")
                                        return
                                    except Exception as e:
                                        print(f"   ❌ Delete failed: {e}")
                                        return
                
                print("   ✅ No deletion needed - Normal user message")
                
            except Exception as e:
                print(f"❌ Error in message handler: {e}")
        
        # Start bot connection
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        print(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # 🎯 AUTO CONFIGURATION
        allowed_groups.add("-1002129045974")  # Your group ID
        safe_bots.update(["grouphelp", "vid", "like"])  # Safe bots
        
        print(f"✅ Auto-allowed group: {allowed_groups}")
        print("🗑️ MESSAGE DELETION: READY")
        print("🛡️ SLEEP PROTECTION: ACTIVE")
        
        # Startup message
        await app.send_message("me", """
✅ **BOT STARTED SUCCESSFULLY!**

🗑️ **DELETION RULES:**
• Bot messages → DELETE
• Messages with @bot mentions → DELETE  
• Messages with @user mentions → ❌ NOT DELETE
• Normal messages → ❌ NOT DELETE

🛡️ **SLEEP PROTECTION: ACTIVE**

**READY FOR USE!**
        """)
        
        # Permanent run
        await asyncio.Future()
        
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    print("🚀 ULTIMATE BOT STARTING...")
    asyncio.run(main())
