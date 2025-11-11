# IMGHDR FIX - Add this at the VERY TOP of userbot.py
import sys
import types

# Fix for imghdr in Python 3.13+
try:
    import imghdr
except ImportError:
    imghdr = types.ModuleType('imghdr')
    def what(file, h=None):
        return None
    imghdr.what = what
    sys.modules['imghdr'] = imghdr

# Now continue with your original imports
import requests
import threading
import time
import os
import http.server
import socketserver

# Keep-alive system - Render ko sleep se bachane ke liye
def keep_alive():
    time.sleep(30)  # App start hone ka wait karo
    
    while True:
        try:
            render_url = os.environ.get('RENDER_URL')
            if render_url and 'onrender.com' in render_url:
                response = requests.get(render_url, timeout=10)
                print(f"🔄 Keep-alive ping: {response.status_code}")
            else:
                # Self-ping if URL not set
                try:
                    requests.get('http://localhost:8080', timeout=5)
                    print("🔄 Self ping sent")
                except:
                    print("🔄 Keep-alive active")
        except Exception as e:
            print(f"❌ Keep-alive failed: {e}")
        
        time.sleep(600)  # Har 10 minute mein ping

# Start keep-alive
keep_thread = threading.Thread(target=keep_alive, daemon=True)
keep_thread.start()

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
import json
import asyncio
import logging
import sys

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# API credentials - YAHAN SESSION STRING ADD KARO
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', '1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc=')

if not session_string:
    logger.error("❌ SESSION_STRING environment variable not set!")
    sys.exit(1)

# Create client with session string
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Regular expression to detect ALL types of links
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
                data = json.load(f)
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    return default_data

def save_data(data):
    try:
        with open('bot_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving data: {e}")

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
        logger.error(f"❌ Error in delayed deletion: {e}")

@client.on(events.NewMessage)
async def handle_all_messages(event):
    try:
        if not event.is_group:
            return
        
        if not event.sender:
            return
            
        group_id = str(event.chat_id)
        if not is_group_allowed(group_id):
            return
        
        me = await client.get_me()
        if event.sender_id == me.id:
            return
        
        message_text = event.message.text or event.message.caption
        
        if event.sender.bot:
            sender_username = event.sender.username
            if sender_username:
                if is_safe_bot(sender_username):
                    return
                
                if is_delayed_bot(sender_username):
                    if contains_any_link(message_text):
                        try:
                            await event.delete()
                            logger.info(f"🗑️ Immediately deleted message with link from: {sender_username}")
                            return
                        except Exception as e:
                            logger.error(f"❌ Error deleting message: {e}")
                    else:
                        asyncio.create_task(delete_after_delay(event, 60))
                        logger.info(f"⏰ Scheduled deletion for: {sender_username}")
                        return
                else:
                    try:
                        await event.delete()
                        logger.info(f"🗑️ Deleted message from: {sender_username}")
                        return
                    except Exception as e:
                        logger.error(f"❌ Error deleting message: {e}")
        
        if message_text and contains_any_link(message_text):
            for pattern in ALL_LINK_PATTERNS:
                matches = re.findall(pattern, message_text)
                for match in matches:
                    if isinstance(match, str) and match.lower().endswith('bot'):
                        if not is_safe_bot(match):
                            try:
                                await event.delete()
                                logger.info(f"🗑️ Deleted message with bot link: {match}")
                                return
                            except Exception as e:
                                logger.error(f"❌ Error deleting message: {e}")
                    
    except Exception as e:
        logger.error(f"❌ Error in handle_all_messages: {e}")

# Command to add bot to safe list
@client.on(events.NewMessage(pattern=r'(?i)^!safe (@?\w+)$'))
async def add_safe_bot(event):
    try:
        me = await client.get_me()
        if not is_authorized_user(event.sender_id, me):
            return
        
        bot_username = event.pattern_match.group(1).replace('@', '')
        data = load_data()
        data['delayed_bots'] = [b for b in data['delayed_bots'] if b.lower() != bot_username.lower()]
        
        if bot_username.lower() not in [b.lower() for b in data['safe_bots']]:
            data['safe_bots'].append(bot_username)
            save_data(data)
            await event.reply(f"✅ @{bot_username} ko safe list mein add kar diya!")
            logger.info(f"✅ Added to safe: {bot_username}")
        else:
            await event.reply(f"ℹ️ @{bot_username} already safe list mein hai!")
    except Exception as e:
        logger.error(f"❌ Error in add_safe_bot: {e}")

# Command to add bot to delayed delete list
@client.on(events.NewMessage(pattern=r'(?i)^!delayed (@?\w+)$'))
async def add_delayed_bot(event):
    try:
        me = await client.get_me()
        if not is_authorized_user(event.sender_id, me):
            return
        
        bot_username = event.pattern_match.group(1).replace('@', '')
        data = load_data()
        data['safe_bots'] = [b for b in data['safe_bots'] if b.lower() != bot_username.lower()]
        
        if bot_username.lower() not in [b.lower() for b in data['delayed_bots']]:
            data['delayed_bots'].append(bot_username)
            save_data(data)
            await event.reply(f"⏰ @{bot_username} ko delayed list mein add kar diya!")
            logger.info(f"⏰ Added to delayed: {bot_username}")
        else:
            await event.reply(f"ℹ️ @{bot_username} already delayed list mein hai!")
    except Exception as e:
        logger.error(f"❌ Error in add_delayed_bot: {e}")

# Command to remove bot from any list
@client.on(events.NewMessage(pattern=r'(?i)^!remove (@?\w+)$'))
async def remove_bot(event):
    try:
        me = await client.get_me()
        if not is_authorized_user(event.sender_id, me):
            return
        
        bot_username = event.pattern_match.group(1).replace('@', '')
        data = load_data()
        
        removed_from = []
        for list_name in ['safe_bots', 'delayed_bots']:
            original_length = len(data[list_name])
            data[list_name] = [b for b in data[list_name] if b.lower() != bot_username.lower()]
            if len(data[list_name]) < original_length:
                removed_from.append(list_name)
        
        if removed_from:
            save_data(data)
            await event.reply(f"✅ @{bot_username} ko remove kar diya from: {', '.join(removed_from)}")
            logger.info(f"✅ Removed from lists: {bot_username} from {removed_from}")
        else:
            await event.reply(f"❌ @{bot_username} kisi list mein nahi mila!")
    except Exception as e:
        logger.error(f"❌ Error in remove_bot: {e}")

# Command to show current lists
@client.on(events.NewMessage(pattern=r'(?i)^!showbots$'))
async def show_bots(event):
    try:
        me = await client.get_me()
        if not is_authorized_user(event.sender_id, me):
            return
        
        data = load_data()
        message = "🤖 **Bot Lists:**\n\n🛡️ **Safe Bots:**\n"
        
        if data['safe_bots']:
            for bot in data['safe_bots']:
                message += f"✅ @{bot}\n"
        else:
            message += "❌ None\n"
        
        message += "\n⏰ **Delayed Bots:**\n"
        if data['delayed_bots']:
            for bot in data['delayed_bots']:
                message += f"⏰ @{bot}\n"
        else:
            message += "❌ None\n"
        
        await event.reply(message)
    except Exception as e:
        logger.error(f"❌ Error in show_bots: {e}")

# Command to add current group to allowed list
@client.on(events.NewMessage(pattern=r'(?i)^!allow$'))
async def allow_group(event):
    try:
        me = await client.get_me()
        if not is_authorized_user(event.sender_id, me):
            return
        
        if not event.is_group:
            return
        
        group_id = str(event.chat_id)
        group_title = event.chat.title
        
        data = load_data()
        
        if group_id not in data['allowed_groups']:
            data['allowed_groups'].append(group_id)
            save_data(data)
            await event.reply(f"✅ Group **{group_title}** ko allowed list mein add kar diya!")
            logger.info(f"✅ Added group to allowed: {group_title} ({group_id})")
        else:
            await event.reply(f"ℹ️ Group **{group_title}** already allowed list mein hai!")
    except Exception as e:
        logger.error(f"❌ Error in allow_group: {e}")

# Command to get current group ID
@client.on(events.NewMessage(pattern=r'(?i)^!groupid$'))
async def get_group_id(event):
    try:
        me = await client.get_me()
        if not is_authorized_user(event.sender_id, me):
            return
        
        if not event.is_group:
            return
        
        group_id = str(event.chat_id)
        group_title = event.chat.title
        
        await event.reply(f"🏠 **Group Info:**\n\n📝 Name: {group_title}\n🆔 ID: `{group_id}`")
        logger.info(f"🔧 Group ID requested: {group_title} ({group_id})")
    except Exception as e:
        logger.error(f"❌ Error in get_group_id: {e}")

# Command to show allowed groups
@client.on(events.NewMessage(pattern=r'(?i)^!showgroups$'))
async def show_groups(event):
    try:
        me = await client.get_me()
        if not is_authorized_user(event.sender_id, me):
            return
        
        data = load_data()
        message = "🏠 **Allowed Groups List:**\n\n"
        
        if data['allowed_groups']:
            for group_id in data['allowed_groups']:
                try:
                    chat = await client.get_entity(int(group_id))
                    message += f"✅ {chat.title} (ID: `{group_id}`)\n"
                except:
                    message += f"✅ Unknown Group (ID: `{group_id}`)\n"
            message += f"\n📊 Total: {len(data['allowed_groups'])} groups"
        else:
            message += "❌ Koi group allowed list mein nahi hai\n"
        
        await event.reply(message)
    except Exception as e:
        logger.error(f"❌ Error in show_groups: {e}")

# HTTP Server for Render port requirement - SIMPLE VERSION
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'UserBot is running with keep-alive!')
    
    def log_message(self, format, *args):
        print(f"HTTP: {format % args}")

def start_http_server():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"🌐 HTTP server started on port {PORT}")
        httpd.serve_forever()

# Start HTTP server in background
http_thread = threading.Thread(target=start_http_server, daemon=True)
http_thread.start()

# Keep main process alive for Render
def keep_process_alive():
    while True:
        time.sleep(3600)

async def main():
    await client.start()
    me = await client.get_me()
    logger.info(f"🤖 Userbot started successfully for: {me.first_name} (ID: {me.id})")
    logger.info("🔄 Keep-alive system active")
    logger.info("🚀 UserBot is now running 24/7 without sleep!")
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        # Start keep-alive thread for main process
        process_thread = threading.Thread(target=keep_process_alive, daemon=True)
        process_thread.start()
        
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Userbot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
