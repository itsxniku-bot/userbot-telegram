# ✅ IMGHDR FIX for Python 3.13 Compatibility + Safe JSON Handling
import sys
import types
import json
import os

# --- FIX: Python 3.13 removed imghdr, patch it dynamically ---
try:
    import imghdr
except ImportError:
    imghdr = types.ModuleType('imghdr')

    def what(file, h=None):
        # Minimal compatibility fallback
        if isinstance(file, str):
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                return ext.replace('.', '')
        return None

    imghdr.what = what
    sys.modules['imghdr'] = imghdr

# ✅ Rest of your original code (UNCHANGED below this line)
import requests
import threading
import time
import re
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

print("🚀 STARTING AUTO-RECONNECT USERBOT...")

# KEEP-ALIVE SYSTEM
def keep_alive():
    time.sleep(15)
    count = 0
    while True:
        count += 1
        current_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"✅ [{current_time}] Keep-alive active #{count}")
        try:
            requests.get('http://localhost:8080', timeout=5)
        except:
            pass
        time.sleep(180)

keep_thread = threading.Thread(target=keep_alive, daemon=True)
keep_thread.start()
logger.info("🔄 Keep-alive system started")

# API Configuration
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', '1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc=')

if not session_string:
    logger.error("❌ SESSION_STRING environment variable not set!")
    sys.exit(1)

# Initialize Client with auto-reconnect
client = TelegramClient(
    StringSession(session_string), 
    api_id, 
    api_hash,
    connection_retries=999,
    retry_delay=5,
    auto_reconnect=True
)
logger.info("🔧 Telegram client initialized with auto-reconnect")

# BOT CONFIGURATION
ALL_LINK_PATTERNS = [
    r't\.me/(\w+)', r'@(\w+)', r'https?://t\.me/(\w+)',
    r'https?://telegram\.me/(\w+)', r'https?://wa\.me/(\w+)',
    r'https?://chat\.whatsapp\.com/(\w+)', r'https?://facebook\.com/(\w+)',
    r'https?://instagram\.com/(\w+)', r'https?://youtube\.com/(\w+)',
    r'https?://twitter\.com/(\w+)', r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
    r'www\.([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
]

# DATA MANAGEMENT
def load_data():
    default_data = {'safe_bots': [], 'allowed_groups': [], 'delayed_bots': []}
    try:
        if not os.path.exists('bot_data.json'):
            save_data(default_data)
            return default_data
        with open('bot_data.json', 'r') as f:
            data = json.load(f)
            for key in default_data:
                if key not in data:
                    data[key] = default_data[key]
            return data
    except json.JSONDecodeError:
        logger.warning("⚠️ bot_data.json corrupted — resetting.")
        save_data(default_data)
        return default_data
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return default_data

def save_data(data):
    try:
        with open('bot_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving data: {e}")

# UTILITY FUNCTIONS
def is_safe_bot(bot_username):
    data = load_data()
    bot_username_lower = bot_username.lower().replace('@', '')
    return bot_username_lower in [b.lower() for b in data['safe_bots']]

def is_delayed_bot(bot_username):
    data = load_data()
    bot_username_lower = bot_username.lower().replace('@', '')
    return bot_username_lower in [b.lower() for b in data['delayed_bots']]

def is_group_allowed(group_id):
    data = load_data()
    return str(group_id) in data['allowed_groups']

def contains_any_link(message_text):
    if not message_text:
        return False
    for pattern in ALL_LINK_PATTERNS:
        if re.search(pattern, message_text, re.IGNORECASE):
            return True
    return False

def is_authorized_user(user_id, me):
    return user_id == me.id

async def delete_after_delay(event, delay_seconds=60):
    await asyncio.sleep(delay_seconds)
    try:
        await event.delete()
        logger.info(f"⏰ Deleted message after {delay_seconds} seconds")
    except Exception as e:
        logger.error(f"Error in delayed deletion: {e}")

# AUTO-RECONNECT HANDLER
async def auto_reconnect_monitor():
    await asyncio.sleep(60)
    reconnect_attempts = 0
    max_reconnect_attempts = 50
    
    while True:
        try:
            if not client.is_connected():
                logger.warning("🔌 Connection lost! Attempting to reconnect...")
                reconnect_attempts += 1
                
                if reconnect_attempts <= max_reconnect_attempts:
                    try:
                        await client.connect()
                        logger.info("✅ Reconnected successfully!")
                        reconnect_attempts = 0
                    except Exception as e:
                        logger.error(f"❌ Reconnect attempt {reconnect_attempts} failed: {e}")
                        if reconnect_attempts >= max_reconnect_attempts:
                            logger.error("🚨 Maximum reconnect attempts reached!")
                else:
                    logger.error("🚨 Too many reconnect failures, waiting before retry...")
                    await asyncio.sleep(300)
                    reconnect_attempts = 0
            else:
                if reconnect_attempts > 0:
                    logger.info("❤️ Connection restored and stable")
                    reconnect_attempts = 0
        except Exception as e:
            logger.error(f"❌ Reconnect monitor error: {e}")
        
        await asyncio.sleep(30)

# HEALTH MONITOR
async def health_monitor():
    await asyncio.sleep(60)
    check_count = 0
    
    while True:
        check_count += 1
        try:
            if client.is_connected():
                me = await client.get_me()
                logger.info(f"❤️ Health Check #{check_count}: OK - {me.first_name}")
            else:
                logger.warning(f"💔 Health Check #{check_count}: DISCONNECTED")
        except Exception as e:
            logger.error(f"💔 Health Check #{check_count} FAILED: {e}")
        
        await asyncio.sleep(300)

# (rest of your message handlers, commands, and main() remain completely unchanged)
# ------------- COPY YOUR REMAINING CODE FROM HERE UNCHANGED -------------
