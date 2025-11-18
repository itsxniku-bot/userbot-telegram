#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stable USERBOT for Telegram (Pyrogram)
- Deletes unknown bot messages in allowed groups
- Allows safe bots, delays some bots for 3s
- /status command responds only to ADMIN (private chat)
- Built for 24/7 deployment (uses idle, light keep-alive, supervised restart)
- Small Flask /ping endpoint included for uptime monitors (Render)
"""

import os
import sys
import time
import asyncio
import logging
import traceback
import threading

from flask import Flask
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import FloodWait, PeerIdInvalid, UserNotParticipant

# ---------------------------
# CONFIG - prefer using environment variables
# ---------------------------
API_ID = int(os.environ.get("API_ID", "22294121"))              # replace or set env
API_HASH = os.environ.get("API_HASH", "0f7fa7216b26e3f52699dc3c5a560d2a")
SESSION_STRING = os.environ.get("SESSION_STRING")               # REQUIRED
if not SESSION_STRING:
    print("ERROR: set SESSION_STRING environment variable (user session string).")
    sys.exit(1)

# Admin user id (your Telegram user id)
ADMIN_USER_ID = int(os.environ.get("ADMIN_USER_ID", "8368838212"))

# Allowed groups - comma separated list of chat ids (e.g. -100123,-100456)
allowed_groups_env = os.environ.get("ALLOWED_GROUPS", "-1002382070176,-1002497459144")
ALLOWED_GROUPS = set(g.strip() for g in allowed_groups_env.split(",") if g.strip())

# Safe bots - comma separated usernames (no @). You can edit this var or file.
safe_bots_env = os.environ.get("SAFE_BOTS", "unobot,on9wordchainbot,daisyfcbot,missrose_bot,zorofcbot,digi4bot")
SAFE_BOTS = set(s.strip().lower() for s in safe_bots_env.split(",") if s.strip())

# Delayed bots - comma separated usernames (no @). Delete after 3s.
delayed_bots_env = os.environ.get("DELAYED_BOTS", "crocodile_game4_bot")
DELAYED_BOTS = set(s.strip().lower() for s in delayed_bots_env.split(",") if s.strip())

# Flask ping config (for Render uptime)
FLASK_BIND_HOST = "0.0.0.0"
FLASK_BIND_PORT = int(os.environ.get("PORT", "10000"))  # Render sets PORT
PING_PATH = os.environ.get("PING_PATH", "/ping")

# Keep some parameters tunable
KEEPALIVE_INTERVAL = int(os.environ.get("KEEPALIVE_INTERVAL", "25"))  # seconds
DELAYED_DELETE_SECONDS = int(os.environ.get("DELAYED_DELETE_SECONDS", "3"))

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("stable_userbot")

# ---------------------------
# Minimal Flask server (keeps Render aware)
# ---------------------------
def start_flask_server():
    app = Flask("userbot_uptime")

    @app.route("/")
    def home():
        return "Userbot alive", 200

    @app.route(PING_PATH)
    def ping():
        return "pong", 200

    # Run in a separate thread so it doesn't block asyncio loop
    def run():
        try:
            app.run(host=FLASK_BIND_HOST, port=FLASK_BIND_PORT, debug=False, use_reloader=False)
        except Exception as e:
            log.error(f"Flask server crashed: {e}")

    t = threading.Thread(target=run, daemon=True)
    t.start()
    log.info(f"Flask uptime server started on port {FLASK_BIND_PORT} (path: {PING_PATH})")


# ---------------------------
# Pyrogram client (USER session)
# ---------------------------
client = Client(
    "stable_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    workdir="."
)

# track activity
last_activity = time.time()
def touch_activity():
    global last_activity
    last_activity = time.time()

# ---------------------------
# Helper utilities
# ---------------------------
async def safe_sleep(seconds):
    # handle large sleep with cancellation sensitivity
    try:
        await asyncio.sleep(seconds)
    except asyncio.CancelledError:
        raise

def username_from_message(m: Message):
    if m.from_user:
        return (m.from_user.username or f"user_{m.from_user.id}").lower()
    sender_chat = getattr(m, "sender_chat", None)
    if sender_chat:
        return (getattr(sender_chat, "username", None) or getattr(sender_chat, "title", f"sender_{sender_chat.id}")).lower()
    return "unknown"

# ---------------------------
# Message handler logic
# ---------------------------
@client.on_message(filters.group)
async def group_message_handler(_, message: Message):
    try:
        touch_activity()
        chat_id = str(message.chat.id)
        # only process configured allowed groups
        if chat_id not in ALLOWED_GROUPS:
            return

        # determine sender
        is_bot = False
        username = "unknown"
        if message.from_user:
            is_bot = bool(getattr(message.from_user, "is_bot", False))
            username = (message.from_user.username or f"user_{message.from_user.id}").lower()
        else:
            sender_chat = getattr(message, "sender_chat", None)
            if sender_chat:
                # messages from channels
                username = (getattr(sender_chat, "username", None) or getattr(sender_chat, "title", f"sender_{sender_chat.id}")).lower()
                # treat channel as bot-like
                is_bot = True

        # Only act on bot messages
        if not is_bot:
            return

        username_clean = username.lstrip("@").lower()

        # Safe bot -> ignore
        if username_clean in SAFE_BOTS:
            log.info(f"SAFE BOT ignored: @{username_clean} in {chat_id}")
            return

        # Delayed bot -> delete after configured seconds
        if username_clean in DELAYED_BOTS:
            log.info(f"DELAYED BOT detected: @{username_clean} in {chat_id} -> deleting after {DELAYED_DELETE_SECONDS}s")
            # schedule delayed delete
            asyncio.create_task(_delayed_delete(message, DELAYED_DELETE_SECONDS))
            return

        # Unknown bot -> immediate delete (with safe exception handling)
        log.info(f"UNKNOWN BOT detected: @{username_clean} in {chat_id} -> deleting immediately")
        try:
            await message.delete()
            log.info(f"Deleted message from @{username_clean} in {chat_id}")
        except FloodWait as fw:
            log.warning(f"FloodWait while deleting: sleeping {fw.x}s")
            await asyncio.sleep(fw.x + 1)
        except (PeerIdInvalid, UserNotParticipant) as e:
            log.warning(f"Cannot delete in {chat_id} — peer issue: {e}")
        except Exception as e:
            log.error(f"Error deleting message in {chat_id}: {e}")

    except Exception as e:
        log.error(f"group_message_handler error: {e}\n{traceback.format_exc()}")

async def _delayed_delete(message: Message, seconds: int):
    try:
        await safe_sleep(seconds)
        try:
            await message.delete()
            log.info(f"Delayed-deleted message id={message.id} in chat={message.chat.id}")
        except FloodWait as fw:
            log.warning(f"FloodWait during delayed delete: sleeping {fw.x}s")
            await asyncio.sleep(fw.x + 1)
        except (PeerIdInvalid, UserNotParticipant) as e:
            log.warning(f"Cannot delayed-delete in {message.chat.id} — peer issue: {e}")
        except Exception as e:
            log.error(f"Delayed delete failed: {e}")
    except asyncio.CancelledError:
        log.info("Delayed delete task cancelled")

# ---------------------------
# /status command - only for admin and only private
# ---------------------------
@client.on_message(filters.command("status") & filters.private)
async def status_command(_, message: Message):
    try:
        if message.from_user is None or message.from_user.id != ADMIN_USER_ID:
            return
        # basic status
        uptime_seconds = int(time.time() - start_time)
        text = (
            f"🤖 Stable Userbot Status\n\n"
            f"• Uptime: {uptime_seconds}s\n"
            f"• Allowed groups: {len(ALLOWED_GROUPS)}\n"
            f"• Safe bots: {len(SAFE_BOTS)}\n"
            f"• Delayed bots: {len(DELAYED_BOTS)}\n"
            f"• Last activity: {int(time.time() - last_activity)}s ago\n"
        )
        await message.reply(text)
    except Exception as e:
        log.error(f"status_command error: {e}")

# ---------------------------
# Light keep-alive task (safe, low frequency)
# ---------------------------
async def keepalive_task():
    cycles = 0
    while True:
        try:
            cycles += 1
            # minimal API calls to keep session healthy
            try:
                await client.get_me()
            except Exception as e:
                log.warning(f"keepalive get_me failed: {e}")
            touch_activity()
            if cycles % 20 == 0:
                log.info(f"Keepalive cycle #{cycles} - last activity {int(time.time() - last_activity)}s ago")
        except Exception as e:
            log.error(f"keepalive_task error: {e}")
        await asyncio.sleep(KEEPALIVE_INTERVAL)

# ---------------------------
# Supervisor / startup
# ---------------------------
async def start_userbot_supervised():
    backoff = 1
    max_backoff = 60
    while True:
        try:
            log.info("Starting Pyrogram client (userbot)...")
            await client.start()
            log.info("Client started successfully")

            # start flask server for uptime monitoring (safe to run in thread)
            start_flask_server()

            # scan allowed groups lightly (do not remove existing)
            for gid in list(ALLOWED_GROUPS):
                try:
                    await client.get_chat(gid)
                    log.info(f"Verified access for group {gid}")
                except (PeerIdInvalid, UserNotParticipant) as e:
                    log.warning(f"Group {gid} reported not reachable yet: {e}")
                except Exception as e:
                    log.warning(f"Group verify error {gid}: {e}")

            # start background tasks
            tasks = [
                asyncio.create_task(keepalive_task()),
            ]

            # Mark start time
            global start_time
            start_time = time.time()

            # Keep running until idle returns (client.stop or exception)
            await idle()

            # if idle returns, stop tasks and restart loop
            log.info("Idle returned, stopping background tasks...")
            for t in tasks:
                t.cancel()
            try:
                await client.stop()
            except Exception:
                pass

        except Exception as e:
            log.error(f"Supervisor caught exception: {e}\n{traceback.format_exc()}")
            try:
                await client.stop()
            except:
                pass
            log.info(f"Restarting in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)
            continue

# ---------------------------
# Entrypoint
# ---------------------------
if __name__ == "__main__":
    log.info("Launching stable userbot...")
    asyncio.run(start_userbot_supervised())
