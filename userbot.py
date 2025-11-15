print("🔥 ULTIMATE BOT STARTING - 24/7 STRONG CONNECTION FIX...")

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
import signal

# ---------------------------
# ADVANCED LOGGING (ROTATING)
# ---------------------------
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "bot_activity.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("ultimate_bot")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Also print to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def log_info(msg):
    logger.info(msg)


def log_error(msg):
    logger.error(msg)


def log_critical(msg):
    logger.critical(msg)

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

# If files were empty (first run), enforce the clean master lists the user wanted
if not allowed_groups:
    allowed_groups = {"-1002382070176", "-1002497459144"}
if not safe_bots:
    safe_bots = {"unobot","on9wordchainbot","daisyfcbot","missrose_bot","zorofcbot","digi4bot"}
if not delayed_bots:
    delayed_bots = {"crocodile_game4_bot"}

# Save ensured defaults back
save_data(ALLOWED_GROUPS_FILE, allowed_groups)
save_data(SAFE_BOTS_FILE, safe_bots)
save_data(DELAYED_BOTS_FILE, delayed_bots)

# YOUR USER ID
ADMIN_USER_ID = 8368838212

log_info(f"✅ Loaded {len(allowed_groups)} groups, {len(safe_bots)} safe bots, {len(delayed_bots)} delayed bots")

# 🛡️ ULTIMATE SLEEP PROTECTION
class SleepProtection:
    def __init__(self):
        self.ping_count = 0
        self.start_time = time.time()
        self.external_urls = [
            "https://userbot-telegram-1.onrender.com/",
            "https://userbot-telegram-1.onrender.com/ping"
        ]
        self.last_external_ping = 0
        self.monitor_restart_url = "https://userbot-telegram-1.onrender.com/restart"  # optional endpoint if hosted

    def start_protection(self):
        log_info("🛡️ Starting Ultimate Sleep Protection...")
        self.start_flask()
        self.start_external_pings()
        log_info("✅ SLEEP PROTECTION: ACTIVATED")
    
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
        log_info("✅ Flask Server: RUNNING")
    
    def start_external_pings(self):
        def external_pinger():
            while True:
                for url in self.external_urls:
                    try:
                        requests.get(url, timeout=10)
                        self.last_external_ping = time.time()
                    except Exception as e:
                        log_error(f"External ping failed: {e}")
                time.sleep(60)
        
        threading.Thread(target=external_pinger, daemon=True).start()
        log_info("✅ External Pings: RUNNING")


# 🚀 INITIALIZE SLEEP PROTECTION
log_info("🛡️ Initializing Sleep Protection...")
sleep_protector = SleepProtection()
sleep_protector.start_protection()

# Keep track of last activity so watchdog can detect freezes
last_activity = time.time()

# Helper to update activity
def touch_activity():
    global last_activity
    last_activity = time.time()

# 🔥 TELEGRAM BOT - 24/7 STRONG CONNECTION FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - 24/7 STRONG CONNECTION FIX...")
    
    # ✅ SESSION STABILITY VARIABLES
    session_active = True
    connection_checks = 0
    restart_attempts = 0
    message_count = 0

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
        
        # -----------------------------
        # 24/7 STRONG CONNECTION MANAGER
        # -----------------------------
        class ConnectionManager:
            def __init__(self):
                self.last_connection_check = time.time()
                self.connection_status = "🟢 CONNECTED"
                self.reconnect_count = 0
                self.message_count = 0
            
            async def maintain_strong_connection(self):
                """Maintain 24/7 strong connection without device dependency"""
                try:
                    # CRITICAL: Keep connection alive by making API calls
                    await app.get_me()
                    
                    # Access all groups to maintain strong connection
                    for group_id in allowed_groups:
                        try:
                            group_id_int = int(group_id)
                            # Lightweight access to maintain connection
                            await app.get_chat_members_count(group_id_int)
                            await asyncio.sleep(0.5)  # Small delay
                        except:
                            continue
                    
                    self.connection_status = "🟢 STRONG CONNECTION"
                    self.last_connection_check = time.time()
                    return True
                    
                except Exception as e:
                    log_error(f"❌ Connection maintenance failed: {e}")
                    self.connection_status = "🔴 CONNECTION LOST"
                    return False
            
            def get_connection_status(self):
                status = {
                    "status": self.connection_status,
                    "last_check": int(time.time() - self.last_connection_check),
                    "reconnect_count": self.reconnect_count,
                    "message_count": self.message_count
                }
                return status

        # Initialize connection manager
        connection_manager = ConnectionManager()

        # -----------------------------
        # 24/7 STRONG CONNECTION MAINTAINER
        # -----------------------------
        async def strong_connection_maintainer():
            """Maintain 24/7 strong connection"""
            maintain_count = 0
            while session_active:
                try:
                    maintain_count += 1
                    
                    # MAINTAIN STRONG CONNECTION
                    success = await connection_manager.maintain_strong_connection()
                    
                    if success:
                        log_info(f"🌐 STRONG CONNECTION #{maintain_count} - 24/7 ACTIVE")
                    else:
                        log_error(f"❌ Connection maintenance #{maintain_count} failed")
                        connection_manager.reconnect_count += 1
                    
                    touch_activity()
                    
                except Exception as e:
                    log_error(f"❌ Connection maintainer error: {e}")
                
                # Maintain connection every 2 minutes
                await asyncio.sleep(120)

        # -----------------------------
        # SIMPLE & RELIABLE DELETE
        # -----------------------------
        async def reliable_delete(message_obj):
            """
            RELIABLE DELETE that works 24/7
            """
            touch_activity()
            connection_manager.message_count += 1
            
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            
            log_info(f"🗑️ RELIABLE DELETE #{connection_manager.message_count}: {message_id}")
            
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ RELIABLE DELETE SUCCESS: {message_id}")
                return True
            except Exception as e:
                log_error(f"❌ RELIABLE DELETE FAILED: {e}")
                return False

        async def delete_after_delay_reliable(message_obj, seconds):
            await asyncio.sleep(seconds)
            await reliable_delete(message_obj)

        # ✅ 24/7 ONLINE STATUS
        async def always_online_status():
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    await app.get_me()
                    log_info(f"🟢 24/7 ONLINE #{online_count} - NO DEVICE NEEDED")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ 24/7 Online Status Failed: {e}")
                await asyncio.sleep(60)  # Check every 1 minute

        # ✅ AGGRESSIVE SESSION KEEP-ALIVE
        async def aggressive_keep_alive():
            nonlocal connection_checks, session_active
            keep_alive_count = 0
            
            while session_active:
                keep_alive_count += 1
                connection_checks += 1
                
                try:
                    # Aggressive keep-alive - frequent API calls
                    await app.get_me()
                    
                    if keep_alive_count % 10 == 0:
                        log_info(f"💓 AGGRESSIVE KEEP-ALIVE #{keep_alive_count} - 24/7 STRONG")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Aggressive Keep-Alive Failed: {e}")
                
                await asyncio.sleep(30)  # Every 30 seconds

        # -------------------------
        # AGGRESSIVE WATCHDOG
        # -------------------------
        async def aggressive_watchdog():
            nonlocal restart_attempts
            while True:
                try:
                    idle = time.time() - last_activity
                    if idle > 180:  # Restart if no activity for 3 minutes
                        restart_attempts += 1
                        log_error(f"⚠️ AGGRESSIVE WATCHDOG: Restarting - No activity for {int(idle)}s")
                        
                        try:
                            for h in logger.handlers:
                                h.flush()
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        except Exception as e:
                            log_error(f"Watchdog restart failed: {e}")

                        await asyncio.sleep(30)
                    else:
                        await asyncio.sleep(10)
                except Exception as e:
                    log_error(f"Watchdog error: {e}")
                    await asyncio.sleep(5)

        # ✅ ALL COMMANDS - WORKING VERSION
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            connection_manager.message_count += 1
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **BOT STARTED!**\n24/7 Strong Connection Applied!")
                log_info("✅ /start executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 /test from {message.from_user.id}")
            touch_activity()
            connection_manager.message_count += 1
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing 24/7 RELIABLE DELETE...")
                await asyncio.sleep(2)
                success = await reliable_delete(test_msg)
                if success:
                    await message.reply("✅ **24/7 RELIABLE DELETE WORKING!**")
                else:
                    await message.reply("❌ DELETE FAILED!")
                log_info("✅ /test executed")

        @app.on_message(filters.command("connection"))
        async def connection_command(client, message: Message):
            """Check 24/7 connection status"""
            log_info(f"📩 /connection from {message.from_user.id}")
            touch_activity()
            connection_manager.message_count += 1
            if message.from_user and is_admin(message.from_user.id):
                status = connection_manager.get_connection_status()
                
                status_text = f"""
🌐 **24/7 STRONG CONNECTION STATUS**

**Connection:** {status['status']}
**Last Check:** {status['last_check']}s ago
**Reconnects:** {status['reconnect_count']}
**Messages Processed:** {status['message_count']}

**Device Independent:** ✅ YES
**24/7 Online:** ✅ YES
**Strong Connection:** ✅ ACTIVE

**Bot ab kisi device par depend nahi hai!** 🔥
                """
                await message.reply(status_text)
                log_info("✅ /connection executed")

        # ---------------------------------------------------------
        # 24/7 STRONG CONNECTION MESSAGE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def strong_connection_handler(client, message: Message):
            try:
                # UPDATE ACTIVITY & MESSAGE COUNT
                touch_activity()
                connection_manager.message_count += 1
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # SELF CHECK
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return

                # GET BASIC INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                message_text_lower = message_text.lower()

                # LOG EVERY MESSAGE - PROVES 24/7 WORKING
                log_info(f"🌐 24/7 MESSAGE #{connection_manager.message_count}: @{username} (bot: {is_bot})")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    log_info(f"✅ Safe bot: @{username}")
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        log_info(f"🚫 Delayed bot with links: RELIABLE DELETE NOW")
                        await reliable_delete(message)
                    else:
                        log_info(f"⏰ Delayed bot: RELIABLE DELETE IN 30s")
                        asyncio.create_task(delete_after_delay_reliable(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: RELIABLE DELETE NOW")
                    await reliable_delete(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    log_info(f"🔗 User with links: RELIABLE DELETE NOW")
                    await reliable_delete(message)
                    return

                log_info(f"ℹ️ Normal message - 24/7 Connection Strong")

            except Exception as e:
                log_error(f"❌ 24/7 Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START
        log_info("🔗 Connecting to Telegram with 24/7 Strong Connection...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Start CRITICAL 24/7 background tasks
        keep_alive_task = asyncio.create_task(aggressive_keep_alive())
        online_task = asyncio.create_task(always_online_status())
        watchdog_task = asyncio.create_task(aggressive_watchdog())
        connection_maintainer_task = asyncio.create_task(strong_connection_maintainer())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💓 Aggressive Keep-Alive: ACTIVE")
        log_info("🟢 24/7 Online: ACTIVE") 
        log_info("🌐 Strong Connection: RUNNING")
        log_info("🗑️ Reliable Delete: READY")
        log_info("🚀 Device Independent: YES")
        
        # Initial connection test
        log_info("🔍 Testing 24/7 strong connection...")
        await connection_manager.maintain_strong_connection()
        
        # Startup message
        try:
            await app.send_message("me", """
✅ **BOT STARTED - 24/7 STRONG CONNECTION!**

🎯 **24/7 FEATURES:**
• Device Independent Operation
• Strong Connection Maintenance
• Aggressive Keep-Alive
• 24/7 Message Monitoring

🚀 **COMMANDS:**
• `/test` - Test 24/7 delete
• `/connection` - Check connection status

**Bot ab kisi device par depend nahi hai! 24/7 online rahega!** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - 24/7 Strong Connection Applied!")
        
        # Keep running 24/7
        try:
            while session_active:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_active = False
            keep_alive_task.cancel()
            online_task.cancel()
            watchdog_task.cancel()
            connection_maintainer_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - 24/7 STRONG CONNECTION...")

    try:
        asyncio.run(main())
    except Exception as e:
        log_critical(f"CRASH: {e}")
        for h in logger.handlers:
            try:
                h.flush()
            except:
                pass
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except:
            pass
        sys.exit(1)
