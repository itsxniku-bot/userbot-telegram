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
import threading
import re
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

print("🚀 Starting UserBot...")

# Flask web server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is Running on Render!"

@app.route('/ping')
def ping():
    return "🏓 Pong! Bot is alive"

@app.route('/health')
def health():
    return "✅ Bot is healthy and running"

def run_flask():
    # RENDER AUTO PORT DETECTION - 5000 use karega
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# API credentials
api_id = 22294121
api_hash = "0f7fa7216b26e3f52699dc3c5a560d2a"
session_string = "1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc="

# Create client
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Store data in memory
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

# Link pattern for detection
LINK_PATTERN = re.compile(r't\.me/|@\w+', re.IGNORECASE)

# Main message handler
@client.on(events.NewMessage)
async def handle_messages(event):
    try:
        # Only work in groups
        if not event.is_group:
            return
            
        # Check if group is allowed
        group_id = str(event.chat_id)
        if group_id not in allowed_groups:
            return
        
        # Don't process own messages
        me = await client.get_me()
        if event.sender_id == me.id:
            return
            
        message_text = event.message.text or event.message.caption or ""
        
        # Handle bot messages
        if event.sender and event.sender.bot:
            sender_username = event.sender.username or ""
            if sender_username:
                sender_username_lower = sender_username.lower()
                
                # Safe bots are allowed
                if sender_username_lower in safe_bots:
                    return
                
                # Delayed bots - delete links immediately
                if sender_username_lower in delayed_bots:
                    if message_text and LINK_PATTERN.search(message_text):
                        try:
                            await event.delete()
                            print(f"🗑️ Deleted link from delayed bot: {sender_username}")
                        except Exception as e:
                            print(f"❌ Failed to delete from delayed bot: {e}")
                    return
                else:
                    # Regular bots - delete immediately
                    try:
                        await event.delete()
                        print(f"🗑️ Deleted bot message: {sender_username}")
                    except Exception as e:
                        print(f"❌ Failed to delete bot: {e}")
            return
            
        # Delete messages containing t.me links or @mentions
        if message_text and LINK_PATTERN.search(message_text):
            try:
                await event.delete()
                print(f"🗑️ Deleted link message from user")
            except Exception as e:
                print(f"❌ Failed to delete user message: {e}")
                
    except Exception as e:
        print(f"❌ Error in handler: {e}")

# BOT MANAGEMENT COMMANDS
@client.on(events.NewMessage(pattern=r'^!safe (@?\w+)$'))
async def safe_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    bot_username = event.pattern_match.group(1).replace('@', '').lower()
    safe_bots.add(bot_username)
    # Remove from delayed if present
    if bot_username in delayed_bots:
        delayed_bots.remove(bot_username)
    await event.reply(f"✅ @{bot_username} added to safe list!")

@client.on(events.NewMessage(pattern=r'^!delay (@?\w+)$'))
async def delay_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    bot_username = event.pattern_match.group(1).replace('@', '').lower()
    delayed_bots.add(bot_username)
    # Remove from safe if present
    if bot_username in safe_bots:
        safe_bots.remove(bot_username)
    await event.reply(f"⏰ @{bot_username} added to delayed list!")

@client.on(events.NewMessage(pattern=r'^!remove (@?\w+)$'))
async def remove_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    bot_username = event.pattern_match.group(1).replace('@', '').lower()
    removed_from = []
    
    if bot_username in safe_bots:
        safe_bots.remove(bot_username)
        removed_from.append('safe')
    
    if bot_username in delayed_bots:
        delayed_bots.remove(bot_username)
        removed_from.append('delayed')
    
    if removed_from:
        await event.reply(f"✅ @{bot_username} removed from: {', '.join(removed_from)}")
    else:
        await event.reply(f"❌ @{bot_username} not found in any list!")

@client.on(events.NewMessage(pattern=r'^!allow (-?\d+)$'))
async def allow_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    group_id = event.pattern_match.group(1)
    allowed_groups.add(group_id)
    await event.reply(f"✅ Group ID `{group_id}` allowed!")

@client.on(events.NewMessage(pattern=r'^!disallow (-?\d+)$'))
async def disallow_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    group_id = event.pattern_match.group(1)
    if group_id in allowed_groups:
        allowed_groups.remove(group_id)
        await event.reply(f"✅ Group ID `{group_id}` removed!")
    else:
        await event.reply(f"❌ Group ID `{group_id}` not in allowed list!")

# STATUS COMMANDS
@client.on(events.NewMessage(pattern='!ping'))
async def ping_handler(event):
    await event.reply('🏓 Pong! Bot is alive!')

@client.on(events.NewMessage(pattern='!status'))
async def status_handler(event):
    me = await client.get_me()
    status_text = f"""
🤖 **Bot Status**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {len(safe_bots)}
└─ **Delayed Bots:** {len(delayed_bots)}

**Commands:**
!allow <group_id> - Add group
!disallow <group_id> - Remove group  
!safe @bot - Add safe bot
!delay @bot - Add delayed bot
!remove @bot - Remove bot
!status - This message
"""
    await event.reply(status_text)

@client.on(events.NewMessage(pattern='!lists'))
async def lists_handler(event):
    safe_list = "\n".join([f"• @{bot}" for bot in safe_bots]) or "None"
    delayed_list = "\n".join([f"• @{bot}" for bot in delayed_bots]) or "None"
    groups_list = "\n".join([f"• `{group}`" for group in allowed_groups]) or "None"
    
    lists_text = f"""
📋 **Bot Lists**

**🤖 Safe Bots:**
{safe_list}

**⏰ Delayed Bots:**
{delayed_list}

**👥 Allowed Groups:**
{groups_list}
"""
    await event.reply(lists_text)

# Main function
async def main():
    # Start Flask in background thread - NON-BLOCKING
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Flask server started on port 5000")
    
    await client.start()
    me = await client.get_me()
    print(f"✅ Bot started: {me.first_name} (ID: {me.id})")
    print(f"📊 Allowed groups: {len(allowed_groups)}")
    print(f"🤖 Safe bots: {len(safe_bots)}")
    print(f"⏰ Delayed bots: {len(delayed_bots)}")
    print("🚀 Bot is now running with FIXED THREADING!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
