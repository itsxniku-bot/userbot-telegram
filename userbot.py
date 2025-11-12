# IMGHDR FIX
import sys
import types
try:
    import imghdr
except ImportError:
    imghdr = types.ModuleType('imghdr')
    def what(file, h=None): return None
    imghdr.what = what
    sys.modules['imghdr'] = imghdr

import requests
import threading
import time
import os
from datetime import datetime

print("🚀 STARTING...")

# KEEP-ALIVE (Working - same as before)
def keep_alive():
    print("🔄 KEEP-ALIVE STARTED")
    time.sleep(10)
    
    count = 0
    while True:
        count += 1
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"✅ [{current_time}] KEEP-ALIVE ACTIVE #{count}")
            requests.get('http://localhost:8080', timeout=5)
        except: pass
        time.sleep(120)

thread = threading.Thread(target=keep_alive)
thread.daemon = True
thread.start()

# HTTP SERVER
def simple_server():
    import http.server
    import socketserver
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self): 
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        def log_message(self, *args): pass
    try:
        with socketserver.TCPServer(("", 8080), Handler) as httpd:
            print("🌐 HTTP Server started")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ HTTP Error: {e}")

http_thread = threading.Thread(target=simple_server)
http_thread.daemon = True
http_thread.start()

# TELEGRAM BOT - DEBUG VERSION
print("📱 LOADING TELEGRAM CLIENT...")
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Your credentials
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', '1AZWarzwBu0-LovZ8Z49vquFuHumXjYjVhvOy3BsxrrYp5qtVtPo9hkNYZ19qtGw3KCZLwNXOAwAaraKF6N8vtJkjOUpmc112-i289RtR6nuJaTorpJ1yXQzGvJ-RF14DUVnc-c_UYF4PR64wPaTSF-0qDYH3F_NcV2lbyJJSqxN96NauXuuxdhl1bYAtPoV58-e2RRdmF3G5Ozp55n-RPu9GO0Q_ZU7U865ekQrCwQDrkF77GKyv1RXo97S_B4iAgQDDaXSlLWqkYqozkEoZUSrRAYs1mpoYItir7l9is-TV4FAW9gz8e2N4pwKsJ9tDwBMK8snMHDhdtsvRuEO1WyALndXBnTc=')

print(f"🔑 API_ID: {api_id}")
print(f"🔑 API_HASH: {api_hash}")
print(f"🔑 SESSION_LENGTH: {len(session_string) if session_string else 0}")

if not session_string:
    logger.error("❌ SESSION_STRING not set!")
    sys.exit(1)

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# TEST EVENT - Simple message handler
@client.on(events.NewMessage)
async def test_handler(event):
    try:
        print(f"📩 MESSAGE RECEIVED: {event.text}")
        logger.info(f"📩 Message from {event.sender_id}: {event.text}")
        
        # Test command
        if event.text and event.text.startswith('!test'):
            await event.reply("🤖 Bot is WORKING! Test successful!")
            logger.info("✅ Test command executed")
            
    except Exception as e:
        logger.error(f"❌ Handler error: {e}")

# Connection events
@client.on(events.ConnectionError)
async def connection_error(event):
    logger.error("❌ Connection error!")

@client.on(events.Disconnect)
async def disconnect(event):
    logger.error("❌ Disconnected!")

async def main():
    print("🔑 STARTING TELEGRAM CLIENT...")
    try:
        await client.start()
        print("✅ TELEGRAM CLIENT STARTED")
        
        me = await client.get_me()
        print(f"🤖 LOGGED IN AS: {me.first_name} (ID: {me.id})")
        logger.info(f"🤖 Bot started for: {me.first_name} (ID: {me.id})")
        
        # Send a message to saved messages to test
        try:
            await client.send_message('me', '🤖 Bot started successfully!')
            print("✅ TEST MESSAGE SENT")
        except Exception as e:
            print(f"❌ Test message failed: {e}")
        
        print("🔄 RUNNING CLIENT...")
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ Telegram client failed: {e}")
        print(f"❌ TELEGRAM ERROR: {e}")

if __name__ == '__main__':
    print("🎯 STARTING BOT...")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"🚨 FATAL ERROR: {e}")
        print(f"🚨 FATAL: {e}")
