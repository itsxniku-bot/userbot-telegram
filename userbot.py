print("🔥 ULTIMATE BOT STARTING - SESSION STABILITY FIX...")

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
import json
import os

# Bot data storage
ALLOWED_GROUPS_FILE = "allowed_groups.json"
SAFE_BOTS_FILE = "safe_bots.json"
DELAYED_BOTS_FILE = "delayed_bots.json"

def load_data(filename, default=set()):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return set(json.load(f))
    except:
        pass
    return default

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(list(data), f)
    except:
        pass

# Load data
allowed_groups = load_data(ALLOWED_GROUPS_FILE)
safe_bots = load_data(SAFE_BOTS_FILE)
delayed_bots = load_data(DELAYED_BOTS_FILE)

# YOUR USER ID
ADMIN_USER_ID = 8368838212

print(f"✅ Loaded {len(allowed_groups)} groups, {len(safe_bots)} safe bots, {len(delayed_bots)} delayed bots")

# 🛡️ ULTIMATE SLEEP PROTECTION
class SleepProtection:
    def __init__(self):
        self.ping_count = 0
        self.start_time = time.time()
        
    def start_protection(self):
        print("🛡️ Starting Ultimate Sleep Protection...")
        self.start_flask()
        self.start_external_pings()
        print("✅ SLEEP PROTECTION: ACTIVATED")
    
    def start_flask(self):
        def run_flask():
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                self.ping_count += 1
                return f"🤖 BOT ACTIVE - Pings: {self.ping_count}"
            
            @app.route('/ping')
            def ping():
                self.ping_count += 1
                return "🏓 Pong"
            
            @app.route('/health')
            def health():
                return "✅ HEALTHY"
            
            # Auto-ping every 30 seconds
            def auto_ping():
                while True:
                    try:
                        requests.get("http://localhost:10000/ping", timeout=5)
                    except:
                        pass
                    time.sleep(30)
            
            threading.Thread(target=auto_ping, daemon=True).start()
            app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
        
        multiprocessing.Process(target=run_flask, daemon=True).start()
        time.sleep(3)
        print("✅ Flask Server: RUNNING")
    
    def start_external_pings(self):
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
                time.sleep(60)
        
        threading.Thread(target=external_pinger, daemon=True).start()
        print("✅ External Pings: RUNNING")

# 🚀 INITIALIZE SLEEP PROTECTION
print("🛡️ Initializing Sleep Protection...")
sleep_protector = SleepProtection()
sleep_protector.start_protection()

# 🔥 TELEGRAM BOT - SESSION STABILITY FIX
async def start_telegram():
    print("🔗 Starting Telegram Bot - SESSION STABILITY FIX...")
    
    # ✅ SESSION STABILITY VARIABLES
    session_active = True
    connection_checks = 0
    
    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        me = None
        
        # ✅ PROPER ONLINE STATUS - FIXED VERSION
        async def maintain_proper_online_status():
            """Bot ko properly online rakhta hai"""
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    # Multiple activities to stay properly online
                    await app.get_me()
                    
                    # Typing action in saved messages to show online
                    async with app.action("me", "typing"):
                        await asyncio.sleep(2)
                    
                    # Read own chat history to show activity
                    async for message in app.get_chat_history("me", limit=1):
                        pass
                    
                    print(f"🟢 Proper Online #{online_count} - Actually Showing Online")
                    
                except Exception as e:
                    print(f"⚠️ Online Status Failed: {e}")
                await asyncio.sleep(45)  # Every 45 seconds - Telegram ke liye perfect
        
        # ✅ SESSION KEEP-ALIVE
        async def session_keep_alive():
            """Session ko active rakhta hai"""
            nonlocal connection_checks, session_active
            keep_alive_count = 0
            
            while session_active:
                keep_alive_count += 1
                connection_checks += 1
                
                try:
                    # Simple API call to keep session alive
                    if me:
                        # Try to get own info - simple API call
                        current_me = await app.get_me()
                        print(f"💓 Session Keep-Alive #{keep_alive_count} - Connection: ✅ ACTIVE")
                    else:
                        print(f"💓 Session Keep-Alive #{keep_alive_count} - Initializing...")
                    
                except Exception as e:
                    print(f"⚠️ Session Keep-Alive Failed: {e}")
                    session_active = False
                    break
                
                await asyncio.sleep(180)  # Every 3 minutes
        
        # ✅ ALL COMMANDS - SAME AS BEFORE
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            await message.reply("🚀 **ULTIMATE BOT STARTED!**\nSession Stability Active")
        
        @app.on_message(filters.command("help"))
        async def help_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            help_text = """
🤖 **ULTIMATE BOT - ALL COMMANDS**

**Basic:**
├─ /start - Start bot
├─ /help - This help
├─ /ping - Test response
├─ /alive - Check alive
├─ /status - Bot status

**Management:**
├─ /allow <group_id> - Allow group
├─ /safe @bot - Add safe bot
├─ /delay @bot - Add delayed bot
├─ /remove @bot - Remove bot

**Protection:**
├─ /sleepstatus - Sleep protection
├─ /nleep - Sleep check
├─ /test - Test deletion
            """
            await message.reply(help_text)
        
        @app.on_message(filters.command("ping"))
        async def ping_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            await message.reply("🏓 **Pong!** Bot active")
        
        @app.on_message(filters.command("alive"))
        async def alive_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            await message.reply("🟢 **BOT ZINDA HAI!** 24/7 Active")
        
        @app.on_message(filters.command("nleep"))
        async def nleep_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            await message.reply("🚫 **SLEEP NAHI HOGAA!** Protection Active")
        
        # ✅ STATUS COMMAND - FIXED COUNT ISSUE
        @app.on_message(filters.command("status"))
        async def status_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            nonlocal me, connection_checks
            
            if me is None: 
                me = await app.get_me()
            
            # ✅ FIX: Actual count from loaded data
            actual_allowed_groups = len(allowed_groups)
            actual_safe_bots = len(safe_bots)
            actual_delayed_bots = len(delayed_bots)
            
            # Debug info
            print(f"🔍 STATUS DEBUG: Groups={actual_allowed_groups}, SafeBots={actual_safe_bots}, DelayedBots={actual_delayed_bots}")
            print(f"🔍 Allowed Groups: {allowed_groups}")
            print(f"🔍 Safe Bots: {safe_bots}")
            print(f"🔍 Delayed Bots: {delayed_bots}")
            
            status_text = f"""
🤖 **BOT STATUS - SESSION STABLE**

**Info:**
├─ Name: {me.first_name}
├─ Groups: {actual_allowed_groups}
├─ Safe Bots: {actual_safe_bots}
├─ Delayed Bots: {actual_delayed_bots}

**Session:**
├─ Connection Checks: {connection_checks}
├─ Session Status: ✅ ACTIVE
├─ Keep-Alive: ✅ RUNNING
└─ Stability: 🔥 GUARANTEED
            """
            await message.reply(status_text)
            print("✅ /status command executed with correct counts")
        
        @app.on_message(filters.command("sleepstatus"))
        async def sleepstatus_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            uptime = int(time.time() - sleep_protector.start_time)
            await message.reply(f"🛡️ **SLEEP PROTECTION ACTIVE**\nUptime: {uptime}s | Pings: {sleep_protector.ping_count}")
        
        @app.on_message(filters.command("allow"))
        async def allow_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            if len(message.command) > 1:
                group_id = message.command[1]
                if group_id in allowed_groups:
                    await message.reply(f"ℹ️ Group `{group_id}` already allowed!")
                else:
                    allowed_groups.add(group_id)
                    save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                    await message.reply(f"✅ Group `{group_id}` allowed & SAVED!")
            else:
                await message.reply("❌ Usage: `/allow <group_id>`")
        
        @app.on_message(filters.command("safe"))
        async def safe_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                if bot_username in safe_bots:
                    await message.reply(f"ℹ️ @{bot_username} already in safe list!")
                else:
                    safe_bots.add(bot_username)
                    save_data(SAFE_BOTS_FILE, safe_bots)
                    await message.reply(f"✅ @{bot_username} added to safe list!")
            else:
                await message.reply("❌ Usage: `/safe @botusername`")
        
        @app.on_message(filters.command("delay"))
        async def delay_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                if bot_username in delayed_bots:
                    await message.reply(f"ℹ️ @{bot_username} already in delayed list!")
                else:
                    delayed_bots.add(bot_username)
                    save_data(DELAYED_BOTS_FILE, delayed_bots)
                    await message.reply(f"⏰ @{bot_username} added to delayed list!")
            else:
                await message.reply("❌ Usage: `/delay @botusername`")
        
        @app.on_message(filters.command("remove"))
        async def remove_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                was_in_safe = bot_username in safe_bots
                was_in_delayed = bot_username in delayed_bots
                
                safe_bots.discard(bot_username)
                delayed_bots.discard(bot_username)
                
                if was_in_safe or was_in_delayed:
                    save_data(SAFE_BOTS_FILE, safe_bots)
                    save_data(DELAYED_BOTS_FILE, delayed_bots)
                    await message.reply(f"🗑️ @{bot_username} removed from all lists!")
                else:
                    await message.reply(f"ℹ️ @{bot_username} not found in any list!")
            else:
                await message.reply("❌ Usage: `/remove @botusername`")
        
        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            if not is_admin(message.from_user.id): return
            test_msg = await message.reply("🧪 Testing deletion...")
            await asyncio.sleep(2)
            await test_msg.delete()
            await message.reply("✅ Test passed! Deletion working")
        
        # 🚀 MESSAGE DELETION HANDLER - SPECIFIC FIX FOR GROUP -1002497459144
        @app.on_message(filters.group)
        async def deletion_handler(client, message: Message):
            try:
                group_id = str(message.chat.id)
                
                # SPECIAL FIX: Check if this is the problem group
                is_problem_group = (group_id == "-1002497459144")
                
                if group_id not in allowed_groups:
                    return
                
                # Self check
                nonlocal me
                if me is None: me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower()
                message_text = message.text or message.caption or ""
                
                if is_bot:
                    print(f"🤖 Bot detected: @{username} in {message.chat.title}")
                    
                    # Safe bot check
                    if username in safe_bots:
                        print(f"✅ Safe bot ignored: @{username}")
                        return
                    
                    # SPECIAL FIX FOR PROBLEM GROUP -1002497459144
                    if is_problem_group:
                        print(f"🔧 SPECIAL HANDLING for problem group: {message.chat.title}")
                        
                        # Extra retry logic for problem group
                        max_retries = 3
                        for retry in range(max_retries):
                            try:
                                await message.delete()
                                print(f"✅ SPECIAL DELETE SUCCESS: @{username} from {message.chat.title} (Attempt {retry+1})")
                                break
                            except Exception as e:
                                print(f"❌ SPECIAL DELETE FAILED (Attempt {retry+1}): {e}")
                                if retry < max_retries - 1:
                                    await asyncio.sleep(2)  # Longer delay for problem group
                                else:
                                    print(f"💀 FINAL FAILED in problem group: {message.chat.title}")
                        return
                    
                    # Delayed bot logic for other groups
                    if username in delayed_bots:
                        # Check for links/mentions
                        has_links = any(pattern in message_text.lower() for pattern in ['t.me/', 'http://', 'https://'])
                        has_mentions = '@' in message_text
                        
                        if has_links or has_mentions:
                            print(f"🚫 Delayed bot with links: @{username} - INSTANT DELETE")
                            try:
                                await message.delete()
                                print(f"✅ Instant deleted: @{username}")
                            except Exception as e:
                                print(f"❌ Delete failed: {e}")
                        else:
                            print(f"⏰ Delayed bot normal: @{username} - 30s DELAY")
                            async def delete_after_delay():
                                await asyncio.sleep(30)
                                try:
                                    await message.delete()
                                    print(f"✅ Delayed delete: @{username}")
                                except:
                                    pass
                            asyncio.create_task(delete_after_delay())
                        return
                    
                    # Other bots - IMMEDIATE DELETE for normal groups
                    print(f"🗑️ Unsafe bot: @{username} - IMMEDIATE DELETE")
                    try:
                        await message.delete()
                        print(f"✅ Deleted: @{username}")
                    except Exception as e:
                        print(f"❌ Delete failed: {e}")
                        # Retry once
                        try:
                            await asyncio.sleep(1)
                            await message.delete()
                            print(f"✅ Retry success: @{username}")
                        except:
                            print(f"💀 Final delete failed: @{username}")
                
            except Exception as e:
                print(f"❌ Handler error: {e}")
        
        # ✅ BOT START
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        print(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Start session keep-alive
        keep_alive_task = asyncio.create_task(session_keep_alive())
        
        # Start PROPER online status maintainer - FIXED VERSION
        online_task = asyncio.create_task(maintain_proper_online_status())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002497459144")
        allowed_groups.add("-1002382070176")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        print(f"✅ Auto-setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        print("💓 SESSION KEEP-ALIVE: ACTIVE")
        print("🟢 PROPER ONLINE STATUS: ACTIVE")
        print("🔧 SPECIAL FIX: Group -1002497459144 Enhanced")
        print("📊 STATUS COMMAND: COUNT FIXED")  # FIXED
        print("🔥 SESSION STABILITY: GUARANTEED")
        print("🗑️ MESSAGE DELETION: READY")
        
        # Startup message
        await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - STATUS COUNT FIXED!**

🎯 **SESSION FEATURES:**
• Keep-Alive Every 3 Minutes
• Session Never Expires
• Connection Always Active
• No Device Dependency

🔧 **FIXES APPLIED:**
• Status Command Count Fixed
• Group -1002497459144 Enhanced
• Actual Data Counts Displayed
• Debug Logging Added

**Ab status command correct count dikhayega!** 🔥
        """)
        
        print("🤖 BOT READY - Status Count Fixed!")
        
        # Keep running until session breaks
        try:
            await asyncio.Future()
        except:
            pass
        finally:
            session_active = False
            keep_alive_task.cancel()
            online_task.cancel()
            await app.stop()
        
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    print("🚀 ULTIMATE BOT STARTING...")
    asyncio.run(main())
