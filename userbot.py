#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🔥 ULTIMATE BOT STARTING - COMPLETE MESSAGE CAPTURE FIX (WITH SUPERVISOR)...")

import asyncio
import multiprocessing
import re
import traceback
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, ChannelPrivate, PeerIdInvalid
import threading
import requests
import time
import sys
import json
import os
import signal
import logging
from logging.handlers import RotatingFileHandler

# ---------------------------
# ADVANCED LOGGING (ROTATING)
# ---------------------------
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


# -----------------------
# Data (files + defaults)
# -----------------------
ALLOWED_GROUPS_FILE = "allowed_groups.json"
SAFE_BOTS_FILE = "safe_bots.json"
DELAYED_BOTS_FILE = "delayed_bots.json"
PEER_STATUS_FILE = "peer_status.json"


def load_data(filename, default=None):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                # Ensure set for in-memory usage
                if isinstance(data, list):
                    return set(data)
                if isinstance(data, dict):
                    return set(data.keys())
                return set(data)
    except Exception as e:
        log_error(f"load_data({filename}) failed: {e}")
    return default if default is not None else set()


def save_data(filename, data):
    try:
        # convert sets to list
        to_save = list(data) if isinstance(data, (set, list)) else data
        with open(filename, 'w') as f:
            json.dump(to_save, f)
    except Exception as e:
        log_error(f"save_data({filename}) failed: {e}")


def load_peer_status():
    try:
        if os.path.exists(PEER_STATUS_FILE):
            with open(PEER_STATUS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        log_error(f"load_peer_status failed: {e}")
    return {"private_peer_activated": False, "last_activation": None}


def save_peer_status(status):
    try:
        with open(PEER_STATUS_FILE, 'w') as f:
            json.dump(status, f)
    except Exception as e:
        log_error(f"save_peer_status failed: {e}")


# Load data - defaults
allowed_groups = {"-1002382070176", "-1002497459144"}  # Direct set
safe_bots = load_data(SAFE_BOTS_FILE, default={"unobot", "on9wordchainbot", "daisyfcbot", "missrose_bot", "zorofcbot", "digi4bot"})
delayed_bots = load_data(DELAYED_BOTS_FILE, default={"crocodile_game4_bot"})
peer_status = load_peer_status()

# Save ensured defaults back
save_data(ALLOWED_GROUPS_FILE, allowed_groups)
save_data(SAFE_BOTS_FILE, safe_bots)
save_data(DELAYED_BOTS_FILE, delayed_bots)

# YOUR USER ID (admin)
ADMIN_USER_ID = 8368838212

log_info(f"✅ Loaded {len(allowed_groups)} groups, {len(safe_bots)} safe bots, {len(delayed_bots)} delayed bots")
log_info(f"📡 Peer Status: {peer_status}")

# -----------------------
# Sleep protection (Flask + pinger)
# -----------------------
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
        self._flask_process = None

    def start_protection(self):
        log_info("🛡️ Starting Ultimate Sleep Protection...")
        self.start_flask()
        self.start_external_pings()
        log_info("✅ SLEEP PROTECTION: ACTIVATED")

    def start_flask(self):
        def run_flask_forever():
            # Run Flask in loop so that crash -> restart automatically.
            while True:
                try:
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

                    # Auto-ping every 30 seconds to keep local Flask alive
                    def auto_ping():
                        while True:
                            try:
                                requests.get("http://localhost:10000/ping", timeout=5)
                            except:
                                pass
                            time.sleep(30)

                    threading.Thread(target=auto_ping, daemon=True).start()
                    # Run flask (blocking) - if it raises, the outer loop will restart it
                    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
                except Exception as e:
                    log_error(f"Flask crashed, restarting: {e}")
                    time.sleep(2)

        # Run Flask in a separate process to isolate it from main Python process
        self._flask_process = multiprocessing.Process(target=run_flask_forever, daemon=True)
        self._flask_process.start()
        time.sleep(3)
        log_info("✅ Flask Server: RUNNING (supervised)")

    def start_external_pings(self):
        def external_pinger():
            while True:
                for url in self.external_urls:
                    try:
                        requests.get(url, timeout=10)
                        self.last_external_ping = time.time()
                    except Exception as e:
                        log_error(f"External ping failed to {url}: {e}")
                time.sleep(60)

        threading.Thread(target=external_pinger, daemon=True).start()
        log_info("✅ External Pings: RUNNING")


# Initialize sleep protection
log_info("🛡️ Initializing Sleep Protection...")
sleep_protector = SleepProtection()
sleep_protector.start_protection()

# Keep track of last activity so watchdog can detect freezes
last_activity = time.time()


def touch_activity():
    global last_activity
    last_activity = time.time()


# -----------------------
# CompleteCaptureManager
# -----------------------
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
        self.peer_maintenance_interval = 60  # 1 minute
        self.force_reconnect = False
        self.peer_recovery_attempts = 0

        # Link patterns
        self.all_link_patterns = [
            'http://', 'https://', 't.me/', 'telegram.me/', 'tg://',
            'facebook.com/', 'instagram.com/', 'twitter.com/', 'youtube.com/',
            'drive.google.com/', 'mega.nz/', 'dropbox.com/', 'bit.ly/',
            '.com/', '.org/', '.net/', '.in/', '@'
        ]

    def contains_any_links_or_mentions(self, text):
        if not text:
            return False
        text_lower = text.lower()
        for pattern in self.all_link_patterns:
            if pattern in text_lower:
                return True
        return False


manager = CompleteCaptureManager()

# -----------------------
# Pyrogram Client (single instance)
# -----------------------
# Use your original credentials / session_string
client = Client(
    "ultimate_bot",
    api_id=22294121,
    api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
    session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
)

# helper
def is_admin(user_id):
    return user_id == ADMIN_USER_ID

# -----------------------
# Handlers (registered once)
# -----------------------
@client.on_message(filters.command("start"))
async def start_command(c, message: Message):
    try:
        log_info(f"📩 /start from {getattr(message.from_user,'id','unknown')}")
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
• Peer Recovery: {manager.peer_recovery_attempts} 🔄

🎯 **PERMANENT PEER STATUS:**
• Private Group: {'✅ ACCESS' if access['private'] else '❌ NO ACCESS'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO DELETE RIGHTS'}
• Public Group: {'✅ ACCESS' if access['public'] else '❌ NO ACCESS'}
• Peer Activated: {'✅ PERMANENT' if manager.peer_activated else '❌ INACTIVE'}

🔧 **COMPLETE CAPTURE:**
• Every Message Logged
• Instant Delete (No Delay)
• **PERMANENT PEER CONNECTION** 🔗
• Auto Peer Recovery
• No Messages Skipped

**Status: {'COMPLETE CAPTURE ACTIVE' if manager.peer_activated else 'NEEDS ACTIVATION'}** 🔥
                """
            await message.reply(status_msg)
            log_info("✅ /start executed")
    except Exception as e:
        log_error(f"/start handler error: {e}")

@client.on_message(filters.command("msg_stats"))
async def msg_stats_command(c, message: Message):
    try:
        log_info(f"📩 /msg_stats from {getattr(message.from_user,'id','unknown')}")
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
• Peer Recovery Attempts: {manager.peer_recovery_attempts}
• Last Message Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(manager.last_message_time)) if manager.last_message_time > 0 else 'Never'}

💡 **Capture Status:** {'✅ ACTIVE - No messages skipped' if manager.total_messages_received > 0 else '🔄 WAITING FOR MESSAGES'}
                """
            await message.reply(stats_msg)
    except Exception as e:
        log_error(f"/msg_stats handler error: {e}")

@client.on_message(filters.command("alive"))
async def alive_command(c, message: Message):
    try:
        if message.from_user and is_admin(message.from_user.id):
            await message.reply("🔥 Userbot is alive & PERMANENT PEER is ACTIVE!")
            log_info("✅ /alive command executed")
    except Exception as e:
        log_error(f"/alive handler error: {e}")

# Keep a very light handler to keep userbot "active" in Telegram's eyes
@client.on_message(filters.all & filters.private)
async def _private_keepalive(c, message: Message):
    # empty handler: just touching activity so session considered active
    touch_activity()

# Main group handler (registered once)
@client.on_message(filters.group)
async def complete_capture_handler(c, message: Message):
    try:
        touch_activity()
        manager.total_messages_received += 1
        manager.last_message_time = time.time()
        group_id = str(message.chat.id)
        is_private = group_id == manager.private_group_id

        # FASTEST POSSIBLE MESSAGE PROCESSING
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
                await instant_delete_with_peer_recovery(message)
            else:
                log_info(f"⏰ DELAYED BOT NORMAL #{manager.total_messages_received}: DELETE IN 5s - @{username_clean}")
                asyncio.create_task(delete_after_delay_instant(message, 5))
            return

        log_info(f"🗑️ UNSAFE BOT #{manager.total_messages_received}: INSTANT DELETE - @{username_clean}")
        await instant_delete_with_peer_recovery(message)

    except Exception as e:
        log_error(f"❌ Complete Capture Handler error: {e}")
        touch_activity()


# -----------------------
# Core async helpers that rely on `client` & `manager`
# -----------------------
async def force_peer_connection(group_id):
    try:
        log_info(f"🔗 FORCING PEER CONNECTION: {group_id}")
        chat = await client.get_chat(group_id)
        log_info(f"✅ Peer connected: {getattr(chat,'title', 'unknown')}")
        try:
            async for message in client.get_chat_history(group_id, limit=1):
                log_info(f"✅ Chat history accessed: {message.id}")
                break
        except Exception as e:
            log_info(f"⚠️ Chat history skipped: {e}")
        try:
            async for member in client.get_chat_members(group_id, limit=1):
                log_info(f"✅ Chat members accessed")
                break
        except Exception as e:
            log_info(f"⚠️ Chat members skipped: {e}")
        return True
    except Exception as e:
        log_error(f"❌ Force peer connection failed: {e}")
        return False


async def maintain_peers_continuously():
    maintenance_count = 0
    while True:
        try:
            maintenance_count += 1
            for group_id in allowed_groups:
                try:
                    await client.get_chat(group_id)
                    if maintenance_count % 10 == 0:
                        log_info(f"🔗 PEER ACTIVE: {group_id}")
                except (ChannelPrivate, PeerIdInvalid) as e:
                    log_error(f"❌ PEER LOST: {group_id} - {e}")
                    await force_peer_connection(group_id)
                except Exception as e:
                    log_error(f"⚠️ Peer check failed: {group_id} - {e}")
            touch_activity()
            await asyncio.sleep(30)
        except Exception as e:
            log_error(f"❌ Peer maintenance error: {e}")
            await asyncio.sleep(5)


async def activate_permanent_private_group_peer(private_group_id):
    try:
        log_info("🔄 PERMANENT PEER: Activating private group peer...")
        connection_methods = [
            ("Get Chat", lambda: client.get_chat(private_group_id)),
            ("Chat History", lambda: client.get_chat_history(private_group_id, limit=2)),
            ("Chat Members", lambda: client.get_chat_members(private_group_id, limit=2)),
        ]
        success_count = 0
        for method_name, method_func in connection_methods:
            try:
                result = await method_func()
                if method_name == "Get Chat":
                    log_info(f"✅ Chat fetched: {getattr(result,'title', 'unknown')}")
                else:
                    async for item in result:
                        break
                    log_info(f"✅ {method_name} connection established")
                success_count += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                log_info(f"⚠️ {method_name} connection skipped: {e}")
        if success_count >= 1:
            manager.peer_activated = True
            manager.peer_activation_time = time.time()
            manager.peer_recovery_attempts = 0
            peer_status.update({
                "private_peer_activated": True,
                "last_activation": manager.peer_activation_time,
                "group_id": private_group_id
            })
            save_peer_status(peer_status)
            log_info("🟢 PERMANENT PEER ACTIVATED — Will NOT disconnect")
            return True
        else:
            log_error("❌ All peer connection methods failed")
            return False
    except Exception as e:
        log_error(f"❌ PERMANENT PEER ACTIVATION FAILED: {e}")
        return False


async def instant_delete_with_peer_recovery(message_obj):
    chat_id = message_obj.chat.id
    message_id = message_obj.id
    is_private = str(chat_id) == manager.private_group_id

    try:
        # METHOD 1: Direct delete
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

        # PEER RECOVERY ATTEMPT
        manager.peer_recovery_attempts += 1
        log_info(f"🔄 PEER RECOVERY ATTEMPT #{manager.peer_recovery_attempts} for {chat_id}")

        # IMMEDIATELY TRY TO RECONNECT PEER
        recovery_success = await force_peer_connection(str(chat_id))

        if recovery_success:
            log_info("✅ Peer recovered, retrying delete...")
            try:
                await message_obj.delete()
                if is_private:
                    manager.private_delete_count += 1
                else:
                    manager.public_delete_count += 1
                log_info(f"✅ DELETE AFTER RECOVERY: {message_id}")
                return True
            except Exception as e2:
                log_error(f"❌ Delete after recovery failed: {e2}")

        # METHOD 3: Final attempt with chat resolve
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
        except Exception as e3:
            log_error(f"❌ Resolve delete failed: {e3}")
            if is_private:
                manager.private_delete_failures += 1
            else:
                manager.public_delete_failures += 1
            manager.force_reconnect = True
            return False


async def delete_after_delay_instant(message_obj, seconds):
    await asyncio.sleep(seconds)
    await instant_delete_with_peer_recovery(message_obj)


async def maintain_permanent_peer():
    current_time = time.time()
    if not manager.peer_activated:
        return False

    if current_time - manager.last_peer_maintenance < manager.peer_maintenance_interval and not manager.force_reconnect:
        return True

    try:
        log_info("🔧 PEER MAINTENANCE: Checking group connections...")
        for group_id in allowed_groups:
            try:
                chat = await client.get_chat(group_id)
                log_info(f"✅ Peer active: {getattr(chat,'title', 'unknown')}")
            except Exception as e:
                log_error(f"❌ Peer check failed for {group_id}: {e}")
                await force_peer_connection(group_id)
        manager.last_peer_maintenance = current_time
        manager.force_reconnect = False
        return True
    except Exception as e:
        log_error(f"❌ Peer maintenance failed: {e}")
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
    while True:
        keep_alive_count += 1
        try:
            await client.get_me()
            # Every 10th keep-alive, do peer maintenance
            if keep_alive_count % 10 == 0:
                await maintain_permanent_peer()
                log_info(f"💓 Keep-Alive #{keep_alive_count} - Peer Maintenance")
            elif keep_alive_count % 30 == 0:
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
                log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Total Msgs: {manager.total_messages_received}, Private: {manager.private_delete_count}, Public: {manager.public_delete_count}, Peer Recovery: {manager.peer_recovery_attempts}")

            if manager.peer_activated and watchdog_count % 15 == 0:
                await maintain_permanent_peer()

            if manager.peer_recovery_attempts >= 3:
                log_info("🔄 Watchdog: Too many recovery attempts, forcing peer reconnect...")
                for group_id in allowed_groups:
                    await force_peer_connection(group_id)
                manager.peer_recovery_attempts = 0

            if idle > 300:
                log_error(f"⚠️ Watchdog: Restarting - No activity for {int(idle)}s")
                for h in logger.handlers:
                    try:
                        h.flush()
                    except:
                        pass
                try:
                    # graceful restart: raise an exception to let supervisor restart the client
                    raise RuntimeError("Watchdog triggered restart due to inactivity")
                except Exception as e:
                    log_error(f"Watchdog requested restart: {e}")
            await asyncio.sleep(10)
        except Exception as e:
            log_error(f"Watchdog error: {e}")
            await asyncio.sleep(5)


async def check_group_access():
    results = {'private': False, 'public': False, 'private_admin': False}
    try:
        for group_id in allowed_groups:
            try:
                chat = await client.get_chat(group_id)
                if group_id == manager.private_group_id:
                    results['private'] = True
                    log_info(f"✅ Private Group Access: {getattr(chat,'title', 'unknown')}")
                    results['private_admin'] = await check_private_group_admin()
                else:
                    results['public'] = True
                    log_info(f"✅ Public Group Access: {chat.title}")
            except Exception as e:
                if group_id == manager.private_group_id:
                    log_error(f"❌ Private Group Access Failed: {e}")
                else:
                    log_error(f"❌ Public Group Access Failed: {e}")
    except Exception as e:
        log_error(f"Group access check failed: {e}")
    return results


# -----------------------
# Auto-online module
# -----------------------
async def stay_online_safe():
    online_count = 0
    while True:
        try:
            await client.get_me()
            await client.get_users("me")
            touch_activity()
            online_count += 1
            if online_count % 20 == 0:
                log_info(f"🟢 AUTO-ONLINE: Session active - Cycle #{online_count}")
        except Exception as e:
            tb = traceback.format_exc()
            log_error(f"❌ Auto-online error: {repr(e)}\n{tb}")
        await asyncio.sleep(15)


# -----------------------
# Supervisor: start client, monitor tasks, auto-restart on failure
# -----------------------
async def client_supervisor():
    backoff = 1
    max_backoff = 60
    while True:
        try:
            log_info("🔗 Supervisor: Starting client...")
            await client.start()
            me = await client.get_me()
            log_info(f"✅ BOT CONNECTED: {me.first_name} (@{getattr(me,'username','unknown')})")

            # start essential operations
            # ensure peer activation
            if not manager.peer_activated:
                log_info("🚀 STARTUP: Auto-activating permanent private group peer...")
                try:
                    await activate_permanent_private_group_peer(manager.private_group_id)
                except Exception as e:
                    log_error(f"Peer activation attempt failed at startup: {e}")

            # Force peer connections for all groups once
            for group_id in allowed_groups:
                try:
                    await force_peer_connection(group_id)
                except Exception as e:
                    log_error(f"Force initial connection failed for {group_id}: {e}")

            access = await check_group_access()
            log_info(f"🎯 COMPLETE MESSAGE CAPTURE ACTIVATED")
            log_info(f"🔗 Link Patterns: {len(manager.all_link_patterns)} types")
            log_info(f"🛡️ Safe Bots: {len(safe_bots)}")
            log_info(f"📊 Group Access - Private: {access['private']}, Private Admin: {access['private_admin']}, Public: {access['public']}, Peer Activated: {manager.peer_activated}")

            # prepare tasks
            tasks = []
            tasks.append(asyncio.create_task(instant_keep_alive()))
            tasks.append(asyncio.create_task(maintain_peers_continuously()))
            tasks.append(asyncio.create_task(stay_online_safe()))
            tasks.append(asyncio.create_task(complete_capture_watchdog()))

            # notify owner (best-effort)
            try:
                await client.send_message("me", f"✅ **BOT STARTED - COMPLETE MESSAGE CAPTURE!**\nStatus: {'COMPLETE CAPTURE ACTIVE' if manager.peer_activated else 'NEEDS ACTIVATION'}")
            except Exception as e:
                log_error(f"Startup DM failed: {e}")

            # supervise tasks: if any task exits with exception, restart whole client
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

            # if we reach here, a task finished (likely with exception)
            for d in done:
                if d.cancelled():
                    log_info("Supervisor: a task was cancelled")
                else:
                    exc = d.exception()
                    if exc:
                        log_error(f"Supervisor: Task raised exception: {exc}")
                    else:
                        log_info("Supervisor: a task finished without exception")

            # cancel pending tasks
            for p in pending:
                try:
                    p.cancel()
                except:
                    pass

            # attempt graceful stop of client
            try:
                await client.stop()
            except Exception as e:
                log_error(f"Error stopping client during supervisor restart: {e}")

            # prepare for restart
            log_info(f"🔁 Supervisor: Restarting client in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(max_backoff, backoff * 2)  # exponential backoff
            continue

        except Exception as e:
            log_error(f"❌ Supervisor encountered error: {e}\n{traceback.format_exc()}")
            try:
                await client.stop()
            except Exception:
                pass
            log_info(f"⏳ Supervisor: Waiting {backoff}s before restart...")
            await asyncio.sleep(backoff)
            backoff = min(max_backoff, backoff * 2)
            continue


# -----------------------
# Entrypoint
# -----------------------
async def main():
    # Run supervisor; it will manage start/stop/restarts
    await client_supervisor()


if __name__ == "__main__":
    log_info("🚀 BOT STARTING - SUPERVISED MODE...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_info("Received KeyboardInterrupt, shutting down...")
        try:
            asyncio.run(client.stop())
        except:
            pass
    except Exception as e:
        log_critical(f"CRASH: {e}\n{traceback.format_exc()}")
        for h in logger.handlers:
            try:
                h.flush()
            except:
                pass
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            log_critical(f"Final execv restart failed: {e}")
        sys.exit(1)
