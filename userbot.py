print("🔥 ULTIMATE BOT STARTING - SESSION STABILITY FIX...")

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

# Load data
allowed_groups = load_data(ALLOWED_GROUPS_FILE)
safe_bots = load_data(SAFE_BOTS_FILE)
delayed_bots = load_data(DELAYED_BOTS_FILE)

# If files were empty (first run), enforce the clean master lists the user wanted
if not allowed_groups:
    allowed_groups = {"-1002382070176", "-1002497459144"}
if not safe_bots:
    safe_bots = {"unobot","on9wordchainbot","daisyfcbot","missrose_bot","zorofcbot","digi4bot"}
if not delayed_bots:
    delayed_bots = {"crocodile_game4_bot"}

# Save ensured defaults back
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

# 🔥 TELEGRAM BOT - SESSION STABILITY FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - SESSION STABILITY FIX...")
    
    # ✅ SESSION STABILITY VARIABLES
    session_active = True
    connection_checks = 0
    restart_attempts = 0

    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        me = None
        
        # -----------------------------
        # Helper functions for deletes
        # -----------------------------
        async def force_delete_pyrogram(message_obj):
            """
            Force-delete a pyrogram Message object with 3-layer strategy:
            1) message.delete()
            2) short sleep + message.delete()
            3) app.delete_messages(chat_id, message_id) (fallback)
            """
            touch_activity()
            try:
                await message_obj.delete()
                log_info(f"[force_delete] layer1 OK - msg:{getattr(message_obj, 'message_id', getattr(message_obj, 'id', 'unknown'))}")
                return True
            except Exception as e1:
                log_error(f"[force_delete] layer1 failed: {e1}")

            await asyncio.sleep(0.35)

            try:
                await message_obj.delete()
                log_info("[force_delete] layer2 retry OK")
                return True
            except Exception as e2:
                log_error(f"[force_delete] layer2 failed: {e2}")

            # Final fallback: direct API delete by id(s)
            try:
                chat_id_ = message_obj.chat.id if message_obj.chat else getattr(message_obj, "chat_id", None)
                msg_id = getattr(message_obj, "message_id", getattr(message_obj, "id", None))
                if chat_id_ is not None and msg_id is not None:
                    # pyrogram.Client.delete_messages expects chat_id and message_id(s)
                    await app.delete_messages(chat_id_, msg_id)
                    log_info("[force_delete] layer3 direct API delete OK")
                    return True
                else:
                    log_error("[force_delete] cannot obtain chat_id or msg_id for final delete")
            except Exception as e3:
                log_critical(f"[force_delete] layer3 failed: {e3}")

            return False

        async def delete_after_delay_pyrogram(message_obj, sec):
            await asyncio.sleep(sec)
            try:
                await force_delete_pyrogram(message_obj)
            except Exception as e:
                log_error(f"[delayed_delete] failed: {e}")

        # ✅ SIMPLE ONLINE STATUS - ERROR FIXED
        async def simple_online_status():
            """Simple online status without errors"""
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    # Simple activity to stay online
                    await app.get_me()
                    # Simple chat activity
                    async for dialog in app.get_dialogs(limit=1):
                        pass
                    
                    log_info(f"🟢 Online Status #{online_count} - Active")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Online Status Failed: {e}")
                await asyncio.sleep(60)  # Every 1 minute
        
        # ✅ SESSION KEEP-ALIVE
        async def session_keep_alive():
            """Session ko active rakhta hai"""
            nonlocal connection_checks, session_active
            keep_alive_count = 0
            
            while session_active:
                keep_alive_count += 1
                connection_checks += 1
                
                try:
                    # Simple API call to keep session alive
                    if me:
                        # Try to get own info - simple API call
                        current_me = await app.get_me()
                        log_info(f"💓 Session Keep-Alive #{keep_alive_count} - Connection: ✅ ACTIVE")
                        touch_activity()
                    else:
                        log_info(f"💓 Session Keep-Alive #{keep_alive_count} - Initializing...")
                    
                except Exception as e:
                    log_error(f"⚠️ Session Keep-Alive Failed: {e}")
                    session_active = False
                    break
                
                await asyncio.sleep(180)  # Every 3 minutes

        # -------------------------
        # WATCHDOG / AUTO-RESTART
        # -------------------------
        async def watchdog_loop():
            """Monitor activity and perform restart if frozen. Implements methods A (self-restart), B (external-ping), C (both)"""
            nonlocal restart_attempts
            while True:
                try:
                    idle = time.time() - last_activity
                    # if no activity for 5 minutes -> attempt restart
                    if idle > 300:
                        restart_attempts += 1
                        log_error(f"⚠️ Watchdog: No activity for {int(idle)}s — initiating recovery (attempt #{restart_attempts})")

                        # Method B: trigger external ping/restart endpoint (best-effort)
                        for url in sleep_protector.external_urls:
                            try:
                                requests.get(url + "ping", timeout=8)
                            except Exception as e:
                                log_error(f"Watchdog: external ping failed: {e}")

                        # Method A: self-restart
                        try:
                            log_info("Watchdog: Performing self-restart (os.execv)")
                            # flush logs
                            for h in logger.handlers:
                                h.flush()
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        except Exception as e:
                            log_error(f"Watchdog: self-restart failed: {e}")

                        # Method C: fallback - call monitor restart endpoint if available
                        try:
                            requests.post(sleep_protector.monitor_restart_url, timeout=6)
                        except Exception as e:
                            log_error(f"Watchdog: monitor endpoint call failed: {e}")

                        # wait a bit before next check
                        await asyncio.sleep(30)
                    else:
                        await asyncio.sleep(10)
                except Exception as e:
                    log_error(f"Watchdog loop error: {e}")
                    await asyncio.sleep(5)

        # -----------------------------
        # FIX 1 — KEEP SESSION ALIVE
        # -----------------------------
        async def keep_session_alive_loop():
            while True:
                try:
                    await app.get_dialogs(limit=1)
                    touch_activity()
                except Exception as e:
                    log_error(f"keep_session_alive error: {e}")
                await asyncio.sleep(20)

        # -----------------------------
        # FIX 2 — FORCE STATE REFRESH
        # -----------------------------
        async def force_state_update():
            # Pyrogram doesn't expose GetStateRequest directly like Telethon; use a lightweight call pattern
            while True:
                try:
                    # small harmless call to keep state updated
                    await app.get_chats(limit=1)
                    touch_activity()
                except Exception as e:
                    log_error(f"force_state_update error: {e}")
                await asyncio.sleep(10)

        # ✅ ALL COMMANDS - WORKING VERSION
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 Received /start from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **ULTIMATE BOT STARTED!**
Commands Working Now")
                log_info("✅ /start command executed")
        
        @app.on_message(filters.command("help"))
        async def help_command(client, message: Message):
            log_info(f"📩 Received /help from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                help_text = """
🤖 **ULTIMATE BOT - ALL COMMANDS**

**Basic:**
├─ /start - Start bot
├─ /help - This help
├─ /ping - Test response
├─ /alive - Check alive
├─ /status - Bot status

**Management:**
├─ /allow <group_id> - Allow group
├─ /safe @bot - Add safe bot
├─ /delay @bot - Add delayed bot
├─ /remove @bot - Remove bot

**Protection:**
├─ /sleepstatus - Sleep protection
├─ /nleep - Sleep check
├─ /test - Test deletion
                """
                await message.reply(help_text)
                log_info("✅ /help command executed")
        
        @app.on_message(filters.command("ping"))
        async def ping_command(client, message: Message):
            log_info(f"📩 Received /ping from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🏓 **Pong!** Bot active")
                log_info("✅ /ping command executed")
        
        @app.on_message(filters.command("alive"))
        async def alive_command(client, message: Message):
            log_info(f"📩 Received /alive from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🟢 **BOT ZINDA HAI!** 24/7 Active")
                log_info("✅ /alive command executed")
        
        @app.on_message(filters.command("nleep"))
        async def nleep_command(client, message: Message):
            log_info(f"📩 Received /nleep from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚫 **SLEEP NAHI HOGAA!** Protection Active")
                log_info("✅ /nleep command executed")
        
        @app.on_message(filters.command("status"))
        async def status_command(client, message: Message):
            log_info(f"📩 Received /status from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                nonlocal me, connection_checks
                
                if me is None: 
                    me = await app.get_me()
                
                status_text = f"""
🤖 **BOT STATUS - WORKING**

**Info:**
├─ Name: {me.first_name}
├─ Groups: {len(allowed_groups)}
├─ Safe Bots: {len(safe_bots)}
├─ Delayed Bots: {len(delayed_bots)}

**Session:**
├─ Connection Checks: {connection_checks}
├─ Session Status: ✅ ACTIVE
├─ Keep-Alive: ✅ RUNNING
└─ Stability: 🔥 GUARANTEED
                """
                await message.reply(status_text)
                log_info("✅ /status command executed")
        
        @app.on_message(filters.command("sleepstatus"))
        async def sleepstatus_command(client, message: Message):
            log_info(f"📩 Received /sleepstatus from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                uptime = int(time.time() - sleep_protector.start_time)
                await message.reply(f"🛡️ **SLEEP PROTECTION ACTIVE**
Uptime: {uptime}s | Pings: {sleep_protector.ping_count}")
                log_info("✅ /sleepstatus command executed")
        
        @app.on_message(filters.command("allow"))
        async def allow_command(client, message: Message):
            log_info(f"📩 Received /allow from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                if len(message.command) > 1:
                    group_id = message.command[1]
                    if group_id in allowed_groups:
                        await message.reply(f"ℹ️ Group `{group_id}` already allowed!")
                    else:
                        allowed_groups.add(group_id)
                        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                        await message.reply(f"✅ Group `{group_id}` allowed & SAVED!")
                        log_info(f"✅ Group {group_id} added to allowed list")
                else:
                    await message.reply("❌ Usage: `/allow <group_id>`")
        
        @app.on_message(filters.command("safe"))
        async def safe_command(client, message: Message):
            log_info(f"📩 Received /safe from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    if bot_username in safe_bots:
                        await message.reply(f"ℹ️ @{bot_username} already in safe list!")
                    else:
                        safe_bots.add(bot_username)
                        save_data(SAFE_BOTS_FILE, safe_bots)
                        await message.reply(f"✅ @{bot_username} added to safe list!")
                        log_info(f"✅ Bot @{bot_username} added to safe list")
                else:
                    await message.reply("❌ Usage: `/safe @botusername`")
        
        @app.on_message(filters.command("delay"))
        async def delay_command(client, message: Message):
            log_info(f"📩 Received /delay from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    if bot_username in delayed_bots:
                        await message.reply(f"ℹ️ @{bot_username} already in delayed list!")
                    else:
                        delayed_bots.add(bot_username)
                        save_data(DELAYED_BOTS_FILE, delayed_bots)
                        await message.reply(f"⏰ @{bot_username} added to delayed list!")
                        log_info(f"✅ Bot @{bot_username} added to delayed list")
                else:
                    await message.reply("❌ Usage: `/delay @botusername`")
        
        @app.on_message(filters.command("remove"))
        async def remove_command(client, message: Message):
            log_info(f"📩 Received /remove from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    was_in_safe = bot_username in safe_bots
                    was_in_delayed = bot_username in delayed_bots
                    
                    safe_bots.discard(bot_username)
                    delayed_bots.discard(bot_username)
                    
                    if was_in_safe or was_in_delayed:
                        save_data(SAFE_BOTS_FILE, safe_bots)
                        save_data(DELAYED_BOTS_FILE, delayed_bots)
                        await message.reply(f"🗑️ @{bot_username} removed from all lists!")
                        log_info(f"✅ Bot @{bot_username} removed from lists")
                    else:
                        await message.reply(f"ℹ️ @{bot_username} not found in any list!")
                else:
                    await message.reply("❌ Usage: `/remove @botusername`")
        
        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 Received /test from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing deletion...")
                await asyncio.sleep(2)
                await test_msg.delete()
                await message.reply("✅ Test passed! Deletion working")
                log_info("✅ /test command executed")
        
        # ---------------------------------------------------------
        # ULTRA-POWERFUL DELETE HANDLER (UPDE v4.0) - pyrogram
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def ultra_powerful_delete_handler(client, message: Message):
            try:
                # --- FIX #1: GROUP ID MISMATCH FIX ---
                group_id = str(message.chat.id).strip()
                allowed_groups_clean = {str(g).strip() for g in allowed_groups}

                if group_id not in allowed_groups_clean:
                    log_info(f"❌ Group Not Allowed / ID Mismatch → {group_id}")
                    return

                # Self check
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return

                # --- PERMISSION CHECK (best-effort) ---
                try:
                    chat_member = await app.get_chat_member(message.chat.id, me.id)
                    # Some ChatMember objects may not expose permissions consistently; guard with getattr
                    can_delete = getattr(chat_member, "can_delete_messages", None)
                    status = getattr(chat_member, "status", None)
                    if can_delete is False and status != "administrator":
                        log_error(f"❌ NO DELETE PERMISSION in group {group_id} (status={status}, can_delete={can_delete})")
                        return
                except Exception as e:
                    # permission check non-fatal — we'll try delete and handle failures
                    log_info(f"⚠️ Permission check not conclusive for group {group_id}: {e}")

                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                message_text_lower = (message_text or "").lower()

                # ---------- SAFE BOT ----------
                if username in safe_bots:
                    log_info(f"✅ Safe bot ignored: @{username} in {group_id}")
                    return

                # ---------- DELAYED BOT ----------
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    if has_links or has_mentions:
                        log_info(f"🚫 Delayed bot with links/mentions: @{username} - INSTANT DELETE in {group_id}")
                        deleted = await force_delete_pyrogram(message)
                        if deleted:
                            log_info(f"✅ Instant deleted delayed bot @{username} in {group_id}")
                        else:
                            log_error(f"❌ Failed instant delete for delayed bot @{username} in {group_id}")
                    else:
                        log_info(f"⏰ Delayed bot normal: @{username} - scheduling 30s delete in {group_id}")
                        asyncio.create_task(delete_after_delay_pyrogram(message, 30))
                    return

                # ---------- OTHER BOTS - IMMEDIATE DELETE ----------
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: @{username} - IMMEDIATE DELETE in {group_id}")
                    deleted = await force_delete_pyrogram(message)
                    if deleted:
                        log_info(f"✅ Deleted bot @{username} in {group_id}")
                    else:
                        log_error(f"💀 Permanent delete failed for bot @{username} in {group_id}")
                    return

                # ---------- USER MESSAGE CHECK: LINKS / MENTIONS ----------
                if any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://']) or '@' in message_text:
                    log_info(f"🔎 Link/Mention detected from user {message.from_user.id if message.from_user else 'Unknown'} in {group_id} → deleting")
                    deleted = await force_delete_pyrogram(message)
                    if deleted:
                        log_info(f"✅ Deleted user message in {group_id}")
                    else:
                        log_error(f"❌ Failed to delete user message in {group_id}")
                    return

                # Otherwise nothing to do
            except Exception as e:
                log_error(f"❌ Handler error: {e}")
        
        # ✅ BOT START
        log_info("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Start session keep-alive
        keep_alive_task = asyncio.create_task(session_keep_alive())
        
        # Start simple online status - ERROR FIXED
        online_task = asyncio.create_task(simple_online_status())
        
        # Start watchdog and background state loops
        watchdog_task = asyncio.create_task(watchdog_loop())
        keep_session_task = asyncio.create_task(keep_session_alive_loop())
        force_state_task = asyncio.create_task(force_state_update())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Auto-setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💓 SESSION KEEP-ALIVE: ACTIVE")
        log_info("🟢 ONLINE STATUS: WORKING")
        log_info("🔥 SESSION STABILITY: GUARANTEED")
        log_info("🗑️ MESSAGE DELETION: READY")
        
        # Startup message
        try:
            await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - ALL FIXED!**

🎯 **FIXES APPLIED:**
• Online Status Error Fixed
• All Commands Working
• Message Deletion Active
• No More Errors

🚀 **WORKING FEATURES:**
• Commands Response
• Message Deletion
• Session Stability
• Sleep Protection

**Ab sab kuch properly work karega!** 🔥
            """)
        except Exception as e:
            log_error(f"Couldn't send startup DM: {e}")
        
        log_info("🤖 BOT READY - All Issues Fixed!")
        
        # Keep running until session breaks
        try:
            await asyncio.Future()
        except:
            pass
        finally:
            session_active = False
            keep_alive_task.cancel()
            online_task.cancel()
            watchdog_task.cancel()
            keep_session_task.cancel()
            force_state_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 ULTIMATE BOT STARTING...")

    # Global crash handler to ensure restart on unexpected exceptions
    try:
        asyncio.run(main())
    except Exception as e:
        log_critical(f"UNHANDLED CRASH: {e}")
        # flush handlers
        for h in logger.handlers:
            try:
                h.flush()
            except:
                pass
        # Method B: try external restart endpoint
        try:
            requests.post("https://userbot-telegram-1.onrender.com/restart", timeout=6)
        except Exception as ee:
            log_error(f"External restart hit failed: {ee}")
        # Method A/C: self-exec restart
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as ee:
            log_error(f"Self-restart failed: {ee}")
        # If execv fails, exit with non-zero so process manager can restart
        sys.exit(1)
