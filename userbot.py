print("🔥 ULTIMATE BOT STARTING - REJOIN ADMIN FIX...")

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

# 🔥 REJOIN ADMIN FIX MANAGER
class RejoinAdminFixManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.session_refreshed = False
        self.groups_activated = False
        self.delete_count = 0
        self.cache_clear_attempts = 0
        
    async def force_session_refresh(self, app):
        """Force session refresh after rejoin"""
        try:
            # METHOD 1: Send message to activate session
            log_info("🔄 Force activating private group session...")
            activation_msg = await app.send_message(self.private_group_id, "🤖 Session activation...")
            await asyncio.sleep(1)
            await app.delete_messages(self.private_group_id, activation_msg.id)
            log_info("✅ Private group session activated")
            
            # METHOD 2: Send message to public group
            log_info("🔄 Force activating public group session...")
            activation_msg2 = await app.send_message(self.public_group_id, "🤖 Session activation...")
            await asyncio.sleep(1)
            await app.delete_messages(self.public_group_id, activation_msg2.id)
            log_info("✅ Public group session activated")
            
            self.session_refreshed = True
            return True
            
        except Exception as e:
            log_error(f"❌ Session activation failed: {e}")
            return False
    
    async def clear_cache_and_retry(self, app, group_id, group_name):
        """Clear cache and retry access"""
        self.cache_clear_attempts += 1
        
        try:
            # METHOD 1: Direct access
            chat = await app.get_chat(int(group_id))
            log_info(f"✅ {group_name}: {chat.title}")
            return True
        except Exception as e:
            log_error(f"❌ {group_name} direct access failed: {e}")
        
        try:
            # METHOD 2: Send and delete message
            test_msg = await app.send_message(group_id, "🧪 Cache clearance test...")
            await asyncio.sleep(2)
            await app.delete_messages(group_id, test_msg.id)
            log_info(f"✅ {group_name}: Cache cleared via message")
            return True
        except Exception as e:
            log_error(f"❌ {group_name} message test failed: {e}")
        
        return False
    
    async def rejoin_admin_delete(self, app, message_obj):
        """Delete function for rejoin admin scenario"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        is_private = str(chat_id) == self.private_group_id
        
        log_info(f"🗑️ REJOIN ADMIN DELETE: {message_id} in {'PRIVATE' if is_private else 'PUBLIC'}")
        
        try:
            # DIRECT DELETE ATTEMPT
            await app.delete_messages(chat_id, message_id)
            self.delete_count += 1
            log_info(f"✅ REJOIN DELETE SUCCESS: {message_id}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            log_error(f"❌ REJOIN DELETE FAILED: {error_msg}")
            
            # If session needs refresh, try to activate
            if not self.session_refreshed:
                log_info("🔄 Attempting session refresh...")
                await self.force_session_refresh(app)
                
                # Retry delete after refresh
                try:
                    await app.delete_messages(chat_id, message_id)
                    self.delete_count += 1
                    log_info(f"✅ DELETE SUCCESS AFTER REFRESH: {message_id}")
                    return True
                except Exception as e2:
                    log_error(f"❌ DELETE FAILED AFTER REFRESH: {e2}")
            
            return False

# 🔥 TELEGRAM BOT - REJOIN ADMIN FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - REJOIN ADMIN FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True,
        'delete_success_count': 0,
        'delete_fail_count': 0
    }

    # Initialize rejoin admin fix manager
    rejoin_manager = RejoinAdminFixManager()

    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA",
            sleep_threshold=60
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # -----------------------------
        # REJOIN ADMIN DELETE FUNCTION
        # -----------------------------
        async def rejoin_admin_delete_function(message_obj):
            """
            DELETE FUNCTION FOR REJOIN ADMIN SCENARIO
            """
            touch_activity()
            
            success = await rejoin_manager.rejoin_admin_delete(app, message_obj)
            if success:
                session_data['delete_success_count'] += 1
            else:
                session_data['delete_fail_count'] += 1
            
            return success

        async def delete_after_delay_rejoin(message_obj, seconds):
            await asyncio.sleep(seconds)
            await rejoin_admin_delete_function(message_obj)

        # ✅ SESSION ACTIVATOR
        async def session_activator():
            """Activate session in both groups"""
            activator_count = 0
            while session_data['active']:
                activator_count += 1
                try:
                    # Force session activation every 2 minutes until successful
                    if activator_count % 2 == 0 and not rejoin_manager.session_refreshed:
                        log_info("🔄 Session Activator: Attempting session refresh...")
                        success = await rejoin_manager.force_session_refresh(app)
                        if success:
                            log_info("✅ Session Activator: Session refreshed successfully")
                    
                    # Clear cache in both groups every 5 minutes
                    if activator_count % 5 == 0:
                        log_info("🔄 Session Activator: Clearing group cache...")
                        private_ok = await rejoin_manager.clear_cache_and_retry(app, rejoin_manager.private_group_id, "PRIVATE GROUP")
                        public_ok = await rejoin_manager.clear_cache_and_retry(app, rejoin_manager.public_group_id, "PUBLIC GROUP")
                        rejoin_manager.groups_activated = private_ok or public_ok
                    
                    await asyncio.sleep(30)
                    
                except Exception as e:
                    log_error(f"Session activator error: {e}")
                    await asyncio.sleep(60)

        # ✅ AGGRESSIVE KEEP-ALIVE
        async def aggressive_keep_alive():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    await app.get_me()
                    
                    # Send keep-alive messages to groups
                    if keep_alive_count % 10 == 0 and rejoin_manager.session_refreshed:
                        try:
                            # Keep private group active
                            ka_msg = await app.send_message(rejoin_manager.private_group_id, "💓")
                            await asyncio.sleep(1)
                            await app.delete_messages(rejoin_manager.private_group_id, ka_msg.id)
                        except:
                            pass
                        
                        try:
                            # Keep public group active  
                            ka_msg2 = await app.send_message(rejoin_manager.public_group_id, "💓")
                            await asyncio.sleep(1)
                            await app.delete_messages(rejoin_manager.public_group_id, ka_msg2.id)
                        except:
                            pass
                    
                    if keep_alive_count % 15 == 0:
                        log_info(f"💓 Aggressive Keep-Alive #{keep_alive_count}")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Keep-Alive Failed: {e}")
                await asyncio.sleep(20)

        # -------------------------
        # REJOIN WATCHDOG
        # -------------------------
        async def rejoin_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 5 == 0:
                        log_info(f"🐕 Rejoin Watchdog - Idle: {int(idle)}s, Deletes: {rejoin_manager.delete_count}, Cache Attempts: {rejoin_manager.cache_clear_attempts}")
                    
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
                # Force session refresh
                session_ok = await rejoin_manager.force_session_refresh(app)
                private_ok = await rejoin_manager.clear_cache_and_retry(app, rejoin_manager.private_group_id, "PRIVATE GROUP")
                public_ok = await rejoin_manager.clear_cache_and_retry(app, rejoin_manager.public_group_id, "PUBLIC GROUP")
                
                status_msg = f"""
🚀 **BOT STARTED - REJOIN ADMIN FIX!**

📊 **REJOIN STATUS:**
• Session Refreshed: {'✅ YES' if session_ok else '❌ NO'}
• Private Group: {'✅ ACTIVATED' if private_ok else '🔄 PENDING'}
• Public Group: {'✅ ACTIVATED' if public_ok else '🔄 PENDING'}
• Cache Clear Attempts: {rejoin_manager.cache_clear_attempts}
• Successful Deletes: {rejoin_manager.delete_count}

🎯 **FIX APPLIED:**
• Force Session Refresh
• Cache Clearance
• Aggressive Activation
• Rejoin Admin Handling

**Status: {'ACTIVE' if session_ok else 'ACTIVATING'}** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("force_activation"))
        async def force_activation_command(client, message: Message):
            log_info(f"📩 /force_activation from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🔄 **FORCING GROUP ACTIVATION...**")
                
                # Test both groups with actual messages
                results = []
                
                # Test private group
                try:
                    test_msg = await app.send_message(rejoin_manager.private_group_id, "🧪 Private activation test...")
                    await asyncio.sleep(2)
                    await app.delete_messages(rejoin_manager.private_group_id, test_msg.id)
                    results.append("Private: ✅ ACTIVATED")
                    rejoin_manager.session_refreshed = True
                except Exception as e:
                    results.append(f"Private: ❌ ({e})")
                
                # Test public group
                try:
                    test_msg = await app.send_message(rejoin_manager.public_group_id, "🧪 Public activation test...")
                    await asyncio.sleep(2)
                    await app.delete_messages(rejoin_manager.public_group_id, test_msg.id)
                    results.append("Public: ✅ ACTIVATED")
                    rejoin_manager.session_refreshed = True
                except Exception as e:
                    results.append(f"Public: ❌ ({e})")
                
                await message.reply("🧪 **ACTIVATION RESULTS:**\n" + "\n".join(results))
                log_info("✅ /force_activation executed")

        @app.on_message(filters.command("test_rejoin"))
        async def test_rejoin_command(client, message: Message):
            log_info(f"📩 /test_rejoin from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                try:
                    # Test in private group
                    test_msg = await app.send_message(rejoin_manager.private_group_id, "🧪 Rejoin delete test...")
                    await asyncio.sleep(2)
                    success = await rejoin_admin_delete_function(test_msg)
                    
                    if success:
                        await message.reply("✅ **REJOIN DELETE WORKING!**\nBot can delete in private group!")
                    else:
                        await message.reply("❌ **REJOIN DELETE FAILED!**\nSession may need manual activation.")
                        
                except Exception as e:
                    await message.reply(f"❌ Rejoin test failed: {e}")

        # ---------------------------------------------------------
        # REJOIN ADMIN DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def rejoin_admin_handler(client, message: Message):
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
                message_text_lower = message_text.lower()

                log_info(f"🎯 REJOIN GROUP: @{username} in {message.chat.title}")

                # ✅ SAFE BOT - IGNORE
                if username in safe_bots:
                    return

                # ⏰ DELAYED BOT - DELETE AFTER DELAY
                if username in delayed_bots:
                    has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                    has_mentions = '@' in message_text
                    
                    if has_links or has_mentions:
                        await rejoin_admin_delete_function(message)
                    else:
                        asyncio.create_task(delete_after_delay_rejoin(message, 30))
                    return

                # 🗑️ OTHER BOTS - INSTANT DELETE
                if is_bot:
                    await rejoin_admin_delete_function(message)
                    return

                # 🔗 USER MESSAGES WITH LINKS/MENTIONS - DELETE
                has_links = any(pattern in message_text_lower for pattern in ['t.me/', 'http://', 'https://'])
                has_mentions = '@' in message_text
                
                if has_links or has_mentions:
                    await rejoin_admin_delete_function(message)
                    return

            except Exception as e:
                log_error(f"❌ Rejoin Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - REJOIN ADMIN FIX
        log_info("🔗 Connecting to Telegram - REJOIN ADMIN FIX...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # FORCE SESSION REFRESH AFTER REJOIN
        log_info("🔄 FORCING SESSION REFRESH AFTER REJOIN...")
        session_activated = await rejoin_manager.force_session_refresh(app)
        
        if session_activated:
            log_info("🎯 REJOIN FIX: Session successfully refreshed!")
        else:
            log_info("⚠️ REJOIN FIX: Session refresh failed - will retry automatically")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(aggressive_keep_alive())
        activator_task = asyncio.create_task(session_activator())
        watchdog_task = asyncio.create_task(rejoin_watchdog())
        
        log_info("💓 Aggressive Keep-Alive: ACTIVE")
        log_info("🔄 Session Activator: ACTIVE")
        log_info("🗑️ Rejoin Admin Delete: READY")
        
        # Test rejoin functionality
        try:
            if session_activated:
                test_msg = await app.send_message(rejoin_manager.private_group_id, "🧪 Rejoin functionality test...")
                await asyncio.sleep(2)
                test_success = await rejoin_admin_delete_function(test_msg)
                log_info(f"✅ Rejoin test: {'SUCCESS' if test_success else 'FAILED'}")
        except Exception as e:
            log_error(f"Rejoin test error: {e}")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - REJOIN ADMIN FIX!**

🎯 **SPECIAL FEATURES:**
• Force Session Refresh
• Cache Clearance System
• Aggressive Group Activation
• Rejoin Admin Handling

📊 **STATUS:**
• Session Refreshed: {'✅ YES' if session_activated else '🔄 RETRYING'}
• Cache Attempts: {rejoin_manager.cache_clear_attempts}
• Successful Deletes: {rejoin_manager.delete_count}

🚀 **NEXT STEPS:**
1. Use /force_activation command
2. Use /test_rejoin to verify
3. Bot will auto-activate groups

**Rejoin Fix: {'ACTIVE' if session_activated else 'ACTIVATING'}** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - Rejoin Admin Fix Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            activator_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - REJOIN ADMIN FIX...")

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
