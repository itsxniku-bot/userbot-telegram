print("🔥 ULTIMATE BOT STARTING - SYNTAX ERROR FIX...")

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

# 🔥 SIMPLE BOTS DELETE MANAGER
class SimpleBotsDeleteManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_delete_count = 0
        self.public_delete_count = 0
        self.users_ignored_count = 0
        
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

# 🔥 TELEGRAM BOT - SIMPLE WORKING FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - SIMPLE WORKING FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True
    }

    # Initialize simple manager
    simple_manager = SimpleBotsDeleteManager()

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
            SIMPLE DELETE - NO COMPLEX LOGIC
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private = str(chat_id) == simple_manager.private_group_id
            
            try:
                await app.delete_messages(chat_id, message_id)
                if is_private:
                    simple_manager.private_delete_count += 1
                    log_info(f"✅ PRIVATE DELETE SUCCESS: {message_id}")
                else:
                    simple_manager.public_delete_count += 1
                    log_info(f"✅ PUBLIC DELETE SUCCESS: {message_id}")
                return True
            except Exception as e:
                log_error(f"❌ DELETE FAILED: {e}")
                return False

        async def delete_after_delay_simple(message_obj, seconds):
            await asyncio.sleep(seconds)
            await simple_delete(message_obj)

        # ✅ SIMPLE KEEP-ALIVE
        async def simple_keep_alive():
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
                await asyncio.sleep(30)

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
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Private: {simple_manager.private_delete_count}, Public: {simple_manager.public_delete_count}")
                    
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
                    await asyncio.sleep(10)

        # ✅ CHECK GROUP ACCESS FUNCTION
        async def check_group_access():
            """Check if bot has access to both groups"""
            results = {
                'private': False,
                'public': False
            }
            
            try:
                # Check public group access
                try:
                    public_chat = await app.get_chat(simple_manager.public_group_id)
                    results['public'] = True
                    log_info(f"✅ Public Group Access: {public_chat.title}")
                except Exception as e:
                    log_error(f"❌ Public Group Access Failed: {e}")
                
                # Check private group access  
                try:
                    private_chat = await app.get_chat(simple_manager.private_group_id)
                    results['private'] = True
                    log_info(f"✅ Private Group Access: {private_chat.title}")
                except Exception as e:
                    log_error(f"❌ Private Group Access Failed: {e}")
                    
            except Exception as e:
                log_error(f"Group access check failed: {e}")
                
            return results

        # ✅ ALL COMMANDS
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                # Check current group access
                access = await check_group_access()
                
                status_msg = f"""
🚀 **BOT STARTED - SIMPLE WORKING FIX!**

📊 **DELETE STATS:**
• Private Group: {simple_manager.private_delete_count} ✅
• Public Group: {simple_manager.public_delete_count} ✅
• Users Ignored: {simple_manager.users_ignored_count} 👥

🎯 **GROUP ACCESS:**
• Private Group: {'✅ ACCESS' if access['private'] else '❌ NO ACCESS'}
• Public Group: {'✅ ACCESS' if access['public'] else '❌ NO ACCESS'}

🔧 **CONFIGURATION:**
• Delete: ONLY UNSAFE BOTS
• Ignore: ALL USERS
• Links: {len(simple_manager.all_link_patterns)} types detected
• Safe Bots: {len(safe_bots)} protected

**Status: {'OPTIMAL' if access['private'] and access['public'] else 'NEEDS ATTENTION'}** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("test_bot"))
        async def test_bot_command(client, message: Message):
            log_info(f"📩 /test_bot from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                try:
                    # First check group access
                    access = await check_group_access()
                    
                    if not access['public'] and not access['private']:
                        await message.reply("❌ **NO GROUP ACCESS** - Add bot to both groups first!")
                        return
                    
                    test_results = {
                        'private': 'NOT TESTED',
                        'public': 'NOT TESTED'
                    }
                    
                    # Test public group if accessible
                    if access['public']:
                        try:
                            test_msg_public = await app.send_message(simple_manager.public_group_id, "🧪 Public test message - will delete in 2 sec...")
                            await asyncio.sleep(2)
                            public_success = await simple_delete(test_msg_public)
                            test_results['public'] = '✅ SUCCESS' if public_success else '❌ FAILED'
                        except Exception as e:
                            test_results['public'] = f'❌ ERROR: {str(e)}'
                    
                    # Test private group if accessible
                    if access['private']:
                        try:
                            test_msg_private = await app.send_message(simple_manager.private_group_id, "🧪 Private test message - will delete in 2 sec...")
                            await asyncio.sleep(2)
                            private_success = await simple_delete(test_msg_private)
                            test_results['private'] = '✅ SUCCESS' if private_success else '❌ FAILED'
                        except Exception as e:
                            test_results['private'] = f'❌ ERROR: {str(e)}'
                    
                    # Send results
                    result_msg = f"""
🧪 **TEST RESULTS:**

**Public Group ({simple_manager.public_group_id}):**
{test_results['public']}

**Private Group ({simple_manager.private_group_id}):**  
{test_results['private']}

💡 **Note:** If private group shows errors, make sure bot is added to that group with delete permissions.
                    """
                    await message.reply(result_msg)
                        
                except Exception as e:
                    await message.reply(f"❌ Test failed: {e}")

        # ---------------------------------------------------------
        # SIMPLE BOTS DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def simple_bots_handler(client, message: Message):
            try:
                # UPDATE ACTIVITY IMMEDIATELY
                touch_activity()
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # SELF CHECK - FIXED VARIABLE NAME
                try:
                    current_me = await app.get_me()
                    if message.from_user and message.from_user.id == current_me.id:
                        return
                except:
                    return

                # GET BASIC INFO - FIXED VARIABLE NAME
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                is_private = group_id == simple_manager.private_group_id

                # 🎯 LOGIC: SIRF BOTS KE MESSAGES DELETE KARO
                
                # ✅ USER MESSAGES - COMPLETELY IGNORE
                if not is_bot:
                    simple_manager.users_ignored_count += 1
                    log_info(f"👥 USER IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return

                # ✅ SAFE BOTS - IGNORE
                if username in safe_bots:
                    log_info(f"✅ SAFE BOT IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return

                # ✅ CHECK FOR ANY LINKS OR MENTIONS
                has_links_or_mentions = simple_manager.contains_any_links_or_mentions(message_text)
                
                # ⏰ DELAYED BOTS - DELETE BASED ON LINKS
                if username in delayed_bots:
                    if has_links_or_mentions:
                        log_info(f"🚫 DELAYED BOT WITH LINKS: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        await simple_delete(message)
                    else:
                        log_info(f"⏰ DELAYED BOT NORMAL: DELETE IN 30s - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        asyncio.create_task(delete_after_delay_simple(message, 30))
                    return

                # 🗑️ OTHER BOTS (UNSAFE BOTS) - INSTANT DELETE
                log_info(f"🗑️ UNSAFE BOT: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                await simple_delete(message)

            except Exception as e:
                log_error(f"❌ Simple Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - SIMPLE WORKING FIX
        log_info("🔗 Connecting to Telegram - SIMPLE WORKING FIX...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Check group access immediately
        access = await check_group_access()
        
        log_info(f"🎯 SIMPLE WORKING FIX ACTIVATED")
        log_info(f"🔗 Link Patterns: {len(simple_manager.all_link_patterns)} types")
        log_info(f"🛡️ Safe Bots: {len(safe_bots)}")
        log_info(f"📊 Group Access - Private: {access['private']}, Public: {access['public']}")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(simple_keep_alive())
        watchdog_task = asyncio.create_task(simple_watchdog())
        
        log_info("💓 Keep-Alive: ACTIVE")
        log_info("🗑️ Simple Delete: READY")
        
        # Startup message with access info
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - SIMPLE WORKING FIX!**

🎯 **GROUP ACCESS STATUS:**
• Private Group: {'✅ ACCESSIBLE' if access['private'] else '❌ NOT ACCESSIBLE'}
• Public Group: {'✅ ACCESSIBLE' if access['public'] else '❌ NOT ACCESSIBLE'}

📊 **INITIAL CONFIG:**
• Safe Bots: {len(safe_bots)}
• Delayed Bots: {len(delayed_bots)}
• Link Patterns: {len(simple_manager.all_link_patterns)}

🔧 **COMMANDS:**
• /start - Check status
• /test_bot - Test both groups

💡 **NOTE:** If private group shows inaccessible, add bot to that group with delete permissions.

**Status: {'OPTIMAL' if access['private'] and access['public'] else 'NEEDS ATTENTION'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Simple Working Fix Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - SIMPLE WORKING FIX...")

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
