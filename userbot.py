print("🔥 ULTIMATE BOT STARTING - PERMANENT ONLINE STATUS...")

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

# 🔥 PERMANENT ONLINE STATUS MANAGER
class PermanentOnlineManager:
    def __init__(self):
        self.online_status_count = 0
        self.last_status_update = 0
        self.typing_actions_count = 0
        self.typing_groups = {}
        
    async def update_online_status(self, client):
        """Update bot's online status - makes bot show as 'online'"""
        try:
            self.online_status_count += 1
            
            # Multiple methods to show online status
            methods = [
                self._method_get_me,
                self._method_get_users,
                self._method_send_chat_action,
                self._method_update_status
            ]
            
            success_count = 0
            for method in methods:
                try:
                    await method(client)
                    success_count += 1
                    await asyncio.sleep(0.5)
                except Exception as e:
                    log_info(f"⚠️ Online status method failed: {e}")
            
            if self.online_status_count % 10 == 0:
                log_info(f"🟢 PERMANENT ONLINE: Cycle #{self.online_status_count} - {success_count}/{len(methods)} methods")
                
            self.last_status_update = time.time()
            return True
            
        except Exception as e:
            log_error(f"❌ Online status update failed: {e}")
            return False
    
    async def _method_get_me(self, client):
        """Basic API call - shows activity"""
        await client.get_me()
    
    async def _method_get_users(self, client):
        """Another API call for activity"""
        await client.get_users("me")
    
    async def _method_send_chat_action(self, client):
        """Send typing action to groups - shows real-time activity"""
        for group_id in allowed_groups:
            try:
                await client.send_chat_action(group_id, "typing")
                self.typing_actions_count += 1
                
                # Track typing per group
                if group_id not in self.typing_groups:
                    self.typing_groups[group_id] = 0
                self.typing_groups[group_id] += 1
                
                # Small delay between groups
                await asyncio.sleep(0.3)
            except Exception as e:
                log_info(f"⚠️ Typing action failed for {group_id}: {e}")
    
    async def _method_update_status(self, client):
        """Update profile status (if possible)"""
        try:
            # This method tries to update last seen time
            await client.invoke("account.updateStatus", offline=False)
        except:
            # Fallback to simple API call
            await client.get_me()

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
        
        # GROUP ACCESS STATUS
        self.group_access_status = {}
        
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

# 🔥 TELEGRAM BOT - PERMANENT ONLINE STATUS
async def start_telegram():
    log_info("🔗 Starting Telegram Bot - PERMANENT ONLINE STATUS...")
    
    # ✅ SESSION DATA
    session_data = {'active': True}

    # Initialize managers
    manager = CompleteCaptureManager()
    online_manager = PermanentOnlineManager()

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
        
        # ----------------------------- PERMANENT ONLINE STATUS FUNCTIONS -----------------------------
        
        # ⭐ PERMANENT ONLINE STATUS MODULE
        async def maintain_permanent_online():
            """MAINTAIN PERMANENT ONLINE STATUS - Har 15 seconds mein"""
            online_cycle = 0
            
            while session_data['active']:
                try:
                    online_cycle += 1
                    
                    # UPDATE ONLINE STATUS
                    await online_manager.update_online_status(client)
                    
                    touch_activity()
                    
                    if online_cycle % 20 == 0:  # Har 5 minutes detailed log
                        log_info(f"🔵 PERMANENT ONLINE: Cycle #{online_cycle} - Typing Actions: {online_manager.typing_actions_count}")

                except Exception as e:
                    log_error(f"❌ Permanent online error: {e}")

                # 15 SECOND INTERVAL - FREQUENT UPDATES
                await asyncio.sleep(15)

        # ⭐ ULTRA-STRONG ONLINE MODULE (Multiple API Calls)
        async def stay_online_ultra():
            """MAXIMUM ONLINE STRENGTH - Multiple API calls from different methods"""
            online_cycle = 0
            
            while session_data['active']:
                try:
                    online_cycle += 1
                    
                    # MULTIPLE API CALLS IN EACH CYCLE
                    successful_calls = 0
                    
                    # Call 1: Basic API call
                    try:
                        await client.get_me()
                        successful_calls += 1
                    except: pass
                    
                    await asyncio.sleep(0.3)
                    
                    # Call 2: Another API call
                    try:
                        await client.get_users("me")
                        successful_calls += 1
                    except: pass
                    
                    await asyncio.sleep(0.3)
                    
                    # Call 3: Chat API call
                    try:
                        await client.get_chat("me")
                        successful_calls += 1
                    except: pass
                    
                    await asyncio.sleep(0.3)
                    
                    # Call 4: Profile photos
                    try:
                        await client.get_profile_photos("me", limit=1)
                        successful_calls += 1
                    except: pass
                    
                    await asyncio.sleep(0.3)
                    
                    # Call 5: Account TTL
                    try:
                        await client.get_account_ttl()
                        successful_calls += 1
                    except: pass
                    
                    touch_activity()
                    
                    if online_cycle % 10 == 0:  # Log every 10 cycles
                        log_info(f"🟢 ULTRA-ONLINE: Cycle #{online_cycle} - {successful_calls}/5 API calls successful")

                except Exception as e:
                    log_error(f"❌ Ultra-online error: {e}")

                # SHORTER INTERVAL - 12 SECONDS
                await asyncio.sleep(12)

        # ⭐ IMPROVED PEER MAINTENANCE WITH BETTER ERROR HANDLING
        async def maintain_peers_extreme():
            """EXTREME PEER MAINTENANCE - Har 20 seconds mein"""
            extreme_count = 0
            while session_data['active']:
                try:
                    extreme_count += 1
                    
                    # HAR GROUP KA EXTREME PEER CHECK
                    for group_id in allowed_groups:
                        try:
                            # Check if we have access to this group
                            chat = await client.get_chat(group_id)
                            chat_title = getattr(chat, 'title', group_id)
                            
                            # Update access status
                            manager.group_access_status[group_id] = {
                                'accessible': True,
                                'title': chat_title,
                                'last_check': time.time()
                            }
                            
                            # Send typing action to show online status
                            try:
                                await client.send_chat_action(group_id, "typing")
                                online_manager.typing_actions_count += 1
                                await asyncio.sleep(0.2)
                                await client.send_chat_action(group_id, "cancel")
                            except Exception as e:
                                log_info(f"⚠️ Typing action failed for {chat_title}: {e}")
                                
                            if extreme_count % 15 == 0:  # Har 5 minutes log
                                log_info(f"🔗 EXTREME PEER ACTIVE: {chat_title}")
                                
                        except (ChannelPrivate, PeerIdInvalid, UserNotParticipant) as e:
                            # Update access status to failed
                            manager.group_access_status[group_id] = {
                                'accessible': False,
                                'error': str(e),
                                'last_check': time.time()
                            }
                            log_error(f"❌ NO ACCESS TO GROUP: {group_id} - {e}")
                        except Exception as e:
                            log_info(f"⚠️ Extreme peer check: {group_id} - {e}")
                    
                    touch_activity()
                    await asyncio.sleep(20)  # HAR 20 SECONDS MEIN - EXTREME FREQUENCY
                    
                except Exception as e:
                    log_error(f"❌ Extreme peer maintenance error: {e}")
                    await asyncio.sleep(10)

        async def force_peer_connection_aggressive(group_id):
            """IMPROVED AGGRESSIVE PEER CONNECTION - Better error handling"""
            try:
                log_info(f"🔗 AGGRESSIVE PEER CONNECTION ATTEMPT: {group_id}")
                
                success_count = 0
                error_messages = []
                
                # METHOD 1: Get Chat (Basic access check)
                try:
                    chat = await client.get_chat(group_id)
                    chat_title = getattr(chat, 'title', 'unknown')
                    log_info(f"✅ Aggressive peer: {chat_title}")
                    success_count += 1
                    
                    # Update access status
                    manager.group_access_status[group_id] = {
                        'accessible': True,
                        'title': chat_title,
                        'last_check': time.time()
                    }
                    
                except (ChannelPrivate, PeerIdInvalid, UserNotParticipant) as e:
                    error_messages.append(f"Get Chat Failed: {e}")
                    manager.group_access_status[group_id] = {
                        'accessible': False,
                        'error': str(e),
                        'last_check': time.time()
                    }
                except Exception as e:
                    error_messages.append(f"Get Chat Error: {e}")
                
                await asyncio.sleep(0.3)
                
                # Only try additional methods if basic access works
                if success_count > 0:
                    # METHOD 2: Chat History
                    try:
                        async for msg in client.get_chat_history(group_id, limit=2):
                            break
                        success_count += 1
                    except Exception as e:
                        error_messages.append(f"Chat History: {e}")
                    
                    await asyncio.sleep(0.3)
                    
                    # METHOD 3: Chat Members
                    try:
                        async for member in client.get_chat_members(group_id, limit=2):
                            break
                        success_count += 1
                    except Exception as e:
                        error_messages.append(f"Chat Members: {e}")
                    
                    await asyncio.sleep(0.3)
                    
                    # METHOD 4: Send Chat Action
                    try:
                        await client.send_chat_action(group_id, "typing")
                        await asyncio.sleep(0.3)
                        await client.send_chat_action(group_id, "cancel")
                        success_count += 1
                    except Exception as e:
                        error_messages.append(f"Chat Action: {e}")

                if success_count > 0:
                    log_info(f"✅ AGGRESSIVE PEER SUCCESS: {success_count}/4 methods for {group_id}")
                    return True
                else:
                    log_error(f"❌ AGGRESSIVE PEER FAILED: {group_id} - {', '.join(error_messages)}")
                    return False
                
            except Exception as e:
                log_error(f"❌ Aggressive peer connection failed: {e}")
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
                
                # Check if we have access to this group
                group_access = manager.group_access_status.get(str(chat_id), {})
                if not group_access.get('accessible', False):
                    log_error(f"❌ No access to group {chat_id}, skipping delete")
                    if is_private:
                        manager.private_delete_failures += 1
                    else:
                        manager.public_delete_failures += 1
                    return False
                
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

        async def instant_keep_alive_ultra():
            keep_alive_count = 0
            while session_data['active']:
                keep_alive_count += 1
                try:
                    await client.get_me()
                    
                    # Every 5th keep-alive, do ultra peer maintenance
                    if keep_alive_count % 5 == 0:
                        # Send typing actions to all groups
                        for group_id in allowed_groups:
                            try:
                                await client.send_chat_action(group_id, "typing")
                                online_manager.typing_actions_count += 1
                                await asyncio.sleep(0.2)
                            except: pass
                        log_info(f"💓 Ultra Keep-Alive #{keep_alive_count} - Typing Actions Sent")
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
                        # Log group access status
                        access_status = {}
                        for group_id in allowed_groups:
                            status = manager.group_access_status.get(group_id, {})
                            access_status[group_id] = status.get('accessible', 'Unknown')
                        
                        log_info(f"🐕 ULTRA WATCHDOG - Idle: {int(idle)}s, Msgs: {manager.total_messages_received}, Online Cycles: {online_manager.online_status_count}, Typing Actions: {online_manager.typing_actions_count}")
                    
                    # Force online status update every 10 watchdog cycles
                    if watchdog_count % 10 == 0:
                        await online_manager.update_online_status(client)
                    
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
                            # Check admin permissions
                            try:
                                me = await client.get_me()
                                member = await client.get_chat_member(manager.private_group_id, me.id)
                                can_delete = False
                                if hasattr(member, "privileges") and member.privileges:
                                    can_delete = getattr(member.privileges, "can_delete_messages", False)
                                if can_delete:
                                    manager.private_has_admin = True
                                    results['private_admin'] = True
                                    log_info("✅ PRIVATE GROUP: Bot has DELETE permissions")
                                else:
                                    manager.private_has_admin = False
                                    log_error("❌ PRIVATE GROUP: Bot MISSING DELETE permissions")
                                manager.private_access_checked = True
                            except Exception as e:
                                log_error(f"❌ Admin check failed: {e}")
                        else:
                            results['public'] = True
                            log_info(f"✅ Public Group Access: {chat.title}")
                    except (ChannelPrivate, PeerIdInvalid, UserNotParticipant) as e:
                        if group_id == manager.private_group_id:
                            log_error(f"❌ Private Group Access Failed: {e}")
                        else:
                            log_error(f"❌ Public Group Access Failed: {e}")
                    except Exception as e:
                        log_error(f"Group access check failed for {group_id}: {e}")
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
                
                # Check if this group is in our allowed list
                if group_id not in allowed_groups:
                    return
                
                is_private = group_id == manager.private_group_id
                
                # ULTRA FAST MESSAGE PROCESSING
                username = "unknown"
                is_bot = False
                detection_reason = "unknown"
                
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
                            is_bot = True
                            detection_reason = "sender_chat_via_bot"
                        else:
                            detection_reason = "sender_chat"
                    else:
                        fwd = getattr(message, "forward_from", None)
                        if fwd:
                            username = (getattr(fwd, "username", None) or f"user_{getattr(fwd,'id','unknown')}").lower()
                            is_bot = bool(getattr(fwd, "is_bot", False))
                            detection_reason = "forward_from"
                
                if not is_bot and getattr(message, "via_bot", None):
                    is_bot = True
                    detection_reason = "via_bot"
                
                message_text = message.text or message.caption or ""
                message_preview = message_text[:50] + "..." if len(message_text) > 50 else message_text
                
                log_info(f"[ULTRA MSG #{manager.total_messages_received}] group={group_id} user={username} bot={is_bot} reason={detection_reason} text={message_preview}")
                
                # BOT DETECTION AND HANDLING LOGIC
                if is_bot:
                    if username in safe_bots:
                        log_info(f"✅ SAFE BOT IGNORED: {username}")
                        return
                    
                    if username in delayed_bots:
                        log_info(f"⏰ DELAYED BOT: {username} - Will delete after delay")
                        asyncio.create_task(delete_after_delay_ultra(message, 3))
                        return
                    
                    # INSTANT DELETE FOR UNKNOWN BOTS
                    log_info(f"🚫 UNKNOWN BOT DETECTED: {username} - INSTANT DELETE")
                    await instant_delete_ultra(message)
                    return
                
                # USER MESSAGE HANDLING
                if not is_bot:
                    manager.users_ignored_count += 1
                    if manager.users_ignored_count % 20 == 0:
                        log_info(f"👤 User messages ignored: {manager.users_ignored_count}")
                    return
                    
            except Exception as e:
                log_error(f"❌ Ultra message handler error: {e}")

        # ----------------- STARTUP SEQUENCE -----------------
        @client.on_message(filters.command("start") & filters.private)
        async def start_command(c, message: Message):
            await message.reply_text("🤖 ULTIMATE BOT ACTIVE - PERMANENT ONLINE STATUS")

        @client.on_message(filters.command("status") & filters.private)
        async def status_command(c, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            status_text = f"""
🤖 **ULTIMATE BOT STATUS - PERMANENT ONLINE**

📊 **Message Statistics:**
• Total Messages: {manager.total_messages_received}
• Private Deletes: {manager.private_delete_count}
• Public Deletes: {manager.public_delete_count}
• Delete Failures: {manager.private_delete_failures + manager.public_delete_failures}
• Users Ignored: {manager.users_ignored_count}

🟢 **Online Status:**
• Online Cycles: {online_manager.online_status_count}
• Typing Actions: {online_manager.typing_actions_count}
• Last Update: {time.time() - online_manager.last_status_update:.1f}s ago

🔗 **Peer Status:**
• Recovery Attempts: {manager.peer_recovery_attempts}
• Force Reconnect: {manager.force_reconnect}

🛡️ **Group Access Status:**
"""
            
            for group_id in allowed_groups:
                status = manager.group_access_status.get(group_id, {})
                if status.get('accessible'):
                    status_text += f"• {status.get('title', group_id)}: ✅ ACCESSIBLE\n"
                else:
                    error = status.get('error', 'Unknown error')
                    status_text += f"• {group_id}: ❌ NO ACCESS - {error}\n"
            
            await message.reply_text(status_text)

        # ----------------- MAIN BOT STARTUP -----------------
        log_info("🚀 STARTING TELEGRAM CLIENT...")
        await client.start()
        log_info("✅ TELEGRAM CLIENT STARTED")
        
        bot_me = await client.get_me()
        log_info(f"🤖 BOT IDENTITY: {bot_me.first_name} (@{bot_me.username})")
        
        # CHECK GROUP ACCESS
        log_info("🔍 CHECKING GROUP ACCESS...")
        access_results = await check_group_access()
        
        if not access_results['private'] and not access_results['public']:
            log_error("❌ CRITICAL: Bot has no access to any groups! Please add bot to groups.")
        else:
            if access_results['private']:
                log_info("✅ PRIVATE GROUP: Access confirmed")
                if access_results['private_admin']:
                    log_info("✅ PRIVATE GROUP: Bot has admin permissions")
                else:
                    log_error("❌ PRIVATE GROUP: Bot needs admin permissions to delete messages")
            else:
                log_error("❌ PRIVATE GROUP: No access")
            
            if access_results['public']:
                log_info("✅ PUBLIC GROUP: Access confirmed")
            else:
                log_error("❌ PUBLIC GROUP: No access")
        
        # START ALL BACKGROUND TASKS - PERMANENT ONLINE FOCUS
        log_info("🔄 STARTING BACKGROUND TASKS...")
        asyncio.create_task(maintain_permanent_online())  # PRIMARY ONLINE TASK
        asyncio.create_task(stay_online_ultra())
        asyncio.create_task(maintain_peers_extreme())
        asyncio.create_task(instant_keep_alive_ultra())
        asyncio.create_task(complete_capture_watchdog_ultra())
        
        log_info("🎉 ULTIMATE BOT FULLY OPERATIONAL - PERMANENT ONLINE STATUS ACTIVATED!")
        
        # KEEP RUNNING
        while session_data['active']:
            await asyncio.sleep(1)
            
    except Exception as e:
        log_critical(f"💥 FATAL ERROR in Telegram bot: {e}")
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
    log_info("🎬 STARTING ULTIMATE BOT - MAIN EXECUTION")
    await start_telegram()

if __name__ == "__main__":
    # Signal handlers for graceful shutdown
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
        tb = traceback.format_exc()
        log_critical(f"Traceback: {tb}")
