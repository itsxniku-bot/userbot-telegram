print("🔥 ULTIMATE BOT STARTING - SESSION RESET FIX...")

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

# 🔥 SESSION RESET MANAGER
class SessionResetManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.session_valid = False
        self.groups_accessible = False
        self.delete_count = 0
        self.session_reset_count = 0
        
    async def validate_session(self, app):
        """Validate if session is working and can access groups"""
        try:
            # First check if session is valid
            me = await app.get_me()
            log_info(f"✅ Session Valid: {me.first_name} (@{me.username})")
            self.session_valid = True
            
            # Now try to access saved messages (should always work)
            try:
                await app.send_message("me", "🤖 Session validation test")
                log_info("✅ Saved Messages: ACCESSIBLE")
            except Exception as e:
                log_error(f"❌ Saved Messages Failed: {e}")
                self.session_valid = False
                return False
            
            return True
            
        except Exception as e:
            log_error(f"❌ Session Validation Failed: {e}")
            self.session_valid = False
            return False
    
    async def test_group_access(self, app, group_id, group_name):
        """Test access to a specific group"""
        try:
            chat = await app.get_chat(int(group_id))
            log_info(f"✅ {group_name}: {chat.title}")
            
            # Try to send a test message
            test_msg = await app.send_message(group_id, "🤖 Access test...")
            await asyncio.sleep(1)
            await app.delete_messages(group_id, test_msg.id)
            log_info(f"✅ {group_name}: MESSAGE ACCESS WORKS")
            return True
            
        except Exception as e:
            error_msg = str(e)
            if "PEER_ID_INVALID" in error_msg:
                log_info(f"ℹ️ {group_name}: Bot not in group or no access")
            elif "CHAT_ADMIN_REQUIRED" in error_msg:
                log_info(f"ℹ️ {group_name}: Admin rights required")
            elif "USER_BANNED" in error_msg:
                log_info(f"ℹ️ {group_name}: Bot banned from group")
            else:
                log_error(f"❌ {group_name} Access Failed: {e}")
            return False
    
    async def smart_delete(self, app, message_obj):
        """Smart delete that works with current session"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        
        try:
            await app.delete_messages(chat_id, message_id)
            self.delete_count += 1
            log_info(f"✅ DELETE SUCCESS: {message_id}")
            return True
        except Exception as e:
            log_error(f"❌ DELETE FAILED: {e}")
            return False

# 🔥 TELEGRAM BOT - SESSION RESET FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - SESSION RESET FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True,
        'delete_success_count': 0,
        'delete_fail_count': 0
    }

    # Initialize session reset manager
    session_manager = SessionResetManager()

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
        # SIMPLE DELETE FUNCTION
        # -----------------------------
        async def simple_delete(message_obj):
            """
            SIMPLE DELETE - No complex access checks
            """
            touch_activity()
            
            success = await session_manager.smart_delete(app, message_obj)
            if success:
                session_data['delete_success_count'] += 1
            else:
                session_data['delete_fail_count'] += 1
            
            return success

        async def delete_after_delay_simple(message_obj, seconds):
            await asyncio.sleep(seconds)
            await simple_delete(message_obj)

        # ✅ SESSION VALIDATOR
        async def session_validator():
            """Continuously validate session and group access"""
            validator_count = 0
            while session_data['active']:
                validator_count += 1
                try:
                    # Validate session every 5 minutes
                    if validator_count % 5 == 0:
                        session_ok = await session_manager.validate_session(app)
                        if not session_ok:
                            log_error("🔴 SESSION INVALID - Needs reset")
                    
                    # Test group access every 10 minutes
                    if validator_count % 10 == 0 and session_manager.session_valid:
                        private_access = await session_manager.test_group_access(app, session_manager.private_group_id, "PRIVATE GROUP")
                        public_access = await session_manager.test_group_access(app, session_manager.public_group_id, "PUBLIC GROUP")
                        session_manager.groups_accessible = private_access or public_access
                    
                    await asyncio.sleep(60)
                    
                except Exception as e:
                    log_error(f"Session validator error: {e}")
                    await asyncio.sleep(120)

        # ✅ BASIC KEEP-ALIVE
        async def basic_keep_alive():
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
        # SIMPLE WATCHDOG
        # -------------------------
        async def simple_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 10 == 0:
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Deletes: {session_manager.delete_count}")
                    
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
                session_ok = await session_manager.validate_session(app)
                private_access = await session_manager.test_group_access(app, session_manager.private_group_id, "PRIVATE GROUP")
                public_access = await session_manager.test_group_access(app, session_manager.public_group_id, "PUBLIC GROUP")
                
                status_msg = f"""
🚀 **BOT STARTED - SESSION RESET FIX!**

📊 **SESSION STATUS:**
• Session Valid: {'✅ YES' if session_ok else '❌ NO'}
• Private Group: {'✅ ACCESS' if private_access else '❌ NO ACCESS'}
• Public Group: {'✅ ACCESS' if public_access else '❌ NO ACCESS'}
• Total Deletes: {session_manager.delete_count}

🔧 **SOLUTIONS:**
1. If NO ACCESS: Re-add bot to groups
2. If SESSION INVALID: Get new session string
3. Ensure bot has delete permissions

**Status: {'WORKING' if session_ok and (private_access or public_access) else 'NEEDS SETUP'}** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("reset_session"))
        async def reset_session_command(client, message: Message):
            log_info(f"📩 /reset_session from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🔄 **RESETTING SESSION...**")
                
                # Force restart
                for h in logger.handlers:
                    try:
                        h.flush()
                    except:
                        pass
                try:
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                except Exception as e:
                    await message.reply(f"❌ Reset failed: {e}")

        @app.on_message(filters.command("test_me"))
        async def test_me_command(client, message: Message):
            log_info(f"📩 /test_me from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                try:
                    test_msg = await message.reply("🧪 Testing bot functionality...")
                    await asyncio.sleep(2)
                    success = await simple_delete(test_msg)
                    if success:
                        await message.reply("✅ **BOT IS WORKING!**\nDelete functionality is active.")
                    else:
                        await message.reply("❌ **DELETE FAILED!**\nSession may be invalid.")
                except Exception as e:
                    await message.reply(f"❌ Test failed: {e}")

        # ---------------------------------------------------------
        # SIMPLE DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def simple_delete_handler(client, message: Message):
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
                    return  # Session issue

                # GET BASIC INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                message_text_lower = message_text.lower()

                log_info(f"🎯 GROUP MESSAGE: @{username} in {message.chat.title}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        await simple_delete(message)
                    else:
                        asyncio.create_task(delete_after_delay_simple(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    await simple_delete(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    await simple_delete(message)
                    return

            except Exception as e:
                log_error(f"❌ Simple Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - SESSION RESET FIX
        log_info("🔗 Connecting to Telegram - SESSION RESET FIX...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Validate session and group access
        log_info("🔍 Validating session and group access...")
        session_ok = await session_manager.validate_session(app)
        private_access = await session_manager.test_group_access(app, session_manager.private_group_id, "PRIVATE GROUP")
        public_access = await session_manager.test_group_access(app, session_manager.public_group_id, "PUBLIC GROUP")
        
        if session_ok:
            log_info("✅ Session: VALID AND WORKING")
        else:
            log_error("🔴 Session: INVALID - May need new session string")
        
        if private_access or public_access:
            log_info("✅ Groups: AT LEAST ONE GROUP ACCESSIBLE")
        else:
            log_info("🔴 Groups: NO GROUP ACCESS - Bot needs to be added to groups")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(basic_keep_alive())
        validator_task = asyncio.create_task(session_validator())
        watchdog_task = asyncio.create_task(simple_watchdog())
        
        log_info("💓 Basic Keep-Alive: ACTIVE")
        log_info("🔍 Session Validator: ACTIVE")
        log_info("🗑️ Simple Delete: READY")
        
        # Test bot functionality
        try:
            test_msg = await app.send_message("me", "🧪 Bot functionality test...")
            await asyncio.sleep(2)
            test_success = await simple_delete(test_msg)
            log_info(f"✅ Bot test: {'SUCCESS' if test_success else 'FAILED'}")
        except Exception as e:
            log_error(f"Bot test error: {e}")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - SESSION RESET FIX!**

🎯 **CURRENT STATUS:**
• Session Valid: {'✅ YES' if session_ok else '❌ NO'}
• Private Group: {'✅ ACCESS' if private_access else '❌ NO ACCESS'} 
• Public Group: {'✅ ACCESS' if public_access else '❌ NO ACCESS'}

🚨 **IF NO GROUP ACCESS:**
1. Add bot to both groups as ADMIN
2. Ensure DELETE MESSAGE permission
3. Use /reset_session after adding

🔧 **COMMANDS:**
• /start - Check status
• /test_me - Test bot functionality
• /reset_session - Force restart

**Action Required: {'NONE' if session_ok and (private_access or public_access) else 'ADD BOT TO GROUPS'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Session Reset Fix Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            validator_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - SESSION RESET FIX...")

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
