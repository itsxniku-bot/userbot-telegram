import os
import asyncio
import logging
import json
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

print("🚀 Starting UserBot...")

# API credentials - YAHAN VARIABLES ADD KARO
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', '1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc=')

if not session_string:
    logger.error("❌ SESSION_STRING not set!")
    exit(1)

# Create client
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Link patterns
LINK_PATTERNS = [
    r't\.me/(\w+)', r'@(\w+)', r'https?://t\.me/(\w+)',
    r'https?://telegram\.me/(\w+)', r'https?://wa\.me/(\w+)',
    r'https?://chat\.whatsapp\.com/(\w+)'
]

# Data management
def load_data():
    default_data = {
        'safe_bots': [],
        'allowed_groups': [], 
        'delayed_bots': []
    }
    try:
        if os.path.exists('bot_data.json'):
            with open('bot_data.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return default_data

def save_data(data):
    try:
        with open('bot_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

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
    if not message_text:
        return False
    for pattern in LINK_PATTERNS:
        if re.search(pattern, message_text, re.IGNORECASE):
            return True
    return False

# Main message handler
@client.on(events.NewMessage)
async def handle_all_messages(event):
    try:
        if not event.is_group or not event.sender:
            return
            
        group_id = str(event.chat_id)
        if not is_group_allowed(group_id):
            return
        
        me = await client.get_me()
        if event.sender_id == me.id:
            return
        
        message_text = event.message.text or event.message.caption
        
        # Handle bot messages
        if event.sender.bot:
            sender_username = event.sender.username
            if sender_username:
                if is_safe_bot(sender_username):
                    return
                
                if is_delayed_bot(sender_username):
                    if contains_any_link(message_text):
                        await event.delete()
                        logger.info(f"🗑️ Deleted message with link from: {sender_username}")
                    return
                else:
                    await event.delete()
                    logger.info(f"🗑️ Deleted message from: {sender_username}")
                    return
        
        # Handle links in user messages
        if message_text and contains_any_link(message_text):
            for pattern in LINK_PATTERNS:
                matches = re.findall(pattern, message_text)
                for match in matches:
                    if isinstance(match, str) and match.lower().endswith('bot'):
                        if not is_safe_bot(match):
                            await event.delete()
                            logger.info(f"🗑️ Deleted message with bot link: {match}")
                            return
                    
    except Exception as e:
        logger.error(f"Error: {e}")

# Bot management commands
@client.on(events.NewMessage(pattern=r'(?i)^!safe (@?\w+)$'))
async def add_safe_bot(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    bot_username = event.pattern_match.group(1).replace('@', '')
    data = load_data()
    
    if bot_username.lower() not in [b.lower() for b in data['safe_bots']]:
        data['safe_bots'].append(bot_username)
        save_data(data)
        await event.reply(f"✅ @{bot_username} added to safe list!")

@client.on(events.NewMessage(pattern=r'(?i)^!delayed (@?\w+)$'))
async def add_delayed_bot(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    bot_username = event.pattern_match.group(1).replace('@', '')
    data = load_data()
    
    if bot_username.lower() not in [b.lower() for b in data['delayed_bots']]:
        data['delayed_bots'].append(bot_username)
        save_data(data)
        await event.reply(f"⏰ @{bot_username} added to delayed list!")

@client.on(events.NewMessage(pattern=r'(?i)^!showbots$'))
async def show_bots(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    data = load_data()
    message = "🤖 **Bot Lists:**\n\n🛡️ **Safe Bots:**\n"
    message += "\n".join([f"✅ @{bot}" for bot in data['safe_bots']]) or "❌ None\n"
    message += "\n⏰ **Delayed Bots:**\n"
    message += "\n".join([f"⏰ @{bot}" for bot in data['delayed_bots']]) or "❌ None"
    await event.reply(message)

# Group management commands
@client.on(events.NewMessage(pattern=r'(?i)^!allow$'))
async def allow_group(event):
    me = await client.get_me()
    if event.sender_id != me.id or not event.is_group:
        return
        
    group_id = str(event.chat_id)
    data = load_data()
    
    if group_id not in data['allowed_groups']:
        data['allowed_groups'].append(group_id)
        save_data(data)
        await event.reply(f"✅ Group **{event.chat.title}** added to allowed list!")

@client.on(events.NewMessage(pattern=r'(?i)^!ping$'))
async def ping_handler(event):
    await event.reply('🏓 Pong!')

@client.on(events.NewMessage(pattern=r'(?i)^!help$'))
async def help_handler(event):
    help_text = """
🤖 **Bot Commands:**
• `!safe @bot` - Add bot to safe list
• `!delayed @bot` - Add bot to delayed list
• `!showbots` - Show bot lists
• `!allow` - Allow current group
• `!ping` - Check bot status
• `!help` - Show this help
"""
    await event.reply(help_text)

# Main function
async def main():
    await client.start()
    me = await client.get_me()
    logger.info(f"🤖 Bot started: {me.first_name}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
