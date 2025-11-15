print("🔥 ULTIMATE BOT STARTING - PRIVATE SUPER GROUP FIX...")

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

# Load data - SIRF 2 GROUPS RAKHO
allowed_groups = {"-1002382070176", "-1002497459144"}  # Direct set karo
safe_bots = load_data(SAFE_BOTS_FILE)
delayed_bots = load_data(DELAYED_BOTS_FILE)

# If files were empty (first run), enforce the clean master lists
if not safe_bots:
    safe_bots = {"unobot","on9wordchainbot","daisyfcbot","missrose_bot","zorofcbot","digi4bot"}
if not delayed_bots:
    delayed_bots = {"crocodile_game4_bot"}

# Save ensured defaults back - SIRF 2 GROUPS SAVE KARO
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

# 🔥 PRIVATE SUPER GROUP MANAGER
class PrivateGroupManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_group_retry_count = 0
        self.max_private_retries = 10
        
    async def ensure_private_group_access(self, app):
        """Ensure bot has access to private super group"""
        try:
            # Try to get private group info
            chat = await app.get_chat(int(self.private_group_id))
            self.private_group_retry_count = 0
            log_info(f"✅ Private Group Access: {chat.title}")
            return True
        except Exception as e:
            self.private_group_retry_count += 1
            log_error(f"❌ Private Group Access Failed ({self.private_group_retry_count}/{self.max_private_retries}): {e}")
            
            if self.private_group_retry_count >= self.max_private_retries:
                log_error("🔴 Private group access permanently failed - focusing on public group")
                allowed_groups.discard(self.private_group_id)
                save_data(ALLOWED_GROUPS_FILE, allowed_groups)
            
            return False

# 🔥 TELEGRAM BOT - PRIVATE SUPER GROUP FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - PRIVATE SUPER GROUP FIX...")
    
    # ✅ SESSION VARIABLES
    session_active = True
    delete_success_count = 0
    delete_fail_count = 0
    private_group_delete_count = 0
    public_group_delete_count = 0

    # Initialize private group manager
    private_manager = PrivateGroupManager()

    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA",
            sleep_threshold=120,  # Increased for stability
            max_concurrent_transmissions=1,  # Single transmission for reliability
            workers=1,  # Single worker
            no_updates=False,  # Enable updates for private group
            app_version="1.0.0",
            device_model="Python",
            system_version="Linux"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # -----------------------------
        # SUPER DELETE FUNCTION - PRIVATE GROUP OPTIMIZED
        # -----------------------------
        async def super_delete_optimized(message_obj):
            """
            SUPER DELETE OPTIMIZED FOR PRIVATE GROUPS
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private_group = str(chat_id) == private_manager.private_group_id
            
            log_info(f"🗑️ DELETE ATTEMPT: {message_id} in {'PRIVATE' if is_private_group else 'PUBLIC'} group")
            
            try:
                # For private group - special handling
                if is_private_group:
                    # First ensure we have access
                    await private_manager.ensure_private_group_access(app)
                    
                # DIRECT DELETE - No retry, simple approach
                await app.delete_messages(chat_id, message_id)
                
                # Track success
                nonlocal delete_success_count, private_group_delete_count, public_group_delete_count
                delete_success_count += 1
                
                if is_private_group:
                    private_group_delete_count += 1
                    log_info(f"✅ PRIVATE GROUP DELETE SUCCESS: {message_id} (Total: {private_group_delete_count})")
                else:
                    public_group_delete_count += 1
                    log_info(f"✅ PUBLIC GROUP DELETE SUCCESS: {message_id} (Total: {public_group_delete_count})")
                
                return True
                
            except Exception as e:
                error_msg = str(e)
                log_error(f"❌ DELETE FAILED in {'PRIVATE' if is_private_group else 'PUBLIC'}: {error_msg}")
                nonlocal delete_fail_count
                delete_fail_count += 1
                
                # Special handling for private group errors
                if is_private_group:
                    if "CHAT_ADMIN_REQUIRED" in error_msg:
                        log_error("🔴 Bot needs admin rights in private group!")
                    elif "USER_NOT_PARTICIPANT" in error_msg:
                        log_error("🔴 Bot not participant in private group!")
                    elif "CHAT_FORBIDDEN" in error_msg:
                        log_error("🔴 Bot kicked from private group!")
                
                return False

        async def delete_after_delay_super(message_obj, seconds):
            await asyncio.sleep(seconds)
            await super_delete_optimized(message_obj)

        # ✅ PRIVATE GROUP MONITOR
        async def private_group_monitor():
            """Monitor private group connection specifically"""
            monitor_count = 0
            while session_active:
                monitor_count += 1
                try:
                    # Check private group access every 5 minutes
                    if monitor_count % 5 == 0:
                        await private_manager.ensure_private_group_access(app)
                    
                    # Log status every 10 minutes
                    if monitor_count % 10 == 0:
                        log_info(f"🔍 Private Group Monitor: Access attempts {private_manager.private_group_retry_count}")
                    
                    await asyncio.sleep(60)  # Check every minute
                except Exception as e:
                    log_error(f"Private group monitor error: {e}")
                    await asyncio.sleep(30)

        # ✅ STRONG KEEP-ALIVE
        async def strong_keep_alive():
            keep_alive_count = 0
            while session_active:
                keep_alive_count += 1
                try:
                    # Get me to keep session alive
                    await app.get_me()
                    
                    # Log every 10 keep-alives
                    if keep_alive_count % 10 == 0:
                        log_info(f"💓 Strong Keep-Alive #{keep_alive_count} - Session Active")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                
                await asyncio.sleep(60)  # Every minute

        # -------------------------
        # AGGRESSIVE WATCHDOG
        # -------------------------
        async def aggressive_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    # Log every 5 minutes
                    if watchdog_count % 5 == 0:
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Private: {private_group_delete_count}, Public: {public_group_delete_count}")
                    
                    # Restart if no activity for 5 minutes
                    if idle > 300:
                        log_error(f"⚠️ Watchdog: Restarting - No activity for {int(idle)}s")
                        for h in logger.handlers:
                            try:
                                h.flush()
                            except:
                                pass
                        try:
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        except Exception as e:
                            log_error(f"Watchdog restart failed: {e}")
                        await asyncio.sleep(30)
                    else:
                        await asyncio.sleep(10)
                except Exception as e:
                    log_error(f"Watchdog error: {e}")
                    await asyncio.sleep(5)

        # ✅ ALL COMMANDS
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                status_msg = f"""
🚀 **BOT STARTED - PRIVATE GROUP FIX!**

📊 **DELETE STATS:**
• Total: {delete_success_count} ✅ / {delete_fail_count} ❌
• Private Group: {private_group_delete_count} ✅
• Public Group: {public_group_delete_count} ✅

**Private Group: ACTIVE** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 /test from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing SUPER DELETE...")
                await asyncio.sleep(2)
                success = await super_delete_optimized(test_msg)
                if success:
                    await message.reply("✅ **SUPER DELETE WORKING!**")
                else:
                    await message.reply("❌ DELETE FAILED!")
                log_info("✅ /test executed")

        @app.on_message(filters.command("status"))
        async def status_command(client, message: Message):
            if message.from_user and is_admin(message.from_user.id):
                private_access = await private_manager.ensure_private_group_access(app)
                status_msg = f"""
📊 **BOT STATUS - PRIVATE GROUP FIX**

🗑️ **Delete Stats:**
• Total: {delete_success_count} ✅ / {delete_fail_count} ❌
• Private Group: {private_group_delete_count} ✅
• Public Group: {public_group_delete_count} ✅

🔍 **Group Status:**
• Private Group Access: {'✅' if private_access else '❌'}
• Private Retry Count: {private_manager.private_group_retry_count}
• Monitored Groups: {len(allowed_groups)}

⏱️ **Last Activity:** {int(time.time() - last_activity)}s ago

**Status: {'ACTIVE' if private_access else 'ISSUES'}** 🔥
                """
                await message.reply(status_msg)

        # ---------------------------------------------------------
        # SUPER DELETE HANDLER - PRIVATE GROUP OPTIMIZED
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def super_delete_handler(client, message: Message):
            try:
                # UPDATE ACTIVITY IMMEDIATELY
                touch_activity()
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # SELF CHECK
                try:
                    current_me = await app.get_me()
                    if message.from_user and message.from_user.id == current_me.id:
                        return
                except:
                    pass

                # GET BASIC INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                message_text_lower = message_text.lower()

                is_private = group_id == private_manager.private_group_id
                group_type = "PRIVATE" if is_private else "PUBLIC"
                
                log_info(f"🎯 {group_type} GROUP MESSAGE: @{username} (bot: {is_bot})")

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
                        await super_delete_optimized(message)
                    else:
                        log_info(f"⏰ Delayed bot normal: DELETE IN 30s")
                        asyncio.create_task(delete_after_delay_super(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: DELETE NOW")
                    await super_delete_optimized(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    log_info(f"🔗 User with links: DELETE NOW")
                    await super_delete_optimized(message)
                    return

                log_info(f"ℹ️ Normal message - No action")

            except Exception as e:
                log_error(f"❌ Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - PRIVATE GROUP FOCUS
        log_info("🔗 Connecting to Telegram - PRIVATE GROUP FIX...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Verify private group access
        log_info("🔍 Checking private group access...")
        private_access = await private_manager.ensure_private_group_access(app)
        
        if private_access:
            log_info("✅ Private group access: SUCCESS")
        else:
            log_info("❌ Private group access: FAILED - will retry")
        
        log_info(f"👥 Monitoring Groups: {allowed_groups}")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(strong_keep_alive())
        private_monitor_task = asyncio.create_task(private_group_monitor())
        watchdog_task = asyncio.create_task(aggressive_watchdog())
        
        log_info(f"✅ Setup: {len(allowed_groups)} groups")
        log_info("💓 Strong Keep-Alive: ACTIVE")
        log_info("🔍 Private Group Monitor: ACTIVE")
        log_info("🗑️ Super Delete: OPTIMIZED FOR PRIVATE GROUP")
        
        # Test delete in both groups
        try:
            # Test in private group if accessible
            if private_access:
                try:
                    test_msg_private = await app.send_message(private_manager.private_group_id, "🧪 Private group delete test...")
                    await asyncio.sleep(2)
                    success_private = await super_delete_optimized(test_msg_private)
                    if success_private:
                        log_info("✅ Private group test: DELETE WORKING!")
                    else:
                        log_info("❌ Private group test: DELETE FAILED!")
                except Exception as e:
                    log_error(f"Private group test error: {e}")
            
            # Test in public group
            try:
                test_msg_public = await app.send_message(private_manager.public_group_id, "🧪 Public group delete test...")
                await asyncio.sleep(2)
                success_public = await super_delete_optimized(test_msg_public)
                if success_public:
                    log_info("✅ Public group test: DELETE WORKING!")
                else:
                    log_info("❌ Public group test: DELETE FAILED!")
            except Exception as e:
                log_error(f"Public group test error: {e}")
                
        except Exception as e:
            log_error(f"Startup test error: {e}")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - PRIVATE GROUP FIX!**

🎯 **SPECIAL FEATURES:**
• Private Super Group Optimized
• Strong Connection Management
• Private Group Access Monitoring
• Aggressive Watchdog

📊 **STATUS:**
• Private Group Access: {'✅ SUCCESS' if private_access else '❌ RETRYING'}
• Private Deletes: {private_group_delete_count}
• Public Deletes: {public_group_delete_count}

**Private Group Delete: {'ACTIVE' if private_access else 'RETRYING'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Private Group Fix Active!")
        
        # Keep running
        try:
            while session_active:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_active = False
            keep_alive_task.cancel()
            private_monitor_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - PRIVATE SUPER GROUP FIX...")

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
