print("🔥 ULTIMATE BOT STARTING - SPECIFIC GROUP FIX...")

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

# Bot data storage
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

print(f"✅ Loaded {len(allowed_groups)} groups")

# 🛡️ SLEEP PROTECTION
def run_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 BOT ACTIVE"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong"
    
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

print("🔥 Starting Flask...")
flask_process = multiprocessing.Process(target=run_flask, daemon=True)
flask_process.start()
time.sleep(3)
print("✅ Flask started!")

# 🔥 TELEGRAM BOT WITH SPECIFIC GROUP DEBUG
async def start_telegram():
    print("🔗 Starting Telegram Bot - SPECIFIC GROUP DEBUG...")
    
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
        
        # ✅ COMMANDS
        @app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            await message.reply("🚀 **BOT STARTED!** Specific Group Debug")
        
        @app.on_message(filters.command("debug"))
        async def debug_command(client, message: Message):
            if not is_admin(message.from_user.id):
                return
            
            # Test specific group
            test_group = "-1002497459144"
            debug_info = f"""
🔍 **DEBUG INFO - GROUP -1002497459144**

**Group in Allowed List:** {'✅ YES' if test_group in allowed_groups else '❌ NO'}
**Total Allowed Groups:** {len(allowed_groups)}
**Bot Connected:** {'✅ YES' if me else '❌ NO'}

**Next Steps:**
1. Check if bot is ADMIN in group
2. Check "Delete Messages" permission  
3. Send bot message in group for test
            """
            await message.reply(debug_info)
            print(f"🔍 DEBUG: Group -1002497459144 in allowed_groups: {test_group in allowed_groups}")
        
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
        
        # 🚀 SPECIFIC GROUP DEBUG HANDLER
        @app.on_message(filters.group)
        async def specific_group_debug_handler(client, message: Message):
            try:
                group_id = str(message.chat.id)
                group_title = message.chat.title
                
                print(f"🔍 MESSAGE IN: {group_title} ({group_id})")
                
                # SPECIFIC DEBUG FOR PROBLEM GROUP
                if group_id == "-1002497459144":
                    print(f"🎯 TARGET GROUP DETECTED: {group_title}")
                    print(f"   Allowed: {'✅ YES' if group_id in allowed_groups else '❌ NO'}")
                
                if group_id not in allowed_groups:
                    print(f"   ❌ GROUP NOT ALLOWED: {group_title}")
                    return
                
                print(f"   ✅ GROUP ALLOWED: {group_title}")
                
                # Self check
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                is_bot = message.from_user.is_bot if message.from_user else False
                username = (message.from_user.username or "").lower()
                
                if is_bot:
                    print(f"   🤖 BOT DETECTED: @{username}")
                    
                    if username in safe_bots:
                        print(f"   ✅ SAFE BOT IGNORED: @{username}")
                        return
                    
                    # DELETE ATTEMPT WITH DETAILED LOGGING
                    print(f"   🗑️ ATTEMPTING DELETE: @{username} in {group_title}")
                    try:
                        await message.delete()
                        print(f"   ✅ DELETE SUCCESS: @{username} in {group_title}")
                    except Exception as e:
                        print(f"   ❌ DELETE FAILED: @{username} in {group_title}")
                        print(f"   ERROR: {e}")
                        # Permission error check
                        if "DELETE_MESSAGE" in str(e) or "permission" in str(e).lower():
                            print(f"   🔒 PERMISSION ERROR: Bot needs 'Delete Messages' admin right")
                
            except Exception as e:
                print(f"❌ Handler error in {message.chat.title if message.chat else 'Unknown'}: {e}")
        
        # ✅ BOT START
        print("🔗 Connecting to Telegram...")
        await app.start()
        
        me = await app.get_me()
        print(f"✅ BOT CONNECTED: {me.first_name} (@{me.username})")
        
        # 🎯 FORCE ADD PROBLEM GROUP
        allowed_groups.add("-1002129045974")  # Working group
        allowed_groups.add("-1002497459144")  # ❌ PROBLEM GROUP - FORCE ADD
        
        save_data(ALLOWED_GROUPS_FILE, allowed_groups)
        safe_bots.update(["grouphelp", "vid", "like"])
        save_data(SAFE_BOTS_FILE, safe_bots)
        
        print(f"✅ GROUPS FORCE ADDED: {allowed_groups}")
        print("🔍 DEBUG MODE: ACTIVE")
        
        # Startup confirmation
        await app.send_message("me", """
✅ **BOT STARTED - SPECIFIC GROUP DEBUG!**

🎯 **TARGET GROUP: -1002497459144**
• Force added to allowed list
• Debug logging active
• Permission checking enabled

🔍 **DEBUG COMMANDS:**
• /debug - Check group status
• /allow - Add group manually

**Check console logs for detailed debugging!** 🔧
        """)
        
        print("🤖 BOT READY - Specific Group Debug Active!")
        
        # Keep running
        await asyncio.Future()
        
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Main execution
async def main():
    await start_telegram()

if __name__ == "__main__":
    print("🚀 ULTIMATE BOT STARTING...")
    asyncio.run(main())
