print("🔥 ULTIMATE BOT STARTING - SESSION STABILITY FIX...")

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

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(list(data), f)
    except:
        pass

# ---------------------------------------------------------
# ✅ CLEAN MASTER LISTS (as you gave)
# ---------------------------------------------------------
allowed_groups = {
    "-1002382070176",
    "-1002497459144"
}

safe_bots = {
    "unobot",
    "on9wordchainbot",
    "daisyfcbot",
    "missrose_bot",
    "zorofcbot",
    "digi4bot"
}

delayed_bots = {
    "crocodile_game4_bot"
}

# Save clean lists to files
save_data(ALLOWED_GROUPS_FILE, allowed_groups)
save_data(SAFE_BOTS_FILE, safe_bots)
save_data(DELAYED_BOTS_FILE, delayed_bots)

print("✅ Clean lists applied (old entries removed & replaced)")

# YOUR USER ID
ADMIN_USER_ID = 8368838212

# 🛡️ ULTIMATE SLEEP PROTECTION
class SleepProtection:
    def __init__(self):
        self.ping_count = 0
        self.start_time = time.time()
        
    def start_protection(self):
        print("🛡️ Starting Ultimate Sleep Protection...")
        self.start_flask()
        self.start_external_pings()
        print("✅ SLEEP PROTECTION: ACTIVATED")
    
    def start_flask(self):
        def run_flask():
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                self.ping_count += 1
                return f"🤖 BOT ACTIVE - Pings: {self.ping_count}"
            
            @app.route('/ping')
            def ping():
                self.ping_count += 1
                return "🏓 Pong"
            
            @app.route('/health')
            def health():
                return "✅ HEALTHY"
            
            def auto_ping():
                while True:
                    try:
                        requests.get("http://localhost:10000/ping", timeout=5)
                    except:
                        pass
                    time.sleep(30)
            
            threading.Thread(target=auto_ping, daemon=True).start()
            app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
        
        multiprocessing.Process(target=run_flask, daemon=True).start()
        time.sleep(3)
        print("✅ Flask Server: RUNNING")
    
    def start_external_pings(self):
        def external_pinger():
            urls = [
                "https://userbot-telegram-1.onrender.com/",
                "https://userbot-telegram-1.onrender.com/ping"
            ]
            while True:
                for url in urls:
                    try:
                        requests.get(url, timeout=10)
                    except:
                        pass
                time.sleep(60)
        
        threading.Thread(target=external_pinger, daemon=True).start()
        print("✅ External Pings: RUNNING")

# Start protection
sleep_protector = SleepProtection()
sleep_protector.start_protection()

# 🔥 TELEGRAM BOT START
async def start_telegram():
    print("🔗 Starting Telegram Bot - SESSION STABILITY FIX...")
    
    session_active = True
    connection_checks = 0
    
    try:
        app = Client(
            "ultimate_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        def is_admin(uid):
            return uid == ADMIN_USER_ID
        
        me = None
        
        # --------------------------
        # ONLINE STATUS LOOP
        # --------------------------
        async def simple_online_status():
            online_count = 0
            while session_active:
                online_count += 1
                try:
                    await app.get_me()
                    print(f"🟢 Online Status #{online_count}")
                except Exception as e:
                    print(f"⚠️ Online Status Error: {e}")
                await asyncio.sleep(60)
        
        # --------------------------
        # KEEP ALIVE LOOP
        # --------------------------
        async def session_keep_alive():
            nonlocal connection_checks, session_active
            count = 0
            while session_active:
                count += 1
                connection_checks += 1
                try:
                    if me:
                        await app.get_me()
                except:
                    session_active = False
                    break
                await asyncio.sleep(180)

        # COMMANDS (unchanged)
        @app.on_message(filters.command("start"))
        async def start_command(client, message):
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🚀 **ULTIMATE BOT STARTED!**")

        @app.on_message(filters.command("help"))
        async def help_command(client, message):
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("📘 Help Working")

        @app.on_message(filters.command("ping"))
        async def ping_command(client, message):
            if message.from_user and is_admin(message.from_user.id):
                await message.reply("🏓 Pong!")

        @app.on_message(filters.command("status"))
        async def status_command(client, message):
            if message.from_user and is_admin(message.from_user.id):
                nonlocal me
                if me is None:
                    me = await app.get_me()
                await message.reply(f"Alive: {connection_checks}")

        # ---------------------------------------------------------
        # 🚨 SUPER-STABLE DELETE HANDLER (UPGRADED)
        # ---------------------------------------------------------
        @app.on_message(filters.group)
        async def deletion_handler(client, message: Message):
            try:
                # Allowed group check
                if str(message.chat.id) not in allowed_groups:
                    return

                # Self-ignore
                nonlocal me
                if me is None:
                    me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return

                if not message.from_user:
                    return

                is_bot = message.from_user.is_bot
                username = (message.from_user.username or "").lower()
                text = (message.text or message.caption or "").lower()

                if not is_bot:
                    return

                print(f"🤖 Bot detected: @{username}")

                # SAFE BOT
                if username in safe_bots:
                    print(f"🟢 Safe bot ignored: @{username}")
                    return

                # DELAY BOT LOGIC
                if username in delayed_bots:
                    has_link = "t.me/" in text or "http" in text
                    has_at = "@" in text

                    if has_link or has_at:
                        print("🚫 Link detected in delay bot — INSTANT DELETE")
                        await message.delete()
                        return

                    print("⏳ Delay bot — deleting in 30 seconds")
                    async def delayed_del():
                        await asyncio.sleep(30)
                        try:
                            await message.delete()
                        except:
                            pass
                    asyncio.create_task(delayed_del())
                    return

                # DEFAULT UNSAFE BOT -> IMMEDIATE DELETE
                print(f"🗑️ Unsafe bot -> DELETE @{username}")
                try:
                    await message.delete()
                except:
                    await asyncio.sleep(1)
                    try:
                        await message.delete()
                    except:
                        print("❌ Delete failed")

            except Exception as e:
                print(f"❌ Delete handler error: {e}")

        # START APP
        print("🔗 Connecting...")
        await app.start()
        me = await app.get_me()

        keep_alive = asyncio.create_task(session_keep_alive())
        online = asyncio.create_task(simple_online_status())

        print("🤖 BOT READY!")

        await asyncio.Future()

    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# Runner
async def main():
    await start_telegram()

if __name__ == "__main__":
    asyncio.run(main())
