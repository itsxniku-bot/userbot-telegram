print("🔥 ULTIMATE BOT STARTING - ADMIN ACCESS FIX...")

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

# 🔥 ULTIMATE ACCESS FIX MANAGER
class UltimateAccessFixManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_group_accessible = False
        self.public_group_accessible = False
        self.private_delete_count = 0
        self.public_delete_count = 0
        self.access_attempts = 0
        
    async def ultimate_access_fix(self, app):
        """ULTIMATE ACCESS FIX - All methods to gain access"""
        self.access_attempts += 1
        
        # METHOD 1: Try simple chat access
        try:
            chat = await app.get_chat(int(self.private_group_id))
            log_info(f"✅ PRIVATE GROUP ACCESS: {chat.title}")
            self.private_group_accessible = True
            return True
        except Exception as e:
            log_error(f"❌ Private Access Method 1 Failed: {e}")
        
        # METHOD 2: Try to send a message (activates chat)
        try:
            test_msg = await app.send_message(self.private_group_id, "🤖 Bot activation...")
            await asyncio.sleep(2)
            await app.delete_messages(self.private_group_id, test_msg.id)
            log_info("✅ PRIVATE GROUP ACCESS: Activated via message")
            self.private_group_accessible = True
            return True
        except Exception as e:
            log_error(f"❌ Private Access Method 2 Failed: {e}")
        
        # METHOD 3: Check if we're in participants list
        try:
            async for member in app.get_chat_members(self.private_group_id, limit=5):
                if member.user.id == (await app.get_me()).id:
                    log_info("✅ PRIVATE GROUP ACCESS: Found in participants")
                    self.private_group_accessible = True
                    return True
            log_info("ℹ️ Private Group: Bot not found in participants")
        except Exception as e:
            log_error(f"❌ Private Access Method 3 Failed: {e}")
        
        # METHOD 4: Try to get chat history (lightweight)
        try:
            async for message in app.get_chat_history(self.private_group_id, limit=1):
                log_info("✅ PRIVATE GROUP ACCESS: Can access chat history")
                self.private_group_accessible = True
                return True
        except Exception as e:
            log_error(f"❌ Private Access Method 4 Failed: {e}")
        
        log_info("🔴 PRIVATE GROUP: All access methods failed - Bot may not be in group")
        self.private_group_accessible = False
        return False
    
    async def fix_public_group_access(self, app):
        """Fix public group access"""
        try:
            chat = await app.get_chat(int(self.public_group_id))
            log_info(f"✅ PUBLIC GROUP ACCESS: {chat.title}")
            self.public_group_accessible = True
            return True
        except Exception as e:
            log_error(f"❌ Public Group Access Failed: {e}")
            self.public_group_accessible = False
            return False
    
    async def ultimate_delete(self, app, message_obj):
        """ULTIMATE DELETE with access recovery"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        is_private = str(chat_id) == self.private_group_id
        
        log_info(f"🗑️ ULTIMATE DELETE: {message_id} in {'PRIVATE' if is_private else 'PUBLIC'}")
        
        try:
            # Try direct delete first
            await app.delete_messages(chat_id, message_id)
            
            if is_private:
                self.private_delete_count += 1
                log_info(f"✅ ULTIMATE PRIVATE DELETE: {message_id}")
            else:
                self.public_delete_count += 1
                log_info(f"✅ ULTIMATE PUBLIC DELETE: {message_id}")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            log_error(f"❌ ULTIMATE DELETE FAILED: {error_msg}")
            
            # If access error, try to recover access
            if "PEER_ID_INVALID" in error_msg or "CHANNEL_INVALID" in error_msg:
                log_info("🔄 Attempting access recovery...")
                if is_private:
                    await self.ultimate_access_fix(app)
                else:
                    await self.fix_public_group_access(app)
            
            return False

# 🔥 TELEGRAM BOT - ULTIMATE ACCESS FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - ULTIMATE ACCESS FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True,
        'delete_success_count': 0,
        'delete_fail_count': 0
    }

    # Initialize ultimate access manager
    access_manager = UltimateAccessFixManager()

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
        # ULTIMATE DELETE FUNCTION
        # -----------------------------
        async def ultimate_delete_function(message_obj):
            """
            ULTIMATE DELETE WITH ACCESS RECOVERY
            """
            touch_activity()
            
            success = await access_manager.ultimate_delete(app, message_obj)
            if success:
                session_data['delete_success_count'] += 1
            else:
                session_data['delete_fail_count'] += 1
            
            return success

        async def delete_after_delay_ultimate(message_obj, seconds):
            await asyncio.sleep(seconds)
            await ultimate_delete_function(message_obj)

        # ✅ ACCESS RECOVERY MANAGER
        async def access_recovery_manager():
            """Continuously recover access to groups"""
            recovery_count = 0
            while session_data['active']:
                recovery_count += 1
                try:
                    # Try to recover private group access every 5 minutes
                    if recovery_count % 5 == 0 and not access_manager.private_group_accessible:
                        log_info("🔄 Attempting private group access recovery...")
                        await access_manager.ultimate_access_fix(app)
                    
                    # Check public group access every 10 minutes
                    if recovery_count % 10 == 0 and not access_manager.public_group_accessible:
                        log_info("🔄 Checking public group access...")
                        await access_manager.fix_public_group_access(app)
                    
                    # Log status every 15 minutes
                    if recovery_count % 15 == 0:
                        log_info(f"🔍 Access Status - Private: {access_manager.private_group_accessible}, Public: {access_manager.public_group_accessible}")
                    
                    await asyncio.sleep(60)  # Check every minute
                    
                except Exception as e:
                    log_error(f"Access recovery error: {e}")
                    await asyncio.sleep(120)

        # ✅ STRONG KEEP-ALIVE
        async def strong_keep_alive():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    await app.get_me()
                    if keep_alive_count % 20 == 0:
                        log_info(f"💓 Keep-Alive #{keep_alive_count}")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                await asyncio.sleep(45)

        # -------------------------
        # ULTIMATE WATCHDOG
        # -------------------------
        async def ultimate_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    # Log status every 3 minutes
                    if watchdog_count % 6 == 0:
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Private: {access_manager.private_delete_count}, Public: {access_manager.public_delete_count}")
                    
                    # Restart if no activity for 8 minutes
                    if idle > 480:
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
                # Force access check
                private_access = await access_manager.ultimate_access_fix(app)
                public_access = await access_manager.fix_public_group_access(app)
                
                status_msg = f"""
🚀 **BOT STARTED - ULTIMATE ACCESS FIX!**

📊 **DELETE STATS:**
• Total: {session_data['delete_success_count']} ✅ / {session_data['delete_fail_count']} ❌
• Private: {access_manager.private_delete_count} ✅
• Public: {access_manager.public_delete_count} ✅

🔍 **ACCESS STATUS:**
• Private Group: {'✅ ACCESSIBLE' if private_access else '❌ NOT ACCESSIBLE'}
• Public Group: {'✅ ACCESSIBLE' if public_access else '❌ NOT ACCESSIBLE'}
• Access Attempts: {access_manager.access_attempts}

**Solution: {'FULL ACCESS' if private_access and public_access else 'PARTIAL ACCESS'}** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("force_access"))
        async def force_access_command(client, message: Message):
            log_info(f"📩 /force_access from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🔄 **FORCING ACCESS RECOVERY...**")
                
                private_access = await access_manager.ultimate_access_fix(app)
                public_access = await access_manager.fix_public_group_access(app)
                
                if private_access or public_access:
                    await message.reply(f"✅ **ACCESS RECOVERY SUCCESS!**\nPrivate: {'✅' if private_access else '❌'}\nPublic: {'✅' if public_access else '❌'}")
                else:
                    await message.reply("❌ **ACCESS RECOVERY FAILED!**\nBot may not be in groups.")
                
                log_info("✅ /force_access executed")

        @app.on_message(filters.command("test_groups"))
        async def test_groups_command(client, message: Message):
            log_info(f"📩 /test_groups from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                results = []
                
                # Test private group
                if access_manager.private_group_accessible:
                    try:
                        test_msg = await app.send_message(access_manager.private_group_id, "🧪 Private test...")
                        await asyncio.sleep(2)
                        success = await ultimate_delete_function(test_msg)
                        results.append(f"Private: {'✅' if success else '❌'}")
                    except Exception as e:
                        results.append(f"Private: ❌ ({e})")
                else:
                    results.append("Private: ❌ (No access)")
                
                # Test public group  
                if access_manager.public_group_accessible:
                    try:
                        test_msg = await app.send_message(access_manager.public_group_id, "🧪 Public test...")
                        await asyncio.sleep(2)
                        success = await ultimate_delete_function(test_msg)
                        results.append(f"Public: {'✅' if success else '❌'}")
                    except Exception as e:
                        results.append(f"Public: ❌ ({e})")
                else:
                    results.append("Public: ❌ (No access)")
                
                await message.reply(f"🧪 **GROUP TESTS:**\n" + "\n".join(results))
                log_info("✅ /test_groups executed")

        # ---------------------------------------------------------
        # ULTIMATE DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def ultimate_delete_handler(client, message: Message):
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

                is_private = group_id == access_manager.private_group_id
                
                # Only process if we have access to the group
                if (is_private and not access_manager.private_group_accessible) or (not is_private and not access_manager.public_group_accessible):
                    return
                
                log_info(f"🎯 {'PRIVATE' if is_private else 'PUBLIC'} GROUP: @{username}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        await ultimate_delete_function(message)
                    else:
                        asyncio.create_task(delete_after_delay_ultimate(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    await ultimate_delete_function(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    await ultimate_delete_function(message)
                    return

            except Exception as e:
                log_error(f"❌ Ultimate Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - ULTIMATE ACCESS FIX
        log_info("🔗 Connecting to Telegram - ULTIMATE ACCESS FIX...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # ULTIMATE ACCESS FIX ATTEMPT
        log_info("🔄 Attempting ULTIMATE ACCESS FIX...")
        private_access = await access_manager.ultimate_access_fix(app)
        public_access = await access_manager.fix_public_group_access(app)
        
        if private_access:
            log_info("🎯 Private Group: ULTIMATE ACCESS FIX SUCCESS!")
        else:
            log_info("🔴 Private Group: ULTIMATE ACCESS FIX FAILED - Bot may need to be re-added")
        
        if public_access:
            log_info("🎯 Public Group: ACCESS GRANTED!")
        else:
            log_info("🔴 Public Group: ACCESS FAILED - Check group ID")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(strong_keep_alive())
        recovery_task = asyncio.create_task(access_recovery_manager())
        watchdog_task = asyncio.create_task(ultimate_watchdog())
        
        log_info("💓 Strong Keep-Alive: ACTIVE")
        log_info("🔄 Access Recovery: ACTIVE")
        log_info("🗑️ Ultimate Delete: READY")
        
        # Test accessible groups
        try:
            if public_access:
                test_public = await app.send_message(access_manager.public_group_id, "🧪 Public test...")
                await asyncio.sleep(2)
                public_success = await ultimate_delete_function(test_public)
                log_info(f"✅ Public test: {'SUCCESS' if public_success else 'FAILED'}")
        except Exception as e:
            log_error(f"Public test error: {e}")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - ULTIMATE ACCESS FIX!**

🎯 **ULTIMATE FEATURES:**
• 4 Different Access Methods
• Continuous Access Recovery
• Automatic Session Activation
• Access Error Handling

📊 **ACCESS STATUS:**
• Private Group: {'✅ ACCESSIBLE' if private_access else '❌ NOT ACCESSIBLE'}
• Public Group: {'✅ ACCESSIBLE' if public_access else '❌ NOT ACCESSIBLE'}
• Access Attempts: {access_manager.access_attempts}

🚨 **IF NO ACCESS:**
1. Re-add bot to private group
2. Use /force_access command
3. Check bot admin rights

**Status: {'OPTIMAL' if private_access and public_access else 'NEEDS ATTENTION'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Ultimate Access Fix Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            recovery_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - ULTIMATE ACCESS FIX...")

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
