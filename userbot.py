print("🔥 ULTIMATE BOT STARTING - DEVICE INDEPENDENT PRIVATE GROUP FIX...")

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
class DeviceIndependentPrivateManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_session_active = False
        self.private_heartbeat_count = 0
        self.private_delete_success = 0
        self.private_delete_failed = 0
        self.public_delete_success = 0
        self.last_private_activity = 0
        
        # SAB TARAH KE LINKS PATTERNS
        self.all_link_patterns = [
            'http://', 'https://', 't.me/', 'telegram.me/', 'tg://',
            'facebook.com/', 'instagram.com/', 'twitter.com/', 'youtube.com/',
            'drive.google.com/', 'mega.nz/', 'dropbox.com/', 'bit.ly/',
            '.com/', '.org/', '.net/', '.in/', '@'
        ]
        
    def contains_any_links_or_mentions(self, text):
        """Check if text contains any links or mentions"""
        if not text:
            return False
            
        text_lower = text.lower()
        for pattern in self.all_link_patterns:
            if pattern in text_lower:
                return True
        return False
    
    async def maintain_private_session(self, app):
        """Maintain active session with private group - DEVICE INDEPENDENT"""
        try:
            # METHOD 1: Send heartbeat message to keep session alive
            heartbeat_msg = await app.send_message(self.private_group_id, "💓")
            await asyncio.sleep(1)
            await app.delete_messages(self.private_group_id, heartbeat_msg.id)
            
            self.private_heartbeat_count += 1
            self.private_session_active = True
            self.last_private_activity = time.time()
            
            log_info(f"💓 Private Heartbeat #{self.private_heartbeat_count} - Session Active")
            return True
            
        except Exception as e:
            log_error(f"❌ Private Session Maintenance Failed: {e}")
            self.private_session_active = False
            return False
    
    async def force_private_delete(self, app, message_obj, max_retries=3):
        """Force delete in private group with session recovery"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        username = (message_obj.from_user.username or "").lower() if message_obj.from_user else ""
        
        # Ensure session is active before deleting
        if not self.private_session_active:
            log_info("🔄 Activating private session before delete...")
            await self.maintain_private_session(app)
        
        for attempt in range(max_retries):
            try:
                # DIRECT DELETE ATTEMPT
                await app.delete_messages(chat_id, message_id)
                self.private_delete_success += 1
                self.last_private_activity = time.time()
                log_info(f"✅ PRIVATE DELETE SUCCESS: @{username} - Attempt {attempt + 1}")
                return True
                
            except Exception as e:
                log_error(f"❌ Private Delete Attempt {attempt + 1} Failed: {e}")
                
                # If session issue, try to recover
                if "PEER_ID_INVALID" in str(e) or "SESSION" in str(e):
                    log_info("🔄 Session issue detected - recovering...")
                    await self.maintain_private_session(app)
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    log_info(f"🔄 Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
        
        self.private_delete_failed += 1
        return False
    
    async def public_group_delete(self, app, message_obj):
        """Public group delete"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        username = (message_obj.from_user.username or "").lower() if message_obj.from_user else ""
        
        try:
            await app.delete_messages(chat_id, message_id)
            self.public_delete_success += 1
            log_info(f"✅ PUBLIC DELETE SUCCESS: @{username}")
            return True
        except Exception as e:
            log_error(f"❌ Public Delete Failed: @{username} - {e}")
            return False

# 🔥 TELEGRAM BOT - DEVICE INDEPENDENT PRIVATE GROUP FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - DEVICE INDEPENDENT PRIVATE GROUP FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True
    }

    # Initialize device independent manager
    device_manager = DeviceIndependentPrivateManager()

    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA",
            sleep_threshold=300,  # Increased for device independence
            max_concurrent_transmissions=1
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # -----------------------------
        # DEVICE INDEPENDENT DELETE FUNCTION
        # -----------------------------
        async def device_independent_delete(message_obj):
            """
            DELETE FUNCTION THAT WORKS WITHOUT DEVICE BEING ONLINE
            """
            touch_activity()
            chat_id = message_obj.chat.id
            is_private = str(chat_id) == device_manager.private_group_id
            
            if is_private:
                return await device_manager.force_private_delete(app, message_obj)
            else:
                return await device_manager.public_group_delete(app, message_obj)

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
                    # Maintain private session every 2 minutes
                    if maintainer_count % 2 == 0:
                        session_ok = await device_manager.maintain_private_session(app)
                        if not session_ok:
                            log_error("🔴 Private session lost - will retry")
                    
                    # Log status every 10 minutes
                    if maintainer_count % 10 == 0:
                        time_since_private = time.time() - device_manager.last_private_activity
                        log_info(f"🔧 Session Maintainer - Heartbeats: {device_manager.private_heartbeat_count}, Last Activity: {int(time_since_private)}s ago")
                    
                    await asyncio.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    log_error(f"Session maintainer error: {e}")
                    await asyncio.sleep(60)

        # ✅ AGGRESSIVE KEEP-ALIVE
        async def aggressive_keep_alive():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    # Keep main session alive
                    await app.get_me()
                    
                    # Extra session maintenance for private group
                    if keep_alive_count % 5 == 0 and device_manager.private_session_active:
                        try:
                            # Quick access check
                            await app.get_chat(int(device_manager.private_group_id))
                        except:
                            device_manager.private_session_active = False
                    
                    if keep_alive_count % 15 == 0:
                        log_info(f"💓 Aggressive Keep-Alive #{keep_alive_count}")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                await asyncio.sleep(20)  # Every 20 seconds

        # -------------------------
        # INTELLIGENT WATCHDOG
        # -------------------------
        async def intelligent_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    private_idle = time.time() - device_manager.last_private_activity
                    
                    if watchdog_count % 5 == 0:
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Private Idle: {int(private_idle)}s, Private: {device_manager.private_delete_success}✅/{device_manager.private_delete_failed}❌, Public: {device_manager.public_delete_success}✅")
                    
                    # If no private activity for 5 minutes, force session refresh
                    if private_idle > 300 and device_manager.private_session_active:
                        log_info("🔄 Force refreshing private session...")
                        await device_manager.maintain_private_session(app)
                    
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
                # Force session activation
                session_ok = await device_manager.maintain_private_session(app)
                
                status_msg = f"""
🚀 **BOT STARTED - DEVICE INDEPENDENT FIX!**

🎯 **DEVICE INDEPENDENT FEATURES:**
• Permanent Private Group Session
• Automatic Session Recovery
• Heartbeat System (No device needed)
• Force Delete with Retry

📊 **PRIVATE GROUP STATUS:**
• Session Active: {'✅ YES' if session_ok else '❌ NO'}
• Heartbeats Sent: {device_manager.private_heartbeat_count}
• Deletes: {device_manager.private_delete_success} ✅ / {device_manager.private_delete_failed} ❌
• Last Activity: {int(time.time() - device_manager.last_private_activity)}s ago

📊 **PUBLIC GROUP STATUS:**
• Deletes: {device_manager.public_delete_success} ✅

**Device Independence: {'ACTIVE' if session_ok else 'SETUP NEEDED'}** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("force_session"))
        async def force_session_command(client, message: Message):
            log_info(f"📩 /force_session from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🔄 **FORCING PRIVATE SESSION ACTIVATION...**")
                
                session_ok = await device_manager.maintain_private_session(app)
                
                if session_ok:
                    await message.reply("✅ **PRIVATE SESSION ACTIVATED!**\nBot should now work without device.")
                else:
                    await message.reply("❌ **SESSION ACTIVATION FAILED!**\nCheck if bot is in private group.")
                
                # Test delete after activation
                try:
                    test_msg = await app.send_message(device_manager.private_group_id, "🧪 Device independent test...")
                    await asyncio.sleep(2)
                    test_success = await device_independent_delete(test_msg)
                    if test_success:
                        await message.reply("✅ **DEVICE INDEPENDENT TEST PASSED!**")
                    else:
                        await message.reply("❌ **DEVICE INDEPENDENT TEST FAILED!**")
                except Exception as e:
                    await message.reply(f"❌ Test failed: {e}")

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
                    return

                # GET BASIC INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message_from_user else ""
                message_text = message.text or message.caption or ""
                is_private = group_id == device_manager.private_group_id

                # 🎯 LOGIC: SIRF BOTS KE MESSAGES DELETE KARO
                
                # ✅ USER MESSAGES - COMPLETELY IGNORE
                if not is_bot:
                    log_info(f"👥 USER IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return

                # ✅ SAFE BOTS - IGNORE
                if username in safe_bots:
                    log_info(f"✅ SAFE BOT IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return

                # ✅ CHECK FOR ANY LINKS OR MENTIONS
                has_links_or_mentions = device_manager.contains_any_links_or_mentions(message_text)
                
                # ⏰ DELAYED BOTS - DELETE BASED ON LINKS
                if username in delayed_bots:
                    if has_links_or_mentions:
                        log_info(f"🚫 DELAYED BOT WITH LINKS: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        await device_independent_delete(message)
                    else:
                        log_info(f"⏰ DELAYED BOT NORMAL: DELETE IN 30s - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        asyncio.create_task(delete_after_delay_independent(message, 30))
                    return

                # 🗑️ OTHER BOTS (UNSAFE BOTS) - INSTANT DELETE
                log_info(f"🗑️ UNSAFE BOT: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                await device_independent_delete(message)

            except Exception as e:
                log_error(f"❌ Device Independent Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - DEVICE INDEPENDENT FIX
        log_info("🔗 Connecting to Telegram - DEVICE INDEPENDENT FIX...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # ESTABLISH PERMANENT PRIVATE SESSION
        log_info("🔄 ESTABLISHING DEVICE INDEPENDENT SESSION...")
        session_established = await device_manager.maintain_private_session(app)
        
        if session_established:
            log_info("🎯 DEVICE INDEPENDENT SESSION: ESTABLISHED!")
            log_info("💡 Bot will now work WITHOUT device being online")
        else:
            log_info("⚠️ DEVICE INDEPENDENT SESSION: Setup needed")
            log_info("💡 Use /force_session command to establish session")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(aggressive_keep_alive())
        session_task = asyncio.create_task(permanent_session_maintainer())
        watchdog_task = asyncio.create_task(intelligent_watchdog())
        
        log_info("💓 Aggressive Keep-Alive: ACTIVE")
        log_info("🔄 Permanent Session: ACTIVE")
        log_info("🗑️ Device Independent Delete: READY")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - DEVICE INDEPENDENT FIX!**

🎯 **KEY FEATURES:**
• Works WITHOUT Device Online
• Permanent Private Group Session
• Automatic Session Recovery
• Heartbeat System

📊 **INITIAL STATUS:**
• Private Session: {'✅ ESTABLISHED' if session_established else '🔄 NEEDS SETUP'}
• Heartbeats: {device_manager.private_heartbeat_count}
• Device Independent: {'✅ YES' if session_established else '❌ NO'}

🚀 **NEXT STEPS:**
1. Use /force_session to establish session
2. Bot will work without device online
3. Session automatically maintained

**Device: INDEPENDENT** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Device Independent Fix Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            session_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - DEVICE INDEPENDENT PRIVATE GROUP FIX...")

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
