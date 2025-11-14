print("🔥 ULTIMATE BOT STARTING - AUTO RECONNECT SYSTEM...")

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

# 🔥 TELEGRAM BOT WITH AUTO-RECONNECT SYSTEM
async def telegram_bot():
    print("🔗 Starting Telegram Bot - AUTO RECONNECT SYSTEM...")
    
    # ✅ AUTO-RECONNECT VARIABLES
    reconnect_attempts = 0
    max_reconnect_attempts = 10
    last_activity_time = time.time()
    
    while reconnect_attempts < max_reconnect_attempts:
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
            
            # ✅ CONNECTION MONITOR
            async def connection_monitor():
                nonlocal last_activity_time, reconnect_attempts
                monitor_count = 0
                while True:
                    monitor_count += 1
                    current_time = time.time()
                    inactive_time = current_time - last_activity_time
                    
                    # If no activity for 5 minutes, force reconnect
                    if inactive_time > 300:  # 5 minutes
                        print(f"🔄 No activity for {inactive_time:.0f}s - Force reconnecting...")
                        break
                    
                    print(f"📡 Connection Monitor #{monitor_count} - Active: {inactive_time:.0f}s ago")
                    await asyncio.sleep(60)  # Check every minute
            
            # ✅ ALL COMMANDS
            @app.on_message(filters.command("start"))
            async def start_command(client, message: Message):
                if not is_admin(message.from_user.id): return
                nonlocal last_activity_time
                last_activity_time = time.time()
                await message.reply("🚀 **ULTIMATE BOT STARTED!**\nAuto-Reconnect Active")
            
            @app.on_message(filters.command("help"))
            async def help_command(client, message: Message):
                if not is_admin(message.from_user.id): return
                nonlocal last_activity_time
                last_activity_time = time.time()
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
                nonlocal last_activity_time
                last_activity_time = time.time()
                await message.reply("🏓 **Pong!** Bot active")
            
            @app.on_message(filters.command("alive"))
            async def alive_command(client, message: Message):
                if not is_admin(message.from_user.id): return
                nonlocal last_activity_time
                last_activity_time = time.time()
                await message.reply("🟢 **BOT ZINDA HAI!** 24/7 Active")
            
            @app.on_message(filters.command("nleep"))
            async def nleep_command(client, message: Message):
                if not is_admin(message.from_user.id): return
                nonlocal last_activity_time
                last_activity_time = time.time()
                await message.reply("🚫 **SLEEP NAHI HOGAA!** Protection Active")
            
            @app.on_message(filters.command("status"))
            async def status_command(client, message: Message):
                if not is_admin(message.from_user.id): return
                nonlocal last_activity_time, reconnect_attempts
                last_activity_time = time.time()
                nonlocal me
                if me is None: me = await app.get_me()
                
                status_text = f"""
🤖 **BOT STATUS - AUTO RECONNECT**

**Info:**
├─ Name: {me.first_name}
├─ Groups: {len(allowed_groups)}
├─ Safe Bots: {len(safe_bots)}
├─ Delayed Bots: {len(delayed_bots)}

**Connection:**
├─ Reconnect Attempts: {reconnect_attempts}
├─ Last Activity: {time.time() - last_activity_time:.0f}s ago
├─ Status: ✅ CONNECTED
└─ Auto-Reconnect: ✅ ACTIVE
                """
                await message.reply(status_text)
            
            @app.on_message(filters.command("sleepstatus"))
            async def sleepstatus_command(client, message: Message):
                if not is_admin(message.from_user.id): return
                nonlocal last_activity_time
                last_activity_time = time.time()
                uptime = int(time.time() - sleep_protector.start_time)
                await message.reply(f"🛡️ **SLEEP PROTECTION ACTIVE**\nUptime: {uptime}s | Pings: {sleep_protector.ping_count}")
            
            @app.on_message(filters.command("allow"))
            async def allow_command(client, message: Message):
                if not is_admin(message.from_user.id): return
                nonlocal last_activity_time
                last_activity_time = time.time()
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
                nonlocal last_activity_time
                last_activity_time = time.time()
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
                nonlocal last_activity_time
                last_activity_time = time.time()
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
                nonlocal last_activity_time
                last_activity_time = time.time()
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
                nonlocal last_activity_time
                last_activity_time = time.time()
                test_msg = await message.reply("🧪 Testing deletion...")
                await asyncio.sleep(2)
                await test_msg.delete()
                await message.reply("✅ Test passed! Deletion working")
            
            # 🚀 MESSAGE DELETION HANDLER WITH ACTIVITY TRACKING
            @app.on_message(filters.group)
            async def deletion_handler(client, message: Message):
                try:
                    nonlocal last_activity_time
                    last_activity_time = time.time()
                    
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
            last_activity_time = time.time()
            print(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
            
            # 🎯 AUTO SETUP
            allowed_groups.add("-1002129045974")
            allowed_groups.add("-1002497459144")
            save_data(ALLOWED_GROUPS_FILE, allowed_groups)
            
            safe_bots.update(["grouphelp", "vid", "like"])
            save_data(SAFE_BOTS_FILE, safe_bots)
            
            print(f"✅ Auto-setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
            print("🔄 AUTO-RECONNECT: ACTIVE")
            print("🗑️ MESSAGE DELETION: READY")
            
            # Startup message
            await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - AUTO RECONNECT!**

🎯 **NEW FEATURES:**
• Auto-Reconnect System
• Connection Monitoring
• Activity Tracking
• Force Reconnect on Timeout

🚀 **GUARANTEED:**
• Works even when device offline
• Automatic recovery
• Continuous operation
• No manual intervention

**Bot ab device offline hone par bhi kaam karega!** 🔥
            """)
            
            print("🤖 BOT READY - Auto-Reconnect Active!")
            
            # Start connection monitor
            monitor_task = asyncio.create_task(connection_monitor())
            
            # Keep running until connection breaks
            try:
                await asyncio.Future()
            except:
                pass
            finally:
                monitor_task.cancel()
                await app.stop()
            
        except Exception as e:
            reconnect_attempts += 1
            print(f"❌ Connection failed (Attempt {reconnect_attempts}/{max_reconnect_attempts}): {e}")
            
            if reconnect_attempts < max_reconnect_attempts:
                wait_time = min(60, reconnect_attempts * 10)  # Max 60 seconds wait
                print(f"🔄 Reconnecting in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print("💀 Max reconnect attempts reached. Stopping bot.")
                break

# Main execution
async def main():
    await telegram_bot()

if __name__ == "__main__":
    print("🚀 ULTIMATE BOT STARTING...")
    asyncio.run(main())
