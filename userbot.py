import asyncio
import multiprocessing
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
import re

print("🤖 PYROGRAM BOT STARTING...")

# Flask in background
def run_flask():
    app = Flask(__name__)
    @app.route('/')
    def home(): return "🤖 Bot Alive!"
    @app.route('/ping')  
    def ping(): return "🏓 Pong!"
    print("✅ Flask running on 5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask
p = multiprocessing.Process(target=run_flask)
p.daemon = True
p.start()

# Bot data storage
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

# Pyrogram Bot
async def main():
    print("🔗 Connecting to Telegram...")
    
    # YOUR NEW PYROGRAM SESSION STRING
    app = Client(
        "my_bot",
        api_id=22294121,
        api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
        session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
    )
    
    @app.on_message(filters.command("ping") & filters.private)
    async def ping_handler(client, message: Message):
        await message.reply("🏓 Pong! Bot is working!")
        print("✅ Ping command received")
    
    @app.on_message(filters.command("test"))
    async def test_handler(client, message: Message):
        await message.reply("✅ Test successful! Bot is alive!")
    
    @app.on_message(filters.command("status"))
    async def status_handler(client, message: Message):
        me = await app.get_me()
        status_text = f"""
🤖 **Bot Status**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Safe Bots:** {len(safe_bots)}
└─ **Delayed Bots:** {len(delayed_bots)}

**Commands:**
!allow <group_id> - Add group
!safe @bot - Add safe bot  
!status - Show status
!ping - Test bot
        """
        await message.reply(status_text)
    
    @app.on_message(filters.command("allow") & filters.private)
    async def allow_handler(client, message: Message):
        if len(message.command) > 1:
            group_id = message.command[1]
            allowed_groups.add(group_id)
            await message.reply(f"✅ Group `{group_id}` allowed!")
            print(f"✅ Group added: {group_id}")
        else:
            await message.reply("❌ Usage: !allow <group_id>")
    
    @app.on_message(filters.command("safe") & filters.private)
    async def safe_handler(client, message: Message):
        if len(message.command) > 1:
            bot_username = message.command[1].replace('@', '').lower()
            safe_bots.add(bot_username)
            await message.reply(f"✅ @{bot_username} added to safe list!")
            print(f"✅ Safe bot added: {bot_username}")
        else:
            await message.reply("❌ Usage: !safe @botusername")
    
    # Message handler for links in groups
    @app.on_message(filters.group)
    async def message_handler(client, message: Message):
        try:
            # Check if group is allowed
            group_id = str(message.chat.id)
            if group_id not in allowed_groups:
                return
            
            # Don't process own messages
            me = await app.get_me()
            if message.from_user and message.from_user.id == me.id:
                return
            
            message_text = message.text or message.caption or ""
            
            # Handle bot messages
            if message.from_user and message.from_user.is_bot:
                sender_username = message.from_user.username or ""
                if sender_username:
                    sender_username_lower = sender_username.lower()
                    
                    # Safe bots are allowed
                    if sender_username_lower in safe_bots:
                        return
                    else:
                        # Delete bot messages
                        try:
                            await message.delete()
                            print(f"🗑️ Deleted bot: {sender_username}")
                        except Exception as e:
                            print(f"❌ Failed to delete bot: {e}")
                        return
            
            # Delete messages with t.me links or @ mentions
            if message_text and ('t.me/' in message_text.lower() or '@' in message_text):
                try:
                    await message.delete()
                    print(f"🗑️ Deleted link message from group {group_id}")
                except Exception as e:
                    print(f"❌ Delete failed: {e}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("🚀 Starting Pyrogram bot...")
    await app.start()
    me = await app.get_me()
    print(f"✅ BOT CONNECTED: {me.first_name} ({me.id})")
    print("🤖 Bot is now running with ALL FEATURES!")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())
