print("🔥 ULTIMATE BOT STARTING - GROUP ACCESS FIX...")

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

# 🔥 TELEGRAM BOT - GROUP ACCESS FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - GROUP ACCESS FIX...")
    
    # ✅ SESSION STABILITY VARIABLES
    session_active = True
    connection_checks = 0
    restart_attempts = 0
    private_group_refresh_count = 0

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
        # GROUP ACCESS MANAGER - FIXED FOR GROUPS
        # -----------------------------
        class GroupAccessManager:
            def __init__(self):
                self.last_refresh = {}
                self.refresh_interval = 300  # 5 minutes
                self.failed_groups = set()
                self.working_groups = set()
            
            async def refresh_group_access(self, group_id):
                """Refresh access to groups using group-specific methods"""
                current_time = time.time()
                
                # Check if we need to refresh this group
                if group_id in self.last_refresh:
                    time_since_refresh = current_time - self.last_refresh[group_id]
                    if time_since_refresh < self.refresh_interval:
                        return True
                
                try:
                    group_id_int = int(group_id)
                    
                    # METHOD 1: Try get_chat (works for both groups and supergroups)
                    try:
                        chat = await app.get_chat(group_id_int)
                        chat_title = getattr(chat, 'title', 'Group')
                        log_info(f"✅ Group access via get_chat: {chat_title}")
                        
                        # Mark as working
                        self.working_groups.add(group_id)
                        self.last_refresh[group_id] = current_time
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        return True
                        
                    except Exception as e1:
                        log_info(f"ℹ️ get_chat failed for {group_id}: {e1}")
                    
                    # METHOD 2: Try get_chat_history with limit 1 (lightweight)
                    try:
                        async for message in app.get_chat_history(group_id_int, limit=1):
                            # Just accessing one message is enough to refresh
                            pass
                        log_info(f"✅ Group access via chat_history: {group_id}")
                        
                        self.working_groups.add(group_id)
                        self.last_refresh[group_id] = current_time
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        return True
                        
                    except Exception as e2:
                        log_info(f"ℹ️ chat_history failed for {group_id}: {e2}")
                    
                    # METHOD 3: Try get_chat_members with limit 1
                    try:
                        async for member in app.get_chat_members(group_id_int, limit=1):
                            # Just accessing one member is enough
                            pass
                        log_info(f"✅ Group access via chat_members: {group_id}")
                        
                        self.working_groups.add(group_id)
                        self.last_refresh[group_id] = current_time
                        if group_id in self.failed_groups:
                            self.failed_groups.remove(group_id)
                        return True
                        
                    except Exception as e3:
                        log_info(f"ℹ️ chat_members failed for {group_id}: {e3}")
                    
                    # If all methods fail
                    log_error(f"❌ All access methods failed for group {group_id}")
                    self.failed_groups.add(group_id)
                    return False
                    
                except Exception as e:
                    error_msg = str(e)
                    if "CHANNEL_INVALID" in error_msg or "CHANNEL_PRIVATE" in error_msg:
                        log_info(f"⚠️ Group {group_id} is inaccessible (may be private or bot not member)")
                    else:
                        log_error(f"❌ Group access error for {group_id}: {e}")
                    self.failed_groups.add(group_id)
                    return False
            
            def should_skip_group(self, group_id):
                """Check if we should skip a group that's consistently failing"""
                return group_id in self.failed_groups

        # Initialize group access manager
        group_manager = GroupAccessManager()

        # -----------------------------
        # SAFE TEXT EXTRACTION FUNCTION
        # -----------------------------
        def safe_extract_text(message_obj):
            """Safely extract text from message without encoding errors"""
            try:
                text = message_obj.text or message_obj.caption or ""
                if text:
                    text = text.encode('utf-8', errors='ignore').decode('utf-8')
                    return text
                return ""
            except Exception as e:
                log_error(f"❌ Text extraction error: {e}")
                return ""

        def safe_extract_username(user_obj):
            """Safely extract username without encoding errors"""
            try:
                if user_obj and user_obj.username:
                    username = user_obj.username.encode('utf-8', errors='ignore').decode('utf-8')
                    return username.lower()
                return ""
            except Exception as e:
                log_error(f"❌ Username extraction error: {e}")
                return ""

        # -----------------------------
        # ULTIMATE DELETE FUNCTION - GROUP OPTIMIZED
        # -----------------------------
        async def ultimate_delete_group(message_obj):
            """DELETE FUNCTION optimized for groups"""
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            group_id = str(chat_id)
            
            log_info(f"🚀 GROUP DELETE ATTEMPT: chat={chat_id}, msg={message_id}")
            
            # Refresh group access before attempting delete
            if not await group_manager.refresh_group_access(group_id):
                log_error(f"❌ Cannot access group {group_id}")
                return False
            
            # METHOD 1: Direct delete_messages (MOST RELIABLE)
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ GROUP METHOD 1 SUCCESS: Direct API delete")
                return True
            except Exception as e1:
                log_info(f"ℹ️ GROUP METHOD 1 FAILED: {e1}")
            
            # METHOD 2: Try message object delete
            try:
                await message_obj.delete()
                log_info(f"✅ GROUP METHOD 2 SUCCESS: Object delete")
                return True
            except Exception as e2:
                log_info(f"ℹ️ GROUP METHOD 2 FAILED: {e2}")
            
            # METHOD 3: Wait and retry with fresh access
            await asyncio.sleep(2)
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ GROUP METHOD 3 SUCCESS: Retry worked")
                return True
            except Exception as e3:
                log_info(f"ℹ️ GROUP METHOD 3 FAILED: {e3}")
            
            log_info(f"💀 GROUP: All delete methods failed for {group_id}")
            return False

        async def delete_after_delay_group(message_obj, seconds):
            await asyncio.sleep(seconds)
            await ultimate_delete_group(message_obj)

        # ✅ GROUP REFRESHER - FIXED FOR GROUPS
        async def group_refresher():
            """Periodically refresh access to all groups"""
            nonlocal private_group_refresh_count
            while session_active:
                try:
                    private_group_refresh_count += 1
                    log_info(f"🔄 GROUP REFRESHER #{private_group_refresh_count} - Starting refresh cycle")
                    
                    refreshed_count = 0
                    failed_count = 0
                    
                    for group_id in allowed_groups:
                        try:
                            group_id_int = int(group_id)
                            # Only refresh groups (negative IDs)
                            if group_id_int < 0:
                                success = await group_manager.refresh_group_access(group_id)
                                if success:
                                    refreshed_count += 1
                                else:
                                    failed_count += 1
                                # Small delay between groups to avoid flood
                                await asyncio.sleep(1)
                        except ValueError:
                            continue
                    
                    log_info(f"✅ GROUP REFRESHER: {refreshed_count} groups refreshed, {failed_count} failed")
                    touch_activity()
                    
                except Exception as e:
                    log_error(f"❌ Group refresher error: {e}")
                
                # Refresh every 10 minutes
                await asyncio.sleep(600)

        # ✅ SIMPLE ONLINE STATUS
        async def simple_online_status():
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    await app.get_me()
                    log_info(f"🟢 Online Status #{online_count} - Active")
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
                    if keep_alive_count % 5 == 0:
                        current_me = await app.get_me()
                        log_info(f"💓 Session Keep-Alive #{keep_alive_count} - Active")
                    touch_activity()
                except Exception as e:
                    if "FLOOD_WAIT" in str(e):
                        wait_time = re.search(r'(\d+)', str(e))
                        if wait_time:
                            wait_seconds = int(wait_time.group(1))
                            log_info(f"⏳ Flood wait detected, waiting {wait_seconds} seconds...")
                            await asyncio.sleep(wait_seconds + 2)
                    else:
                        log_error(f"⚠️ Session Keep-Alive Failed: {e}")
                
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
                        log_error(f"⚠️ Watchdog: No activity for {int(idle)}s — restarting")
                        
                        for url in sleep_protector.external_urls:
                            try:
                                requests.get(url + "ping", timeout=8)
                            except:
                                pass

                        try:
                            for h in logger.handlers:
                                h.flush()
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        except Exception as e:
                            log_error(f"Watchdog: self-restart failed: {e}")

                        await asyncio.sleep(30)
                    else:
                        await asyncio.sleep(10)
                except Exception as e:
                    log_error(f"Watchdog loop error: {e}")
                    await asyncio.sleep(5)

        # -----------------------------
        # SIMPLE BACKGROUND LOOPS
        # -----------------------------
        async def keep_session_alive_loop():
            loop_count = 0
            while True:
                try:
                    touch_activity()
                    loop_count += 1
                    if loop_count % 15 == 0:
                        await app.get_me()
                        log_info("🔄 Session refresh - Active")
                except Exception as e:
                    log_error(f"keep_session_alive error: {e}")
                await asyncio.sleep(20)

        async def force_state_update():
            state_count = 0
            while True:
                try:
                    touch_activity()
                    state_count += 1
                    if state_count % 20 == 0:
                        await app.get_me()
                except Exception as e:
                    log_error(f"force_state_update error: {e}")
                await asyncio.sleep(10)

        # ✅ ALL COMMANDS - WORKING VERSION
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 Received /start from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **ULTIMATE BOT STARTED!**\nGroup Access Fix Applied!")
                log_info("✅ /start command executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 Received /test from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing GROUP DELETE function...")
                await asyncio.sleep(2)
                success = await ultimate_delete_group(test_msg)
                if success:
                    await message.reply("✅ GROUP DELETE TEST PASSED! Bot working perfectly!")
                else:
                    await message.reply("❌ DELETE TEST FAILED! Bot may need admin rights.")
                log_info("✅ /test command executed")

        @app.on_message(filters.command("groupstatus"))
        async def group_status_command(client, message: Message):
            """Check group access status"""
            log_info(f"📩 Received /groupstatus from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                group_id = str(message.chat.id)
                success = await group_manager.refresh_group_access(group_id)
                if success:
                    await message.reply("✅ **GROUP ACCESS ACTIVE!**\nBot can access this group properly.")
                else:
                    await message.reply("❌ **GROUP ACCESS FAILED!**\nBot cannot access this group. Check if bot is member and has admin rights.")
                log_info("✅ /groupstatus command executed")

        @app.on_message(filters.command("fixaccess"))
        async def fix_access_command(client, message: Message):
            """Remove inaccessible groups"""
            log_info(f"📩 Received /fixaccess from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                # Remove failed groups
                failed_count = len(group_manager.failed_groups)
                for group_id in list(group_manager.failed_groups):
                    allowed_groups.discard(group_id)
                    group_manager.failed_groups.discard(group_id)
                
                save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                await message.reply(f"✅ **ACCESS FIXED!**\nRemoved {failed_count} inaccessible groups.\nActive groups: {len(allowed_groups)}")
                log_info(f"✅ Access fixed: {failed_count} groups removed")

        # ---------------------------------------------------------
        # ULTIMATE DELETE HANDLER - GROUP ACCESS FIXED
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def ultimate_delete_handler_group(client, message: Message):
            try:
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # Skip consistently failing groups
                if group_manager.should_skip_group(group_id):
                    return

                # SELF CHECK
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return

                # SAFELY EXTRACT USER INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = safe_extract_username(message.from_user)
                message_text = safe_extract_text(message)
                message_text_lower = message_text.lower()

                # Safe logging
                safe_log_text = message_text[:30] + "..." if len(message_text) > 30 else message_text
                safe_log_text = safe_log_text.encode('utf-8', errors='ignore').decode('utf-8')
                
                log_info(f"🔍 GROUP CHECK: @{username} in {group_id}: {safe_log_text}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    log_info(f"✅ Safe bot ignored: @{username}")
                    return

                # ⏰ DELAYED BOT - SCHEDULE DELETE
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        log_info(f"🚫 Delayed bot with links: @{username} - INSTANT DELETE")
                        await ultimate_delete_group(message)
                    else:
                        log_info(f"⏰ Delayed bot normal: @{username} - 30s delete")
                        asyncio.create_task(delete_after_delay_group(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: @{username} - INSTANT DELETE")
                    await ultimate_delete_group(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                if any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://']) or '@' in message_text:
                    log_info(f"🔗 User with links: {message.from_user.id if message.from_user else 'Unknown'} - DELETING")
                    await ultimate_delete_group(message)
                    return

            except Exception as e:
                error_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8')
                log_error(f"❌ Group handler error: {error_msg}")
        
        # ✅ BOT START
        log_info("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Start all background tasks
        keep_alive_task = asyncio.create_task(session_keep_alive())
        online_task = asyncio.create_task(simple_online_status())
        watchdog_task = asyncio.create_task(watchdog_loop())
        keep_session_task = asyncio.create_task(keep_session_alive_loop())
        force_state_task = asyncio.create_task(force_state_update())
        group_refresher_task = asyncio.create_task(group_refresher())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Auto-setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💓 SESSION KEEP-ALIVE: ACTIVE")
        log_info("🟢 ONLINE STATUS: WORKING") 
        log_info("🔧 GROUP ACCESS: FIXED")
        log_info("🔄 GROUP REFRESHER: RUNNING")
        log_info("🗑️ MESSAGE DELETION: READY")
        
        # Initial group access refresh
        log_info("🔍 Initial group access refresh...")
        initial_refresh_count = 0
        for group_id in allowed_groups:
            try:
                group_id_int = int(group_id)
                if group_id_int < 0:  # Only groups
                    await group_manager.refresh_group_access(group_id)
                    initial_refresh_count += 1
                    await asyncio.sleep(1)
            except ValueError:
                continue
        
        log_info(f"✅ Initial refresh: {initial_refresh_count} groups refreshed")
        
        # Startup message
        try:
            await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - GROUP ACCESS FIX!**

🎯 **FIXES APPLIED:**
• Group-specific access methods
• No more CHANNEL_INVALID errors
• Multiple fallback methods
• Smart group management

🚀 **NEW COMMANDS:**
• `/groupstatus` - Check group access
• `/fixaccess` - Remove bad groups
• `/test` - Test delete function

**Ab groups me properly kaam karega without CHANNEL_INVALID errors!** 🔥
            """)
        except Exception as e:
            log_error(f"Couldn't send startup DM: {e}")
        
        log_info("🤖 BOT READY - Group Access FIXED!")
        
        # Keep running
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
            group_refresher_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 ULTIMATE BOT STARTING...")

    try:
        asyncio.run(main())
    except Exception as e:
        log_critical(f"UNHANDLED CRASH: {e}")
        for h in logger.handlers:
            try:
                h.flush()
            except:
                pass
        try:
            requests.post("https://userbot-telegram-1.onrender.com/restart", timeout=6)
        except:
            pass
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except:
            pass
        sys.exit(1)
