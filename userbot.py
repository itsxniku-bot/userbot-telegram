print("🔥 ULTIMATE BOT STARTING - STRONG GROUP ACCESS FIX...")

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

# 🔥 TELEGRAM BOT - STRONG GROUP ACCESS FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - STRONG GROUP ACCESS FIX...")
    
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
        # STRONG GROUP ACCESS MANAGER
        # -----------------------------
        class StrongGroupAccess:
            def __init__(self):
                self.last_access_time = {}
                self.access_count = {}
                self.failed_groups = set()
                self.working_groups = set()
            
            async def strong_group_access(self, group_id):
                """STRONG group access with multiple fallback methods"""
                try:
                    group_id_int = int(group_id)
                    
                    # Update access time
                    self.last_access_time[group_id] = time.time()
                    self.access_count[group_id] = self.access_count.get(group_id, 0) + 1
                    
                    # METHOD 1: get_chat - Most reliable for groups
                    try:
                        chat = await app.get_chat(group_id_int)
                        chat_title = getattr(chat, 'title', 'Group')
                        log_info(f"✅ STRONG ACCESS [get_chat]: {chat_title}")
                        self.working_groups.add(group_id)
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        return True
                    except Exception as e1:
                        log_info(f"ℹ️ get_chat failed: {e1}")
                    
                    # METHOD 2: get_chat_members_count - Lightweight
                    try:
                        count = await app.get_chat_members_count(group_id_int)
                        log_info(f"✅ STRONG ACCESS [members_count]: {count} members")
                        self.working_groups.add(group_id)
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        return True
                    except Exception as e2:
                        log_info(f"ℹ️ members_count failed: {e2}")
                    
                    # METHOD 3: get_chat_history - Single message access
                    try:
                        async for message in app.get_chat_history(group_id_int, limit=1):
                            # Just accessing one message is enough
                            pass
                        log_info(f"✅ STRONG ACCESS [chat_history]")
                        self.working_groups.add(group_id)
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        return True
                    except Exception as e3:
                        log_info(f"ℹ️ chat_history failed: {e3}")
                    
                    # METHOD 4: send_chat_action - Very lightweight
                    try:
                        await app.send_chat_action(group_id_int, "typing")
                        log_info(f"✅ STRONG ACCESS [chat_action]")
                        self.working_groups.add(group_id)
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        return True
                    except Exception as e4:
                        log_info(f"ℹ️ chat_action failed: {e4}")
                    
                    # If all methods fail
                    log_error(f"❌ STRONG ACCESS FAILED for group {group_id}")
                    self.failed_groups.add(group_id)
                    return False
                    
                except Exception as e:
                    log_error(f"❌ Strong access error for {group_id}: {e}")
                    self.failed_groups.add(group_id)
                    return False
            
            def get_group_status(self, group_id):
                """Get detailed status of a group"""
                status = {
                    "access_count": self.access_count.get(group_id, 0),
                    "last_access": self.last_access_time.get(group_id, 0),
                    "is_working": group_id in self.working_groups,
                    "is_failed": group_id in self.failed_groups
                }
                return status

        # Initialize strong group access
        group_access = StrongGroupAccess()

        # -----------------------------
        # POWERFUL DELETE FUNCTION
        # -----------------------------
        async def powerful_delete(message_obj):
            """
            POWERFUL DELETE with strong group access
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            group_id = str(chat_id)
            
            # STRONG ACCESS CHECK before delete
            if not await group_access.strong_group_access(group_id):
                log_error(f"❌ Cannot access group {group_id} for delete")
                return False
            
            log_info(f"💪 POWERFUL DELETE: message {message_id} from {group_id}")
            
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ POWER DELETE SUCCESS: {message_id}")
                return True
            except Exception as e:
                log_error(f"❌ POWER DELETE FAILED: {e}")
                return False

        async def delete_after_delay_powerful(message_obj, seconds):
            await asyncio.sleep(seconds)
            await powerful_delete(message_obj)

        # ✅ STRONG GROUP SESSION MAINTAINER
        async def strong_group_maintainer():
            """Maintain STRONG group session 24/7"""
            refresh_count = 0
            while session_active:
                try:
                    refresh_count += 1
                    working_count = 0
                    failed_count = 0
                    
                    # STRONG ACCESS to all groups
                    for group_id in allowed_groups:
                        success = await group_access.strong_group_access(group_id)
                        if success:
                            working_count += 1
                        else:
                            failed_count += 1
                        await asyncio.sleep(2)  # Delay between groups
                    
                    log_info(f"🛡️ STRONG REFRESH #{refresh_count}: {working_count} working, {failed_count} failed")
                    touch_activity()
                    
                except Exception as e:
                    log_error(f"❌ Strong maintainer error: {e}")
                
                # Refresh every 5 minutes
                await asyncio.sleep(300)

        # ✅ SIMPLE ONLINE STATUS
        async def simple_online_status():
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    await app.get_me()
                    log_info(f"🟢 Online #{online_count} - STRONG ACCESS")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Online Status Failed: {e}")
                await asyncio.sleep(120)

        # ✅ SESSION KEEP-ALIVE
        async def session_keep_alive():
            nonlocal connection_checks, session_active
            keep_alive_count = 0
            
            while session_active:
                keep_alive_count += 1
                connection_checks += 1
                
                try:
                    if keep_alive_count % 3 == 0:
                        await app.get_me()
                        log_info(f"💓 Keep-Alive #{keep_alive_count} - STRONG")
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                
                await asyncio.sleep(180)

        # -------------------------
        # WATCHDOG / AUTO-RESTART
        # -------------------------
        async def watchdog_loop():
            nonlocal restart_attempts
            while True:
                try:
                    idle = time.time() - last_activity
                    if idle > 300:
                        restart_attempts += 1
                        log_error(f"⚠️ Watchdog: Restarting - No activity for {int(idle)}s")
                        
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
                    await asyncio.sleep(5)

        # ✅ ALL COMMANDS - WORKING VERSION
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **BOT STARTED!**\nStrong Group Access Applied!")
                log_info("✅ /start executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 /test from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing STRONG DELETE...")
                await asyncio.sleep(2)
                success = await powerful_delete(test_msg)
                if success:
                    await message.reply("✅ **STRONG DELETE WORKING!**")
                else:
                    await message.reply("❌ DELETE FAILED! Check group access.")
                log_info("✅ /test executed")

        @app.on_message(filters.command("strongstatus"))
        async def strong_status_command(client, message: Message):
            """Check strong group access status"""
            log_info(f"📩 /strongstatus from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                group_id = str(message.chat.id)
                status = group_access.get_group_status(group_id)
                access_time = time.time() - status["last_access"] if status["last_access"] > 0 else 999
                
                status_text = f"""
🛡️ **STRONG GROUP STATUS**

**Group ID:** `{group_id}`
**Access Count:** `{status['access_count']}`
**Last Access:** `{int(access_time)}s ago`
**Status:** `{'✅ WORKING' if status['is_working'] else '❌ FAILED'}`

**Strong Access:** `🛡️ ACTIVE`
                """
                await message.reply(status_text)
                log_info("✅ /strongstatus executed")

        @app.on_message(filters.command("refreshall"))
        async def refresh_all_command(client, message: Message):
            """Manually refresh all groups"""
            log_info(f"📩 /refreshall from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                working_count = 0
                for group_id in allowed_groups:
                    if await group_access.strong_group_access(group_id):
                        working_count += 1
                    await asyncio.sleep(1)
                
                await message.reply(f"✅ **STRONG REFRESH COMPLETE!**\n{working_count}/{len(allowed_groups)} groups active")
                log_info("✅ /refreshall executed")

        # ---------------------------------------------------------
        # STRONG GROUP DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def strong_group_handler(client, message: Message):
            try:
                # UPDATE ACTIVITY
                touch_activity()
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # STRONG ACCESS CHECK
                if not await group_access.strong_group_access(group_id):
                    log_error(f"❌ Strong access failed for {group_id}")
                    return

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

                # LOG EVERY MESSAGE WITH STRONG ACCESS
                log_info(f"🛡️ STRONG MESSAGE: @{username} (bot: {is_bot})")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    log_info(f"✅ Safe bot: @{username}")
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        log_info(f"🚫 Delayed bot with links: POWER DELETE NOW")
                        await powerful_delete(message)
                    else:
                        log_info(f"⏰ Delayed bot: POWER DELETE IN 30s")
                        asyncio.create_task(delete_after_delay_powerful(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: POWER DELETE NOW")
                    await powerful_delete(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    log_info(f"🔗 User with links: POWER DELETE NOW")
                    await powerful_delete(message)
                    return

                log_info(f"ℹ️ Normal message - Strong access maintained")

            except Exception as e:
                log_error(f"❌ Strong handler error: {e}")
                touch_activity()
        
        # ✅ BOT START
        log_info("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Start background tasks - STRONG MAINTAINER IS CRITICAL
        keep_alive_task = asyncio.create_task(session_keep_alive())
        online_task = asyncio.create_task(simple_online_status())
        watchdog_task = asyncio.create_task(watchdog_loop())
        strong_maintainer_task = asyncio.create_task(strong_group_maintainer())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💓 Keep-Alive: ACTIVE")
        log_info("🟢 Online: WORKING") 
        log_info("🛡️ Strong Group Access: RUNNING")
        log_info("💪 Powerful Delete: READY")
        
        # Initial STRONG access test
        log_info("🔍 Initial STRONG group access...")
        working_count = 0
        for group_id in allowed_groups:
            if await group_access.strong_group_access(group_id):
                working_count += 1
            await asyncio.sleep(2)
        
        log_info(f"✅ Initial STRONG access: {working_count}/{len(allowed_groups)} groups")
        
        # Startup message
        try:
            await app.send_message("me", """
✅ **BOT STARTED - STRONG GROUP ACCESS!**

🎯 **STRONG FEATURES:**
• 4-Layer Group Access System
• Strong Session Maintenance
• Powerful Delete Function
• 24/7 Access Guarantee

🚀 **COMMANDS:**
• `/test` - Test strong delete
• `/strongstatus` - Check access status
• `/refreshall` - Refresh all groups

**Ab group access strong hai! Online/offline dono me kaam karega!** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Strong Group Access Applied!")
        
        # Keep running
        try:
            while session_active:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_active = False
            keep_alive_task.cancel()
            online_task.cancel()
            watchdog_task.cancel()
            strong_maintainer_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - STRONG ACCESS...")

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
