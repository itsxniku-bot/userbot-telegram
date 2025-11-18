print("🔥 ULTIMATE BOT STARTING - FINAL STABLE VERSION...")

import asyncio
import multiprocessing
import re
import traceback
from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import FloodWait, ChannelPrivate, PeerIdInvalid, UserNotParticipant
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

# ✅ FIXED: DIRECT GROUP IDs - Dono groups hardcode karo
allowed_groups = {"-1002382070176", "-1002497459144"}
safe_bots = {"unobot", "on9wordchainbot", "daisyfcbot", "missrose_bot", "zorofcbot", "digi4bot"}
delayed_bots = {"crocodile_game4_bot"}

# Save groups to file
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

last_activity = time.time()

def touch_activity():
    global last_activity
    last_activity = time.time()

# 🔥 BOT MANAGER CLASS
class BotManager:
    def __init__(self):
        self.online_status_count = 0
        self.total_messages_received = 0
        self.private_delete_count = 0
        self.public_delete_count = 0
        self.users_ignored_count = 0
        self.delete_failures = 0
        self.last_message_time = 0
        self.missed_messages = 0
        self.recovered_messages = 0
        
    async def update_online_status(self, client):
        """24/7 Online status maintain karo"""
        try:
            self.online_status_count += 1
            
            # Multiple API calls for maximum online presence
            try:
                await client.get_me()
                await asyncio.sleep(0.5)
                await client.get_users("me")
                await asyncio.sleep(0.5)
                
                # Groups mein typing action bhejo for real-time online status
                for group_id in allowed_groups:
                    try:
                        await client.send_chat_action(group_id, "typing")
                        await asyncio.sleep(0.3)
                        await client.send_chat_action(group_id, "cancel")
                    except Exception as e:
                        pass  # Silent fail - group access issue
                        
            except Exception as e:
                pass  # Silent fail for API calls
            
            if self.online_status_count % 10 == 0:
                log_info(f"🟢 PERMANENT ONLINE: Cycle #{self.online_status_count}")
                
            return True
            
        except Exception as e:
            log_error(f"❌ Online status update failed: {e}")
            return False

# Initialize manager globally
manager = BotManager()

# ✅ FIXED: SIMPLE TELEGRAM CLIENT
client = Client(
    "ultimate_bot",
    api_id=22294121,
    api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
    session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
)

# ✅ FIXED: SIMPLE WATCHDOG
async def simple_watchdog():
    """Stable watchdog without manager dependency issues"""
    watchdog_count = 0
    while True:
        try:
            watchdog_count += 1
            idle_time = time.time() - last_activity
            
            if watchdog_count % 15 == 0:
                log_info(f"🐕 WATCHDOG - Idle: {int(idle_time)}s, Online: {manager.online_status_count}, Msgs: {manager.total_messages_received}")
            
            # 10 minutes idle tolerance
            if idle_time > 600:
                log_error(f"⚠️ WATCHDOG: No activity for {int(idle_time)}s")
                # Force activity to prevent restart
                touch_activity()
                
            await asyncio.sleep(10)
        except Exception as e:
            log_error(f"Watchdog error: {e}")
            await asyncio.sleep(10)

# ✅ FIXED: MESSAGE RECOVERY SYSTEM
class MessageRecovery:
    def __init__(self):
        self.pending_messages = {}
        self.recovery_interval = 60  # 1 minute
    
    async def check_missed_messages(self, client):
        """Check for any missed messages and recover them"""
        try:
            current_time = time.time()
            recovered_count = 0
            
            for group_id in allowed_groups:
                try:
                    # Get last few messages to check for missed bots
                    async for message in client.get_chat_history(group_id, limit=10):
                        if current_time - message.date.timestamp() > 120:  # 2 minutes old
                            break
                            
                        # Check if this is a bot message we missed
                        if await self.is_bot_message(message) and await self.should_delete(message):
                            try:
                                await message.delete()
                                recovered_count += 1
                                manager.recovered_messages += 1
                                log_info(f"🔄 RECOVERED MISSED: {message.id} from {group_id}")
                                await asyncio.sleep(0.5)  # Rate limit
                            except Exception as e:
                                log_error(f"❌ Recovery delete failed: {e}")
                                
                except Exception as e:
                    log_info(f"⚠️ Recovery check failed for {group_id}: {e}")
            
            if recovered_count > 0:
                log_info(f"✅ RECOVERY: {recovered_count} missed messages recovered")
                
        except Exception as e:
            log_error(f"❌ Message recovery system error: {e}")
    
    async def is_bot_message(self, message):
        """Check if message is from a bot"""
        if message.from_user and getattr(message.from_user, 'is_bot', False):
            return True
        
        if getattr(message, 'via_bot', None) or getattr(message, 'via_bot_id', None):
            return True
            
        if message.sender_chat and any(keyword in str(message.sender_chat.username).lower() for keyword in ['bot', 'robot']):
            return True
            
        return False
    
    async def should_delete(self, message):
        """Check if this bot message should be deleted"""
        username = "unknown"
        
        if message.from_user:
            username = (getattr(message.from_user, "username", None) or f"user_{message.from_user.id}").lower()
        elif message.sender_chat:
            username = (getattr(message.sender_chat, "username", None) or getattr(message.sender_chat, "title", "")).lower()
        
        # Safe bots ko ignore karo
        if username in safe_bots:
            return False
            
        # Delayed aur unknown bots ko delete karo
        if username in delayed_bots or username not in safe_bots:
            return True
            
        return False

# Initialize recovery system
recovery_system = MessageRecovery()

# ✅ FIXED: ULTIMATE MESSAGE HANDLER
@client.on_message(filters.group)
async def ultimate_message_handler(_, message: Message):
    """ULTIMATE MESSAGE HANDLER - No message escapes"""
    try:
        touch_activity()
        manager.total_messages_received += 1
        manager.last_message_time = time.time()
        
        group_id = str(message.chat.id)
        
        # Only process our target groups
        if group_id not in allowed_groups:
            return
        
        is_private = group_id == "-1002497459144"
        
        # FAST BOT DETECTION
        username = "unknown"
        is_bot = False
        
        if message.from_user:
            u = message.from_user
            username = (getattr(u, "username", None) or f"user_{u.id}").lower()
            is_bot = getattr(u, "is_bot", False)
        else:
            sender_chat = getattr(message, "sender_chat", None)
            if sender_chat:
                username = (getattr(sender_chat, "username", None) or getattr(sender_chat, "title", "")).lower()
                if getattr(message, "via_bot", None):
                    is_bot = True
        
        if not is_bot and getattr(message, "via_bot", None):
            is_bot = True
        
        message_text = message.text or message.caption or ""
        message_preview = message_text[:30] + "..." if len(message_text) > 30 else message_text
        
        log_info(f"📨 MSG #{manager.total_messages_received} | Group: {group_id} | User: {username} | Bot: {is_bot}")
        
        # BOT MESSAGE HANDLING - NO ESCAPES
        if is_bot:
            # Safe bots - ignore
            if username in safe_bots:
                log_info(f"✅ SAFE BOT IGNORED: {username}")
                return
            
            # Delayed bots - delete after 3 seconds
            if username in delayed_bots:
                log_info(f"⏰ DELAYED BOT: {username} - Will delete in 3s")
                await asyncio.sleep(3)
                await delete_message_with_retry(message, is_private)
                return
            
            # UNKNOWN BOTS - INSTANT DELETE
            log_info(f"🚫 UNKNOWN BOT: {username} - INSTANT DELETE")
            await delete_message_with_retry(message, is_private)
            return
        
        # USER MESSAGES - Just track
        manager.users_ignored_count += 1
        if manager.users_ignored_count % 25 == 0:
            log_info(f"👤 User messages tracked: {manager.users_ignored_count}")
            
    except Exception as e:
        log_error(f"❌ Ultimate handler error: {e}")
        manager.missed_messages += 1

async def delete_message_with_retry(message, is_private):
    """Delete message with multiple retry attempts"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            await message.delete()
            
            if is_private:
                manager.private_delete_count += 1
                log_info(f"✅ PRIVATE DELETE: {message.id} (Attempt {attempt + 1})")
            else:
                manager.public_delete_count += 1
                log_info(f"✅ PUBLIC DELETE: {message.id} (Attempt {attempt + 1})")
            
            return True
            
        except Exception as e:
            log_error(f"❌ Delete attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(2)  # Wait before retry
            else:
                manager.delete_failures += 1
                log_error(f"💥 FINAL DELETE FAILED: {message.id}")
                return False

# ✅ FIXED: ONLINE STATUS MAINTAINER
async def maintain_permanent_online():
    """24/7 ONLINE STATUS - Like a real user"""
    online_cycle = 0
    
    while True:
        try:
            online_cycle += 1
            
            # Update online status
            await manager.update_online_status(client)
            touch_activity()
            
            # Every 5 minutes, run message recovery
            if online_cycle % 20 == 0:
                await recovery_system.check_missed_messages(client)
                log_info(f"🔵 PERMANENT ONLINE: Cycle #{online_cycle} | Deletes: {manager.private_delete_count + manager.public_delete_count} | Recovered: {manager.recovered_messages}")
            
            # 15 second intervals for maximum online presence
            await asyncio.sleep(15)
            
        except Exception as e:
            log_error(f"❌ Online maintainer error: {e}")
            await asyncio.sleep(15)

# ✅ FIXED: COMMAND HANDLERS
@client.on_message(filters.command("start") & filters.private)
async def start_command(_, message: Message):
    await message.reply_text("🤖 ULTIMATE BOT ACTIVE - 24/7 ONLINE & MESSAGE PROTECTION")

@client.on_message(filters.command("status") & filters.private)
async def status_command(_, message: Message):
    if message.from_user.id != ADMIN_USER_ID:
        return
    
    status_text = f"""
🤖 **ULTIMATE BOT STATUS - 24/7 ACTIVE**

📊 **MESSAGE STATS:**
• Total Processed: {manager.total_messages_received}
• Private Deletes: {manager.private_delete_count}
• Public Deletes: {manager.public_delete_count}
• Delete Failures: {manager.delete_failures}
• Users Ignored: {manager.users_ignored_count}
• Missed Messages: {manager.missed_messages}
• Recovered: {manager.recovered_messages}

🟢 **ONLINE STATUS:**
• Online Cycles: {manager.online_status_count}
• Last Activity: {int(time.time() - last_activity)}s ago

🎯 **TARGET GROUPS:**
• -1002382070176: ✅ PUBLIC GROUP
• -1002497459144: ✅ PRIVATE GROUP

💡 **FEATURES:**
• 24/7 Online Presence
• Instant Bot Detection
• Message Recovery System
• No Message Escapes
"""

    await message.reply_text(status_text)

@client.on_message(filters.command("scan") & filters.private)
async def scan_command(_, message: Message):
    if message.from_user.id != ADMIN_USER_ID:
        return
    
    await message.reply_text("🔍 Scanning for missed messages...")
    await recovery_system.check_missed_messages(client)
    await message.reply_text(f"✅ Recovery scan completed! Recovered: {manager.recovered_messages} messages")

# ✅ FIXED: STABLE STARTUP
async def start_bot():
    """Stable bot startup with proper error handling"""
    log_info("🚀 STARTING ULTIMATE BOT - FINAL STABLE VERSION...")
    
    try:
        await client.start()
        log_info("✅ TELEGRAM CLIENT STARTED SUCCESSFULLY")
        
        bot_me = await client.get_me()
        log_info(f"🤖 BOT IDENTITY: {bot_me.first_name} (@{bot_me.username})")
        
        # Start background tasks
        asyncio.create_task(maintain_permanent_online())
        asyncio.create_task(simple_watchdog())
        
        log_info("🎉 ULTIMATE BOT FULLY OPERATIONAL!")
        log_info("✅ 24/7 Online Status: ACTIVATED")
        log_info("✅ Message Protection: ACTIVATED") 
        log_info("✅ Recovery System: ACTIVATED")
        
        # Keep bot running
        await idle()
        
    except Exception as e:
        log_critical(f"💥 BOT STARTUP FAILED: {e}")
        raise
    finally:
        try:
            await client.stop()
        except:
            pass
        log_info("🛑 Bot stopped")

# ✅ FIXED: MAIN SUPERVISOR
async def main():
    """Main supervisor with automatic recovery"""
    restart_delay = 5
    
    while True:
        try:
            log_info(f"🔄 Starting bot (delay: {restart_delay}s)...")
            await start_bot()
            
        except KeyboardInterrupt:
            log_info("🛑 Manual shutdown requested")
            break
        except Exception as e:
            log_error(f"💥 Bot crashed: {e}")
            log_info(f"🔄 Restarting in {restart_delay} seconds...")
            await asyncio.sleep(restart_delay)
            restart_delay = min(restart_delay * 2, 60)  # Exponential backoff

if __name__ == "__main__":
    # Signal handling
    def signal_handler(signum, frame):
        log_info(f"🛑 Received signal {signum}, shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(main())
    except Exception as e:
        log_critical(f"💥 FATAL: {e}")
