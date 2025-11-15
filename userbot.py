print("🔥 ULTIMATE BOT STARTING - STABLE CONNECTION FIX...")

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

# 🔥 CONNECTION STABILITY MANAGER
class ConnectionManager:
    def __init__(self):
        self.connection_retries = 0
        self.max_retries = 5
        self.reconnect_delay = 10
        self.last_successful_connection = time.time()
        
    async def ensure_connection(self, app):
        """Ensure bot is properly connected to Telegram"""
        try:
            me = await app.get_me()
            self.connection_retries = 0
            self.last_successful_connection = time.time()
            return True
        except Exception as e:
            self.connection_retries += 1
            log_error(f"❌ Connection check failed ({self.connection_retries}/{self.max_retries}): {e}")
            
            if self.connection_retries >= self.max_retries:
                log_critical("🔄 Maximum connection retries reached, restarting...")
                await self.force_restart()
            
            return False
    
    async def force_restart(self):
        """Force restart the bot"""
        log_info("🔄 Force restart initiated...")
        for h in logger.handlers:
            try:
                h.flush()
            except:
                pass
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            log_critical(f"Restart failed: {e}")
            sys.exit(1)

# 🔥 TELEGRAM BOT - STABLE CONNECTION FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - STABLE CONNECTION FIX...")
    
    # ✅ ENHANCED SESSION STABILITY VARIABLES
    session_active = True
    connection_checks = 0
    restart_attempts = 0
    delete_success_count = 0
    delete_fail_count = 0
    
    # Initialize connection manager
    conn_manager = ConnectionManager()

    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA",
            sleep_threshold=30,  # Reduced sleep threshold
            max_concurrent_transmissions=2  # Limit concurrent operations
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # -----------------------------
        # ENHANCED DELETE FUNCTION WITH RETRY
        # -----------------------------
        async def enhanced_delete_with_retry(message_obj, max_retries=3):
            """
            ENHANCED DELETE WITH RETRY MECHANISM
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            
            log_info(f"🗑️ DELETE ATTEMPT: {message_id} in {chat_id}")
            
            for attempt in range(max_retries):
                try:
                    # First ensure connection is alive
                    await conn_manager.ensure_connection(app)
                    
                    # DIRECT DELETE
                    await app.delete_messages(chat_id, message_id)
                    log_info(f"✅ DELETE SUCCESS: {message_id} (attempt {attempt + 1})")
                    nonlocal delete_success_count
                    delete_success_count += 1
                    return True
                    
                except Exception as e:
                    log_error(f"❌ DELETE FAILED (attempt {attempt + 1}): {e}")
                    
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        log_info(f"🔄 Retrying delete in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        nonlocal delete_fail_count
                        delete_fail_count += 1
                        return False
            
            return False

        async def delete_after_delay_enhanced(message_obj, seconds):
            await asyncio.sleep(seconds)
            await enhanced_delete_with_retry(message_obj)

        # ✅ ENHANCED ONLINE STATUS WITH CONNECTION VERIFICATION
        async def enhanced_online_status():
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    # Verify connection is actually working
                    current_me = await app.get_me()
                    connection_status = await conn_manager.ensure_connection(app)
                    status_icon = "🟢" if connection_status else "🔴"
                    log_info(f"{status_icon} Online #{online_count} - Connection: {connection_status}")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Online Status Failed: {e}")
                await asyncio.sleep(120)

        # ✅ ENHANCED SESSION KEEP-ALIVE
        async def enhanced_keep_alive():
            keep_alive_count = 0
            
            while session_active:
                keep_alive_count += 1
                nonlocal connection_checks
                connection_checks += 1
                
                try:
                    # More frequent connection checks
                    if keep_alive_count % 3 == 0:
                        connection_ok = await conn_manager.ensure_connection(app)
                        if connection_ok:
                            log_info(f"💓 Keep-Alive #{keep_alive_count} - Connection Stable")
                        else:
                            log_error(f"💔 Keep-Alive #{keep_alive_count} - Connection Issues")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                
                await asyncio.sleep(120)  # Reduced from 180 to 120

        # -------------------------
        # ENHANCED WATCHDOG
        # -------------------------
        async def enhanced_watchdog():
            watchdog_count = 0
            
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    # Log watchdog status periodically
                    if watchdog_count % 30 == 0:
                        log_info(f"🐕 Watchdog Active - Idle: {int(idle)}s, Success: {delete_success_count}, Fail: {delete_fail_count}")
                    
                    if idle > 240:  # Reduced from 300 to 240 seconds
                        nonlocal restart_attempts
                        restart_attempts += 1
                        log_error(f"⚠️ Watchdog: Restarting - No activity for {int(idle)}s")
                        
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

        # ✅ GROUP CONNECTION MONITOR
        async def group_connection_monitor():
            """Monitor connection to specific groups"""
            monitor_count = 0
            while session_active:
                monitor_count += 1
                try:
                    for group_id in allowed_groups:
                        try:
                            # Try to get group info to verify connection
                            chat = await app.get_chat(int(group_id))
                            if monitor_count % 10 == 0:
                                log_info(f"👥 Group Monitor: Connected to {chat.title}")
                        except Exception as e:
                            log_error(f"❌ Group connection failed for {group_id}: {e}")
                    
                    await asyncio.sleep(300)  # Check every 5 minutes
                except Exception as e:
                    log_error(f"Group monitor error: {e}")
                    await asyncio.sleep(60)

        # ✅ ALL COMMANDS - ENHANCED VERSION
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **BOT STARTED!**\nStable Connection Fix Applied!")
                log_info("✅ /start executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 /test from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing ENHANCED DELETE...")
                await asyncio.sleep(2)
                success = await enhanced_delete_with_retry(test_msg)
                if success:
                    await message.reply("✅ **ENHANCED DELETE WORKING!**")
                else:
                    await message.reply("❌ DELETE FAILED!")
                log_info("✅ /test executed")

        @app.on_message(filters.command("status"))
        async def status_command(client, message: Message):
            if message.from_user and is_admin(message.from_user.id):
                status_msg = f"""
📊 **BOT STATUS**

✅ **Connection:** {session_active}
🔄 **Restart Attempts:** {restart_attempts}
🗑️ **Delete Stats:** {delete_success_count} ✅ / {delete_fail_count} ❌
⏱️ **Last Activity:** {int(time.time() - last_activity)}s ago
👥 **Monitored Groups:** {len(allowed_groups)}

**Stable Connection: ACTIVE** 🔥
                """
                await message.reply(status_msg)

        # ---------------------------------------------------------
        # ENHANCED DELETE HANDLER - STABLE VERSION
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def enhanced_delete_handler(client, message: Message):
            try:
                # UPDATE ACTIVITY IMMEDIATELY
                touch_activity()
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # SELF CHECK
                current_me = await app.get_me()
                if message.from_user and message.from_user.id == current_me.id:
                    return

                # ENSURE CONNECTION BEFORE PROCESSING
                connection_ok = await conn_manager.ensure_connection(app)
                if not connection_ok:
                    log_error("⚠️ Skipping message - Connection unstable")
                    return

                # GET BASIC INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                message_text_lower = message_text.lower()

                # LOG EVERY MESSAGE
                log_info(f"🎯 MESSAGE DETECTED: @{username} (bot: {is_bot}) in {message.chat.title}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    log_info(f"✅ Safe bot ignored: @{username}")
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        log_info(f"🚫 Delayed bot with links: DELETE NOW")
                        await enhanced_delete_with_retry(message)
                    else:
                        log_info(f"⏰ Delayed bot normal: DELETE IN 30s")
                        asyncio.create_task(delete_after_delay_enhanced(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: DELETE NOW")
                    await enhanced_delete_with_retry(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    log_info(f"🔗 User with links: DELETE NOW")
                    await enhanced_delete_with_retry(message)
                    return

                log_info(f"ℹ️ Normal message - No action")

            except Exception as e:
                log_error(f"❌ Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START WITH ENHANCED CONNECTION
        log_info("🔗 Connecting to Telegram with enhanced stability...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Verify initial connection to all groups
        log_info("👥 Verifying group connections...")
        for group_id in allowed_groups:
            try:
                chat = await app.get_chat(int(group_id))
                log_info(f"✅ Connected to group: {chat.title}")
            except Exception as e:
                log_error(f"❌ Failed to connect to group {group_id}: {e}")
        
        # Start ENHANCED background tasks
        keep_alive_task = asyncio.create_task(enhanced_keep_alive())
        online_task = asyncio.create_task(enhanced_online_status())
        watchdog_task = asyncio.create_task(enhanced_watchdog())
        group_monitor_task = asyncio.create_task(group_connection_monitor())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💓 Enhanced Keep-Alive: ACTIVE")
        log_info("🟢 Enhanced Online: WORKING") 
        log_info("🗑️ Enhanced Delete: READY WITH RETRY")
        log_info("👥 Group Monitor: ACTIVE")
        
        # Enhanced startup test
        try:
            test_msg = await app.send_message("me", "🧪 Enhanced startup delete test...")
            await asyncio.sleep(1)
            success = await enhanced_delete_with_retry(test_msg)
            if success:
                log_info("✅ Enhanced startup test: DELETE WORKING!")
            else:
                log_info("❌ Enhanced startup test: DELETE FAILED!")
        except Exception as e:
            log_error(f"Enhanced startup test error: {e}")
        
        # Enhanced startup message
        try:
            await app.send_message("me", """
✅ **BOT STARTED - STABLE CONNECTION FIX!**

🎯 **ENHANCED FEATURES:**
• Connection Manager with Retry
• Enhanced Delete with Retry Mechanism  
• Group Connection Monitoring
• Stable Session Management
• Exponential Backoff for Failures

**Ab delete hamesha hoga!** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Stable Connection Active!")
        
        # Keep running with enhanced monitoring
        try:
            while session_active:
                # Periodic connection health check
                if connection_checks % 10 == 0:
                    await conn_manager.ensure_connection(app)
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_active = False
            keep_alive_task.cancel()
            online_task.cancel()
            watchdog_task.cancel()
            group_monitor_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - STABLE CONNECTION FIX...")

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
