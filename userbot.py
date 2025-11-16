print("🔥 ULTIMATE BOT STARTING - INSTANT DELETE + PERMANENT PEER FIX...")

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
PEER_STATUS_FILE = "peer_status.json"


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

def load_peer_status():
    try:
        if os.path.exists(PEER_STATUS_FILE):
            with open(PEER_STATUS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"private_peer_activated": False, "last_activation": None}

def save_peer_status(status):
    try:
        with open(PEER_STATUS_FILE, 'w') as f:
            json.dump(status, f)
    except:
        pass

# Load data - SIRF 2 GROUPS RAKHO
allowed_groups = {"-1002382070176", "-1002497459144"}  # Direct set karo
safe_bots = load_data(SAFE_BOTS_FILE)
delayed_bots = load_data(DELAYED_BOTS_FILE)
peer_status = load_peer_status()

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
log_info(f"📡 Peer Status: {peer_status}")

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

# 🔥 INSTANT DELETE + PERMANENT PEER MANAGER
class InstantDeleteManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_delete_count = 0
        self.public_delete_count = 0
        self.users_ignored_count = 0
        self.private_delete_failures = 0
        self.private_access_checked = False
        self.private_has_admin = False
        self.peer_activated = peer_status.get("private_peer_activated", False)
        self.peer_activation_time = peer_status.get("last_activation", None)
        
        # INSTANT DELETE SETTINGS
        self.last_peer_maintenance = 0
        self.peer_maintenance_interval = 300  # 5 minutes
        self.force_reconnect = False
        
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

# 🔥 TELEGRAM BOT - INSTANT DELETE + PERMANENT PEER FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - INSTANT DELETE + PERMANENT PEER FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True
    }

    # Initialize manager
    manager = InstantDeleteManager()

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
        # ✅ PERMANENT PEER ACTIVATION (SILENT - NO MESSAGES)
        # -----------------------------
        async def activate_permanent_private_group_peer(app, private_group_id):
            try:
                log_info("🔄 PERMANENT PEER: Activating private group peer...")

                # STEP 1: Force fetch chat info (creates permanent peer)
                chat = await app.get_chat(private_group_id)
                log_info(f"✅ Chat fetched: {chat.title}")

                # STEP 2: Multiple deep connection methods (SILENT)
                connection_methods = [
                    ("Chat Members", lambda: app.get_chat_members(private_group_id, limit=1)),
                    ("Chat History", lambda: app.get_chat_history(private_group_id, limit=1)),
                ]
                
                for method_name, method_func in connection_methods:
                    try:
                        async for _ in method_func():
                            break
                        log_info(f"✅ {method_name} connection established")
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        log_info(f"⚠️ {method_name} connection skipped: {e}")

                # STEP 3: Save permanent peer status
                manager.peer_activated = True
                manager.peer_activation_time = time.time()
                
                # Update global peer status
                peer_status.update({
                    "private_peer_activated": True,
                    "last_activation": manager.peer_activation_time,
                    "group_title": chat.title,
                    "group_id": private_group_id
                })
                save_peer_status(peer_status)

                log_info("🟢 PERMANENT PEER ACTIVATED — Will NOT disconnect")
                return True

            except Exception as e:
                log_error(f"❌ PERMANENT PEER ACTIVATION FAILED: {e}")
                return False

        # -----------------------------
        # ✅ INSTANT DELETE FUNCTION (NO DELAY)
        # -----------------------------
        async def instant_delete(message_obj):
            """
            INSTANT DELETE - No delays, immediate action
            """
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private = str(chat_id) == manager.private_group_id

            try:
                # METHOD 1: Direct delete (fastest)
                await message_obj.delete()
                
                if is_private:
                    manager.private_delete_count += 1
                    log_info(f"🚀 INSTANT PRIVATE DELETE: {message_id}")
                else:
                    manager.public_delete_count += 1
                    log_info(f"🚀 INSTANT PUBLIC DELETE: {message_id}")
                return True

            except Exception as e:
                log_error(f"❌ Instant delete failed: {e}")

                # METHOD 2: Resolve chat and delete
                try:
                    chat = await app.get_chat(chat_id)
                    await app.delete_messages(chat.id, message_id)
                    
                    if is_private:
                        manager.private_delete_count += 1
                        log_info(f"✅ RESOLVE DELETE PRIVATE: {message_id}")
                    else:
                        manager.public_delete_count += 1
                        log_info(f"✅ RESOLVE DELETE PUBLIC: {message_id}")
                    return True
                except Exception as e2:
                    log_error(f"❌ Resolve delete failed: {e2}")
                    
                    if is_private:
                        manager.private_delete_failures += 1
                        # Trigger peer reactivation on failure
                        manager.force_reconnect = True
                    return False

        async def delete_after_delay_instant(message_obj, seconds):
            await asyncio.sleep(seconds)
            await instant_delete(message_obj)

        # -----------------------------
        # ✅ SILENT PEER MAINTENANCE (NO MESSAGES)
        # -----------------------------
        async def maintain_permanent_peer():
            """Maintain permanent peer connection without sending messages"""
            current_time = time.time()
            
            # Check if we need to maintain peer
            if not manager.peer_activated:
                return False
                
            if current_time - manager.last_peer_maintenance < manager.peer_maintenance_interval and not manager.force_reconnect:
                return True
                
            try:
                log_info("🔧 SILENT PEER MAINTENANCE: Checking private group connection...")
                
                # Silent check - just get chat info, no messages
                chat = await app.get_chat(manager.private_group_id)
                log_info(f"✅ Silent maintenance: {chat.title} connected")
                
                # Silent connection refresh
                try:
                    async for _ in app.get_chat_history(manager.private_group_id, limit=1):
                        break
                    log_info("✅ Silent connection refreshed")
                except Exception as e:
                    log_info(f"⚠️ Silent refresh failed: {e}")
                
                manager.last_peer_maintenance = current_time
                manager.force_reconnect = False
                return True
                
            except Exception as e:
                log_error(f"❌ Silent peer maintenance failed: {e}")
                manager.force_reconnect = True
                return False

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

        # ✅ INSTANT KEEP-ALIVE WITH SILENT MAINTENANCE
        async def instant_keep_alive():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    await app.get_me()
                    
                    # Every 20th keep-alive, do silent maintenance
                    if keep_alive_count % 20 == 0:
                        await maintain_permanent_peer()
                        log_info(f"💓 Instant Keep-Alive #{keep_alive_count} - Silent Maintenance")
                    elif keep_alive_count % 50 == 0:
                        log_info(f"💓 Keep-Alive #{keep_alive_count}")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                await asyncio.sleep(30)

        # -------------------------
        # INSTANT DELETE WATCHDOG
        # -------------------------
        async def instant_delete_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 10 == 0:
                        log_info(f"🐕 Instant Watchdog - Idle: {int(idle)}s, Private: {manager.private_delete_count}, Public: {manager.public_delete_count}, Private Fails: {manager.private_delete_failures}, Peer Active: {manager.peer_activated}")
                    
                    # Silent peer maintenance every 30 watchdog cycles
                    if manager.peer_activated and watchdog_count % 30 == 0:
                        await maintain_permanent_peer()
                    
                    # Agar private group mein failures zyada hai to admin check karo
                    if manager.private_delete_failures >= 2 and not manager.private_access_checked:
                        log_info("🔄 Watchdog: Checking private group admin rights...")
                        await check_private_group_admin()
                    
                    # Agar peer activate nahi hua hai ya force reconnect hai
                    if (not manager.peer_activated or manager.force_reconnect) and manager.private_delete_failures >= 1:
                        log_info("🔄 Watchdog: Activating permanent private group peer...")
                        success = await activate_permanent_private_group_peer(app, manager.private_group_id)
                        if success:
                            manager.force_reconnect = False
                    
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
🚀 **BOT STARTED - INSTANT DELETE + PERMANENT PEER!**

📊 **DELETE STATS:**
• Private Group: {manager.private_delete_count} ✅
• Public Group: {manager.public_delete_count} ✅
• Private Failures: {manager.private_delete_failures} ❌
• Users Ignored: {manager.users_ignored_count} 👥

🎯 **PERMANENT PEER STATUS:**
• Private Group: {'✅ ACCESS' if access['private'] else '❌ NO ACCESS'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO DELETE RIGHTS'}
• Public Group: {'✅ ACCESS' if access['public'] else '❌ NO ACCESS'}
• Peer Activated: {'✅ PERMANENT' if manager.peer_activated else '❌ INACTIVE'}
• Last Activation: {manager.peer_activation_time or 'Never'}

🔧 **INSTANT FEATURES:**
• Instant Delete (No Delay)
• Permanent Peer Connection
• Silent Maintenance (No Messages)
• No Heartbeat Messages
• Always Connected

**Status: {'INSTANT + PERMANENT' if manager.peer_activated else 'NEEDS ACTIVATION'}** 🔥
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
                            test_msg_public = await app.send_message(manager.public_group_id, "🧪 Public test - instant delete...")
                            await asyncio.sleep(0.5)  # Shorter delay
                            public_success = await instant_delete(test_msg_public)
                            test_results['public'] = '✅ INSTANT SUCCESS' if public_success else '❌ FAILED'
                        except Exception as e:
                            test_results['public'] = f'❌ ERROR: {str(e)}'
                    
                    # Test private group if accessible
                    if access['private']:
                        try:
                            test_msg_private = await app.send_message(manager.private_group_id, "🧪 Private test - instant delete...")
                            await asyncio.sleep(0.5)  # Shorter delay
                            private_success = await instant_delete(test_msg_private)
                            test_results['private'] = '✅ INSTANT SUCCESS' if private_success else '❌ FAILED'
                        except Exception as e:
                            test_results['private'] = f'❌ ERROR: {str(e)}'
                    
                    # Send results
                    result_msg = f"""
🧪 **INSTANT TEST RESULTS:**

**Public Group ({manager.public_group_id}):**
{test_results['public']}

**Private Group ({manager.private_group_id}):**  
{test_results['private']}

🔧 **INSTANT FEATURES:**
• Delete Method: 🚀 INSTANT
• Permanent Peer: {'✅ ACTIVE' if manager.peer_activated else '❌ INACTIVE'}
• Maintenance: 🔇 SILENT
• Messages: 🚫 NO HEARTBEAT

📊 **Admin Status:** {'✅ HAS DELETE RIGHTS' if access['private_admin'] else '❌ MISSING DELETE RIGHTS'}
                    """
                    await message.reply(result_msg)
                        
                except Exception as e:
                    await message.reply(f"❌ Test failed: {e}")

        @app.on_message(filters.command("activate_permanent_peer"))
        async def activate_permanent_peer_command(client, message: Message):
            log_info(f"📩 /activate_permanent_peer from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                try:
                    await message.reply("🔄 Activating PERMANENT private group peer (SILENT)...")
                    success = await activate_permanent_private_group_peer(app, manager.private_group_id)
                    if success:
                        await message.reply("✅ PERMANENT private group peer ACTIVATED! Silent connection established.")
                    else:
                        await message.reply("❌ Permanent peer activation FAILED. Check logs.")
                except Exception as e:
                    await message.reply(f"❌ Activation failed: {e}")

        # ---------------------------------------------------------
        # INSTANT BOTS DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def instant_bots_handler(client, message: Message):
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

                # 🎯 LOG MESSAGE DETAILS (ESPECIALLY FOR PRIVATE GROUP)
                if is_private:
                    log_info(f"📩 PRIVATE GROUP MESSAGE: @{username} - {message_text[:50]}...")
                else:
                    if manager.public_delete_count % 10 == 0:  # Less public logging
                        log_info(f"📩 PUBLIC GROUP MESSAGE: @{username} - {message_text[:50]}...")

                # 🎯 LOGIC: SIRF BOTS KE MESSAGES DELETE KARO
                
                # ✅ USER MESSAGES - COMPLETELY IGNORE
                if not is_bot:
                    manager.users_ignored_count += 1
                    return

                # ✅ SAFE BOTS - IGNORE
                if username in safe_bots:
                    log_info(f"✅ SAFE BOT IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return

                # ✅ CHECK FOR ANY LINKS OR MENTIONS
                has_links_or_mentions = manager.contains_any_links_or_mentions(message_text)
                
                # ⏰ DELAYED BOTS - INSTANT DELETE BASED ON LINKS
                if username in delayed_bots:
                    if has_links_or_mentions:
                        log_info(f"🚫 DELAYED BOT WITH LINKS: INSTANT DELETE - @{username}")
                        await instant_delete(message)
                    else:
                        log_info(f"⏰ DELAYED BOT NORMAL: DELETE IN 5s - @{username}")
                        asyncio.create_task(delete_after_delay_instant(message, 5))  # Reduced from 30s to 5s
                    return

                # 🗑️ OTHER BOTS (UNSAFE BOTS) - INSTANT DELETE
                log_info(f"🗑️ UNSAFE BOT: INSTANT DELETE - @{username}")
                await instant_delete(message)

            except Exception as e:
                log_error(f"❌ Instant Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - INSTANT DELETE + PERMANENT PEER
        log_info("🔗 Connecting to Telegram - INSTANT DELETE + PERMANENT PEER...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Auto-activate permanent private group peer on startup if not already activated
        if not manager.peer_activated:
            log_info("🚀 STARTUP: Auto-activating permanent private group peer...")
            await activate_permanent_private_group_peer(app, manager.private_group_id)
        else:
            log_info("🔗 STARTUP: Permanent peer already activated, doing silent maintenance...")
            await maintain_permanent_peer()
        
        # Check group access immediately with admin check
        access = await check_group_access()
        
        log_info(f"🎯 INSTANT DELETE + PERMANENT PEER ACTIVATED")
        log_info(f"🔗 Link Patterns: {len(manager.all_link_patterns)} types")
        log_info(f"🛡️ Safe Bots: {len(safe_bots)}")
        log_info(f"📊 Group Access - Private: {access['private']}, Private Admin: {access['private_admin']}, Public: {access['public']}, Peer Activated: {manager.peer_activated}")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(instant_keep_alive())
        watchdog_task = asyncio.create_task(instant_delete_watchdog())
        
        log_info("💓 Instant Keep-Alive: ACTIVE")
        log_info("🚀 Instant Delete: READY")
        log_info("🔇 Silent Peer Maintenance: ACTIVE")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - INSTANT DELETE + PERMANENT PEER!**

🎯 **INSTANT FEATURES:**
• Delete Speed: 🚀 INSTANT
• Peer Connection: 🔗 PERMANENT  
• Maintenance: 🔇 SILENT
• Heartbeat: 🚫 NONE

📊 **STATUS:**
• Private Group: {'✅ ACCESSIBLE' if access['private'] else '❌ NOT ACCESSIBLE'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO RIGHTS'}
• Peer Activated: {'✅ PERMANENT' if manager.peer_activated else '❌ TEMPORARY'}

💡 **Key Feature:** Instant deletion + Permanent peer connection!

**Status: {'OPTIMAL' if manager.peer_activated else 'NEEDS ACTIVATION'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Instant Delete + Permanent Peer Active!")
        
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
    log_info("🚀 BOT STARTING - INSTANT DELETE + PERMANENT PEER...")

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
