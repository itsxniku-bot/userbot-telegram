print("🔥 ULTIMATE BOT STARTING - FINAL FIX...")

import asyncio
import requests
import time
import json
import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot Configuration
ADMIN_USER_ID = 8368838212

# Data storage
ALLOWED_GROUPS_FILE = "allowed_groups.json"
SAFE_BOTS_FILE = "safe_bots.json"

def load_data(filename, default=set()):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return set(json.load(f))
    except:
        return default

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(list(data), f)
    except:
        pass

# Load data with default groups
allowed_groups = load_data(ALLOWED_GROUPS_FILE, {"-1002129045974", "-1002497459144"})
safe_bots = load_data(SAFE_BOTS_FILE, {"grouphelp", "vid", "like"})

print(f"✅ Loaded {len(allowed_groups)} groups, {len(safe_bots)} safe bots")

# Simple Sleep Protection
def start_ping():
    def ping_server():
        while True:
            try:
                requests.get("https://userbot-telegram-1.onrender.com/", timeout=5)
            except:
                pass
            time.sleep(300)
    
    import threading
    threading.Thread(target=ping_server, daemon=True).start()
    print("✅ Sleep protection started")

start_ping()

async def main():
    print("🔗 Starting Telegram Bot...")
    
    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # Global variable for bot info
        bot_me = None
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        # ✅ WORKING COMMANDS
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            if is_admin(message.from_user.id):
                await message.reply("🚀 **BOT STARTED SUCCESSFULLY!**\nAll features working!")
                print("✅ /start command executed")
        
        @app.on_message(filters.command("ping"))
        async def ping_command(client, message: Message):
            if is_admin(message.from_user.id):
                await message.reply("🏓 **Pong!** Bot is alive and responding!")
                print("✅ /ping command executed")
        
        @app.on_message(filters.command("alive"))
        async def alive_command(client, message: Message):
            if is_admin(message.from_user.id):
                await message.reply("🟢 **BOT ZINDA HAI!** Commands and deletion working!")
                print("✅ /alive command executed")
        
        @app.on_message(filters.command("status"))
        async def status_command(client, message: Message):
            if is_admin(message.from_user.id):
                nonlocal bot_me
                if not bot_me:
                    bot_me = await app.get_me()
                
                status_text = f"""
🤖 **BOT STATUS - FULLY WORKING**

**Bot Info:**
├─ Name: {bot_me.first_name}
├─ Username: @{bot_me.username}
├─ ID: {bot_me.id}

**Protection:**
├─ Groups: {len(allowed_groups)}
├─ Safe Bots: {len(safe_bots)}
├─ Status: ✅ ACTIVE
└─ Device: ❌ OFFLINE FIXED

**Commands: ✅ WORKING**
**Deletion: ✅ WORKING**
                """
                await message.reply(status_text)
                print("✅ /status command executed")
        
        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            if is_admin(message.from_user.id):
                test_msg = await message.reply("🧪 Testing deletion in 2 seconds...")
                await asyncio.sleep(2)
                await test_msg.delete()
                await message.reply("✅ Test passed! Deletion working perfectly!")
                print("✅ /test command executed")
        
        @app.on_message(filters.command("allow"))
        async def allow_command(client, message: Message):
            if is_admin(message.from_user.id):
                if len(message.command) > 1:
                    group_id = message.command[1]
                    if group_id in allowed_groups:
                        await message.reply(f"ℹ️ Group `{group_id}` already allowed!")
                    else:
                        allowed_groups.add(group_id)
                        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                        await message.reply(f"✅ Group `{group_id}` allowed & SAVED!")
                        print(f"✅ Group {group_id} added to allowed list")
                else:
                    await message.reply("❌ Usage: `/allow <group_id>`")
        
        @app.on_message(filters.command("safe"))
        async def safe_command(client, message: Message):
            if is_admin(message.from_user.id):
                if len(message.command) > 1:
                    bot_username = message.command[1].replace('@', '').lower()
                    if bot_username in safe_bots:
                        await message.reply(f"ℹ️ @{bot_username} already in safe list!")
                    else:
                        safe_bots.add(bot_username)
                        save_data(SAFE_BOTS_FILE, safe_bots)
                        await message.reply(f"✅ @{bot_username} added to safe list!")
                        print(f"✅ Bot @{bot_username} added to safe list")
                else:
                    await message.reply("❌ Usage: `/safe @botusername`")
        
        # 🚀 SIMPLE & WORKING DELETION HANDLER
        @app.on_message(filters.group)
        async def deletion_handler(client, message: Message):
            try:
                # Get group ID
                group_id = str(message.chat.id)
                
                # Check if group is allowed
                if group_id not in allowed_groups:
                    return
                
                # Get bot info if not available
                nonlocal bot_me
                if not bot_me:
                    bot_me = await app.get_me()
                
                # Skip own messages
                if message.from_user and message.from_user.id == bot_me.id:
                    return
                
                # Check if message is from a bot
                if message.from_user and message.from_user.is_bot:
                    username = (message.from_user.username or "").lower()
                    
                    # Skip safe bots
                    if username in safe_bots:
                        return
                    
                    # Delete the bot message
                    try:
                        await message.delete()
                        print(f"✅ Deleted message from @{username} in {message.chat.title}")
                    except Exception as e:
                        print(f"❌ Failed to delete from @{username}: {e}")
                
            except Exception as e:
                print(f"❌ Error in handler: {e}")
        
        # ✅ START BOT
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        bot_me = await app.get_me()
        print(f"✅ BOT CONNECTED: {bot_me.first_name} (@{bot_me.username})")
        
        # Save initial data
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        # Send startup message
        await app.send_message("me", """
✅ **ULTIMATE BOT STARTED SUCCESSFULLY!**

🎯 **ALL FEATURES WORKING:**
• Commands: ✅ Active
• Message Deletion: ✅ Active  
• Group Protection: ✅ Active
• Device Offline: ✅ Fixed

🚀 **TEST COMMANDS:**
• /ping - Check bot response
• /test - Test message deletion
• /status - Check bot status

**Bot ab poora work karega!** 🔥
        """)
        
        print("🤖 BOT READY - All features ACTIVE!")
        print("📱 Monitoring groups for bot messages...")
        
        # Keep the bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")

if __name__ == "__main__":
    print("🚀 STARTING ULTIMATE BOT - FINAL WORKING VERSION...")
    asyncio.run(main())
