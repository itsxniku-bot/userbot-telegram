print("🔥 ULTIMATE BOT STARTING - PEER ID FIX...")

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

# 🔥 SMART PRIVATE GROUP MANAGER
class SmartPrivateGroupManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_group_accessible = False
        self.private_delete_attempts = 0
        self.private_delete_success = 0
        self.last_access_check = 0
        
    async def smart_access_check(self, app):
        """Smart access check that doesn't fail on PEER_ID_INVALID"""
        current_time = time.time()
        
        # Don't check too frequently
        if current_time - self.last_access_check < 300:  # 5 minutes
            return self.private_group_accessible
            
        self.last_access_check = current_time
        
        try:
            # Try lightweight method first - just get chat
            chat = await app.get_chat(int(self.private_group_id))
            self.private_group_accessible = True
            log_info(f"✅ Private Group Access: {chat.title}")
            return True
        except Exception as e:
            error_msg = str(e)
            
            if "PEER_ID_INVALID" in error_msg or "CHANNEL_INVALID" in error_msg:
                log_info("ℹ️ Private Group: Bot not in group or no access")
                self.private_group_accessible = False
            else:
                log_error(f"❌ Private Group Access Error: {e}")
                self.private_group_accessible = False
            
            return False
    
    async def smart_private_delete(self, app, message_obj):
        """Smart delete that handles PEER_ID_INVALID gracefully"""
        self.private_delete_attempts += 1
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        
        # First check if we have access
        has_access = await self.smart_access_check(app)
        
        if not has_access:
            log_info("⏩ Skipping private delete - No access to group")
            return False
        
        try:
            # DIRECT DELETE ATTEMPT
            await app.delete_messages(chat_id, message_id)
            self.private_delete_success += 1
            log_info(f"✅ PRIVATE DELETE SUCCESS: {message_id}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            
            if "PEER_ID_INVALID" in error_msg or "CHANNEL_INVALID" in error_msg:
                log_info("ℹ️ Private Delete: Bot removed from group")
                self.private_group_accessible = False
            elif "MESSAGE_DELETE_FORBIDDEN" in error_msg:
                log_error("❌ Private Delete: No permission to delete")
            elif "CHAT_ADMIN_REQUIRED" in error_msg:
                log_error("❌ Private Delete: Admin rights required")
            else:
                log_error(f"❌ Private Delete Failed: {e}")
            
            return False

# 🔥 TELEGRAM BOT - PEER ID FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - PEER ID FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True,
        'delete_success_count': 0,
        'delete_fail_count': 0,
        'public_group_delete_count': 0,
        'private_group_delete_count': 0
    }

    # Initialize smart private group manager
    private_manager = SmartPrivateGroupManager()

    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # -----------------------------
        # SMART DELETE FUNCTION
        # -----------------------------
        async def smart_delete(message_obj):
            """
            SMART DELETE THAT HANDLES PEER_ID_INVALID
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private_group = str(chat_id) == private_manager.private_group_id
            
            log_info(f"🗑️ SMART DELETE: {message_id} in {'PRIVATE' if is_private_group else 'PUBLIC'}")
            
            try:
                if is_private_group:
                    # PRIVATE GROUP: Use smart delete
                    success = await private_manager.smart_private_delete(app, message_obj)
                    if success:
                        session_data['delete_success_count'] += 1
                        session_data['private_group_delete_count'] += 1
                        return True
                    else:
                        session_data['delete_fail_count'] += 1
                        return False
                else:
                    # PUBLIC GROUP: Simple delete
                    await app.delete_messages(chat_id, message_id)
                    session_data['delete_success_count'] += 1
                    session_data['public_group_delete_count'] += 1
                    log_info(f"✅ PUBLIC DELETE SUCCESS: {message_id}")
                    return True
                    
            except Exception as e:
                log_error(f"❌ SMART DELETE FAILED: {e}")
                session_data['delete_fail_count'] += 1
                return False

        async def delete_after_delay_smart(message_obj, seconds):
            await asyncio.sleep(seconds)
            await smart_delete(message_obj)

        # ✅ ACCESS CHECKER
        async def access_checker():
            """Periodically check private group access"""
            checker_count = 0
            while session_data['active']:
                checker_count += 1
                try:
                    # Check access every 10 minutes
                    if checker_count % 10 == 0:
                        current_access = await private_manager.smart_access_check(app)
                        if current_access:
                            if checker_count % 20 == 0:
                                log_info("✅ Access Checker: Private group accessible")
                        else:
                            log_info("ℹ️ Access Checker: Private group not accessible")
                    
                    await asyncio.sleep(60)  # Check every minute
                    
                except Exception as e:
                    log_error(f"Access checker error: {e}")
                    await asyncio.sleep(120)

        # ✅ SIMPLE KEEP-ALIVE
        async def simple_keep_alive():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    await app.get_me()
                    if keep_alive_count % 30 == 0:
                        log_info(f"💓 Keep-Alive #{keep_alive_count}")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                await asyncio.sleep(60)

        # -------------------------
        # SMART WATCHDOG
        # -------------------------
        async def smart_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    # Log status every 5 minutes
                    if watchdog_count % 10 == 0:
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Private: {session_data['private_group_delete_count']}, Public: {session_data['public_group_delete_count']}")
                    
                    # Restart if no activity for 10 minutes
                    if idle > 600:
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
                    await asyncio.sleep(10)

        # ✅ ALL COMMANDS
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                private_access = await private_manager.smart_access_check(app)
                
                status_msg = f"""
🚀 **BOT STARTED - PEER ID FIX!**

📊 **DELETE STATS:**
• Total: {session_data['delete_success_count']} ✅ / {session_data['delete_fail_count']} ❌
• Private: {session_data['private_group_delete_count']} ✅
• Public: {session_data['public_group_delete_count']} ✅

🔍 **Private Group:**
• Access: {'✅ AVAILABLE' if private_access else '❌ NOT AVAILABLE'}
• Attempts: {private_manager.private_delete_attempts}
• Success: {private_manager.private_delete_success}

**Status: ACTIVE** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("check_private"))
        async def check_private_command(client, message: Message):
            log_info(f"📩 /check_private from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                private_access = await private_manager.smart_access_check(app)
                if private_access:
                    await message.reply("✅ **PRIVATE GROUP ACCESSIBLE**\nBot can delete messages in private group!")
                else:
                    await message.reply("❌ **PRIVATE GROUP NOT ACCESSIBLE**\nBot is not in the private group or has no access.")
                log_info("✅ /check_private executed")

        # ---------------------------------------------------------
        # SMART DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def smart_delete_handler(client, message: Message):
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
                
                # Only log if it's private group and we have access, or it's public
                if not is_private or private_manager.private_group_accessible:
                    log_info(f"🎯 {'PRIVATE' if is_private else 'PUBLIC'} GROUP: @{username}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        await smart_delete(message)
                    else:
                        asyncio.create_task(delete_after_delay_smart(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    await smart_delete(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    await smart_delete(message)
                    return

            except Exception as e:
                log_error(f"❌ Smart Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - PEER ID FIX
        log_info("🔗 Connecting to Telegram - PEER ID FIX...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Check private group access
        log_info("🔍 Checking private group access...")
        private_access = await private_manager.smart_access_check(app)
        
        if private_access:
            log_info("🎯 Private Group: ACCESS GRANTED - Ready for deletion")
        else:
            log_info("ℹ️ Private Group: NO ACCESS - Will only work in public group")
        
        log_info(f"👥 Public Group: READY - {private_manager.public_group_id}")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(simple_keep_alive())
        access_checker_task = asyncio.create_task(access_checker())
        watchdog_task = asyncio.create_task(smart_watchdog())
        
        log_info("💓 Keep-Alive: ACTIVE")
        log_info("🔍 Access Checker: ACTIVE")
        log_info("🗑️ Smart Delete: READY")
        
        # Test public group
        try:
            test_public = await app.send_message(private_manager.public_group_id, "🧪 Public group test...")
            await asyncio.sleep(2)
            public_success = await smart_delete(test_public)
            log_info(f"✅ Public test: {'SUCCESS' if public_success else 'FAILED'}")
        except Exception as e:
            log_error(f"Public test error: {e}")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - PEER ID FIX!**

🎯 **SMART FEATURES:**
• Handles PEER_ID_INVALID Gracefully
• Smart Access Checking
• No Crash on Invalid Groups
• Focus on Working Groups

📊 **STATUS:**
• Private Access: {'✅ AVAILABLE' if private_access else '❌ NOT AVAILABLE'}
• Public Group: ✅ READY
• Private Deletes: {session_data['private_group_delete_count']}
• Public Deletes: {session_data['public_group_delete_count']}

**Strategy: {'DUAL GROUP' if private_access else 'PUBLIC ONLY'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Peer ID Fix Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            access_checker_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - PEER ID FIX...")

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
