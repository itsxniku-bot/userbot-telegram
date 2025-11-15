print("🔥 ULTIMATE BOT STARTING - FINAL FIX...")

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

# 🔥 TELEGRAM BOT - FINAL FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - FINAL FIX...")
    
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
        # ULTIMATE DELETE FUNCTION - FINAL VERSION
        # -----------------------------
        async def ultimate_delete_final(message_obj):
            """
            FINAL DELETE FUNCTION - Works in both public and private groups
            """
            touch_activity()
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            
            log_info(f"🚀 DELETE ATTEMPT: chat={chat_id}, msg={message_id}")
            
            # METHOD 1: Direct delete_messages (MOST RELIABLE)
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ METHOD 1 SUCCESS: Direct API delete")
                return True
            except Exception as e1:
                log_info(f"ℹ️ METHOD 1 FAILED: {e1}")
            
            # METHOD 2: Try message object delete
            try:
                await message_obj.delete()
                log_info(f"✅ METHOD 2 SUCCESS: Object delete")
                return True
            except Exception as e2:
                log_info(f"ℹ️ METHOD 2 FAILED: {e2}")
            
            # METHOD 3: Wait and retry direct method
            await asyncio.sleep(1)
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ METHOD 3 SUCCESS: Retry worked")
                return True
            except Exception as e3:
                log_info(f"ℹ️ METHOD 3 FAILED: {e3}")
            
            log_info(f"💀 ALL DELETE METHODS FAILED - Bot may not have admin rights in private group")
            return False

        async def delete_after_delay_final(message_obj, seconds):
            await asyncio.sleep(seconds)
            await ultimate_delete_final(message_obj)

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
                    if keep_alive_count % 5 == 0:  # Reduce API calls
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
                    if loop_count % 15 == 0:  # Reduce frequency
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
                    if state_count % 20 == 0:  # Reduce frequency
                        await app.get_me()
                except Exception as e:
                    log_error(f"force_state_update error: {e}")
                await asyncio.sleep(10)

        # ✅ SMART ADMIN CHECK (WITHOUT FLOOD WAIT)
        async def smart_admin_check(chat_id):
            """Smart admin check that avoids flood wait"""
            try:
                # Convert to integer and validate
                chat_id_int = int(chat_id)
                
                # Skip invalid chat IDs
                if chat_id_int >= 0:  # User IDs are positive, group IDs are negative
                    log_info(f"⚠️ Skipping admin check for user ID: {chat_id}")
                    return False
                
                # Try to get chat info first
                try:
                    chat = await app.get_chat(chat_id_int)
                    log_info(f"ℹ️ Chat info: {chat.title if hasattr(chat, 'title') else 'Unknown'}")
                except Exception as chat_error:
                    log_info(f"⚠️ Could not get chat info for {chat_id}: {chat_error}")
                    return False
                
                # Now check admin status with delay to avoid flood
                await asyncio.sleep(2)
                chat_member = await app.get_chat_member(chat_id_int, (await app.get_me()).id)
                status = getattr(chat_member, "status", None)
                can_delete = getattr(chat_member, "can_delete_messages", False)
                
                if status == "administrator" and can_delete:
                    log_info(f"✅ Bot is ADMIN in group {chat_id} with delete rights")
                    return True
                else:
                    log_info(f"❌ Bot is NOT ADMIN in group {chat_id} (Status: {status}, Can Delete: {can_delete})")
                    return False
                    
            except Exception as e:
                if "FLOOD_WAIT" in str(e):
                    log_info(f"⏳ Flood wait during admin check for {chat_id}, skipping...")
                    return None  # Return None to indicate flood wait
                elif "PEER_ID_INVALID" in str(e):
                    log_info(f"⚠️ Invalid peer ID: {chat_id}, removing from allowed groups")
                    allowed_groups.discard(chat_id)
                    save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                    return False
                else:
                    log_error(f"❌ Admin check error for {chat_id}: {e}")
                    return False

        # ✅ ALL COMMANDS - WORKING VERSION
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 Received /start from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **ULTIMATE BOT STARTED!**\nFinal Fix Applied!")
                log_info("✅ /start command executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 Received /test from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing DELETE function...")
                await asyncio.sleep(2)
                success = await ultimate_delete_final(test_msg)
                if success:
                    await message.reply("✅ DELETE TEST PASSED! Bot can delete messages!")
                else:
                    await message.reply("❌ DELETE TEST FAILED! Bot may need admin rights in private groups.")
                log_info("✅ /test command executed")

        @app.on_message(filters.command("admincheck"))
        async def admin_check_command(client, message: Message):
            """Check if bot is admin in current group"""
            log_info(f"📩 Received /admincheck from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                is_admin_in_group = await smart_admin_check(str(message.chat.id))
                if is_admin_in_group:
                    await message.reply("✅ **BOT IS ADMIN** in this group!\nDelete function will work properly.")
                elif is_admin_in_group is None:
                    await message.reply("⚠️ **FLOOD WAIT** - Please try again in a few seconds.")
                else:
                    await message.reply("❌ **BOT IS NOT ADMIN** in this group!\nPlease make bot admin with delete message permission.")

        @app.on_message(filters.command("fixgroups"))
        async def fix_groups_command(client, message: Message):
            """Fix invalid group IDs"""
            log_info(f"📩 Received /fixgroups from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                # Remove invalid group IDs
                valid_groups = set()
                for group_id in allowed_groups:
                    try:
                        chat_id_int = int(group_id)
                        if chat_id_int < 0:  # Only negative IDs are groups
                            valid_groups.add(group_id)
                        else:
                            log_info(f"🗑️ Removing invalid group ID: {group_id}")
                    except:
                        log_info(f"🗑️ Removing invalid group ID: {group_id}")
                
                allowed_groups.clear()
                allowed_groups.update(valid_groups)
                save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                
                await message.reply(f"✅ **GROUPS FIXED!**\nValid groups: {len(valid_groups)}\nRemoved invalid group IDs.")
                log_info(f"✅ Groups fixed: {len(valid_groups)} valid groups remaining")

        # ---------------------------------------------------------
        # ULTIMATE DELETE HANDLER - FINAL VERSION
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def ultimate_delete_handler_final(client, message: Message):
            try:
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # SELF CHECK
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return

                # GET USER INFO
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower() if message.from_user else ""
                message_text = message.text or message.caption or ""
                message_text_lower = message_text.lower()

                log_info(f"🔍 Checking message from @{username} in {group_id}: {message_text[:50]}...")

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
                        await ultimate_delete_final(message)
                    else:
                        log_info(f"⏰ Delayed bot normal: @{username} - 30s delete")
                        asyncio.create_task(delete_after_delay_final(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: @{username} - INSTANT DELETE")
                    await ultimate_delete_final(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                if any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://']) or '@' in message_text:
                    log_info(f"🔗 User with links: {message.from_user.id} - DELETING")
                    await ultimate_delete_final(message)
                    return

            except Exception as e:
                log_error(f"❌ Handler error: {e}")
        
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
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Auto-setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💓 SESSION KEEP-ALIVE: ACTIVE")
        log_info("🟢 ONLINE STATUS: WORKING") 
        log_info("🔧 FINAL FIX: APPLIED")
        log_info("🗑️ MESSAGE DELETION: READY")
        
        # Smart admin status check with delays to avoid flood
        log_info("🔍 Smart admin status check starting...")
        valid_groups_count = 0
        for group_id in list(allowed_groups):  # Use list to avoid modification during iteration
            try:
                chat_id_int = int(group_id)
                if chat_id_int < 0:  # Only check negative IDs (groups)
                    await asyncio.sleep(3)  # Delay between checks to avoid flood
                    result = await smart_admin_check(group_id)
                    if result is not None:  # Skip if flood wait
                        valid_groups_count += 1
                else:
                    log_info(f"🗑️ Removing user ID from groups: {group_id}")
                    allowed_groups.discard(group_id)
            except ValueError:
                log_info(f"🗑️ Removing invalid group ID: {group_id}")
                allowed_groups.discard(group_id)
        
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        log_info(f"✅ Admin check completed: {valid_groups_count} valid groups")
        
        # Startup message
        try:
            await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - FINAL FIX!**

🎯 **PROBLEMS SOLVED:**
• Flood wait errors fixed
• Invalid group IDs removed  
• Smart admin checking
• Reduced API calls

🚀 **NEW COMMANDS:**
• `/admincheck` - Check admin status
• `/fixgroups` - Remove invalid groups
• `/test` - Test delete function

**Ab dono groups me properly work karega!** 🔥
            """)
        except Exception as e:
            log_error(f"Couldn't send startup DM: {e}")
        
        log_info("🤖 BOT READY - All Problems Solved!")
        
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
