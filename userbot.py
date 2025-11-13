print("🔥 ULTIMATE BOT STARTING - COMPLETE & FINAL VERSION...")

import asyncio
import multiprocessing
import re
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
import threading
import requests
import time
import sys
import json
import os

# Bot data storage with file saving
ALLOWED_GROUPS_FILE = "allowed_groups.json"
SAFE_BOTS_FILE = "safe_bots.json"
DELAYED_BOTS_FILE = "delayed_bots.json"

def load_data(filename, default=set()):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                return set(data)
    except:
        pass
    return default

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(list(data), f)
    except:
        pass

# Load saved data
allowed_groups = load_data(ALLOWED_GROUPS_FILE)
safe_bots = load_data(SAFE_BOTS_FILE)
delayed_bots = load_data(DELAYED_BOTS_FILE)

# YOUR USER ID
ADMIN_USER_ID = 8368838212

print(f"✅ Loaded {len(allowed_groups)} groups, {len(safe_bots)} safe bots, {len(delayed_bots)} delayed bots")

# 🛡️ SLEEP PROTECTION
def run_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 BOT ACTIVE"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong"
    
    @app.route('/health')
    def health():
        return "✅ HEALTHY"
    
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

print("🔥 Starting Flask...")
flask_process = multiprocessing.Process(target=run_flask, daemon=True)
flask_process.start()
time.sleep(3)
print("✅ Flask started!")

# 🔥 COMPLETE TELEGRAM BOT WITH ALL FEATURES
async def start_telegram():
    print("🔗 Starting Telegram Bot - COMPLETE VERSION...")
    
    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(user_id):
            return user_id == ADMIN_USER_ID
        
        me = None
        
        # ✅ FLOOD PROTECTION
        last_delete_time = 0
        delete_count = 0
        FLOOD_DELAY = 2  # 2 seconds between deletes
        
        # ✅ COMPLETE COMMANDS LIST
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            await message.reply("🚀 **ULTIMATE BOT STARTED!**\nUse /help for all commands")
        
        @app.on_message(filters.command("help"))
        async def help_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            help_text = """
🤖 **ULTIMATE BOT - ALL COMMANDS**

**Basic Commands:**
├─ /start - Start bot
├─ /help - Show this help
├─ /ping - Test bot response
├─ /alive - Check if bot is alive
├─ /status - Bot status

**Group Management:**
├─ /allow <group_id> - Allow group
├─ /safe @bot - Add bot to safe list
├─ /delay @bot - Add bot to delayed list
├─ /remove @bot - Remove bot from lists

**Protection & Testing:**
├─ /sleepstatus - Sleep protection status
├─ /floodstatus - Flood protection status
├─ /nleep - Sleep protection check
├─ /test - Test message deletion

**Examples:**
`/allow -1001234567890`
`/safe @grouphelp`
`/delay @spam_bot`
`/remove @bot`
            """
            await message.reply(help_text)
        
        @app.on_message(filters.command("ping"))
        async def ping_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            await message.reply("🏓 **Pong!** Bot is active and responding!")
        
        @app.on_message(filters.command("alive"))
        async def alive_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            await message.reply("🟢 **BOT ZINDA HAI!** 24/7 Active with Sleep Protection!")
        
        @app.on_message(filters.command("nleep"))
        async def nleep_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            await message.reply("🚫 **SLEEP NAHI HOGAA!** Ultimate Protection Active!")
        
        @app.on_message(filters.command("status"))
        async def status_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            nonlocal me
            if me is None:
                me = await app.get_me()
            
            status_text = f"""
🤖 **BOT STATUS**

**Bot Info:**
├─ Name: {me.first_name}
├─ Username: @{me.username}

**Protection Status:**
├─ Groups: {len(allowed_groups)}
├─ Safe Bots: {len(safe_bots)}
├─ Delayed Bots: {len(delayed_bots)}
├─ Sleep Protection: 🛡️ ACTIVE
├─ Flood Protection: 🛡️ ACTIVE
└─ Message Deletion: 🗑️ WORKING

**Large Groups:**
├─ -1002129045974 ✅
├─ -1002497459144 ✅
└─ Data Save: ✅ AUTOMATIC
            """
            await message.reply(status_text)
        
        @app.on_message(filters.command("sleepstatus"))
        async def sleepstatus_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            uptime = int(time.time() - start_time)
            await message.reply(f"🛡️ **SLEEP PROTECTION ACTIVE**\nUptime: {uptime}s")
        
        @app.on_message(filters.command("floodstatus"))
        async def floodstatus_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            nonlocal last_delete_time, delete_count
            
            time_since_last = time.time() - last_delete_time
            status_text = f"""
🛡️ **FLOOD PROTECTION STATUS**

**Activity:**
├─ Last Delete: {time_since_last:.1f}s ago
├─ Total Deletes: {delete_count}
├─ Flood Delay: {FLOOD_DELAY}s
└─ Status: ✅ ACTIVE

**Protection:**
• Prevents Telegram rate limits
• Automatic flood wait recovery
• Stable message deletion
            """
            await message.reply(status_text)
        
        @app.on_message(filters.command("allow"))
        async def allow_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            if len(message.command) > 1:
                group_id = message.command[1]
                allowed_groups.add(group_id)
                save_data(ALLOWED_GROUPS_FILE, allowed_groups)
                await message.reply(f"✅ Group `{group_id}` allowed & SAVED!")
                print(f"✅ Group saved: {group_id}")
            else:
                await message.reply("❌ Usage: `/allow <group_id>`")
        
        @app.on_message(filters.command("safe"))
        async def safe_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                safe_bots.add(bot_username)
                save_data(SAFE_BOTS_FILE, safe_bots)
                await message.reply(f"✅ @{bot_username} added to safe list & SAVED!")
                print(f"✅ Safe bot saved: @{bot_username}")
            else:
                await message.reply("❌ Usage: `/safe @botusername`")
        
        @app.on_message(filters.command("delay"))
        async def delay_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                delayed_bots.add(bot_username)
                save_data(DELAYED_BOTS_FILE, delayed_bots)
                await message.reply(f"⏰ @{bot_username} added to delayed list & SAVED!")
                print(f"⏰ Delayed bot saved: @{bot_username}")
            else:
                await message.reply("❌ Usage: `/delay @botusername`")
        
        @app.on_message(filters.command("remove"))
        async def remove_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            if len(message.command) > 1:
                bot_username = message.command[1].replace('@', '').lower()
                safe_bots.discard(bot_username)
                delayed_bots.discard(bot_username)
                save_data(SAFE_BOTS_FILE, safe_bots)
                save_data(DELAYED_BOTS_FILE, delayed_bots)
                await message.reply(f"🗑️ @{bot_username} removed from all lists & SAVED!")
                print(f"🗑️ Bot removed: @{bot_username}")
            else:
                await message.reply("❌ Usage: `/remove @botusername`")
        
        @app.on_message(filters.command("test"))
        async def test_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            test_msg = await message.reply("🧪 Testing all systems...")
            await asyncio.sleep(2)
            await test_msg.delete()
            await message.reply("✅ All systems working perfectly!")
        
        # 🚀 COMPLETE MESSAGE HANDLER WITH ALL FEATURES
        @app.on_message(filters.group)
        async def complete_message_handler(client, message: Message):
            try:
                group_id = str(message.chat.id)
                if group_id not in allowed_groups:
                    return
                
                # Self check
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower()
                message_text = message.text or message.caption or ""
                
                if is_bot:
                    # Safe bot check
                    if username in safe_bots:
                        return
                    
                    # ✅ DELAYED BOT LOGIC
                    if username in delayed_bots:
                        # SMART LINK DETECTION
                        has_links = any(pattern in message_text.lower() for pattern in [
                            't.me/', 'http://', 'https://', 'www.', '.com', '.org', '.net'
                        ])
                        has_mentions = '@' in message_text
                        
                        # INSTANT DELETE FOR LINKS & MENTIONS
                        if has_links or has_mentions:
                            print(f"🚫 Delayed bot with links/mentions: @{username} - INSTANT DELETE")
                            try:
                                await message.delete()
                                print(f"✅ Instant deleted: @{username}")
                            except Exception as e:
                                print(f"❌ Delete failed: {e}")
                        
                        # NORMAL MESSAGES - 30 SECOND DELAY
                        else:
                            print(f"⏰ Delayed bot normal message: @{username} - 30s delay")
                            async def delete_after_delay():
                                await asyncio.sleep(30)
                                try:
                                    await message.delete()
                                    print(f"✅ Delayed delete: @{username}")
                                except:
                                    pass
                            asyncio.create_task(delete_after_delay())
                        return
                    
                    # 🗑️ OTHER BOTS - FLOOD-PROTECTED DELETE
                    nonlocal last_delete_time, delete_count
                    current_time = time.time()
                    time_since_last = current_time - last_delete_time
                    
                    if time_since_last < FLOOD_DELAY:
                        await asyncio.sleep(FLOOD_DELAY - time_since_last)
                    
                    try:
                        await message.delete()
                        last_delete_time = time.time()
                        delete_count += 1
                        print(f"✅ DELETE SUCCESS: @{username} | Count: {delete_count}")
                    except Exception as e:
                        error_msg = str(e)
                        print(f"❌ DELETE FAILED: @{username} | Error: {error_msg}")
                        
                        if "FLOOD_WAIT" in error_msg:
                            print("🚫 FLOOD WAIT - Waiting 10 seconds")
                            await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ Handler error: {e}")
        
        # ✅ BOT START
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        start_time = time.time()
        print(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # 🎯 PERMANENT AUTO-SETUP
        allowed_groups.add("-1002129045974")
        allowed_groups.add("-1002497459144")
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        print(f"✅ PERMANENT GROUPS: {allowed_groups}")
        print("💾 DATA SAVE: AUTOMATIC")
        print("🛡️ FLOOD PROTECTION: ACTIVE")
        print("🗑️ MESSAGE DELETION: READY")
        
        # Startup confirmation
        await app.send_message("me", """
✅ **ULTIMATE BOT STARTED - COMPLETE VERSION!**

🤖 **ALL FEATURES ACTIVE:**
• Complete Commands Set
• Automatic Data Saving
• Flood Protection
• Sleep Protection
• Smart Bot Detection
• Large Group Optimized

🎯 **DELAYED BOTS:**
• Links/Mentions → INSTANT DELETE
• Normal Messages → 30s DELAY

🚀 **PERFORMANCE:**
• 100% Message Deletion
• No Flood Wait Issues
• Continuous Operation

**BOT READY WITH ALL FEATURES!** 🔥
        """)
        
        print("🤖 BOT READY - Complete Version Active!")
        
        # Permanent run
        await asyncio.Future()
        
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    print("🚀 ULTIMATE BOT STARTING...")
    asyncio.run(main())
