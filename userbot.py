print("🔥 ULTIMATE BOT STARTING - DEVICE INDEPENDENT FIX...")

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

# 🔥 DEVICE INDEPENDENT PRIVATE GROUP MANAGER
class DeviceIndependentManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_group_active = False
        self.private_session_established = False
        self.last_private_success = 0
        
    async def establish_private_session(self, app):
        """Establish permanent session with private group - DEVICE INDEPENDENT"""
        try:
            # METHOD 1: Try to get chat info
            chat = await app.get_chat(int(self.private_group_id))
            log_info(f"✅ Private Group Session: {chat.title}")
            self.private_group_active = True
            return True
        except Exception as e:
            log_error(f"❌ Private Group Session Failed: {e}")
            
            try:
                # METHOD 2: Try to send a silent message
                test_msg = await app.send_message(self.private_group_id, "🤖")
                await asyncio.sleep(1)
                await app.delete_messages(self.private_group_id, test_msg.id)
                self.private_group_active = True
                log_info("✅ Private Group Session: Established via message")
                return True
            except Exception as e2:
                log_error(f"❌ Private Group Message Failed: {e2}")
                
                try:
                    # METHOD 3: Try to get group participants (bot itself)
                    async for member in app.get_chat_members(self.private_group_id, limit=1):
                        self.private_group_active = True
                        log_info("✅ Private Group Session: Established via members")
                        return True
                except Exception as e3:
                    log_error(f"❌ Private Group Members Failed: {e3}")
                    self.private_group_active = False
                    return False
    
    async def force_private_delete(self, app, message_obj):
        """Force delete in private group - DEVICE INDEPENDENT"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        
        # Always try to establish session first
        if not self.private_session_established:
            self.private_session_established = await self.establish_private_session(app)
        
        delete_attempts = 0
        max_attempts = 3
        
        while delete_attempts < max_attempts:
            delete_attempts += 1
            try:
                # DIRECT DELETE ATTEMPT
                await app.delete_messages(chat_id, message_id)
                self.last_private_success = time.time()
                log_info(f"✅ PRIVATE DELETE SUCCESS (Attempt {delete_attempts}): {message_id}")
                return True
                
            except Exception as e:
                error_msg = str(e)
                log_error(f"❌ Private Delete Attempt {delete_attempts} Failed: {error_msg}")
                
                # Handle specific errors
                if "AUTH_KEY_UNREGISTERED" in error_msg:
                    log_error("🔴 Session expired - needs restart")
                    return False
                elif "SESSION_REVOKED" in error_msg:
                    log_error("🔴 Session revoked - needs restart") 
                    return False
                elif "USER_DEACTIVATED" in error_msg:
                    log_error("🔴 User deactivated - needs restart")
                    return False
                
                # Wait before retry
                if delete_attempts < max_attempts:
                    wait_time = delete_attempts * 2  # Exponential backoff
                    log_info(f"🔄 Retrying private delete in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    
                    # Re-establish session before retry
                    self.private_session_established = await self.establish_private_session(app)
        
        return False

# 🔥 TELEGRAM BOT - DEVICE INDEPENDENT FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - DEVICE INDEPENDENT FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True,
        'delete_success_count': 0,
        'delete_fail_count': 0,
        'public_group_delete_count': 0,
        'private_group_delete_count': 0
    }

    # Initialize device independent manager
    device_manager = DeviceIndependentManager()

    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA",
            sleep_threshold=300,  # Increased for device independence
            max_concurrent_transmissions=1,
            workers=1
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # -----------------------------
        # DEVICE INDEPENDENT DELETE FUNCTION
        # -----------------------------
        async def device_independent_delete(message_obj):
            """
            DELETE THAT WORKS WITHOUT DEVICE BEING ONLINE
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private_group = str(chat_id) == device_manager.private_group_id
            
            log_info(f"🗑️ DEVICE INDEPENDENT DELETE: {message_id} in {'PRIVATE' if is_private_group else 'PUBLIC'}")
            
            try:
                if is_private_group:
                    # PRIVATE GROUP: Use device independent delete
                    success = await device_manager.force_private_delete(app, message_obj)
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
                log_error(f"❌ DEVICE INDEPENDENT DELETE FAILED: {e}")
                session_data['delete_fail_count'] += 1
                return False

        async def delete_after_delay_independent(message_obj, seconds):
            await asyncio.sleep(seconds)
            await device_independent_delete(message_obj)

        # ✅ PERMANENT SESSION MAINTAINER
        async def permanent_session_maintainer():
            """Maintain permanent session with private group"""
            maintainer_count = 0
            while session_data['active']:
                maintainer_count += 1
                try:
                    # Every 2 minutes, maintain private group session
                    if maintainer_count % 2 == 0:
                        session_ok = await device_manager.establish_private_session(app)
                        if session_ok:
                            if maintainer_count % 10 == 0:
                                log_info("✅ Permanent Session: ACTIVE")
                        else:
                            log_error("❌ Permanent Session: LOST - Retrying...")
                    
                    # Every 10 minutes, send heartbeat to private group
                    if maintainer_count % 10 == 0 and device_manager.private_group_active:
                        try:
                            heartbeat = await app.send_message(device_manager.private_group_id, "💓")
                            await asyncio.sleep(1)
                            await app.delete_messages(device_manager.private_group_id, heartbeat.id)
                            log_info("💓 Private Group Heartbeat: SENT")
                        except Exception as e:
                            log_error(f"❌ Heartbeat failed: {e}")
                            device_manager.private_group_active = False
                    
                    await asyncio.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    log_error(f"Session maintainer error: {e}")
                    await asyncio.sleep(60)

        # ✅ STRONG CONNECTION KEEP-ALIVE
        async def strong_connection_keep_alive():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    # Keep session alive
                    await app.get_me()
                    
                    # Log every 15 keep-alives
                    if keep_alive_count % 15 == 0:
                        log_info(f"🔗 Strong Connection #{keep_alive_count} - Device Independent")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Connection Keep-Alive Failed: {e}")
                
                await asyncio.sleep(40)  # Every 40 seconds

        # -------------------------
        # INTELLIGENT WATCHDOG
        # -------------------------
        async def intelligent_watchdog():
            watchdog_count = 0
            last_private_check = 0
            
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    current_time = time.time()
                    
                    # Check private group status every 5 minutes
                    if current_time - last_private_check > 300:
                        private_status = await device_manager.establish_private_session(app)
                        last_private_check = current_time
                        if not private_status:
                            log_error("🔴 Private group session lost!")
                    
                    # Log status every 3 minutes
                    if watchdog_count % 6 == 0:
                        time_since_private = int(current_time - device_manager.last_private_success) if device_manager.last_private_success > 0 else 999
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Private: {session_data['private_group_delete_count']}, Public: {session_data['public_group_delete_count']}, LastPrivate: {time_since_private}s ago")
                    
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
                private_status = await device_manager.establish_private_session(app)
                time_since_private = int(time.time() - device_manager.last_private_success) if device_manager.last_private_success > 0 else 0
                
                status_msg = f"""
🚀 **BOT STARTED - DEVICE INDEPENDENT!**

📊 **DELETE STATS:**
• Total: {session_data['delete_success_count']} ✅ / {session_data['delete_fail_count']} ❌
• Private: {session_data['private_group_delete_count']} ✅
• Public: {session_data['public_group_delete_count']} ✅

🔍 **Private Group:**
• Session: {'✅ ACTIVE' if private_status else '❌ INACTIVE'}
• Last Success: {time_since_private}s ago
• Device Independent: ✅ YES

**Status: DEVICE INDEPENDENT** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("test_private"))
        async def test_private_command(client, message: Message):
            log_info(f"📩 /test_private from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                try:
                    test_msg = await app.send_message(device_manager.private_group_id, "🧪 Device Independent Test...")
                    await asyncio.sleep(2)
                    success = await device_independent_delete(test_msg)
                    if success:
                        await message.reply("✅ **DEVICE INDEPENDENT DELETE WORKING!**")
                    else:
                        await message.reply("❌ DEVICE INDEPENDENT DELETE FAILED!")
                    log_info("✅ /test_private executed")
                except Exception as e:
                    await message.reply(f"❌ Private test failed: {e}")
                    log_error(f"Private test error: {e}")

        # ---------------------------------------------------------
        # DEVICE INDEPENDENT DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def device_independent_handler(client, message: Message):
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

                is_private = group_id == device_manager.private_group_id
                
                log_info(f"🎯 {'PRIVATE' if is_private else 'PUBLIC'} GROUP: @{username}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        await device_independent_delete(message)
                    else:
                        asyncio.create_task(delete_after_delay_independent(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    await device_independent_delete(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    await device_independent_delete(message)
                    return

            except Exception as e:
                log_error(f"❌ Device Independent Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - DEVICE INDEPENDENT
        log_info("🔗 Connecting to Telegram - DEVICE INDEPENDENT...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Establish permanent private group session
        log_info("🔍 Establishing device independent session...")
        private_session = await device_manager.establish_private_session(app)
        
        if private_session:
            log_info("🎯 Private Group: DEVICE INDEPENDENT SESSION ESTABLISHED")
        else:
            log_info("⚠️ Private Group: SESSION ISSUES - Will retry automatically")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(strong_connection_keep_alive())
        session_maintainer_task = asyncio.create_task(permanent_session_maintainer())
        watchdog_task = asyncio.create_task(intelligent_watchdog())
        
        log_info("🔗 Strong Connection: ACTIVE")
        log_info("💾 Permanent Session: ACTIVE") 
        log_info("🗑️ Device Independent Delete: READY")
        
        # Test private group
        try:
            if private_session:
                test_msg = await app.send_message(device_manager.private_group_id, "🧪 Device Independent Test...")
                await asyncio.sleep(2)
                test_success = await device_independent_delete(test_msg)
                log_info(f"✅ Private test: {'SUCCESS' if test_success else 'FAILED'}")
        except Exception as e:
            log_error(f"Private test error: {e}")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - DEVICE INDEPENDENT!**

🎯 **KEY FEATURES:**
• Works Without Device Online
• Permanent Session Management
• Automatic Session Recovery
• Device Independent Deletes

📊 **STATUS:**
• Private Session: {'✅ ESTABLISHED' if private_session else '🔄 RETRYING'}
• Private Deletes: {session_data['private_group_delete_count']}
• Public Deletes: {session_data['public_group_delete_count']}

**Device: INDEPENDENT** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Device Independent Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            session_maintainer_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - DEVICE INDEPENDENT FIX...")

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
