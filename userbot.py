print("🔥 ULTIMATE BOT STARTING - TEST MODE...")

import asyncio
import multiprocessing
import re
import traceback
from flask import Flask
from pyrogram import Client, filters
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
PEER_STATUS_FILE = "peer_status.json"

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

def load_peer_status():
    try:
        if os.path.exists(PEER_STATUS_FILE):
            with open(PEER_STATUS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"private_peer_activated": False, "last_activation": None}

def save_peer_status(status):
    try:
        with open(PEER_STATUS_FILE, 'w') as f:
            json.dump(status, f)
    except:
        pass

# ✅ TEMPORARY FIX: SIRF TEST GROUP RAKHO JAHAN ACCESS HO
# Apna khud ka test group ID yahan dalo
allowed_groups = set()  # Start with empty set

safe_bots = load_data(SAFE_BOTS_FILE)
delayed_bots = load_data(DELAYED_BOTS_FILE)
peer_status = load_peer_status()

if not safe_bots:
    safe_bots = {"unobot","on9wordchainbot","daisyfcbot","missrose_bot","zorofcbot","digi4bot"}
if not delayed_bots:
    delayed_bots = {"crocodile_game4_bot"}

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

# 🔥 SIMPLIFIED BOT MANAGER
class BotManager:
    def __init__(self):
        self.online_status_count = 0
        self.typing_actions_count = 0
        self.total_messages_received = 0
        self.group_access_status = {}
        
    async def update_online_status(self, client):
        """Simple online status maintenance"""
        try:
            self.online_status_count += 1
            
            # Basic API calls for online presence
            try:
                await client.get_me()
                await client.get_users("me")
            except: pass
            
            if self.online_status_count % 10 == 0:
                log_info(f"🟢 ONLINE: Cycle #{self.online_status_count}")
                
            return True
            
        except Exception as e:
            log_error(f"❌ Online status update failed: {e}")
            return False

# 🔥 TELEGRAM BOT - SIMPLIFIED VERSION
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - SIMPLIFIED VERSION...")
    
    session_data = {'active': True}
    manager = BotManager()

    try:
        client = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # ⭐ SIMPLE ONLINE MAINTENANCE
        async def maintain_online():
            online_cycle = 0
            while session_data['active']:
                try:
                    online_cycle += 1
                    await manager.update_online_status(client)
                    touch_activity()
                    
                    if online_cycle % 20 == 0:
                        log_info(f"🔵 ONLINE MAINTENANCE: Cycle #{online_cycle}")
                        
                except Exception as e:
                    log_error(f"❌ Online maintenance error: {e}")
                await asyncio.sleep(20)

        # ⭐ SIMPLE WATCHDOG
        async def simple_watchdog():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 10 == 0:
                        log_info(f"🐕 WATCHDOG - Idle: {int(idle)}s, Online Cycles: {manager.online_status_count}")
                    
                    if idle > 300:  # 5 minutes idle
                        log_error(f"⚠️ WATCHDOG: Restarting - No activity for {int(idle)}s")
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

        # ⭐ CHECK AVAILABLE GROUPS
        async def find_accessible_groups():
            """Find groups where bot has access"""
            log_info("🔍 Scanning for accessible groups...")
            accessible_groups = set()
            
            try:
                # Check common groups
                test_groups = [
                    "-1002382070176",  # Your public group
                    "-1002497459144",  # Your private group
                ]
                
                for group_id in test_groups:
                    try:
                        chat = await client.get_chat(group_id)
                        accessible_groups.add(group_id)
                        log_info(f"✅ ACCESSIBLE: {getattr(chat, 'title', group_id)}")
                        
                        # Check admin permissions
                        try:
                            me = await client.get_me()
                            member = await client.get_chat_member(group_id, me.id)
                            can_delete = False
                            if hasattr(member, "privileges") and member.privileges:
                                can_delete = getattr(member.privileges, "can_delete_messages", False)
                            if can_delete:
                                log_info(f"✅ ADMIN ACCESS: Can delete messages")
                            else:
                                log_info(f"⚠️ LIMITED ACCESS: Cannot delete messages")
                        except Exception as e:
                            log_info(f"⚠️ Cannot check admin permissions: {e}")
                            
                    except (ChannelPrivate, PeerIdInvalid, UserNotParticipant) as e:
                        log_info(f"❌ NO ACCESS: {group_id} - {e}")
                    except Exception as e:
                        log_info(f"⚠️ Error checking {group_id}: {e}")
                
                # Update allowed groups
                global allowed_groups
                allowed_groups = accessible_groups
                save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                
                if accessible_groups:
                    log_info(f"🎯 WORKING GROUPS: {len(accessible_groups)} groups accessible")
                else:
                    log_info("❌ NO GROUPS ACCESSIBLE - Bot needs to be added to groups")
                    
                return accessible_groups
                
            except Exception as e:
                log_error(f"Group scanning failed: {e}")
                return set()

        # ⭐ MESSAGE HANDLER
        @client.on_message(filters.group)
        async def message_handler(c, message: Message):
            try:
                touch_activity()
                manager.total_messages_received += 1
                group_id = str(message.chat.id)
                
                # Only process allowed groups
                if group_id not in allowed_groups:
                    return
                
                # Simple bot detection
                username = "unknown"
                is_bot = False
                
                if message.from_user:
                    u = message.from_user
                    username = (getattr(u, "username", None) or f"user_{u.id}").lower()
                    is_bot = getattr(u, "is_bot", False)
                
                message_text = message.text or message.caption or ""
                message_preview = message_text[:50] + "..." if len(message_text) > 50 else message_text
                
                log_info(f"[MSG #{manager.total_messages_received}] group={group_id} user={username} bot={is_bot} text={message_preview}")
                
                # Bot handling logic
                if is_bot:
                    if username in safe_bots:
                        log_info(f"✅ SAFE BOT: {username}")
                        return
                    
                    if username in delayed_bots:
                        log_info(f"⏰ DELAYED BOT: {username}")
                        await asyncio.sleep(3)
                        try:
                            await message.delete()
                            log_info(f"🗑️ DELETED: {username}")
                        except Exception as e:
                            log_error(f"❌ Delete failed: {e}")
                        return
                    
                    # Delete unknown bots immediately
                    log_info(f"🚫 UNKNOWN BOT: {username} - Deleting...")
                    try:
                        await message.delete()
                        log_info(f"🗑️ DELETED: {username}")
                    except Exception as e:
                        log_error(f"❌ Delete failed: {e}")
                    return
                
                # User messages - just count them
                if manager.total_messages_received % 20 == 0:
                    log_info(f"👤 User messages processed: {manager.total_messages_received}")
                    
            except Exception as e:
                log_error(f"❌ Message handler error: {e}")

        # ⭐ COMMANDS
        @client.on_message(filters.command("start") & filters.private)
        async def start_command(c, message: Message):
            await message.reply_text("🤖 ULTIMATE BOT ACTIVE - SIMPLIFIED MODE")

        @client.on_message(filters.command("status") & filters.private)
        async def status_command(c, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            status_text = f"""
🤖 **BOT STATUS - SIMPLIFIED MODE**

📊 **Statistics:**
• Online Cycles: {manager.online_status_count}
• Messages Received: {manager.total_messages_received}

🛡️ **Groups Access:**
"""
            
            if allowed_groups:
                for group_id in allowed_groups:
                    status_text += f"• {group_id}: ✅ ACCESSIBLE\n"
            else:
                status_text += "• ❌ NO GROUPS ACCESSIBLE\n"
            
            status_text += f"\n💡 **Instruction:**\nAdd bot to groups with admin permissions to enable full functionality."
            
            await message.reply_text(status_text)

        @client.on_message(filters.command("scan") & filters.private)
        async def scan_command(c, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            await message.reply_text("🔍 Scanning for accessible groups...")
            accessible_groups = await find_accessible_groups()
            
            if accessible_groups:
                await message.reply_text(f"✅ Found {len(accessible_groups)} accessible groups!")
            else:
                await message.reply_text("❌ No groups accessible. Please add bot to groups.")

        # ----------------- MAIN STARTUP -----------------
        log_info("🚀 STARTING TELEGRAM CLIENT...")
        await client.start()
        log_info("✅ TELEGRAM CLIENT STARTED")
        
        bot_me = await client.get_me()
        log_info(f"🤖 BOT IDENTITY: {bot_me.first_name} (@{bot_me.username})")
        
        # SCAN FOR ACCESSIBLE GROUPS
        await find_accessible_groups()
        
        # START BACKGROUND TASKS
        log_info("🔄 STARTING BACKGROUND TASKS...")
        asyncio.create_task(maintain_online())
        asyncio.create_task(simple_watchdog())
        
        if allowed_groups:
            log_info("🎉 BOT OPERATIONAL WITH GROUP ACCESS!")
        else:
            log_info("⚠️ BOT RUNNING BUT NO GROUP ACCESS - Add bot to groups for full functionality")
        
        # KEEP RUNNING
        while session_data['active']:
            await asyncio.sleep(1)
            
    except Exception as e:
        log_critical(f"💥 FATAL ERROR: {e}")
        tb = traceback.format_exc()
        log_critical(f"Traceback: {tb}")
    finally:
        session_data['active'] = False
        try:
            await client.stop()
        except:
            pass
        log_info("🛑 Telegram client stopped")

# 🚀 MAIN EXECUTION
async def main():
    log_info("🎬 STARTING BOT - SIMPLIFIED VERSION")
    await start_telegram()

if __name__ == "__main__":
    def signal_handler(signum, frame):
        log_info(f"🛑 Received signal {signum}, shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_info("🛑 Keyboard interrupt received, shutting down...")
    except Exception as e:
        log_critical(f"💥 Main execution failed: {e}")
