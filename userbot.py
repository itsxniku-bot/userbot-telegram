# IMGHDR FIX - Add this at the VERY TOP
import sys
import types
try:
    import imghdr
except ImportError:
    imghdr = types.ModuleType('imghdr')
    def what(file, h=None): return None
    imghdr.what = what
    sys.modules['imghdr'] = imghdr

import requests
import threading
import time
import os
import http.server
import socketserver
import random
from datetime import datetime

# RELIABLE KEEP-ALIVE SYSTEM
def reliable_keep_alive():
    time.sleep(20)  # App properly start hone do
    
    ping_count = 0
    while True:
        try:
            ping_count += 1
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Method 1: Render URL ping
            render_url = os.environ.get('RENDER_URL')
            if render_url and 'onrender.com' in render_url:
                try:
                    response = requests.get(f"{render_url}?ping={ping_count}", timeout=10)
                    print(f"🎯 [{current_time}] Ping #{ping_count} to Render: {response.status_code}")
                except Exception as e:
                    print(f"❌ [{current_time}] Render ping failed: {e}")
            
            # Method 2: Self ping (always works)
            try:
                requests.get('http://localhost:8080', timeout=5)
                print(f"🔷 [{current_time}] Self Ping #{ping_count}: OK")
            except Exception as e:
                print(f"🔄 [{current_time}] Self ping active #{ping_count}")
            
            # Method 3: Additional backup ping
            try:
                requests.get('http://localhost:8080/health', timeout=5)
                print(f"🟢 [{current_time}] Backup Ping #{ping_count}: OK")
            except:
                pass
                
        except Exception as e:
            print(f"🚨 [{current_time}] Keep-alive critical error: {e}")
        
        # Fixed 3-minute interval (180 seconds)
        print(f"⏰ [{current_time}] Next ping in 3 minutes...")
        time.sleep(180)  # Exactly 3 minutes

# Start keep-alive in MAIN thread context
def start_keep_alive():
    keep_thread = threading.Thread(target=reliable_keep_alive, daemon=False)  # daemon=False
    keep_thread.start()
    print("🔄 RELIABLE Keep-alive system STARTED!")

# BACKGROUND ACTIVITY SIMULATOR
def background_activity():
    time.sleep(30)
    activity_count = 0
    while True:
        activity_count += 1
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"🔧 [{current_time}] Background Activity #{activity_count}")
        time.sleep(300)  # Every 5 minutes

def start_background_activity():
    activity_thread = threading.Thread(target=background_activity, daemon=True)
    activity_thread.start()
    print("🔧 Background activity STARTED!")

# APP START
print("🚀 Starting UserBot...")

# Keep-alive IMMEDIATELY start karo
start_keep_alive()
start_background_activity()

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
import json
import asyncio
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# API credentials
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', '1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc=')

if not session_string:
    logger.error("❌ SESSION_STRING not set!")
    sys.exit(1)

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Bot configuration
ALL_LINK_PATTERNS = [
    r't\.me/(\w+)', r'@(\w+)', r'https?://t\.me/(\w+)',
    r'https?://telegram\.me/(\w+)', r'https?://wa\.me/(\w+)',
    r'https?://chat\.whatsapp\.com/(\w+)', r'https?://facebook\.com/(\w+)',
    r'https?://instagram\.com/(\w+)', r'https?://youtube\.com/(\w+)',
    r'https?://twitter\.com/(\w+)', r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
    r'www\.([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
]

def load_data():
    default_data = {'safe_bots': [], 'allowed_groups': [], 'delayed_bots': []}
    if os.path.exists('bot_data.json'):
        try:
            with open('bot_data.json', 'r') as f:
                return json.load(f)
        except: pass
    return default_data

def save_data(data):
    try:
        with open('bot_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    except: pass

def is_safe_bot(bot_username):
    data = load_data()
    return bot_username.lower().replace('@', '') in [b.lower() for b in data['safe_bots']]

def is_delayed_bot(bot_username):
    data = load_data()
    return bot_username.lower().replace('@', '') in [b.lower() for b in data['delayed_bots']]

def is_group_allowed(group_id):
    data = load_data()
    return str(group_id) in data['allowed_groups']

def contains_any_link(message_text):
    if not message_text: return False
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
    except: pass

@client.on(events.NewMessage)
async def handle_all_messages(event):
    try:
        if not event.is_group or not event.sender: return
        
        group_id = str(event.chat_id)
        if not is_group_allowed(group_id): return
        
        me = await client.get_me()
        if event.sender_id == me.id: return
        
        message_text = event.message.text or event.message.caption
        
        if event.sender.bot:
            sender_username = event.sender.username
            if sender_username:
                if is_safe_bot(sender_username): return
                
                if is_delayed_bot(sender_username):
                    if contains_any_link(message_text):
                        await event.delete()
                        logger.info(f"🗑️ Deleted message with link from: {sender_username}")
                    else:
                        asyncio.create_task(delete_after_delay(event, 60))
                        logger.info(f"⏰ Scheduled deletion for: {sender_username}")
                else:
                    await event.delete()
                    logger.info(f"🗑️ Deleted message from: {sender_username}")
                return
        
        if message_text and contains_any_link(message_text):
            for pattern in ALL_LINK_PATTERNS:
                matches = re.findall(pattern, message_text)
                for match in matches:
                    if isinstance(match, str) and match.lower().endswith('bot'):
                        if not is_safe_bot(match):
                            await event.delete()
                            logger.info(f"🗑️ Deleted message with bot link: {match}")
                            return
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# Commands
@client.on(events.NewMessage(pattern=r'(?i)^!safe (@?\w+)$'))
async def add_safe_bot(event):
    me = await client.get_me()
    if not is_authorized_user(event.sender_id, me): return
    bot_username = event.pattern_match.group(1).replace('@', '')
    data = load_data()
    if bot_username.lower() not in [b.lower() for b in data['safe_bots']]:
        data['safe_bots'].append(bot_username)
        save_data(data)
        await event.reply(f"✅ @{bot_username} added to safe list!")

@client.on(events.NewMessage(pattern=r'(?i)^!delayed (@?\w+)$'))
async def add_delayed_bot(event):
    me = await client.get_me()
    if not is_authorized_user(event.sender_id, me): return
    bot_username = event.pattern_match.group(1).replace('@', '')
    data = load_data()
    if bot_username.lower() not in [b.lower() for b in data['delayed_bots']]:
        data['delayed_bots'].append(bot_username)
        save_data(data)
        await event.reply(f"⏰ @{bot_username} added to delayed list!")

@client.on(events.NewMessage(pattern=r'(?i)^!remove (@?\w+)$'))
async def remove_bot(event):
    me = await client.get_me()
    if not is_authorized_user(event.sender_id, me): return
    bot_username = event.pattern_match.group(1).replace('@', '')
    data = load_data()
    removed_from = []
    for list_name in ['safe_bots', 'delayed_bots']:
        original = len(data[list_name])
        data[list_name] = [b for b in data[list_name] if b.lower() != bot_username.lower()]
        if len(data[list_name]) < original: removed_from.append(list_name)
    if removed_from:
        save_data(data)
        await event.reply(f"✅ @{bot_username} removed from: {', '.join(removed_from)}")

@client.on(events.NewMessage(pattern=r'(?i)^!showbots$'))
async def show_bots(event):
    me = await client.get_me()
    if not is_authorized_user(event.sender_id, me): return
    data = load_data()
    message = "🤖 **Bot Lists:**\n\n🛡️ **Safe Bots:**\n"
    message += "\n".join([f"✅ @{bot}" for bot in data['safe_bots']]) or "❌ None\n"
    message += "\n⏰ **Delayed Bots:**\n"
    message += "\n".join([f"⏰ @{bot}" for bot in data['delayed_bots']]) or "❌ None"
    await event.reply(message)

@client.on(events.NewMessage(pattern=r'(?i)^!allow$'))
async def allow_group(event):
    me = await client.get_me()
    if not is_authorized_user(event.sender_id, me) or not event.is_group: return
    group_id = str(event.chat_id)
    data = load_data()
    if group_id not in data['allowed_groups']:
        data['allowed_groups'].append(group_id)
        save_data(data)
        await event.reply(f"✅ Group **{event.chat.title}** added to allowed list!")

@client.on(events.NewMessage(pattern=r'(?i)^!groupid$'))
async def get_group_id(event):
    me = await client.get_me()
    if not is_authorized_user(event.sender_id, me) or not event.is_group: return
    await event.reply(f"🏠 **Group Info:**\n\n📝 Name: {event.chat.title}\n🆔 ID: `{event.chat_id}`")

@client.on(events.NewMessage(pattern=r'(?i)^!showgroups$'))
async def show_groups(event):
    me = await client.get_me()
    if not is_authorized_user(event.sender_id, me): return
    data = load_data()
    message = "🏠 **Allowed Groups:**\n\n"
    for group_id in data['allowed_groups']:
        try:
            chat = await client.get_entity(int(group_id))
            message += f"✅ {chat.title} (ID: `{group_id}`)\n"
        except: message += f"✅ Unknown Group (ID: `{group_id}`)\n"
    await event.reply(message or "❌ No groups in allowed list")

# RELIABLE HTTP SERVER
class ReliableHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'ACTIVE')
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"🌐 [{current_time}] HTTP Request: {self.path}")
    
    def log_message(self, format, *args):
        pass  # Suppress default logs

def start_reliable_http_server():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), ReliableHandler) as httpd:
        print(f"🌐 RELIABLE HTTP server started on port {PORT}")
        httpd.serve_forever()

# START HTTP SERVER
http_thread = threading.Thread(target=start_reliable_http_server, daemon=True)
http_thread.start()

# TELEGRAM ACTIVITY LOGGER
async def telegram_activity_logger():
    await asyncio.sleep(60)
    log_count = 0
    while True:
        log_count += 1
        current_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"📱 [{current_time}] Telegram Bot Active - Log #{log_count}")
        await asyncio.sleep(600)  # Every 10 minutes

async def main():
    await client.start()
    me = await client.get_me()
    
    logger.info("🚀 RELIABLE UserBot Started!")
    logger.info(f"🤖 User: {me.first_name} (ID: {me.id})")
    logger.info("🔄 RELIABLE Keep-alive system ACTIVE")
    logger.info("🔧 Background activity running")
    logger.info("🌐 HTTP server active")
    logger.info("💪 3-minute ping intervals guaranteed!")
    
    # Start telegram activity logger
    asyncio.create_task(telegram_activity_logger())
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    print("🚀 STARTING RELIABLE 24/7 USERBOT...")
    print("💪 RELIABLE KEEP-ALIVE SYSTEM ACTIVATED!")
    print("🔄 3-minute ping intervals")
    print("🔧 Background activities enabled")
    print("🌐 HTTP server running on port 8080")
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
