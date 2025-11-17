print("🔥 ULTIMATE BOT STARTING - MAXIMUM ONLINE STRENGTH...")

import asyncio
import multiprocessing
import re
import traceback
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, ChannelPrivate, PeerIdInvalid
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

# Load data - SIRF 2 GROUPS RAKHO
allowed_groups = {"-1002382070176", "-1002497459144"}  # Direct set karo
safe_bots = load_data(SAFE_BOTS_FILE)
delayed_bots = load_data(DELAYED_BOTS_FILE)
peer_status = load_peer_status()

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
log_info(f"📡 Peer Status: {peer_status}")

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

# 🔥 COMPLETE MESSAGE CAPTURE MANAGER
class CompleteCaptureManager:
    def __init__(self):
        self.private_group_id = "-1002497459144"
        self.public_group_id = "-1002382070176"
        self.private_delete_count = 0
        self.public_delete_count = 0
        self.users_ignored_count = 0
        self.private_delete_failures = 0
        self.public_delete_failures = 0
        self.private_access_checked = False
        self.private_has_admin = False
        self.peer_activated = peer_status.get("private_peer_activated", False)
        self.peer_activation_time = peer_status.get("last_activation", None)
        
        # MESSAGE TRACKING
        self.total_messages_received = 0
        self.last_message_time = 0
        self.message_tracking = {}
        
        # INSTANT DELETE SETTINGS
        self.last_peer_maintenance = 0
        self.peer_maintenance_interval = 30  # 30 seconds - EXTREME PEER MAINTENANCE
        self.force_reconnect = False
        self.peer_recovery_attempts = 0
        
        # SAB TARAH KE LINKS PATTERNS
        self.all_link_patterns = [
            'http://', 'https://', 't.me/', 'telegram.me/', 'tg://',
            'facebook.com/', 'instagram.com/', 'twitter.com/', 'youtube.com/',
            'drive.google.com/', 'mega.nz/', 'dropbox.com/', 'bit.ly/',
            '.com/', '.org/', '.net/', '.in/', '@'
        ]
        
    def contains_any_links_or_mentions(self, text):
        """Check if text contains any links or mentions"""
        if not text:
            return False
            
        text_lower = text.lower()
        for pattern in self.all_link_patterns:
            if pattern in text_lower:
                return True
        return False

# 🔥 TELEGRAM BOT - MAXIMUM ONLINE STRENGTH
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - MAXIMUM ONLINE STRENGTH...")
    
    # ✅ SESSION DATA
    session_data = {'active': True}

    # Initialize manager
    manager = CompleteCaptureManager()

    try:
        # Use 'client' (not 'app') for the Pyrogram Client to avoid name collisions
        client = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # ----------------------------- MAXIMUM ONLINE STRENGTH FUNCTIONS -----------------------------
        
        # ⭐ ULTRA-STRONG ONLINE MODULE (Multiple API Calls)
        async def stay_online_ultra():
            """MAXIMUM ONLINE STRENGTH - Multiple API calls from different methods"""
            online_cycle = 0
            api_methods = [
                # Basic API calls
                lambda: client.get_me(),
                lambda: client.get_users("me"),
                lambda: client.get_chat("me"),
                
                # Profile related
                lambda: client.get_profile_photos("me", limit=1),
                
                # Account related  
                lambda: client.get_account_ttl(),
                
                # Advanced API calls (but safe)
                lambda: client.invoke(Client.invoke(pyrogram.raw.functions.account.GetAccountTTL())),
                lambda: client.invoke(Client.invoke(pyrogram.raw.functions.users.GetUsers(id=[await client.resolve_peer("me")]))),
            ]
            
            while True:
                try:
                    online_cycle += 1
                    
                    # MULTIPLE API CALLS IN EACH CYCLE
                    successful_calls = 0
                    for i, api_method in enumerate(api_methods):
                        try:
                            await api_method()
                            successful_calls += 1
                            # Small delay between calls
                            if i < len(api_methods) - 1:
                                await asyncio.sleep(0.5)
                        except Exception as e:
                            log_info(f"⚠️ API call {i} failed: {e}")
                    
                    touch_activity()
                    
                    if online_cycle % 10 == 0:  # Log every 10 cycles
                        log_info(f"🟢 ULTRA-ONLINE: Cycle #{online_cycle} - {successful_calls}/{len(api_methods)} API calls successful")

                except Exception as e:
                    tb = traceback.format_exc()
                    log_error(f"❌ Ultra-online error: {repr(e)}\n{tb}")

                # SHORTER INTERVAL - 8 SECONDS
                await asyncio.sleep(8)

        # ⭐ EXTREME PEER MAINTENANCE
        async def maintain_peers_extreme():
            """EXTREME PEER MAINTENANCE - Har 20 seconds mein"""
            extreme_count = 0
            while session_data['active']:
                try:
                    extreme_count += 1
                    
                    # HAR GROUP KA EXTREME PEER CHECK
                    for group_id in allowed_groups:
                        try:
                            # MULTIPLE PEER ACTIVITY METHODS
                            chat = await client.get_chat(group_id)
                            
                            # Chat history access
                            try:
                                async for msg in client.get_chat_history(group_id, limit=1):
                                    break
                            except: pass
                            
                            # Chat members access  
                            try:
                                async for member in client.get_chat_members(group_id, limit=1):
                                    break
                            except: pass
                            
                            if extreme_count % 15 == 0:  # Har 5 minutes log
                                log_info(f"🔗 EXTREME PEER ACTIVE: {getattr(chat,'title', group_id)}")
                                
                        except (ChannelPrivate, PeerIdInvalid) as e:
                            log_error(f"❌ EXTREME PEER LOST: {group_id}")
                            # IMMEDIATE AGGRESSIVE RECONNECT
                            await force_peer_connection_aggressive(group_id)
                        except Exception as e:
                            log_info(f"⚠️ Extreme peer check: {group_id} - {e}")
                    
                    touch_activity()
                    await asyncio.sleep(20)  # HAR 20 SECONDS MEIN - EXTREME FREQUENCY
                    
                except Exception as e:
                    log_error(f"❌ Extreme peer maintenance error: {e}")
                    await asyncio.sleep(10)

        async def force_peer_connection_aggressive(group_id):
            """AGGRESSIVE PEER CONNECTION - Multiple methods instantly"""
            try:
                log_info(f"🔗 AGGRESSIVE PEER CONNECTION: {group_id}")
                
                aggressive_methods = [
                    ("Get Chat", lambda: client.get_chat(group_id)),
                    ("Chat History", lambda: client.get_chat_history(group_id, limit=2)),
                    ("Chat Members", lambda: client.get_chat_members(group_id, limit=2)),
                    ("Send Chat Action", lambda: client.send_chat_action(group_id, "typing")),
                ]
                
                success_count = 0
                for method_name, method_func in aggressive_methods:
                    try:
                        if method_name == "Send Chat Action":
                            await method_func()
                            await asyncio.sleep(0.3)  # Typing action ke liye thoda wait
                            await client.send_chat_action(group_id, "cancel")
                        else:
                            result = await method_func()
                            if method_name == "Get Chat":
                                log_info(f"✅ Aggressive peer: {getattr(result,'title', 'unknown')}")
                            else:
                                async for item in result:
                                    break
                        
                        success_count += 1
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        log_info(f"⚠️ Aggressive {method_name} failed: {e}")

                log_info(f"✅ AGGRESSIVE PEER: {success_count}/{len(aggressive_methods)} methods successful")
                return success_count > 0
                
            except Exception as e:
                log_error(f"❌ Aggressive peer connection failed: {e}")
                return False

        async def activate_permanent_private_group_peer(client_obj, private_group_id):
            try:
                log_info("🔄 ULTRA PERMANENT PEER: Activating with maximum strength...")
                
                # ULTRA STRONG PEER ACTIVATION
                connection_methods = [
                    ("Get Chat", lambda: client_obj.get_chat(private_group_id)),
                    ("Chat History", lambda: client_obj.get_chat_history(private_group_id, limit=3)),
                    ("Chat Members", lambda: client_obj.get_chat_members(private_group_id, limit=3)),
                    ("Send Typing", lambda: client_obj.send_chat_action(private_group_id, "typing")),
                ]
                
                success_count = 0
                for method_name, method_func in connection_methods:
                    try:
                        if method_name == "Send Typing":
                            await method_func()
                            await asyncio.sleep(0.5)
                            await client_obj.send_chat_action(private_group_id, "cancel")
                        else:
                            result = await method_func()
                            if method_name == "Get Chat":
                                log_info(f"✅ Ultra peer: {getattr(result,'title', 'unknown')}")
                            else:
                                count = 0
                                async for item in result:
                                    count += 1
                                    if count >= 2: break
                        
                        success_count += 1
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        log_info(f"⚠️ Ultra {method_name} failed: {e}")

                if success_count >= 2:
                    manager.peer_activated = True
                    manager.peer_activation_time = time.time()
                    manager.peer_recovery_attempts = 0
                    
                    peer_status.update({
                        "private_peer_activated": True,
                        "last_activation": manager.peer_activation_time,
                        "group_id": private_group_id
                    })
                    save_peer_status(peer_status)
                    log_info("🟢 ULTRA PERMANENT PEER ACTIVATED — MAXIMUM STRENGTH")
                    return True
                else:
                    log_error("❌ Ultra peer activation failed")
                    return False
                    
            except Exception as e:
                log_error(f"❌ ULTRA PERMANENT PEER ACTIVATION FAILED: {e}")
                return False

        async def instant_delete_ultra(message_obj):
            """ULTRA DELETE with maximum recovery"""
            chat_id = message_obj.chat.id
            message_id = message_obj.id
            is_private = str(chat_id) == manager.private_group_id
            
            try:
                # METHOD 1: Direct delete (fastest)
                await message_obj.delete()
                
                if is_private:
                    manager.private_delete_count += 1
                    log_info(f"🚀 ULTRA PRIVATE DELETE: {message_id}")
                else:
                    manager.public_delete_count += 1
                    log_info(f"🚀 ULTRA PUBLIC DELETE: {message_id}")
                return True

            except Exception as e:
                log_error(f"❌ Ultra delete failed: {e}")
                
                # ULTRA RECOVERY ATTEMPT
                manager.peer_recovery_attempts += 1
                log_info(f"🔄 ULTRA RECOVERY ATTEMPT #{manager.peer_recovery_attempts} for {chat_id}")
                
                # AGGRESSIVE PEER RECOVERY
                recovery_success = await force_peer_connection_aggressive(str(chat_id))
                
                if recovery_success:
                    log_info("✅ Ultra peer recovered, retrying delete...")
                    try:
                        # METHOD 2: Retry delete after recovery
                        await message_obj.delete()
                        if is_private:
                            manager.private_delete_count += 1
                        else:
                            manager.public_delete_count += 1
                        log_info(f"✅ ULTRA DELETE AFTER RECOVERY: {message_id}")
                        return True
                    except Exception as e2:
                        log_error(f"❌ Ultra delete after recovery failed: {e2}")
                
                # METHOD 3: Final ultra attempt
                try:
                    chat = await client.get_chat(chat_id)
                    await client.delete_messages(chat.id, message_id)
                    
                    if is_private:
                        manager.private_delete_count += 1
                        log_info(f"✅ ULTRA RESOLVE DELETE PRIVATE: {message_id}")
                    else:
                        manager.public_delete_count += 1
                        log_info(f"✅ ULTRA RESOLVE DELETE PUBLIC: {message_id}")
                    return True
                except Exception as e3:
                    log_error(f"❌ Ultra resolve delete failed: {e3}")
                    
                    if is_private:
                        manager.private_delete_failures += 1
                    else:
                        manager.public_delete_failures += 1
                    
                    # TRIGGER ULTRA RECONNECT
                    manager.force_reconnect = True
                    return False

        async def delete_after_delay_ultra(message_obj, seconds):
            await asyncio.sleep(seconds)
            await instant_delete_ultra(message_obj)

        async def maintain_permanent_peer_ultra():
            current_time = time.time()
            if not manager.peer_activated:
                return False
                
            if current_time - manager.last_peer_maintenance < manager.peer_maintenance_interval and not manager.force_reconnect:
                return True
                
            try:
                log_info("🔧 ULTRA PEER MAINTENANCE: Extreme group checking...")
                
                # ULTRA CHECK ALL GROUPS
                for group_id in allowed_groups:
                    try:
                        chat = await client.get_chat(group_id)
                        # Additional peer activity
                        try:
                            await client.send_chat_action(group_id, "typing")
                            await asyncio.sleep(0.2)
                            await client.send_chat_action(group_id, "cancel")
                        except: pass
                        
                        log_info(f"✅ Ultra peer active: {getattr(chat,'title', 'unknown')}")
                    except Exception as e:
                        log_error(f"❌ Ultra peer check failed for {group_id}: {e}")
                        # ULTRA AUTO-RECOVER
                        await force_peer_connection_aggressive(group_id)
                
                manager.last_peer_maintenance = current_time
                manager.force_reconnect = False
                return True
                
            except Exception as e:
                log_error(f"❌ Ultra peer maintenance failed: {e}")
                manager.force_reconnect = True
                return False

        async def check_private_group_admin():
            try:
                chat = await client.get_chat(manager.private_group_id)
                me = await client.get_me()
                member = await client.get_chat_member(manager.private_group_id, me.id)
                can_delete = False
                if hasattr(member, "privileges") and member.privileges:
                    can_delete = getattr(member.privileges, "can_delete_messages", False)
                if can_delete:
                    manager.private_has_admin = True
                    log_info("✅ PRIVATE GROUP: Bot has DELETE permissions")
                else:
                    manager.private_has_admin = False
                    log_error("❌ PRIVATE GROUP: Bot MISSING DELETE permissions")
                manager.private_access_checked = True
                return manager.private_has_admin
            except Exception as e:
                log_error(f"❌ Admin check failed: {e}")
                manager.private_access_checked = True
                return False

        async def instant_keep_alive_ultra():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    await client.get_me()
                    
                    # Every 5th keep-alive, do ultra peer maintenance
                    if keep_alive_count % 5 == 0:
                        await maintain_permanent_peer_ultra()
                        log_info(f"💓 Ultra Keep-Alive #{keep_alive_count} - Peer Maintenance")
                    elif keep_alive_count % 20 == 0:
                        log_info(f"💓 Ultra Keep-Alive #{keep_alive_count}")
                    
                    touch_activity()
                except Exception as e:
                    log_error(f"⚠️ Ultra Keep-Alive Failed: {e}")
                await asyncio.sleep(25)  # 25 seconds interval

        async def complete_capture_watchdog_ultra():
            watchdog_count = 0
            while True:
                try:
                    watchdog_count += 1
                    idle = time.time() - last_activity
                    
                    if watchdog_count % 8 == 0:
                        log_info(f"🐕 ULTRA WATCHDOG - Idle: {int(idle)}s, Msgs: {manager.total_messages_received}, Deletes: {manager.private_delete_count + manager.public_delete_count}, Recovery: {manager.peer_recovery_attempts}")
                    
                    # Ultra peer maintenance every 10 watchdog cycles
                    if manager.peer_activated and watchdog_count % 10 == 0:
                        await maintain_permanent_peer_ultra()
                    
                    # Agar peer recovery attempts zyada hai to ultra force reconnect
                    if manager.peer_recovery_attempts >= 2:
                        log_info("🔄 ULTRA WATCHDOG: Force reconnecting all peers...")
                        for group_id in allowed_groups:
                            await force_peer_connection_aggressive(group_id)
                        manager.peer_recovery_attempts = 0
                    
                    if idle > 240:  # 4 minutes idle tolerance
                        log_error(f"⚠️ ULTRA WATCHDOG: Restarting - No activity for {int(idle)}s")
                        for h in logger.handlers:
                            try:
                                h.flush()
                            except:
                                pass
                        try:
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        except Exception as e:
                            log_error(f"Ultra watchdog restart failed: {e}")
                        await asyncio.sleep(30)
                    else:
                        await asyncio.sleep(8)  # 8 seconds watchdog interval
                except Exception as e:
                    log_error(f"Ultra watchdog error: {e}")
                    await asyncio.sleep(8)

        async def check_group_access():
            results = {'private': False, 'public': False, 'private_admin': False}
            try:
                for group_id in allowed_groups:
                    try:
                        chat = await client.get_chat(group_id)
                        if group_id == manager.private_group_id:
                            results['private'] = True
                            log_info(f"✅ Private Group Access: {getattr(chat,'title', 'unknown')}")
                            results['private_admin'] = await check_private_group_admin()
                        else:
                            results['public'] = True
                            log_info(f"✅ Public Group Access: {chat.title}")
                    except Exception as e:
                        if group_id == manager.private_group_id:
                            log_error(f"❌ Private Group Access Failed: {e}")
                        else:
                            log_error(f"❌ Public Group Access Failed: {e}")
            except Exception as e:
                log_error(f"Group access check failed: {e}")
            return results

        # ----------------- ULTRA MESSAGE HANDLER -----------------
        @client.on_message(filters.group)
        async def complete_capture_handler_ultra(c, message: Message):
            try:
                touch_activity()
                manager.total_messages_received += 1
                manager.last_message_time = time.time()
                group_id = str(message.chat.id)
                is_private = group_id == manager.private_group_id
                
                # ULTRA FAST MESSAGE PROCESSING
                username = "unknown"; is_bot = False; detection_reason = "unknown"
                if message.from_user:
                    u = message.from_user
                    username = (getattr(u, "username", None) or f"user_{getattr(u,'id','unknown')}").lower()
                    is_bot = bool(getattr(u, "is_bot", False))
                    detection_reason = "from_user"
                else:
                    sender_chat = getattr(message, "sender_chat", None)
                    if sender_chat:
                        username = (getattr(sender_chat, "username", None) or getattr(sender_chat, "title", None) or f"sender_{getattr(sender_chat,'id','unknown')}").lower()
                        if getattr(message, "via_bot", None) or getattr(message, "via_bot_id", None):
                            is_bot = True; detection_reason = "sender_chat_via_bot"
                        else:
                            detection_reason = "sender_chat"
                    else:
                        fwd = getattr(message, "forward_from", None)
                        if fwd:
                            username = (getattr(fwd, "username", None) or f"user_{getattr(fwd,'id','unknown')}").lower()
                            is_bot = bool(getattr(fwd, "is_bot", False)); detection_reason = "forward_from"
                if not is_bot and getattr(message, "via_bot", None):
                    is_bot = True; detection_reason = "via_bot"
                message_text = message.text or message.caption or ""
                
                log_info(f"[ULTRA MSG #{manager.total_messages_received}] group={group_id} user={username} bot={is_bot} text={message_text[:60]}")
                
                if group_id not in allowed_groups:
                    return
                
                try:
                    current_me = await client.get_me()
                    if message.from_user and message.from_user.id == current_me.id:
                        return
                except Exception as e:
                    log_error(f"❌ Self check failed: {e}")
                
                if not is_bot:
                    manager.users_ignored_count += 1
                    return
                
                username_clean = username.lstrip("@").lower()
                
                if username_clean in safe_bots:
                    return
                
                has_links_or_mentions = manager.contains_any_links_or_mentions(message_text)
                
                if username_clean in delayed_bots:
                    if has_links_or_mentions:
                        await instant_delete_ultra(message)
                    else:
                        asyncio.create_task(delete_after_delay_ultra(message, 3))  # 3 seconds delay
                    return
                
                await instant_delete_ultra(message)

            except Exception as e:
                log_error(f"❌ Ultra Capture Handler error: {e}")
                touch_activity()

        # ---------------------- ULTRA STARTUP ----------------------
        log_info("🔗 Connecting to Telegram - MAXIMUM ONLINE STRENGTH...")
        await client.start()

        # ⭐ START ULTRA ONLINE MODULE
        asyncio.get_event_loop().create_task(stay_online_ultra())
        log_info("🟢 ULTRA ONLINE MODULE: ACTIVATED (8s intervals)")

        me = await client.get_me()
        log_info(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")

        # ⭐ START EXTREME PEER MAINTENANCE
        asyncio.get_event_loop().create_task(maintain_peers_extreme())
        log_info("🔗 EXTREME PEER MAINTENANCE: ACTIVATED (20s intervals)")

        # ULTRA PEER ACTIVATION ON STARTUP
        if not manager.peer_activated:
            log_info("🚀 ULTRA STARTUP: Activating permanent peers with maximum strength...")
            await activate_permanent_private_group_peer(client, manager.private_group_id)
        else:
            log_info("🔗 ULTRA STARTUP: Permanent peers already activated")

        # AGGRESSIVE PEER CONNECTIONS FOR ALL GROUPS
        for group_id in allowed_groups:
            await force_peer_connection_aggressive(group_id)

        access = await check_group_access()
        
        # ⭐ START ULTRA BACKGROUND TASKS
        keep_alive_task = asyncio.create_task(instant_keep_alive_ultra())
        watchdog_task = asyncio.create_task(complete_capture_watchdog_ultra())

        log_info("💓 ULTRA Keep-Alive: ACTIVE (25s)")
        log_info("🚀 ULTRA Message Capture: READY")
        log_info("🔗 EXTREME Peer Maintenance: ACTIVE (20s)")
        log_info("🟢 ULTRA Online: ACTIVE (8s)")

        try:
            await client.send_message("me", f"""
✅ **BOT STARTED - MAXIMUM ONLINE STRENGTH!**

🎯 **ULTRA FEATURES:**
• Every Message Logged ✅  
• Instant Delete 🚀
• **MAXIMUM ONLINE STRENGTH** 🔥
• Extreme Peer Maintenance (20s) 🔗
• Ultra Online (8s intervals) 🟢
• Aggressive Peer Recovery 🔄

📊 **ULTRA STATUS:**
• Private Group: {'✅ ACCESSIBLE' if access['private'] else '❌ NOT ACCESSIBLE'}
• Private Admin: {'✅ DELETE RIGHTS' if access['private_admin'] else '❌ NO RIGHTS'}
• Peer Activated: {'✅ ULTRA STRENGTH' if manager.peer_activated else '❌ NEEDS ACTIVATION'}
• Online Intervals: 8 SECONDS 🟢
• Peer Intervals: 20 SECONDS 🔗

💡 **Your bot is now at MAXIMUM ONLINE STRENGTH!**

**Status: ULTRA ACTIVE** 🔥
            """)
        except Exception as e:
            log_error(f"Ultra startup DM failed: {e}")

        log_info("🤖 ULTRA BOT READY - Maximum Online Strength Active!")

        # Keep running
        try:
            while session_data['active']:
                await asyncio.sleep(1)
        except:
            pass
        finally:
            session_data['active'] = False
            keep_alive_task.cancel()
            watchdog_task.cancel()
            await client.stop()

    except Exception as e:
        log_error(f"❌ Ultra Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    log_info("🚀 ULTRA BOT STARTING - MAXIMUM ONLINE STRENGTH...")

    try:
        asyncio.run(main())
    except Exception as e:
        log_critical(f"ULTRA CRASH: {e}")
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
