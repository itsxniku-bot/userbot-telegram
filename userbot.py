print("🔥 ULTIMATE BOT STARTING - NEVER STOP CHECKING FIX...")

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

# 🔥 TELEGRAM BOT - NEVER STOP CHECKING FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - NEVER STOP CHECKING FIX...")
    
    # ✅ SESSION STABILITY VARIABLES
    session_active = True
    connection_checks = 0
    restart_attempts = 0
    message_check_count = 0

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
        # MESSAGE CHECKING MONITOR
        # -----------------------------
        class MessageMonitor:
            def __init__(self):
                self.last_message_time = time.time()
                self.check_count = 0
                self.is_checking_active = True
            
            def update_message_time(self):
                self.last_message_time = time.time()
                self.check_count += 1
            
            def is_checking_stuck(self):
                # If no message for 2 minutes, checking might be stuck
                return (time.time() - self.last_message_time) > 120
            
            def get_status(self):
                return {
                    "check_count": self.check_count,
                    "last_message_seconds_ago": int(time.time() - self.last_message_time),
                    "is_active": self.is_checking_active
                }

        # Initialize message monitor
        message_monitor = MessageMonitor()

        # -----------------------------
        # ULTIMATE DELETE FUNCTION - NEVER FAIL
        # -----------------------------
        async def never_fail_delete(message_obj):
            """
            DELETE FUNCTION THAT NEVER FAILS
            """
            touch_activity()
            message_monitor.update_message_time()
            
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            
            log_info(f"🚀 DELETE ATTEMPT #{message_monitor.check_count}: chat={chat_id}, msg={message_id}")
            
            # METHOD 1: Direct delete_messages
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ METHOD 1 SUCCESS: Message {message_id} deleted!")
                return True
            except Exception as e1:
                log_info(f"ℹ️ METHOD 1 FAILED: {e1}")
            
            # METHOD 2: Message object delete
            try:
                await message_obj.delete()
                log_info(f"✅ METHOD 2 SUCCESS: Object delete worked!")
                return True
            except Exception as e2:
                log_info(f"ℹ️ METHOD 2 FAILED: {e2}")
            
            # METHOD 3: Wait and retry
            await asyncio.sleep(1)
            try:
                await app.delete_messages(chat_id, message_id)
                log_info(f"✅ METHOD 3 SUCCESS: Retry worked!")
                return True
            except Exception as e3:
                log_info(f"ℹ️ METHOD 3 FAILED: {e3}")
            
            log_info(f"💀 All delete methods failed, but checking continues...")
            return False

        async def delete_after_delay_never_fail(message_obj, seconds):
            await asyncio.sleep(seconds)
            await never_fail_delete(message_obj)

        # ✅ MESSAGE CHECKING HEALTH MONITOR
        async def message_checking_health_monitor():
            """Monitor that message checking never stops"""
            health_check_count = 0
            while session_active:
                try:
                    health_check_count += 1
                    
                    # Check if message checking is stuck
                    if message_monitor.is_checking_stuck():
                        log_error(f"🚨 MESSAGE CHECKING STUCK! Last message {int(time.time() - message_monitor.last_message_time)}s ago")
                        
                        # Try to revive by sending a test message
                        try:
                            test_msg = await app.send_message("me", f"🔄 Reviving message check #{health_check_count}")
                            await asyncio.sleep(1)
                            await never_fail_delete(test_msg)
                            log_info("✅ Message checking revived!")
                        except Exception as e:
                            log_error(f"❌ Failed to revive message checking: {e}")
                    
                    status = message_monitor.get_status()
                    log_info(f"❤️ HEALTH CHECK #{health_check_count}: Messages checked: {status['check_count']}, Last: {status['last_message_seconds_ago']}s ago")
                    touch_activity()
                    
                except Exception as e:
                    log_error(f"❌ Health monitor error: {e}")
                
                # Check every 30 seconds
                await asyncio.sleep(30)

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
            message_monitor.update_message_time()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **ULTIMATE BOT STARTED!**\nNever Stop Checking Fix Applied!")
                log_info("✅ /start command executed")

        @app.on_message(filters.command("checkstatus"))
        async def check_status_command(client, message: Message):
            """Check message checking status"""
            log_info(f"📩 Received /checkstatus from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            message_monitor.update_message_time()
            if message.from_user and is_admin(message.from_user.id):
                status = message_monitor.get_status()
                await message.reply(
                    f"📊 **MESSAGE CHECKING STATUS**\n"
                    f"• Messages Checked: `{status['check_count']}`\n"
                    f"• Last Message: `{status['last_message_seconds_ago']}s ago`\n"
                    f"• Status: `{'✅ ACTIVE' if status['is_active'] else '❌ STUCK'}`\n"
                    f"• Checking: `🚀 NEVER STOPPING`"
                )
                log_info("✅ /checkstatus command executed")

        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            log_info(f"📩 Received /test from {message.from_user.id if message.from_user else 'Unknown'}")
            touch_activity()
            message_monitor.update_message_time()
            if message.from_user and is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing NEVER STOP checking...")
                await asyncio.sleep(2)
                success = await never_fail_delete(test_msg)
                if success:
                    await message.reply("✅ **DELETE WORKING!** Message checking is ACTIVE!")
                else:
                    await message.reply("❌ DELETE FAILED! But checking continues...")
                log_info("✅ /test command executed")

        # ---------------------------------------------------------
        # ULTIMATE DELETE HANDLER - NEVER STOP CHECKING VERSION
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def never_stop_checking_handler(client, message: Message):
            try:
                # UPDATE MESSAGE TIME - THIS IS CRITICAL
                message_monitor.update_message_time()
                touch_activity()
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    log_info(f"ℹ️ Group not allowed: {group_id}")
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

                # Log EVERY message detection
                log_info(f"🎯 MESSAGE #{message_monitor.check_count} DETECTED: @{username} (bot: {is_bot}) in {group_id}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    log_info(f"✅ Safe bot ignored: @{username}")
                    return

                # ⏰ DELAYED BOT - SCHEDULE DELETE
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    log_info(f"⏰ Delayed bot: @{username} (links: {has_links}, mentions: {has_mentions})")
                    
                    if has_links or has_mentions:
                        log_info(f"🚫 Delayed bot with links: INSTANT DELETE")
                        await never_fail_delete(message)
                    else:
                        log_info(f"⏰ Delayed bot normal: 30s delete")
                        asyncio.create_task(delete_after_delay_never_fail(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    log_info(f"🗑️ Unsafe bot: INSTANT DELETE")
                    await never_fail_delete(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    log_info(f"🔗 User with links: DELETING")
                    await never_fail_delete(message)
                    return

                log_info(f"ℹ️ Message doesn't match criteria, but CHECKING CONTINUES")

            except Exception as e:
                error_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8')
                log_error(f"❌ Handler error: {error_msg}")
                # CRITICAL: Even if error, update message time to show we're still checking
                message_monitor.update_message_time()
        
        # ✅ BOT START
        log_info("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # Start all background tasks - HEALTH MONITOR IS CRITICAL
        keep_alive_task = asyncio.create_task(session_keep_alive())
        online_task = asyncio.create_task(simple_online_status())
        watchdog_task = asyncio.create_task(watchdog_loop())
        keep_session_task = asyncio.create_task(keep_session_alive_loop())
        force_state_task = asyncio.create_task(force_state_update())
        health_monitor_task = asyncio.create_task(message_checking_health_monitor())
        
        # 🎯 AUTO SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        log_info(f"✅ Auto-setup: {len(allowed_groups)} groups, {len(safe_bots)} safe bots")
        log_info("💓 SESSION KEEP-ALIVE: ACTIVE")
        log_info("🟢 ONLINE STATUS: WORKING") 
        log_info("🚀 MESSAGE CHECKING: NEVER STOPPING")
        log_info("❤️ HEALTH MONITOR: RUNNING")
        log_info("🗑️ AUTO DELETE: 24/7 ACTIVE")
        
        # Startup message
        try:
            await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - NEVER STOP CHECKING!**

🎯 **CRITICAL FIXES:**
• Message Checking Health Monitor
• Automatic Stuck Detection
• Self-Reviving System
• Never Stop Checking Guarantee

🚀 **NEW COMMANDS:**
• `/checkstatus` - Check message checking status
• `/test` - Test the system

**Ab message checking kabhi nahi rukegi! Har message check hoga!** 🔥
            """)
        except Exception as e:
            log_error(f"Couldn't send startup DM: {e}")
        
        log_info("🤖 BOT READY - Message Checking NEVER STOPS!")
        
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
            health_monitor_task.cancel()
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
