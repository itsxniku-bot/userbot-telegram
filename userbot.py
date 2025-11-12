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
from telethon import TelegramClient, events
from telethon.sessions import StringSession

print("🚀 Starting UserBot...")

# API credentials
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', '1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc=')

if not session_string:
    print("❌ SESSION_STRING not set!")
    exit(1)

# Create client
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Store data in memory
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

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
            
        message_text = event.message.text or event.message.caption
        
        # Handle bot messages
        if event.sender.bot:
            sender_username = event.sender.username
            if sender_username:
                # Safe bots are allowed
                if sender_username.lower() in safe_bots:
                    return
                
                # Delayed bots - delete links immediately
                if sender_username.lower() in delayed_bots:
                    if message_text and ('t.me/' in message_text.lower() or '@' in message_text):
                        try:
                            await event.delete()
                            print(f"🗑️ Deleted link from delayed bot: {sender_username}")
                        except:
                            pass
                    return
                else:
                    # Regular bots - delete immediately
                    try:
                        await event.delete()
                        print(f"🗑️ Deleted bot: {sender_username}")
                    except:
                        pass
            return
            
        # Delete messages containing t.me links
        if message_text and ('t.me/' in message_text.lower() or '@' in message_text):
            try:
                await event.delete()
                print(f"🗑️ Deleted link message")
            except:
                pass
                
    except Exception as e:
        print(f"❌ Error: {e}")

# Bot Management Commands
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

@client.on(events.NewMessage(pattern=r'^!delayed (@?\w+)$'))
async def delayed_handler(event):
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

@client.on(events.NewMessage(pattern='!showbots'))
async def showbots_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    message = "🤖 **Bot Lists:**\n\n🛡️ **Safe Bots:**\n"
    if safe_bots:
        for bot in safe_bots:
            message += f"✅ @{bot}\n"
    else:
        message += "❌ None\n"
    
    message += "\n⏰ **Delayed Bots:**\n"
    if delayed_bots:
        for bot in delayed_bots:
            message += f"⏰ @{bot}\n"
    else:
        message += "❌ None"
    
    await event.reply(message)

# Group Management Commands
@client.on(events.NewMessage(pattern='!allow'))
async def allow_handler(event):
    if not event.is_group:
        return
        
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    group_id = str(event.chat_id)
    allowed_groups.add(group_id)
    await event.reply(f"✅ Group **{event.chat.title}** allowed!")

@client.on(events.NewMessage(pattern='!groupid'))
async def groupid_handler(event):
    if not event.is_group:
        return
        
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    await event.reply(f"🏠 **Group Info:**\n\n📝 Name: {event.chat.title}\n🆔 ID: `{event.chat_id}`")

@client.on(events.NewMessage(pattern='!showgroups'))
async def showgroups_handler(event):
    me = await client.get_me()
    if event.sender_id != me.id:
        return
        
    message = "🏠 **Allowed Groups:**\n\n"
    if allowed_groups:
        for group_id in allowed_groups:
            try:
                chat = await client.get_entity(int(group_id))
                message += f"✅ {chat.title} (ID: `{group_id}`)\n"
            except:
                message += f"✅ Unknown Group (ID: `{group_id}`)\n"
    else:
        message += "❌ No groups allowed yet"
    
    await event.reply(message)

# Utility Commands
@client.on(events.NewMessage(pattern='!ping'))
async def ping_handler(event):
    await event.reply('🏓 Pong!')

@client.on(events.NewMessage(pattern='!status'))
async def status_handler(event):
    me = await client.get_me()
    status_text = f"""
🤖 **Bot Status:** ACTIVE
👤 **User:** {me.first_name}
🆔 **ID:** {me.id}

📊 **Statistics:**
• Safe Bots: {len(safe_bots)}
• Delayed Bots: {len(delayed_bots)}
• Allowed Groups: {len(allowed_groups)}
"""
    await event.reply(status_text)

@client.on(events.NewMessage(pattern='!help'))
async def help_handler(event):
    help_text = """
🤖 **Bot Commands:**

🔧 **Bot Management:**
• `!safe @username` - Add bot to safe list
• `!delayed @username` - Add bot to delayed list  
• `!remove @username` - Remove bot from lists
• `!showbots` - Show all bot lists

🏠 **Group Management:**
• `!allow` - Add current group to allowed list
• `!groupid` - Get current group ID
• `!showgroups` - Show allowed groups

ℹ️ **Utility:**
• `!ping` - Check if bot is alive
• `!status` - Show bot status
• `!help` - Show this help

⚡ **Auto Features:**
• Deletes messages from unauthorized bots
• Deletes messages with suspicious links
• Delayed deletion for specific bots
"""
    await event.reply(help_text)

# Main function
async def main():
    await client.start()
    me = await client.get_me()
    print(f"✅ Bot started: {me.first_name} (ID: {me.id})")
    print("🚀 Bot is now running with ALL COMMANDS!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
