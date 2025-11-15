print("🔥 ULTIMATE BOT STARTING - ONLY BOTS DELETE FIX...")

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

# 🔥 ONLY BOTS DELETE MANAGER
class OnlyBotsDeleteManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.bots_deleted_count = 0
        self.users_ignored_count = 0
        self.safe_bots_ignored_count = 0
        
    async def delete_unsafe_bot_message(self, app, message_obj):
        """Delete only unsafe bot messages"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        username = (message_obj.from_user.username or "").lower() if message_obj.from_user else ""
        
        try:
            await app.delete_messages(chat_id, message_id)
            self.bots_deleted_count += 1
            log_info(f"✅ UNSAFE BOT DELETED: @{username} - {message_id}")
            return True
        except Exception as e:
            log_error(f"❌ BOT DELETE FAILED: @{username} - {e}")
            return False

# 🔥 TELEGRAM BOT - ONLY BOTS DELETE FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - ONLY BOTS DELETE FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True
    }

    # Initialize only bots delete manager
    bots_manager = OnlyBotsDeleteManager()

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
        # ONLY BOTS DELETE FUNCTION
        # -----------------------------
        async def only_bots_delete(message_obj):
            """
            DELETE ONLY UNSAFE BOTS MESSAGES
            """
            touch_activity()
            return await bots_manager.delete_unsafe_bot_message(app, message_obj)

        async def delete_after_delay_bots(message_obj, seconds):
            await asyncio.sleep(seconds)
            await only_bots_delete(message_obj)

        # ✅ STATS MONITOR
        async def stats_monitor():
            """Monitor deletion statistics"""
            monitor_count = 0
            while session_data['active']:
                monitor_count += 1
                try:
                    # Log stats every 10 minutes
                    if monitor_count % 10 == 0:
                        log_info(f"📊 BOTS STATS - Deleted: {bots_manager.bots_deleted_count}, Ignored Users: {bots_manager.users_ignored_count}, Safe Bots: {bots_manager.safe_bots_ignored_count}")
                    
                    await asyncio.sleep(60)
                    
                except Exception as e:
                    log_error(f"Stats monitor error: {e}")
                    await asyncio.sleep(120)

        # ✅ KEEP-ALIVE
        async def keep_alive():
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
        # SIMPLE WATCHDOG
        # -------------------------
        async def simple_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 10 == 0:
                        log_info(f"🐕 Watchdog - Idle: {int(idle)}s, Bots Deleted: {bots_manager.bots_deleted_count}")
                    
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

        # ✅ ALL COMMANDS
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            log_info(f"📩 /start from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                status_msg = f"""
🚀 **BOT STARTED - ONLY BOTS DELETE!**

🎯 **CONFIGURATION:**
• Delete: ONLY UNSAFE BOTS
• Ignore: ALL USERS (even with links/mentions)
• Safe Bots: {len(safe_bots)} bots ignored
• Delayed Bots: {len(delayed_bots)} bots with delay

📊 **STATISTICS:**
• Bots Deleted: {bots_manager.bots_deleted_count}
• Users Ignored: {bots_manager.users_ignored_count}
• Safe Bots Ignored: {bots_manager.safe_bots_ignored_count}

🔧 **SETTINGS:**
• Groups: {len(allowed_groups)}
• Safe Bots: {', '.join(list(safe_bots)[:5])}{'...' if len(safe_bots) > 5 else ''}

**Mode: ONLY BOTS DELETE** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("stats"))
        async def stats_command(client, message: Message):
            log_info(f"📩 /stats from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                stats_msg = f"""
📊 **LIVE STATISTICS**

• 🤖 Bots Deleted: {bots_manager.bots_deleted_count}
• 👥 Users Ignored: {bots_manager.users_ignored_count}
• ✅ Safe Bots Ignored: {bots_manager.safe_bots_ignored_count}

• 🎯 Active Groups: {len(allowed_groups)}
• 🛡️ Protected Bots: {len(safe_bots)}
                """
                await message.reply(stats_msg)
                log_info("✅ /stats executed")

        # ---------------------------------------------------------
        # ONLY BOTS DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def only_bots_handler(client, message: Message):
            try:
                # UPDATE ACTIVITY IMMEDIATELY
                touch_activity()
                
                # CHECK GROUP PERMISSION
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return

                # SELF CHECK - Bot ke apne messages ignore karo
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
                message_text_lower = message_text.lower()

                # 🎯 LOGIC: SIRF BOTS KE MESSAGES DELETE KARO
                
                # ✅ USER MESSAGES - COMPLETELY IGNORE (even with links/mentions)
                if not is_bot:
                    bots_manager.users_ignored_count += 1
                    log_info(f"👥 USER IGNORED: @{username} - (Links/Mentions ignored)")
                    return

                # ✅ SAFE BOTS - IGNORE
                if username in safe_bots:
                    bots_manager.safe_bots_ignored_count += 1
                    log_info(f"✅ SAFE BOT IGNORED: @{username}")
                    return

                # ⏰ DELAYED BOTS - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        log_info(f"🚫 DELAYED BOT WITH LINKS: DELETE NOW - @{username}")
                        await only_bots_delete(message)
                    else:
                        log_info(f"⏰ DELAYED BOT NORMAL: DELETE IN 30s - @{username}")
                        asyncio.create_task(delete_after_delay_bots(message, 30))
                    return

                # 🗑️ OTHER BOTS (UNSAFE BOTS) - INSTANT DELETE
                log_info(f"🗑️ UNSAFE BOT: DELETE NOW - @{username}")
                await only_bots_delete(message)

            except Exception as e:
                log_error(f"❌ Only Bots Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - ONLY BOTS DELETE
        log_info("🔗 Connecting to Telegram - ONLY BOTS DELETE...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        log_info(f"🎯 ONLY BOTS DELETE MODE ACTIVATED")
        log_info(f"🛡️ Safe Bots: {len(safe_bots)}")
        log_info(f"⏰ Delayed Bots: {len(delayed_bots)}")
        log_info(f"👥 Users: COMPLETELY IGNORED (even with links)")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(keep_alive())
        stats_task = asyncio.create_task(stats_monitor())
        watchdog_task = asyncio.create_task(simple_watchdog())
        
        log_info("💓 Keep-Alive: ACTIVE")
        log_info("📊 Stats Monitor: ACTIVE")
        log_info("🗑️ Only Bots Delete: READY")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - ONLY BOTS DELETE MODE!**

🎯 **NEW CONFIGURATION:**
• 🤖 DELETE: Only unsafe bots
• 👥 IGNORE: All users (even with links/mentions)
• ✅ PROTECT: {len(safe_bots)} safe bots
• ⏰ DELAY: {len(delayed_bots)} delayed bots

📋 **RULES:**
1. Users ke messages NEVER delete (chahe links/mentions ho)
2. Safe bots ke messages NEVER delete  
3. Delayed bots - normal messages after 30s, links instantly
4. Other bots - INSTANT DELETE

**Mode: ONLY BOTS DELETE** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Only Bots Delete Mode Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            stats_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - ONLY BOTS DELETE FIX...")

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
