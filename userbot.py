print("🔥 ULTIMATE BOT STARTING - COMPLETE MESSAGE CAPTURE FIX...")

import asyncio
import multiprocessing
import re
import traceback
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
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

# 🔥 COMPLETE MESSAGE CAPTURE MANAGER
class CompleteCaptureManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_delete_count = 0
        self.public_delete_count = 0
        self.users_ignored_count = 0
        self.private_delete_failures = 0
        self.public_delete_failures = 0
        self.private_access_checked = False
        self.private_has_admin = False
        self.peer_activated = peer_status.get("private_peer_activated", False)
        self.peer_activation_time = peer_status.get("last_activation", None)
        
        # MESSAGE TRACKING
        self.total_messages_received = 0
        self.last_message_time = 0
        self.message_tracking = {}
        
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

# 🔥 TELEGRAM BOT - COMPLETE MESSAGE CAPTURE FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - COMPLETE MESSAGE CAPTURE FIX...")
    
    # ✅ SESSION DATA
    session_data = {'active': True}

    # Initialize manager
    manager = CompleteCaptureManager()

    try:
        # Use 'client' (not 'app') for the Pyrogram Client to avoid name collisions
        client = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # ----------------------------- helper functions use 'client' now -----------------------------
        async def activate_permanent_private_group_peer(client_obj, private_group_id):
            try:
                log_info("🔄 PERMANENT PEER: Activating private group peer...")
                chat = await client_obj.get_chat(private_group_id)
                log_info(f"✅ Chat fetched: {getattr(chat,'title', 'unknown')}")
                connection_methods = [
                    ("Chat Members", lambda: client_obj.get_chat_members(private_group_id, limit=1)),
                    ("Chat History", lambda: client_obj.get_chat_history(private_group_id, limit=1)),
                ]
                for method_name, method_func in connection_methods:
                    try:
                        async for _ in method_func():
                            break
                        log_info(f"✅ {method_name} connection established")
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        log_info(f"⚠️ {method_name} connection skipped: {e}")
                manager.peer_activated = True
                manager.peer_activation_time = time.time()
                peer_status.update({
                    "private_peer_activated": True,
                    "last_activation": manager.peer_activation_time,
                    "group_title": getattr(chat, "title", None),
                    "group_id": private_group_id
                })
                save_peer_status(peer_status)
                log_info("🟢 PERMANENT PEER ACTIVATED — Will NOT disconnect")
                return True
            except Exception as e:
                log_error(f"❌ PERMANENT PEER ACTIVATION FAILED: {e}")
                return False

        async def instant_delete(message_obj):
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private = str(chat_id) == manager.private_group_id
            try:
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
                try:
                    chat = await client.get_chat(chat_id)
                    await client.delete_messages(chat.id, message_id)
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
                    else:
                        manager.public_delete_failures += 1
                    manager.force_reconnect = True
                    return False

        async def delete_after_delay_instant(message_obj, seconds):
            await asyncio.sleep(seconds)
            await instant_delete(message_obj)

        async def maintain_permanent_peer():
            current_time = time.time()
            if not manager.peer_activated:
                return False
            if current_time - manager.last_peer_maintenance < manager.peer_maintenance_interval and not manager.force_reconnect:
                return True
            try:
                log_info("🔧 SILENT PEER MAINTENANCE: Checking private group connection...")
                chat = await client.get_chat(manager.private_group_id)
                log_info(f"✅ Silent maintenance: {getattr(chat,'title', 'unknown')} connected")
                try:
                    async for _ in client.get_chat_history(manager.private_group_id, limit=1):
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

        async def check_private_group_admin():
            try:
                chat = await client.get_chat(manager.private_group_id)
                me = await client.get_me()
                member = await client.get_chat_member(manager.private_group_id, me.id)
                can_delete = False
                if hasattr(member, "privileges") and member.privileges:
                    can_delete = getattr(member.privileges, "can_delete_messages", False)
                if can_delete:
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

        async def instant_keep_alive():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    await client.get_me()
                    if keep_alive_count % 20 == 0:
                        await maintain_permanent_peer()
                        log_info(f"💓 Instant Keep-Alive #{keep_alive_count} - Silent Maintenance")
                    elif keep_alive_count % 50 == 0:
                        log_info(f"💓 Keep-Alive #{keep_alive_count}")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                await asyncio.sleep(30)

        async def complete_capture_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    if watchdog_count % 10 == 0:
                        log_info(f"🐕 Complete Capture Watchdog - Idle: {int(idle)}s, Total Msgs: {manager.total_messages_received}, Private: {manager.private_delete_count}, Public: {manager.public_delete_count}, Private Fails: {manager.private_delete_failures}, Peer Active: {manager.peer_activated}")
                    if manager.peer_activated and watchdog_count % 30 == 0:
                        await maintain_permanent_peer()
                    if manager.private_delete_failures >= 2 and not manager.private_access_checked:
                        log_info("🔄 Watchdog: Checking private group admin rights...")
                        await check_private_group_admin()
                    if (not manager.peer_activated or manager.force_reconnect) and manager.private_delete_failures >= 1:
                        log_info("🔄 Watchdog: Activating permanent private group peer...")
                        success = await activate_permanent_private_group_peer(client, manager.private_group_id)
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

        async def check_group_access():
            results = {'private': False, 'public': False, 'private_admin': False}
            try:
                try:
                    public_chat = await client.get_chat(manager.public_group_id)
                    results['public'] = True
                    log_info(f"✅ Public Group Access: {public_chat.title}")
                except Exception as e:
                    log_error(f"❌ Public Group Access Failed: {e}")
                try:
                    private_chat = await client.get_chat(manager.private_group_id)
                    results['private'] = True
                    log_info(f"✅ Private Group Access: {getattr(private_chat,'title', 'unknown')}")
                    results['private_admin'] = await check_private_group_admin()
                except Exception as e:
                    log_error(f"❌ Private Group Access Failed: {e}")
            except Exception as e:
                log_error(f"Group access check failed: {e}")
            return results

        # ----------------- register handlers (they use 'client' now) -----------------
        @client.on_message(filters.command("start"))
        async def start_command(c, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                access = await check_group_access()
                status_msg = f"""
🚀 **BOT STARTED - COMPLETE MESSAGE CAPTURE!**

📊 **MESSAGE STATS:**
• Total Messages: {manager.total_messages_received}
• Private Deletes: {manager.private_delete_count} ✅
• Public Deletes: {manager.public_delete_count} ✅
• Private Failures: {manager.private_delete_failures} ❌
• Users Ignored: {manager.users_ignored_count} 👥

🎯 **PERMANENT PEER STATUS:**
• Private Group: {'✅ ACCESS' if access['private'] else '❌ NO ACCESS'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO DELETE RIGHTS'}
• Public Group: {'✅ ACCESS' if access['public'] else '❌ NO ACCESS'}
• Peer Activated: {'✅ PERMANENT' if manager.peer_activated else '❌ INACTIVE'}

🔧 **COMPLETE CAPTURE:**
• Every Message Logged
• Instant Delete (No Delay)
• Permanent Peer Connection
• No Messages Skipped

**Status: {'COMPLETE CAPTURE ACTIVE' if manager.peer_activated else 'NEEDS ACTIVATION'}** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @client.on_message(filters.command("msg_stats"))
        async def msg_stats_command(c, message: Message):
            log_info(f"📩 /msg_stats from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                stats_msg = f"""
📊 **COMPLETE MESSAGE STATISTICS:**

• Total Messages Received: {manager.total_messages_received}
• Private Group Deletes: {manager.private_delete_count}
• Public Group Deletes: {manager.public_delete_count}
• Private Delete Failures: {manager.private_delete_failures}
• Public Delete Failures: {manager.public_delete_failures}
• Users Ignored: {manager.users_ignored_count}
• Last Message Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(manager.last_message_time)) if manager.last_message_time > 0 else 'Never'}

💡 **Capture Status:** {'✅ ACTIVE - No messages skipped' if manager.total_messages_received > 0 else '🔄 WAITING FOR MESSAGES'}
                """
                await message.reply(stats_msg)

        @client.on_message(filters.command("alive"))
        async def alive_command(c, message: Message):
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🔥 Userbot is alive & auto-online is ACTIVE!")
                log_info("✅ /alive command executed")

        @client.on_message(filters.group)
        async def complete_capture_handler(c, message: Message):
            try:
                touch_activity()
                manager.total_messages_received += 1
                manager.last_message_time = time.time()
                group_id = str(message.chat.id)
                is_private = group_id == manager.private_group_id
                username = "unknown"; is_bot = False; detection_reason = "unknown"
                if message.from_user:
                    u = message.from_user
                    username = (getattr(u, "username", None) or f"user_{getattr(u,'id','unknown')}").lower()
                    is_bot = bool(getattr(u, "is_bot", False))
                    detection_reason = "from_user"
                else:
                    sender_chat = getattr(message, "sender_chat", None)
                    if sender_chat:
                        username = (getattr(sender_chat, "username", None) or getattr(sender_chat, "title", None) or f"sender_{getattr(sender_chat,'id','unknown')}").lower()
                        if getattr(message, "via_bot", None) or getattr(message, "via_bot_id", None):
                            is_bot = True; detection_reason = "sender_chat_via_bot"
                        else:
                            detection_reason = "sender_chat"
                    else:
                        fwd = getattr(message, "forward_from", None)
                        if fwd:
                            username = (getattr(fwd, "username", None) or f"user_{getattr(fwd,'id','unknown')}").lower()
                            is_bot = bool(getattr(fwd, "is_bot", False)); detection_reason = "forward_from"
                if not is_bot and getattr(message, "via_bot", None):
                    is_bot = True; detection_reason = "via_bot"
                message_text = message.text or message.caption or ""
                log_info(f"[MSG #{manager.total_messages_received}] group={group_id} private={is_private} username={username} is_bot={is_bot} reason={detection_reason} text_preview={message_text[:80]}")
                if group_id not in allowed_groups:
                    log_info(f"🚫 IGNORED GROUP MESSAGE #{manager.total_messages_received}: {group_id} - @{username}")
                    return
                try:
                    current_me = await client.get_me()
                    if message.from_user and message.from_user.id == current_me.id:
                        log_info(f"🔁 SELF MESSAGE IGNORED: #{manager.total_messages_received}")
                        return
                except Exception as e:
                    log_error(f"❌ Self check failed: {e}")
                if not is_bot:
                    manager.users_ignored_count += 1
                    log_info(f"👥 USER IGNORED #{manager.total_messages_received}: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return
                username_clean = username.lstrip("@").lower()
                if username_clean in safe_bots:
                    log_info(f"✅ SAFE BOT IGNORED #{manager.total_messages_received}: @{username_clean} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return
                has_links_or_mentions = manager.contains_any_links_or_mentions(message_text)
                if username_clean in delayed_bots:
                    if has_links_or_mentions:
                        log_info(f"🚫 DELAYED BOT WITH LINKS #{manager.total_messages_received}: INSTANT DELETE - @{username_clean}")
                        await instant_delete(message)
                    else:
                        log_info(f"⏰ DELAYED BOT NORMAL #{manager.total_messages_received}: DELETE IN 5s - @{username_clean}")
                        asyncio.create_task(delete_after_delay_instant(message, 5))
                    return
                log_info(f"🗑️ UNSAFE BOT #{manager.total_messages_received}: INSTANT DELETE - @{username_clean}")
                await instant_delete(message)
            except Exception as e:
                log_error(f"❌ Complete Capture Handler error: {e}")
                touch_activity()

        # ---------------------- start client and background tasks ----------------------
        log_info("🔗 Connecting to Telegram - COMPLETE MESSAGE CAPTURE...")
        await client.start()

        # ⭐ ULTRA-SAFE AUTO-ONLINE MODULE (Pure API Calls - NO CHAT ACTIONS)
        async def stay_online_safe(client):
            online_count = 0
            while True:
                try:
                    # Pure API calls only - no chat actions
                    await client.get_me()                    # Simple API call
                    await client.get_users("me")            # Another API call
                    touch_activity()
                    
                    online_count += 1
                    if online_count % 20 == 0:  # Log every 20 cycles (~5 minutes)
                        log_info(f"🟢 AUTO-ONLINE: Session active - Cycle #{online_count}")

                except Exception as e:
                    tb = traceback.format_exc()
                    log_error(f"❌ Auto-online error: {repr(e)}\n{tb}")

                await asyncio.sleep(15)   # safe interval

        # Start auto-online task
        asyncio.get_event_loop().create_task(stay_online_safe(client))
        log_info("🟢 AUTO-ONLINE MODULE: ACTIVATED (Pure API Method)")

        me = await client.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")

        if not manager.peer_activated:
            log_info("🚀 STARTUP: Auto-activating permanent private group peer...")
            await activate_permanent_private_group_peer(client, manager.private_group_id)
        else:
            log_info("🔗 STARTUP: Permanent peer already activated, doing silent maintenance...")
            await maintain_permanent_peer()

        access = await check_group_access()
        log_info(f"🎯 COMPLETE MESSAGE CAPTURE ACTIVATED")
        log_info(f"🔗 Link Patterns: {len(manager.all_link_patterns)} types")
        log_info(f"🛡️ Safe Bots: {len(safe_bots)}")
        log_info(f"📊 Group Access - Private: {access['private']}, Private Admin: {access['private_admin']}, Public: {access['public']}, Peer Activated: {manager.peer_activated}")

        keep_alive_task = asyncio.create_task(instant_keep_alive())
        watchdog_task = asyncio.create_task(complete_capture_watchdog())

        log_info("💓 Instant Keep-Alive: ACTIVE")
        log_info("🚀 Complete Message Capture: READY")
        log_info("🔇 Silent Peer Maintenance: ACTIVE")

        try:
            await client.send_message("me", f"""
✅ **BOT STARTED - COMPLETE MESSAGE CAPTURE!**

🎯 **COMPLETE CAPTURE FEATURES:**
• Every Message Logged ✅
• No Messages Skipped ✅  
• Instant Delete 🚀
• Permanent Peer 🔗
• Silent Maintenance 🔇
• Auto-Online 24/7 🟢

📊 **INITIAL STATUS:**
• Private Group: {'✅ ACCESSIBLE' if access['private'] else '❌ NOT ACCESSIBLE'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO RIGHTS'}
• Peer Activated: {'✅ PERMANENT' if manager.peer_activated else '❌ TEMPORARY'}
• Auto-Online: ✅ ACTIVE

💡 **Use /msg_stats to check message statistics**
💡 **Use /alive to check auto-online status**

**Status: {'COMPLETE CAPTURE ACTIVE' if manager.peer_activated else 'NEEDS ACTIVATION'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")

        log_info("🤖 BOT READY - Complete Message Capture Active!")

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
            await client.stop()

    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - COMPLETE MESSAGE CAPTURE...")

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
