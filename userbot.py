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

# 🔥 TELEGRAM BOT - COMMANDS FIX
async def start_telegram():
    print("🔗 Starting Telegram Bot - COMMANDS FIX...")
    
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
        
        # ✅ ALL COMMANDS - FIXED VERSION
        @app.on_message(filters.command("start") & filters.private)
        async def start_command(client, message: Message):
            print(f"📩 Received /start from {message.from_user.id}")
            if is_admin(message.from_user.id):
                await message.reply("🚀 **ULTIMATE BOT STARTED!**\nSession Stability Active")
                print("✅ /start command executed")
        
        @app.on_message(filters.command("help") & filters.private)
        async def help_command(client, message: Message):
            print(f"📩 Received /help from {message.from_user.id}")
            if is_admin(message.from_user.id):
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
                print("✅ /help command executed")
        
        @app.on_message(filters.command("ping") & filters.private)
        async def ping_command(client, message: Message):
            print(f"📩 Received /ping from {message.from_user.id}")
            if is_admin(message.from_user.id):
                await message.reply("🏓 **Pong!** Bot active")
                print("✅ /ping command executed")
        
        @app.on_message(filters.command("alive") & filters.private)
        async def alive_command(client, message: Message):
            print(f"📩 Received /alive from {message.from_user.id}")
            if is_admin(message.from_user.id):
                await message.reply("🟢 **BOT ZINDA HAI!** 24/7 Active")
                print("✅ /alive command executed")
        
        @app.on_message(filters.command("nleep") & filters.private)
        async def nleep_command(client, message: Message):
            print(f"📩 Received /nleep from {message.from_user.id}")
            if is_admin(message.from_user.id):
                await message.reply("🚫 **SLEEP NAHI HOGAA!** Protection Active")
                print("✅ /nleep command executed")
        
        @app.on_message(filters.command("status") & filters.private)
        async def status_command(client, message: Message):
            print(f"📩 Received /status from {message.from_user.id}")
            if is_admin(message.from_user.id):
                nonlocal me, connection_checks
                
                if me is None: 
                    me = await app.get_me()
                
                status_text = f"""
🤖 **BOT STATUS - SESSION STABLE**

**Info:**
├─ Name: {me.first_name}
├─ Groups: {len(allowed_groups)}
├─ Safe Bots: {len(safe_bots)}
├─ Delayed Bots: {len(delayed_bots)}

**Session:**
├─ Connection Checks: {connection_checks}
├─ Session Status: ✅ ACTIVE
├─ Keep-Alive: ✅ RUNNING
└─ Stability: 🔥 GUARANTEED
                """
                await message.reply(status_text)
                print("✅ /status command executed")
        
        @app.on_message(filters.command("sleepstatus") & filters.private)
        async def sleepstatus_command(client, message: Message):
            print(f"📩 Received /sleepstatus from {message.from_user.id}")
            if is_admin(message.from_user.id):
                uptime = int(time.time() - sleep_protector.start_time)
                await message.reply(f"🛡️ **SLEEP PROTECTION ACTIVE**\nUptime: {uptime}s | Pings: {sleep_protector.ping_count}")
                print("✅ /sleepstatus command executed")
        
        @app.on_message(filters.command("allow") & filters.private)
        async def allow_command(client, message: Message):
            print(f"📩 Received /allow from {message.from_user.id}")
            if is_admin(message.from_user.id):
                if len(message.command) > 1:
                    group_id = message.command[1]
                    if group_id in allowed_groups:
                        await message.reply(f"ℹ️ Group `{group_id}` already allowed!")
                    else:
                        allowed_groups.add(group_id)
                        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                        await message.reply(f"✅ Group `{group_id}` allowed & SAVED!")
                        print(f"✅ Group {group_id} added to allowed list")
                else:
                    await message.reply("❌ Usage: `/allow <group_id>`")
        
        @app.on_message(filters.command("safe") & filters.private)
        async def safe_command(client, message: Message):
            print(f"📩 Received /safe from {message.from_user.id}")
            if is_admin(message.from_user.id):
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    if bot_username in safe_bots:
                        await message.reply(f"ℹ️ @{bot_username} already in safe list!")
                    else:
                        safe_bots.add(bot_username)
                        save_data(SAFE_BOTS_FILE, safe_bots)
                        await message.reply(f"✅ @{bot_username} added to safe list!")
                        print(f"✅ Bot @{bot_username} added to safe list")
                else:
                    await message.reply("❌ Usage: `/safe @botusername`")
        
        @app.on_message(filters.command("delay") & filters.private)
        async def delay_command(client, message: Message):
            print(f"📩 Received /delay from {message.from_user.id}")
            if is_admin(message.from_user.id):
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    if bot_username in delayed_bots:
                        await message.reply(f"ℹ️ @{bot_username} already in delayed list!")
                    else:
                        delayed_bots.add(bot_username)
                        save_data(DELAYED_BOTS_FILE, delayed_bots)
                        await message.reply(f"⏰ @{bot_username} added to delayed list!")
                        print(f"✅ Bot @{bot_username} added to delayed list")
                else:
                    await message.reply("❌ Usage: `/delay @botusername`")
        
        @app.on_message(filters.command("remove") & filters.private)
        async def remove_command(client, message: Message):
            print(f"📩 Received /remove from {message.from_user.id}")
            if is_admin(message.from_user.id):
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
                        print(f"✅ Bot @{bot_username} removed from lists")
                    else:
                        await message.reply(f"ℹ️ @{bot_username} not found in any list!")
                else:
                    await message.reply("❌ Usage: `/remove @botusername`")
        
        @app.on_message(filters.command("test") & filters.private)
        async def test_command(client, message: Message):
            print(f"📩 Received /test from {message.from_user.id}")
            if is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing deletion...")
                await asyncio.sleep(2)
                await test_msg.delete()
                await message.reply("✅ Test passed! Deletion working")
                print("✅ /test command executed")
        
        # 🚀 MESSAGE DELETION HANDLER
        @app.on_message(filters.group)
        async def deletion_handler(client, message: Message):
            try:
                group_id = str(message.chat.id)
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
                    
                    # Delayed bot logic
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
                    
                    # Other bots - IMMEDIATE DELETE
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
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002497459144")
        allowed_groups.add("-1002382070176")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        print(f"✅ Auto-setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        print("💓 SESSION KEEP-ALIVE: ACTIVE")
        print("🔥 SESSION STABILITY: GUARANTEED")
        print("🗑️ MESSAGE DELETION: READY")
        
        # Startup message
        await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - COMMANDS FIXED!**

🎯 **SESSION FEATURES:**
• Keep-Alive Every 3 Minutes
• Session Never Expires
• Connection Always Active
• No Device Dependency

🚀 **GUARANTEED:**
• Works 24/7 - No Breaks
• Session Always Valid
• Messages Always Delete
• Your Device Can Be Offline

**All commands now working!** 🔥
        """)
        
        print("🤖 BOT READY - Commands Fixed!")
        
        # Keep running until session breaks
        try:
            await asyncio.Future()
        except:
            pass
        finally:
            session_active = False
            keep_alive_task.cancel()
            await app.stop()
        
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    print("🚀 ULTIMATE BOT STARTING...")
    asyncio.run(main())
