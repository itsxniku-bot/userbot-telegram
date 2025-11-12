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

# ULTIMATE KEEP-ALIVE SYSTEM
def ultimate_keep_alive():
    time.sleep(10)
    
    ping_methods = [
        lambda: requests.get(f'http://localhost:8080/ping_{random.randint(1000,9999)}', timeout=5),
        lambda: requests.get(f'http://localhost:8080/health_{random.randint(1000,9999)}', timeout=5),
        lambda: requests.get(f'http://localhost:8080/status_{random.randint(1000,9999)}', timeout=5),
        lambda: requests.get(f'http://localhost:8080/api_{random.randint(1000,9999)}', timeout=5),
    ]
    
    while True:
        try:
            # MULTIPLE RENDER URL PINGS
            render_url = os.environ.get('RENDER_URL')
            if render_url:
                for i in range(3):  # Triple ping
                    try:
                        response = requests.get(f"{render_url}?ping={random.randint(10000,99999)}", timeout=8)
                        print(f"🎯 Render Ping {i+1}: {response.status_code}")
                        time.sleep(1)
                    except: pass
            
            # MULTIPLE SELF PINGS  
            for i in range(4):  # 4 different ping methods
                try:
                    ping_methods[i]()
                    print(f"🔷 Self Ping {i+1}: OK")
                    time.sleep(0.5)
                except: pass
                
            print(f"✅ Keep-alive cycle completed at {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ Keep-alive error: {e}")
        
        # RANDOM INTERVAL: 2-4 minutes
        interval = random.randint(120, 240)
        print(f"⏰ Next ping in {interval} seconds")
        time.sleep(interval)

# BACKGROUND ACTIVITY SIMULATOR
def background_activity():
    time.sleep(30)
    activity_count = 0
    activities = [
        "🔄 Memory optimization",
        "📊 Cache cleaning", 
        "🔍 Monitoring logs",
        "🛠️ System check",
        "📈 Performance analysis",
        "🔒 Security scan"
    ]
    
    while True:
        activity_count += 1
        activity = random.choice(activities)
        print(f"{activity} - Activity #{activity_count} at {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(300)  # Every 5 minutes

# START BOTH SYSTEMS
keep_thread = threading.Thread(target=ultimate_keep_alive, daemon=True)
keep_thread.start()

activity_thread = threading.Thread(target=background_activity, daemon=True)
activity_thread.start()

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
session_string = os.environ.get('SESSION_STRING', 'YOUR_SESSION_HERE')

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

# ULTIMATE HTTP SERVER
class UltimateHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'ACTIVE')
        print(f"🌐 HTTP Request: {self.path} at {datetime.now().strftime('%H:%M:%S')}")
    
    def log_message(self, format, *args):
        pass  # Suppress default logs

def start_ultimate_http_server():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), UltimateHandler) as httpd:
        print(f"🌐 ULTIMATE HTTP server started on port {PORT}")
        httpd.serve_forever()

# START HTTP SERVER
http_thread = threading.Thread(target=start_ultimate_http_server, daemon=True)
http_thread.start()

# TELEGRAM ACTIVITY LOGGER
async def telegram_activity_logger():
    await asyncio.sleep(60)
    log_count = 0
    while True:
        log_count += 1
        logger.info(f"📱 Telegram Bot Active - Log #{log_count} - {datetime.now().strftime('%H:%M:%S')}")
        await asyncio.sleep(900)  # Every 15 minutes

async def main():
    await client.start()
    me = await client.get_me()
    
    logger.info("🚀 ULTIMATE UserBot Started!")
    logger.info(f"🤖 User: {me.first_name} (ID: {me.id})")
    logger.info("🔄 ULTIMATE Keep-alive activated")
    logger.info("🔧 Background activity simulator running")
    logger.info("🌐 Enhanced HTTP server active")
    logger.info("📱 Telegram activity logger started")
    logger.info("💪 MAXIMUM UPTIME CONFIGURATION LOADED!")
    
    # Start telegram activity logger
    asyncio.create_task(telegram_activity_logger())
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    print("🚀 STARTING ULTIMATE 24/7 USERBOT...")
    print("💪 MAXIMUM UPTIME CONFIGURATION ACTIVATED!")
    print("🛡️  Multiple keep-alive systems running")
    print("🔧 Background activities enabled")
    print("🌐 Enhanced HTTP server started")
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
