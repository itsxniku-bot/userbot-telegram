# IMGHDR FIX - Add this at the VERY TOP
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
import http.server
import socketserver
from datetime import datetime

print("🚀 SCRIPT STARTING...")

# DEBUG KEEP-ALIVE - With exception handling
def debug_keep_alive():
    print("🔄 KEEP-ALIVE THREAD STARTED!")
    
    ping_count = 0
    while True:
        try:
            ping_count += 1
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"🔄 [{current_time}] Keep-alive loop #{ping_count} - BEFORE PING")
            
            # Try multiple ping methods
            success = False
            for i in range(3):
                try:
                    response = requests.get(f'http://localhost:8080/ping_{ping_count}', timeout=5)
                    print(f"✅ [{current_time}] Ping #{ping_count}.{i+1}: SUCCESS (Status: {response.status_code})")
                    success = True
                    break
                except requests.exceptions.ConnectionError:
                    print(f"❌ [{current_time}] Ping #{ping_count}.{i+1}: Connection failed")
                except Exception as e:
                    print(f"⚠️ [{current_time}] Ping #{ping_count}.{i+1}: Error - {e}")
            
            if not success:
                print(f"🔴 [{current_time}] ALL PING METHODS FAILED!")
            
            print(f"🔄 [{current_time}] Keep-alive loop #{ping_count} - AFTER PING")
            
        except Exception as e:
            print(f"🚨 [{current_time}] KEEP-ALIVE CRITICAL ERROR: {e}")
            print("🔄 Restarting keep-alive in 30 seconds...")
            time.sleep(30)
            continue
        
        # Wait 1 minute (for testing)
        print(f"⏰ [{current_time}] Waiting 60 seconds for next ping...")
        time.sleep(60)

# START KEEP-ALIVE IMMEDIATELY
print("🔧 Starting keep-alive thread...")
try:
    keep_thread = threading.Thread(target=debug_keep_alive, daemon=True)
    keep_thread.start()
    print("✅ Keep-alive thread started successfully!")
except Exception as e:
    print(f"❌ Failed to start keep-alive: {e}")

# SIMPLE HTTP SERVER
class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Bot is running!')
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"🌐 [{current_time}] HTTP Request: {self.path}")
    
    def log_message(self, format, *args):
        pass  # No logs

def start_http_server():
    try:
        server = socketserver.TCPServer(("", 8080), SimpleHandler)
        print("🌐 HTTP Server started on port 8080")
        server.serve_forever()
    except Exception as e:
        print(f"❌ HTTP Server failed: {e}")

print("🔧 Starting HTTP server...")
try:
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    print("✅ HTTP server started!")
except Exception as e:
    print(f"❌ Failed to start HTTP server: {e}")

# Test if threads are alive
def check_threads():
    time.sleep(10)
    print("🔍 THREAD STATUS CHECK:")
    print(f"   Keep-alive thread alive: {keep_thread.is_alive()}")
    print(f"   HTTP server thread alive: {http_thread.is_alive()}")

print("🔧 Starting thread monitor...")
monitor_thread = threading.Thread(target=check_threads, daemon=True)
monitor_thread.start()

# REST OF YOUR TELEGRAM CODE (SAME AS BEFORE)
print("📱 Importing Telegram libraries...")
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
import json
import asyncio
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

print("🔑 Setting up Telegram client...")

# API credentials
api_id = int(os.environ.get('api_id', 22294121))
api_hash = os.environ.get('api_hash', '0f7fa7216b26e3f52699dc3c5a560d2a')
session_string = os.environ.get('SESSION_STRING', 'YOUR_SESSION')

if not session_string:
    logger.error("❌ SESSION_STRING not set!")
    sys.exit(1)

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# ... (REST OF YOUR BOT CODE EXACTLY SAME AS BEFORE)
# [Include all your bot functions, commands, etc. exactly as you had them]

async def main():
    print("🔑 Starting Telegram client...")
    await client.start()
    me = await client.get_me()
    
    logger.info("🚀 DEBUG UserBot Started!")
    logger.info(f"🤖 User: {me.first_name} (ID: {me.id})")
    logger.info("🔄 Debug keep-alive ACTIVE")
    
    # Periodic status check
    async def status_check():
        check_count = 0
        while True:
            check_count += 1
            current_time = datetime.now().strftime('%H:%M:%S')
            logger.info(f"📊 [{current_time}] Status Check #{check_count} - Bot Active")
            await asyncio.sleep(300)  # Every 5 minutes
    
    asyncio.create_task(status_check())
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    print("🎯 DEBUG MODE STARTED!")
    print("🔍 We'll identify why keep-alive stops")
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
