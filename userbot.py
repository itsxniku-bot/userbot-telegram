# IMGHDR FIX - Python 3.13 Compatibility
import sys
import types
try:
    import imghdr
except ImportError:
    imghdr = types.ModuleType('imghdr')
    def what(file, h=None): return None
    imghdr.what = what
    sys.modules['imghdr'] = imghdr

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

# API credentials
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', '1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc=')

if not session_string:
    logger.error("❌ SESSION_STRING not set!")
    exit(1)

# Create simple client
client = TelegramClient(StringSession(session_string), api_id, api_hash)
logger.info("🔧 Telegram client initialized")

# Simple data management
def load_data():
    return {'allowed_groups': []}

def save_data(data):
    try:
        with open('bot_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

def is_group_allowed(group_id):
    data = load_data()
    return str(group_id) in data['allowed_groups']

# Simple auto-reconnect
async def simple_reconnect():
    while True:
        try:
            if not client.is_connected():
                logger.warning("🔌 Reconnecting...")
                await client.connect()
                logger.info("✅ Reconnected!")
        except Exception as e:
            logger.error(f"❌ Reconnect failed: {e}")
        await asyncio.sleep(60)

# Main message handler
@client.on(events.NewMessage)
async def handle_messages(event):
    try:
        # Only work in groups
        if not event.is_group:
            return
            
        # Check group permission
        group_id = str(event.chat_id)
        if not is_group_allowed(group_id):
            return
        
        # Don't process own messages
        me = await client.get_me()
        if event.sender_id == me.id:
            return
            
        message_text = event.message.text or event.message.caption
        
        # Delete all bot messages
        if event.sender.bot:
            try:
                await event.delete()
                logger.info(f"🗑️ Deleted bot message")
            except Exception as e:
                logger.error(f"❌ Error deleting: {e}")
            return
            
        # Delete messages containing t.me links
        if message_text and ('t.me/' in message_text.lower() or '@' in message_text):
            try:
                await event.delete()
                logger.info("🗑️ Deleted message with link")
            except Exception as e:
                logger.error(f"❌ Error deleting: {e}")
                
    except Exception as e:
        logger.error(f"❌ Handler error: {e}")

# Simple commands
@client.on(events.NewMessage(pattern='!ping'))
async def ping_handler(event):
    await event.reply('🏓 Pong!')

@client.on(events.NewMessage(pattern='!allow'))
async def allow_handler(event):
    if not event.is_group:
        return
        
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    group_id = str(event.chat_id)
    data = load_data()
    
    if group_id not in data['allowed_groups']:
        data['allowed_groups'].append(group_id)
        save_data(data)
        await event.reply(f"✅ Group allowed!")

@client.on(events.NewMessage(pattern='!status'))
async def status_handler(event):
    me = await client.get_me()
    await event.reply(f'🤖 Status: ACTIVE\n👤 User: {me.first_name}')

@client.on(events.NewMessage(pattern='!help'))
async def help_handler(event):
    help_text = """
🤖 **Bot Commands:**
• `!allow` - Allow current group
• `!ping` - Check bot status  
• `!status` - Show bot info
• `!help` - Show this help

⚡ **Auto Features:**
• Deletes all bot messages
• Deletes messages with links
"""
    await event.reply(help_text)

# Main function
async def main():
    try:
        await client.start()
        me = await client.get_me()
        logger.info(f"✅ Bot started: {me.first_name}")
        
        # Start simple reconnect
        asyncio.create_task(simple_reconnect())
        
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ Failed to start: {e}")

if __name__ == '__main__':
    asyncio.run(main())
