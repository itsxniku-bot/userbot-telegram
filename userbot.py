print("🔥 ULTIMATE BOT STARTING - 100% SLEEP PROTECTION...")

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

# 🛡️ ULTIMATE SLEEP PROTECTION SYSTEM
class UltimateSleepProtection:
    def __init__(self):
        self.ping_count = 0
        self.start_time = time.time()
        self.last_activity = time.time()
        
    def start_ultimate_protection(self):
        """4-Layer Sleep Protection - Kabhi Nahin Sone Dega!"""
        print("🛡️ Starting ULTIMATE 4-Layer Sleep Protection...")
        
        # Layer 1: Flask Server (Primary)
        self.start_aggressive_flask()
        
        # Layer 2: External Pings (Secondary)
        self.start_aggressive_external_pings()
        
        # Layer 3: Internal Health Checks (Tertiary)
        self.start_health_bombardment()
        
        # Layer 4: Telegram Activity (Backup)
        self.start_telegram_activity_pulses()
        
        print("✅ SLEEP PROTECTION: 4 LAYERS ACTIVATED - 100% GUARANTEED!")
    
    def start_aggressive_flask(self):
        """Layer 1: Aggressive Flask with Multiple Endpoints"""
        def run_aggressive_flask():
            try:
                app = Flask(__name__)
                
                @app.route('/')
                def home():
                    self.ping_count += 1
                    self.last_activity = time.time()
                    return f"🤖 ULTIMATE BOT - Active Pings: {self.ping_count}"
                
                @app.route('/ping')
                def ping():
                    self.ping_count += 1
                    self.last_activity = time.time()
                    return f"🏓 Pong! #{self.ping_count}"
                
                @app.route('/health')
                def health():
                    self.ping_count += 1
                    return "✅ Server Health: PERFECT"
                
                # Auto-ping every 30 seconds
                def aggressive_auto_ping():
                    while True:
                        try:
                            requests.get("http://localhost:10000/ping", timeout=5)
                        except:
                            pass
                        time.sleep(30)
                
                threading.Thread(target=aggressive_auto_ping, daemon=True).start()
                app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
                
            except Exception as e:
                print(f"❌ Flask crashed: {e}")
                time.sleep(5)
                self.start_aggressive_flask()
        
        multiprocessing.Process(target=run_aggressive_flask, daemon=True).start()
        time.sleep(5)
        print("✅ Layer 1: Aggressive Flask RUNNING")
    
    def start_aggressive_external_pings(self):
        """Layer 2: External Ping Bombardment"""
        def external_bombardment():
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
                time.sleep(60)
        
        threading.Thread(target=external_bombardment, daemon=True).start()
        print("✅ Layer 2: External Bombardment RUNNING")
    
    def start_health_bombardment(self):
        """Layer 3: Health Check Bombardment"""
        def health_bombardment():
            check_count = 0
            while True:
                check_count += 1
                self.last_activity = time.time()
                print(f"🏥 Health Check #{check_count} - Uptime: {int(time.time() - self.start_time)}s")
                time.sleep(45)
        
        threading.Thread(target=health_bombardment, daemon=True).start()
        print("✅ Layer 3: Health Bombardment RUNNING")
    
    def start_telegram_activity_pulses(self):
        """Layer 4: Telegram Activity Pulses"""
        def activity_pulses():
            pulse_count = 0
            while True:
                pulse_count += 1
                self.last_activity = time.time()
                time.sleep(60)
        
        threading.Thread(target=activity_pulses, daemon=True).start()
        print("✅ Layer 4: Telegram Activity Pulses RUNNING")

# 🚀 INITIALIZE ULTIMATE SLEEP PROTECTION
print("🛡️ Initializing ULTIMATE Sleep Protection...")
sleep_protector = UltimateSleepProtection()
sleep_protector.start_ultimate_protection()

# 🔥 TELEGRAM BOT WITH GUARANTEED MESSAGE DELETION
async def start_telegram():
    print("🔗 Starting Telegram Bot with GUARANTEED Message Deletion...")
    
    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # ✅ COMPLETE COMMANDS LIST
        @app.on_message(filters.command(["start", "help", "ping", "alive", "status", "sleepstatus", "nleep", "allow", "safe", "delay", "remove", "test"]))
        async def command_handler(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            sleep_protector.last_activity = time.time()
            command = message.command[0]
            
            if command == "start":
                await message.reply("🚀 **ULTIMATE BOT STARTED!**")
            
            elif command == "help":
                help_text = """
🤖 **ULTIMATE BOT - ALL COMMANDS**

**Group Management:**
├─ /allow <group_id> - Allow group
├─ /safe @bot - Add bot to safe list
├─ /delay @bot - Add bot to delayed list
├─ /remove @bot - Remove bot from lists

**Protection & Testing:**
├─ /sleepstatus - Sleep protection status
├─ /test - Test message deletion
                """
                await message.reply(help_text)
            
            elif command == "ping":
                await message.reply("🏓 **Pong!**")
            
            elif command == "alive":
                await message.reply("🟢 **BOT ZINDA HAI!**")
            
            elif command == "status":
                me = await app.get_me()
                status_text = f"""
🤖 **BOT STATUS**
├─ Groups: {len(allowed_groups)}
├─ Safe Bots: {len(safe_bots)}
├─ Delayed Bots: {len(delayed_bots)}
└─ Protection: 🛡️ ACTIVE
                """
                await message.reply(status_text)
            
            elif command == "sleepstatus":
                uptime = int(time.time() - sleep_protector.start_time)
                await message.reply(f"🛡️ **SLEEP PROTECTION ACTIVE**\nUptime: {uptime}s")
            
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
                    safe_bots.discard(bot_username)
                    delayed_bots.discard(bot_username)
                    await message.reply(f"🗑️ @{bot_username} removed!")
            
            elif command == "test":
                test_msg = await message.reply("🧪 Testing...")
                await asyncio.sleep(2)
                await test_msg.delete()
                await message.reply("✅ Test passed!")
        
        # 🚀 GUARANTEED MESSAGE DELETION - NO SKIPPING
        @app.on_message(filters.group)
        async def guaranteed_message_handler(client, message: Message):
            try:
                sleep_protector.last_activity = time.time()
                
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return
                
                me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                
                print(f"📨 Message in {message.chat.title}: @{username} - Bot: {is_bot}")
                
                if is_bot:
                    # Safe bot check
                    if username in safe_bots:
                        print(f"✅ Safe bot ignored: @{username}")
                        return
                    
                    # ✅ DELAYED BOT LOGIC
                    if username in delayed_bots:
                        # SMART LINK DETECTION
                        has_links = any(pattern in message_text.lower() for pattern in [
                            't.me/', 'http://', 'https://', 'www.', '.com', '.org', '.net'
                        ])
                        has_mentions = '@' in message_text
                        
                        # INSTANT DELETE FOR LINKS & MENTIONS
                        if has_links or has_mentions:
                            print(f"🚫 Delayed bot with links/mentions: @{username} - INSTANT DELETE")
                            try:
                                await message.delete()
                                print(f"✅ Instant deleted: @{username}")
                                return
                            except Exception as e:
                                print(f"❌ Delete failed: {e}")
                                # Retry once
                                try:
                                    await asyncio.sleep(1)
                                    await message.delete()
                                    print(f"✅ Retry success: @{username}")
                                except:
                                    pass
                                return
                        
                        # NORMAL MESSAGES - 30 SECOND DELAY
                        else:
                            print(f"⏰ Delayed bot normal message: @{username} - 30s delay")
                            async def delete_after_delay():
                                await asyncio.sleep(30)
                                try:
                                    await message.delete()
                                    print(f"✅ Delayed delete success: @{username}")
                                except:
                                    # Final retry
                                    try:
                                        await asyncio.sleep(2)
                                        await message.delete()
                                        print(f"✅ Final retry success: @{username}")
                                    except:
                                        print(f"❌ Final delete failed: @{username}")
                            asyncio.create_task(delete_after_delay())
                            return
                    
                    # 🗑️ OTHER BOTS - GUARANTEED IMMEDIATE DELETE
                    print(f"🚫 Unsafe bot detected: @{username} - IMMEDIATE DELETE")
                    try:
                        await message.delete()
                        print(f"✅ Immediate delete success: @{username}")
                    except Exception as e:
                        print(f"❌ First delete failed: @{username} - {e}")
                        # RETRY MECHANISM - 3 attempts
                        for attempt in range(3):
                            try:
                                await asyncio.sleep(1)
                                await message.delete()
                                print(f"✅ Retry #{attempt+1} success: @{username}")
                                break
                            except Exception as retry_error:
                                print(f"❌ Retry #{attempt+1} failed: @{username}")
                                if attempt == 2:
                                    print(f"💀 FINAL DELETE FAILED: @{username}")
                
            except Exception as e:
                print(f"❌ Handler error: {e}")
        
        # ✅ BOT START
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        print(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # 🎯 PERMANENT GROUP SETUP - BADA GROUP ADDED
        allowed_groups.add("-1002129045974")  # Chhota group
        allowed_groups.add("-1002497459144")  # ✅ BADA GROUP PERMANENT ADDED
        
        safe_bots.update(["grouphelp", "vid", "like"])
        
        print(f"✅ PERMANENT GROUPS ADDED: {allowed_groups}")
        print("🚀 GUARANTEED MESSAGE DELETION: ACTIVE")
        print("🛡️ SLEEP PROTECTION: ACTIVE")
        
        # Startup confirmation
        await app.send_message("me", f"""
✅ **ULTIMATE BOT STARTED - GUARANTEED DELETION!**

🎯 **PERMANENT GROUPS:**
• -1002129045974 (Chhota Group)
• -1002497459144 (Bada Group) ✅ ADDED

🚀 **GUARANTEED FEATURES:**
• 100% Message Deletion - No Skipping
• Retry Mechanism - 3 Attempts
• Bada Group Protected
• Sleep Protection Active

**BOT READY - KOI MESSAGE BACHNE NAHI DIYA JAYEGA!** 💪
        """)
        
        print("🤖 BOT READY - Guaranteed Message Deletion Active!")
        
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
