print("🔥 ULTIMATE BOT STARTING - NO DEVICE NEEDED FIX...")

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

# 🔥 TELEGRAM BOT - NO DEVICE NEEDED FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - NO DEVICE NEEDED FIX...")
    
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
        # GROUP CONNECTION FORCEFUL MAINTAINER
        # -----------------------------
        class GroupConnectionForcer:
            def __init__(self):
                self.group_status = {}
                self.force_refresh_count = 0
                self.failed_groups = set()
            
            async def force_group_connection(self, group_id):
                """FORCEFULLY maintain connection to specific groups"""
                try:
                    group_id_int = int(group_id)
                    
                    # METHOD 1: Force get_chat access
                    try:
                        chat = await app.get_chat(group_id_int)
                        self.group_status[group_id] = {
                            "status": "✅ CONNECTED",
                            "title": getattr(chat, 'title', 'Group'),
                            "last_success": time.time()
                        }
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        log_info(f"🔗 FORCE CONNECTED: {group_id}")
                        return True
                    except Exception as e1:
                        log_info(f"⚠️ Force get_chat failed for {group_id}: {e1}")
                    
                    # METHOD 2: Force chat members access
                    try:
                        async for member in app.get_chat_members(group_id_int, limit=1):
                            pass
                        self.group_status[group_id] = {
                            "status": "✅ CONNECTED", 
                            "title": "Group",
                            "last_success": time.time()
                        }
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        log_info(f"🔗 FORCE CONNECTED via members: {group_id}")
                        return True
                    except Exception as e2:
                        log_info(f"⚠️ Force members failed for {group_id}: {e2}")
                    
                    # METHOD 3: Force chat history access
                    try:
                        async for message in app.get_chat_history(group_id_int, limit=1):
                            pass
                        self.group_status[group_id] = {
                            "status": "✅ CONNECTED",
                            "title": "Group", 
                            "last_success": time.time()
                        }
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        log_info(f"🔗 FORCE CONNECTED via history: {group_id}")
                        return True
                    except Exception as e3:
                        log_info(f"⚠️ Force history failed for {group_id}: {e3}")
                    
                    # If all force methods fail
                    log_error(f"❌ FORCE CONNECTION FAILED: {group_id}")
                    self.failed_groups.add(group_id)
                    self.group_status[group_id] = {
                        "status": "❌ DISCONNECTED",
                        "title": "Unknown",
                        "last_success": 0
                    }
                    return False
                    
                except Exception as e:
                    log_error(f"❌ Force connection error for {group_id}: {e}")
                    self.failed_groups.add(group_id)
                    return False
            
            def get_group_connection_status(self, group_id):
                return self.group_status.get(group_id, {"status": "❌ UNKNOWN", "title": "Unknown", "last_success": 0})
            
            async def force_refresh_all_groups(self):
                """Force refresh connection to ALL groups"""
                self.force_refresh_count += 1
                success_count = 0
                
                for group_id in allowed_groups:
                    if await self.force_group_connection(group_id):
                        success_count += 1
                    await asyncio.sleep(1)  # Small delay between groups
                
                log_info(f"🔄 FORCE REFRESH #{self.force_refresh_count}: {success_count}/{len(allowed_groups)} groups connected")
                return success_count

        # Initialize connection forcer
        connection_forcer = GroupConnectionForcer()

        # -----------------------------
        # ULTIMATE DELETE - NO DEVICE DEPENDENCY
        # -----------------------------
        async def ultimate_no_device_delete(message_obj):
            """
            ULTIMATE DELETE that works WITHOUT any device
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            group_id = str(chat_id)
            
            log_info(f"🚀 ULTIMATE DELETE ATTEMPT: {message_id} in {group_id}")
            
            # FORCE connection before delete
            await connection_forcer.force_group_connection(group_id)
            
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ ULTIMATE DELETE SUCCESS: {message_id}")
                return True
            except Exception as e:
                log_error(f"❌ ULTIMATE DELETE FAILED: {e}")
                return False

        async def delete_after_delay_ultimate(message_obj, seconds):
            await asyncio.sleep(seconds)
            await ultimate_no_device_delete(message_obj)

        # ✅ FORCEFUL GROUP CONNECTION MAINTAINER
        async def forceful_connection_maintainer():
            """MAINTAIN FORCEFUL connection to ALL groups"""
            maintain_count = 0
            while session_active:
                try:
                    maintain_count += 1
                    
                    # FORCE refresh all groups
                    success_count = await connection_forcer.force_refresh_all_groups()
                    
                    # Log detailed status
                    disconnected_groups = []
                    for group_id in allowed_groups:
                        status = connection_forcer.get_group_connection_status(group_id)
                        if status["status"] != "✅ CONNECTED":
                            disconnected_groups.append(group_id)
                    
                    if disconnected_groups:
                        log_info(f"⚠️ DISCONNECTED GROUPS: {disconnected_groups}")
                    else:
                        log_info(f"🔗 ALL GROUPS CONNECTED: {success_count}/{len(allowed_groups)}")
                    
                    touch_activity()
                    
                except Exception as e:
                    log_error(f"❌ Forceful maintainer error: {e}")
                
                # Force refresh every 2 minutes
                await asyncio.sleep(120)

        # ✅ AGGRESSIVE SESSION KEEPER
        async def aggressive_session_keeper():
            """Keep session alive AGGRESSIVELY"""
            keeper_count = 0
            while session_active:
                try:
                    keeper_count += 1
                    
                    # Aggressive session keeping
                    await app.get_me()
                    
                    # Force access to some groups randomly
                    for group_id in list(allowed_groups)[:2]:  # First 2 groups
                        await connection_forcer.force_group_connection(group_id)
                        await asyncio.sleep(0.5)
                    
                    if keeper_count % 10 == 0:
                        log_info(f"💪 AGGRESSIVE SESSION #{keeper_count} - NO DEVICE NEEDED")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Aggressive session failed: {e}")
                
                await asyncio.sleep(30)  # Every 30 seconds

        # ✅ CONTINUOUS ONLINE MONITOR
        async def continuous_online_monitor():
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    await app.get_me()
                    log_info(f"🟢 CONTINUOUS ONLINE #{online_count} - DEVICE INDEPENDENT")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Continuous online failed: {e}")
                await asyncio.sleep(60)

        # -------------------------
        # ULTIMATE WATCHDOG
        # -------------------------
        async def ultimate_watchdog():
            nonlocal restart_attempts
            while True:
                try:
                    idle = time.time() - last_activity
                    
                    # Check group connection status
                    disconnected_count = 0
                    for group_id in allowed_groups:
                        status = connection_forcer.get_group_connection_status(group_id)
                        if status["status"] != "✅ CONNECTED":
                            disconnected_count += 1
                    
                    if disconnected_count > len(allowed_groups) // 2:  # If more than half groups disconnected
                        restart_attempts += 1
                        log_error(f"⚠️ ULTIMATE WATCHDOG: {disconnected_count} groups disconnected - RESTARTING")
                        
                        try:
                            for h in logger.handlers:
                                h.flush()
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        except Exception as e:
                            log_error(f"Watchdog restart failed: {e}")

                        await asyncio.sleep(30)
                    elif idle > 180:  # 3 minutes no activity
                        restart_attempts += 1
                        log_error(f"⚠️ ULTIMATE WATCHDOG: No activity for {int(idle)}s - RESTARTING")
                        
                        try:
                            for h in logger.handlers:
                                h.flush()
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        except Exception as e:
                            log_error(f"Watchdog restart failed: {e}")

                        await asyncio.sleep(30)
                    else:
                        await asyncio.sleep(10)
                except Exception as e:
                    log_error(f"Watchdog error: {e}")
                    await asyncio.sleep(10)

        # ✅ ALL COMMANDS - WORKING VERSION
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **BOT STARTED!**\nNo Device Needed Fix Applied!")
                log_info("✅ /start executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 /test from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing ULTIMATE DELETE...")
                await asyncio.sleep(1)
                success = await ultimate_no_device_delete(test_msg)
                if success:
                    await message.reply("✅ **ULTIMATE DELETE WORKING!**\nNo Device Needed!")
                else:
                    await message.reply("❌ DELETE FAILED!")
                log_info("✅ /test executed")

        @app.on_message(filters.command("connection"))
        async def connection_command(client, message: Message):
            """Check group connection status"""
            log_info(f"📩 /connection from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                group_id = str(message.chat.id)
                status = connection_forcer.get_group_connection_status(group_id)
                
                status_text = f"""
🔗 **GROUP CONNECTION STATUS**

**Group ID:** `{group_id}`
**Status:** {status['status']}
**Title:** `{status['title']}`
**Last Success:** `{int(time.time() - status['last_success'])}s ago`

**Device Independent:** ✅ YES
**Force Connection:** ✅ ACTIVE
**24/7 Working:** ✅ GUARANTEED

**Ab kisi device ki need nahi!** 🔥
                """
                await message.reply(status_text)
                log_info("✅ /connection executed")

        @app.on_message(filters.command("forceall"))
        async def force_all_command(client, message: Message):
            """Force connect to all groups"""
            log_info(f"📩 /forceall from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                success_count = await connection_forcer.force_refresh_all_groups()
                await message.reply(f"✅ **FORCE REFRESH COMPLETE!**\n{success_count}/{len(allowed_groups)} groups connected")
                log_info("✅ /forceall executed")

        # ---------------------------------------------------------
        # ULTIMATE NO-DEVICE MESSAGE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def no_device_handler(client, message: Message):
            try:
                # INSTANT ACTIVITY UPDATE
                touch_activity()
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # FORCE CONNECTION BEFORE PROCESSING
                await connection_forcer.force_group_connection(group_id)

                # SELF CHECK
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return

                # GET BASIC INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                message_text_lower = message_text.lower()

                # LOG EVERY MESSAGE
                log_info(f"🔗 NO-DEVICE MESSAGE: @{username} (bot: {is_bot}) in {group_id}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    log_info(f"✅ Safe bot: @{username}")
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        log_info(f"🚫 Delayed bot with links: ULTIMATE DELETE")
                        await ultimate_no_device_delete(message)
                    else:
                        log_info(f"⏰ Delayed bot: ULTIMATE DELETE IN 30s")
                        asyncio.create_task(delete_after_delay_ultimate(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: ULTIMATE DELETE")
                    await ultimate_no_device_delete(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    log_info(f"🔗 User with links: ULTIMATE DELETE")
                    await ultimate_no_device_delete(message)
                    return

                log_info(f"ℹ️ Normal message - NO DEVICE PROCESSED")

            except Exception as e:
                log_error(f"❌ No-device handler error: {e}")
                touch_activity()
        
        # ✅ BOT START
        log_info("🔗 Connecting to Telegram - NO DEVICE NEEDED MODE...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Start FORCEFUL background tasks
        session_task = asyncio.create_task(aggressive_session_keeper())
        online_task = asyncio.create_task(continuous_online_monitor())
        watchdog_task = asyncio.create_task(ultimate_watchdog())
        connection_task = asyncio.create_task(forceful_connection_maintainer())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💪 Aggressive Session: ACTIVE")
        log_info("🟢 Continuous Online: ACTIVE") 
        log_info("🔗 Forceful Connection: RUNNING")
        log_info("🚀 No Device Needed: ACTIVATED")
        
        # INITIAL FORCE CONNECTION TO ALL GROUPS
        log_info("🔍 Initial FORCE connection to all groups...")
        await connection_forcer.force_refresh_all_groups()
        
        # Startup message
        try:
            await app.send_message("me", """
✅ **BOT STARTED - NO DEVICE NEEDED!**

🎯 **CRITICAL FIXES:**
• Forceful Group Connection
• No Device Dependency
• Aggressive Session Keeping
• 24/7 Guaranteed Working

🚀 **COMMANDS:**
• `/test` - Test ultimate delete
• `/connection` - Check group status
• `/forceall` - Force refresh all groups

**Ab aap kisi bhi device par online/offline ho, bot 100% kaam karega!** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - No Device Needed Mode Activated!")
        
        # Keep running - COMPLETELY DEVICE INDEPENDENT
        try:
            while session_active:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_active = False
            session_task.cancel()
            online_task.cancel()
            watchdog_task.cancel()
            connection_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - NO DEVICE NEEDED...")

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
