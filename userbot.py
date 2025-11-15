print("🔥 ULTIMATE BOT STARTING - ALL LINKS DELETE FIX...")

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

# 🔥 ALL LINKS DELETE MANAGER
class AllLinksDeleteManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_bots_deleted = 0
        self.private_users_ignored = 0
        self.private_delete_failed = 0
        self.public_bots_deleted = 0
        
        # ✅ SAB TARAH KE LINKS PATTERNS
        self.all_link_patterns = [
            # HTTP/HTTPS Links
            'http://', 'https://', 'http://www.', 'https://www.',
            # Telegram Links
            't.me/', 'telegram.me/', 'tg://',
            # Social Media Links
            'facebook.com/', 'fb.com/', 'instagram.com/', 'twitter.com/', 
            'x.com/', 'youtube.com/', 'youtu.be/', 'linkedin.com/',
            # File Sharing Links
            'drive.google.com/', 'mega.nz/', 'dropbox.com/', 'mediafire.com/',
            # Other Common Links
            'whatsapp.com/', 'wa.me/', 'discord.gg/', 'reddit.com/',
            'pinterest.com/', 'tiktok.com/', 'snapchat.com/',
            # Shortened Links
            'bit.ly/', 'tinyurl.com/', 'goo.gl/', 'ow.ly/',
            # Indian Links
            'jiocinema.com/', 'hotstar.com/', 'mxplayer.in/',
            # Generic Patterns
            '.com/', '.org/', '.net/', '.in/', '.io/'
        ]
        
        # ✅ MENTIONS PATTERNS
        self.mention_patterns = ['@']
        
    def contains_any_links_or_mentions(self, text):
        """Check if text contains any links or mentions"""
        if not text:
            return False
            
        text_lower = text.lower()
        
        # Check for any link pattern
        for pattern in self.all_link_patterns:
            if pattern in text_lower:
                return True
                
        # Check for mentions
        for pattern in self.mention_patterns:
            if pattern in text:
                return True
                
        return False
    
    async def private_group_specific_delete(self, app, message_obj):
        """Private group specific delete with multiple methods"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        username = (message_obj.from_user.username or "").lower() if message_obj.from_user else ""
        
        log_info(f"🔧 PRIVATE GROUP DELETE ATTEMPT: @{username} - {message_id}")
        
        # METHOD 1: Direct delete
        try:
            await app.delete_messages(chat_id, message_id)
            self.private_bots_deleted += 1
            log_info(f"✅ PRIVATE DIRECT DELETE SUCCESS: @{username}")
            return True
        except Exception as e1:
            log_error(f"❌ Private Direct Delete Failed: {e1}")
        
        # METHOD 2: Get chat first then delete
        try:
            chat = await app.get_chat(chat_id)
            await app.delete_messages(chat_id, message_id)
            self.private_bots_deleted += 1
            log_info(f"✅ PRIVATE CHAT-FIRST DELETE SUCCESS: @{username}")
            return True
        except Exception as e2:
            log_error(f"❌ Private Chat-First Delete Failed: {e2}")
        
        # METHOD 3: Different API approach
        try:
            await app.delete_messages(chat_id, [message_id])
            self.private_bots_deleted += 1
            log_info(f"✅ PRIVATE LIST DELETE SUCCESS: @{username}")
            return True
        except Exception as e3:
            log_error(f"❌ Private List Delete Failed: {e3}")
        
        self.private_delete_failed += 1
        return False
    
    async def public_group_delete(self, app, message_obj):
        """Public group delete"""
        chat_id = message_obj.chat.id
        message_id = message_obj.id
        username = (message_obj.from_user.username or "").lower() if message_obj.from_user else ""
        
        try:
            await app.delete_messages(chat_id, message_id)
            self.public_bots_deleted += 1
            log_info(f"✅ PUBLIC DELETE SUCCESS: @{username}")
            return True
        except Exception as e:
            log_error(f"❌ Public Delete Failed: @{username} - {e}")
            return False

# 🔥 TELEGRAM BOT - ALL LINKS DELETE FIX
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - ALL LINKS DELETE FIX...")
    
    # ✅ SESSION DATA
    session_data = {
        'active': True
    }

    # Initialize all links delete manager
    links_manager = AllLinksDeleteManager()

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
        # GROUP SPECIFIC DELETE FUNCTION
        # -----------------------------
        async def group_specific_delete(message_obj):
            """
            DIFFERENT DELETE METHODS FOR PRIVATE VS PUBLIC GROUPS
            """
            touch_activity()
            chat_id = message_obj.chat.id
            is_private = str(chat_id) == links_manager.private_group_id
            
            if is_private:
                return await links_manager.private_group_specific_delete(app, message_obj)
            else:
                return await links_manager.public_group_delete(app, message_obj)

        async def delete_after_delay_specific(message_obj, seconds):
            await asyncio.sleep(seconds)
            await group_specific_delete(message_obj)

        # ✅ PRIVATE GROUP DEBUGGER
        async def private_group_debugger():
            """Debug private group specifically"""
            debug_count = 0
            while session_data['active']:
                debug_count += 1
                try:
                    # Debug private group every 3 minutes
                    if debug_count % 3 == 0:
                        try:
                            chat = await app.get_chat(int(links_manager.private_group_id))
                            log_info(f"🔍 Private Debug: {chat.title} - Access OK")
                        except Exception as e:
                            log_error(f"🔍 Private Debug Error: {e}")
                    
                    await asyncio.sleep(60)
                    
                except Exception as e:
                    log_error(f"Private debugger error: {e}")
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
        # DETAILED WATCHDOG
        # -------------------------
        async def detailed_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 6 == 0:
                        private_success_rate = (links_manager.private_bots_deleted / (links_manager.private_bots_deleted + links_manager.private_delete_failed)) * 100 if (links_manager.private_bots_deleted + links_manager.private_delete_failed) > 0 else 0
                        log_info(f"🐕 Watchdog - Private: {links_manager.private_bots_deleted}✅/{links_manager.private_delete_failed}❌ ({private_success_rate:.1f}%), Public: {links_manager.public_bots_deleted}✅")
                    
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
🚀 **BOT STARTED - ALL LINKS DELETE MODE!**

🎯 **NEW CONFIGURATION:**
• 🤖 DELETE: All unsafe bots (with ANY links/mentions)
• 👥 IGNORE: All users (even with links/mentions)
• 🔗 LINKS: {len(links_manager.all_link_patterns)} types of links detected
• ✅ PROTECT: {len(safe_bots)} safe bots

📊 **STATISTICS:**
• Private Group: {links_manager.private_bots_deleted} ✅ / {links_manager.private_delete_failed} ❌
• Public Group: {links_manager.public_bots_deleted} ✅
• Users Ignored: {links_manager.private_users_ignored} 👥

🔗 **DETECTED LINK TYPES:**
• HTTP/HTTPS, Telegram, Social Media
• File Sharing, Shortened URLs
• All domain extensions (.com, .org, .in, etc.)
• Mentions (@username)

**Mode: ALL LINKS DELETE FOR BOTS** 🔥
                """
                await message.reply(status_msg)
                log_info("✅ /start executed")

        @app.on_message(filters.command("test_links"))
        async def test_links_command(client, message: Message):
            log_info(f"📩 /test_links from {message.from_user.id}")
            touch_activity()
            if message.from_user and is_admin(message.from_user.id):
                test_messages = [
                    "Test with t.me/link",
                    "Test with http://example.com", 
                    "Test with https://google.com",
                    "Test with @mention",
                    "Test with youtube.com/watch"
                ]
                
                results = []
                for test_text in test_messages:
                    if links_manager.contains_any_links_or_mentions(test_text):
                        results.append(f"✅ {test_text}")
                    else:
                        results.append(f"❌ {test_text}")
                
                await message.reply("🔗 **LINK DETECTION TEST:**\n" + "\n".join(results))

        # ---------------------------------------------------------
        # ALL LINKS DELETE HANDLER
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def all_links_delete_handler(client, message: Message):
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
                is_private = group_id == links_manager.private_group_id

                # 🎯 LOGIC: SIRF BOTS KE MESSAGES DELETE KARO
                
                # ✅ USER MESSAGES - COMPLETELY IGNORE (even with ALL links/mentions)
                if not is_bot:
                    if is_private:
                        links_manager.private_users_ignored += 1
                    log_info(f"👥 USER IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'} - (All links/mentions ignored)")
                    return

                # ✅ SAFE BOTS - IGNORE
                if username in safe_bots:
                    log_info(f"✅ SAFE BOT IGNORED: @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                    return

                # ✅ CHECK FOR ANY LINKS OR MENTIONS IN BOT MESSAGES
                has_links_or_mentions = links_manager.contains_any_links_or_mentions(message_text)
                
                # ⏰ DELAYED BOTS - DELETE BASED ON LINKS
                if username in delayed_bots:
                    if has_links_or_mentions:
                        log_info(f"🚫 DELAYED BOT WITH LINKS: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        await group_specific_delete(message)
                    else:
                        log_info(f"⏰ DELAYED BOT NORMAL: DELETE IN 30s - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                        asyncio.create_task(delete_after_delay_specific(message, 30))
                    return

                # 🗑️ OTHER BOTS (UNSAFE BOTS) - INSTANT DELETE (with or without links)
                if has_links_or_mentions:
                    log_info(f"🗑️ UNSAFE BOT WITH LINKS: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                else:
                    log_info(f"🗑️ UNSAFE BOT NO LINKS: DELETE NOW - @{username} in {'PRIVATE' if is_private else 'PUBLIC'}")
                
                await group_specific_delete(message)

            except Exception as e:
                log_error(f"❌ All Links Handler error: {e}")
                touch_activity()
        
        # ✅ BOT START - ALL LINKS DELETE
        log_info("🔗 Connecting to Telegram - ALL LINKS DELETE...")
        await app.start()
        
        me = await app.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        log_info(f"🎯 ALL LINKS DELETE MODE ACTIVATED")
        log_info(f"🔗 Link Patterns: {len(links_manager.all_link_patterns)} types")
        log_info(f"🛡️ Safe Bots: {len(safe_bots)}")
        log_info(f"⏰ Delayed Bots: {len(delayed_bots)}")
        
        # Test link detection
        test_messages = [
            "t.me/test",
            "http://example.com", 
            "Hello @username",
            "Check youtube.com"
        ]
        
        for test_msg in test_messages:
            detected = links_manager.contains_any_links_or_mentions(test_msg)
            log_info(f"🔗 Link Test: '{test_msg}' -> {'✅ DETECTED' if detected else '❌ NOT DETECTED'}")
        
        # Start background tasks
        keep_alive_task = asyncio.create_task(keep_alive())
        debugger_task = asyncio.create_task(private_group_debugger())
        watchdog_task = asyncio.create_task(detailed_watchdog())
        
        log_info("💓 Keep-Alive: ACTIVE")
        log_info("🔧 Private Debugger: ACTIVE")
        log_info("🗑️ All Links Delete: READY")
        
        # Startup message
        try:
            await app.send_message("me", f"""
✅ **BOT STARTED - ALL LINKS DELETE MODE!**

🎯 **COMPLETE LINK DETECTION:**
• HTTP/HTTPS (http://, https://)
• Telegram (t.me/, telegram.me/, tg://)
• Social Media (facebook, instagram, twitter, youtube)
• File Sharing (drive.google, mega.nz, dropbox)
• Shortened URLs (bit.ly, tinyurl)
• All Domains (.com, .org, .net, .in, .io)
• Mentions (@username)

📋 **DELETE RULES:**
1. 🤖 UNSAFE BOTS: ALL messages deleted (with or without links)
2. ⏰ DELAYED BOTS: Links instantly, normal after 30s  
3. ✅ SAFE BOTS: NEVER deleted
4. 👥 USERS: NEVER deleted (even with all links)

**Link Detection: {len(links_manager.all_link_patterns)} PATTERNS** 🔥
            """)
        except Exception as e:
            log_error(f"Startup DM failed: {e}")
        
        log_info("🤖 BOT READY - All Links Delete Mode Active!")
        
        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            debugger_task.cancel()
            watchdog_task.cancel()
            await app.stop()
        
    except Exception as e:
        log_error(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 BOT STARTING - ALL LINKS DELETE FIX...")

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
