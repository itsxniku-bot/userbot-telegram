print("🔥 ULTIMATE BOT STARTING - ALL SUPER FIXES ACTIVATED...")

import asyncio
import multiprocessing
import re
from flask import Flask
from pyrogram import Client, filters, idle
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

# 🔥 SUPER FIX MANAGER
class SuperFixManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_delete_count = 0
        self.public_delete_count = 0
        self.users_ignored_count = 0
        self.private_delete_failures = 0
        self.private_access_checked = False
        self.private_has_admin = False
        self.peer_activated = False
        
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

# 🔥 TELEGRAM BOT - ALL SUPER FIXES ACTIVATED
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - ALL SUPER FIXES ACTIVATED...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True
    }

    # Initialize manager
    manager = SuperFixManager()

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
        # ✅ SUPER FIX 1: PRIVATE GROUP PEER ACTIVATION
        # -----------------------------
        async def activate_private_group_peer(app, private_group_id):
            try:
                log_info("🔄 SUPER FIX: Activating private group peer...")

                # STEP 1: Force fetch chat info
                chat = await app.get_chat(private_group_id)
                log_info(f"✅ Chat fetched: {chat.title}")

                # STEP 2: Force deep peer creation
                try:
                    async for _ in app.get_chat_members(private_group_id):
                        break
                    log_info("✅ Members list fetched (peer created)")
                except:
                    log_info("⚠️ Member fetch skipped (not required)")

                # STEP 3: Silent activation message
                try:
                    await app.send_message(private_group_id, "🔧 Bot peer activated.")
                    log_info("✅ Peer activation message sent")
                except Exception as e:
                    log_info(f"⚠️ Cannot send activation message: {e}")

                log_info("🟢 SUPER FIX COMPLETED — Private group peer saved permanently")
                manager.peer_activated = True
                return True

            except Exception as e:
                log_error(f"❌ SUPER FIX FAILED: {e}")
                return False

        # -----------------------------
        # ✅ SUPER FIX 2: SMART DELETE FUNCTION
        # -----------------------------
        async def smart_delete(message_obj):
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private = str(chat_id) == manager.private_group_id

            try:
                # PRIVATE FIX: Always resolve chat
                chat = await app.get_chat(chat_id)
                await app.delete_messages(chat.id, message_id)
                
                if is_private:
                    manager.private_delete_count += 1
                    log_info(f"✅ PRIVATE DELETE SUCCESS: {message_id}")
                else:
                    manager.public_delete_count += 1
                    log_info(f"✅ PUBLIC DELETE SUCCESS: {message_id}")
                return True

            except Exception as e:
                log_error(f"❌ Normal delete failed: {e}")

                # Hard fallback — works even if peer is broken
                try:
                    await message_obj.delete()
                    log_info("🟢 HARD FIX DELETE WORKED")
                    
                    if is_private:
                        manager.private_delete_count += 1
                    else:
                        manager.public_delete_count += 1
                    return True
                except Exception as e2:
                    log_error(f"❌ HARD FIX FAILED: {e2}")
                    
                    if is_private:
                        manager.private_delete_failures += 1
                    return False

        async def delete_after_delay_smart(message_obj, seconds):
            await asyncio.sleep(seconds)
            await smart_delete(message_obj)

        # -----------------------------
        # ✅ SUPER FIX 3: STARTUP PEER ACTIVATION
        # -----------------------------
        @app.on_message(filters.command("start"))
        async def startup_super_fix(client, message: Message):
            """Auto-activate private group peer on startup"""
            PRIVATE_GROUP_ID = "-1002497459144"
            log_info("🚀 STARTUP: Activating private group peer...")
            await activate_private_group_peer(app, PRIVATE_GROUP_ID)

        # ✅ PRIVATE GROUP ADMIN CHECK
        async def check_private_group_admin():
            """Check if bot has admin rights in private group"""
            try:
                chat = await app.get_chat(manager.private_group_id)
                member = await app.get_chat_member(manager.private_group_id, "me")
                
                if member.privileges and member.privileges.can_delete_messages:
                    manager.private_has_admin = True
                    log_info("✅ PRIVATE GROUP: Bot has DELETE permissions")
                else:
                    manager.private_has_admin = False
                    log_error("❌ PRIVATE GROUP: Bot MISSING DELETE permissions")
                    
                manager.private_access_checked = True
                return manager.private_has_admin
                
            except Exception as e:
                log_error(f"❌ Admin check failed: {e}")
                manager.private_access_checked = True
                return False

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
        # SUPER WATCHDOG
        # -------------------------
        async def super_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 10 == 0:
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Private: {manager.private_delete_count}, Public: {manager.public_delete_count}, Private Fails: {manager.private_delete_failures}")
                    
                    # Agar private group mein failures zyada hai to admin check karo
                    if manager.private_delete_failures >= 5 and not manager.private_access_checked:
                        log_info("🔄 Watchdog: Checking private group admin rights...")
                        await check_private_group_admin()
                    
                    # Agar peer activate nahi hua hai to try karo
                    if not manager.peer_activated and manager.private_delete_failures >= 2:
                        log_info("🔄 Watchdog: Activating private group peer...")
                        await activate_private_group_peer(app, manager.private_group_id)
                    
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
                'public': False,
                'private_admin': False
            }
            
            try:
                # Check public group access
                try:
                    public_chat = await app.get_chat(manager.public_group_id)
                    results['public'] = True
                    log_info(f"✅ Public Group Access: {public_chat.title}")
                except Exception as e:
                    log_error(f"❌ Public Group Access Failed: {e}")
                
                # Check private group access  
                try:
                    private_chat = await app.get_chat(manager.private_group_id)
                    results['private'] = True
                    log_info(f"✅ Private Group Access: {private_chat.title}")
                    
                    # Check admin rights in private group
                    results['private_admin'] = await check_private_group_admin()
                    
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
🚀 **BOT STARTED - ALL SUPER FIXES ACTIVATED!**

📊 **DELETE STATS:**
• Private Group: {manager.private_delete_count} ✅
• Public Group: {manager.public_delete_count} ✅
• Private Failures: {manager.private_delete_failures} ❌
• Users Ignored: {manager.users_ignored_count} 👥

🎯 **GROUP ACCESS:**
• Private Group: {'✅ ACCESS' if access['private'] else '❌ NO ACCESS'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO DELETE RIGHTS'}
• Public Group: {'✅ ACCESS' if access['public'] else '❌ NO ACCESS'}
• Peer Activated: {'✅ YES' if manager.peer_activated else '❌ NO'}

🔧 **SUPER FIXES ACTIVE:**
• Double Delete Method
• Chat Resolution Fix
• Hard Fallback
• PEER_ID_INVALID Fixed
• Private Group Peer Activation
• Auto Startup Activation

**Status: {'OPTIMAL' if access['private'] and access['public'] and access['private_admin'] and manager.peer_activated else 'NEEDS ATTENTION'}** 🔥
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
                            test_msg_public = await app.send_message(manager.public_group_id, "🧪 Public test message - will delete in 2 sec...")
                            await asyncio.sleep(2)
                            public_success = await smart_delete(test_msg_public)
                            test_results['public'] = '✅ SUCCESS' if public_success else '❌ FAILED'
                        except Exception as e:
                            test_results['public'] = f'❌ ERROR: {str(e)}'
                    
                    # Test private group if accessible
                    if access['private']:
                        try:
                            test_msg_private = await app.send_message(manager.private_group_id, "🧪 Private test message - will delete in 2 sec...")
                            await asyncio.sleep(2)
                            private_success = await smart_delete(test_msg_private)
                            test_results['private'] = '✅ SUCCESS' if private_success else '❌ FAILED'
                        except Exception as e:
                            test_results['private'] = f'❌ ERROR: {str(e)}'
                    
                    # Send results with fix suggestions
                    result_msg = f"""
🧪 **TEST RESULTS:**

**Public Group ({manager.public_group_id}):**
{test_results['public']}

**Private Group ({manager.private_group_id}):**  
{test_results['private']}

🔧 **SUPER FIX STATUS:**
• Double Method: ✅ ACTIVE
• Chat Resolution: ✅ ACTIVE  
• Hard Fallback: ✅ ACTIVE
• PEER_ID_INVALID: ✅ FIXED
• Peer Activation: {'✅ ACTIVE' if manager.peer_activated else '❌ INACTIVE'}

📊 **Admin Status:** {'✅ HAS DELETE RIGHTS' if access['private_admin'] else '❌ MISSING DELETE RIGHTS'}
                    """
                    await message.reply(result_msg)
                        
                except Exception as e:
                    await message.reply(f"❌ Test failed: {e}")

        @app.on_message(filters.command("activate_peer"))
        async def activate_peer_command(client, message: Message):
            log_info(f"📩 /activate_peer from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                try:
                    await message.reply("🔄 Activating private group peer...")
                    success = await activate_private_group_peer(app, manager.private_group_id)
                    if success:
                        await message.reply("✅ Private group peer ACTIVATED! Bot should now work in private group.")
                    else:
                        await message.reply("❌ Private group peer activation FAILED. Check logs.")
                except Exception as e:
                    await message.reply(f"❌ Activation failed: {e}")

        # ---------------------------------------------------------
        # SUPER BOTS DELETE HANDLER - WITH ALL FIXES
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def super_bots_handler(client, message: Message):
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
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                is_private = group_id == manager.private_group_id

                # 🎯 LOGIC: SIRF BOTS KE MESSAGES DELETE KARO
                
                # ✅ USER MESSAGES - COMPLETELY IGNORE
                if not is_bot:
                    manager.users_ignored_count += 1
                    if manager.users_ignored_count % 50 == 0:  # Spam log avoid
                        log_info(f"👥 USERS IGNORED: {manager.users_ignored_count} total")
                    return

                # ✅ SAFE BOTS - IGNORE
                if username in safe_bots:
                    log_info(f"✅ SAFE BOT IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return

                # ✅ CHECK FOR ANY LINKS OR MENTIONS
                has_links_or_mentions = manager.contains_any_links_or_mentions(message_text)
                
                # ⏰ DELAYED BOTS - DELETE BASED ON LINKS
                if username in delayed_bots:
                    if has_links_or_mentions:
                        log_info(f"🚫 DELAYED BOT WITH LINKS: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        await smart_delete(message)
                    else:
                        log_info(f"⏰ DELAYED BOT NORMAL: DELETE IN 30s - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        asyncio.create_task(delete_after_delay_smart(message, 30))
                    return

                # 🗑️ OTHER BOTS (UNSAFE BOTS) - INSTANT DELETE
                log_info(f"🗑️ UNSAFE BOT: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                await smart_delete(message)

            except Exception as e:
                log_error(f"❌ Super Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - ALL SUPER FIXES
        log_info("🔗 Connecting to Telegram - ALL SUPER FIXES...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Auto-activate private group peer on startup
        log_info("🚀 STARTUP: Auto-activating private group peer...")
        await activate_private_group_peer(app, manager.private_group_id)
        
        # Check group access immediately with admin check
        access = await check_group_access()
        
        log_info(f"🎯 ALL SUPER FIXES ACTIVATED")
        log_info(f"🔗 Link Patterns: {len(manager.all_link_patterns)} types")
        log_info(f"🛡️ Safe Bots: {len(safe_bots)}")
        log_info(f"📊 Group Access - Private: {access['private']}, Private Admin: {access['private_admin']}, Public: {access['public']}, Peer Activated: {manager.peer_activated}")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(simple_keep_alive())
        watchdog_task = asyncio.create_task(super_watchdog())
        
        log_info("💓 Keep-Alive: ACTIVE")
        log_info("🗑️ Smart Delete: READY")
        
        # Startup message with access info
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - ALL SUPER FIXES ACTIVATED!**

🎯 **GROUP ACCESS STATUS:**
• Private Group: {'✅ ACCESSIBLE' if access['private'] else '❌ NOT ACCESSIBLE'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO DELETE RIGHTS'}
• Public Group: {'✅ ACCESSIBLE' if access['public'] else '❌ NOT ACCESSIBLE'}
• Peer Activated: {'✅ YES' if manager.peer_activated else '❌ NO'}

🔧 **SUPER FIXES ACTIVE:**
• Double Delete Method
• Chat Resolution Fix
• Hard Fallback
• PEER_ID_INVALID Fixed
• Private Group Peer Activation
• Auto Startup Activation

📊 **INITIAL CONFIG:**
• Safe Bots: {len(safe_bots)}
• Delayed Bots: {len(delayed_bots)}
• Link Patterns: {len(manager.all_link_patterns)}

**Status: {'OPTIMAL' if access['private'] and access['public'] and access['private_admin'] and manager.peer_activated else 'NEEDS ATTENTION'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - All Super Fixes Active!")
        
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
    log_info("🚀 BOT STARTING - ALL SUPER FIXES...")

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
