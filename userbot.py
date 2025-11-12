print("🎯 BOT STARTING WITH DELETE FIX...")

import asyncio
import multiprocessing
import re
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot data storage
allowed_groups = set()
safe_bots = set()
delayed_bots = set()

# Flask Server
def start_flask():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 Bot Server Running!"
    
    @app.route('/ping')
    def ping():
        return "🏓 Pong! Bot is alive"
    
    print("🌐 Flask starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask in background
print("🚀 Starting Flask server...")
flask_process = multiprocessing.Process(target=start_flask)
flask_process.daemon = True
flask_process.start()
print("✅ Flask server started!")

# Telegram Bot
async def start_telegram():
    print("🔗 Starting Telegram Bot...")
    
    try:
        from pyrogram import Client, filters
        
        app = Client(
            "delete_bot",
            api_id=22294121,
            api_hash="0f7fa7216b26e3f52699dc3c5a560d2a",
            session_string="AQFULmkANrpQWKdmd5cy7VgvL2DA9KATYlSUq5PSoJ5K1easAzrA_p5fxgFRVEUyABixgFmrCGtF9x_KvrQUoAWdeQ1dGqYggCnST6nMPBipTv7GIgwU_w1kewukwsWPMUbWdos0VI7CtH1HYwW7wz3VQ2_hvtdwQCDRHsIxpwek3IcSXP-hpt8vz_8Z4NYf8uUiIwZCSJluef3vGSh7TLOfekcrjVcRd_2h59kBuGgV7DzyJxZwx8eyNJOyhpYQnlExnd24CnELB6ZNYObYBH6xnE2Rgo97YGN1WPbd9Ra8oQUx2phHT4KTWZNktzjenv6hM7AH8lyVyRvGtillQOA_Dq23TwAAAAHy0lZEAA"
        )
        
        # TEST COMMANDS
        @app.on_message(filters.command("ping"))
        async def ping_handler(client, message: Message):
            await message.reply("🏓 Pong! Delete feature active!")
        
        @app.on_message(filters.command("status"))
        async def status_handler(client, message: Message):
            me = await app.get_me()
            groups_list = ", ".join(allowed_groups) if allowed_groups else "None"
            status_text = f"""
🤖 **Bot Status - DELETE ENABLED**
├─ **Name:** {me.first_name}
├─ **ID:** `{me.id}`
├─ **Allowed Groups:** {len(allowed_groups)}
├─ **Groups:** {groups_list}
├─ **Safe Bots:** {len(safe_bots)}
└─ **Delayed Bots:** {len(delayed_bots)}

**✅ Bot is ready to delete messages!**
            """
            await message.reply(status_text)
            print("✅ Status command executed")
        
        # ALLOW COMMAND - SIMPLE VERSION
        @app.on_message(filters.command("allow"))
        async def allow_handler(client, message: Message):
            if len(message.command) > 1:
                group_id = message.command[1]
                allowed_groups.add(group_id)
                await message.reply(f"✅ Group `{group_id}` allowed!\n\nNow add me to that group as ADMIN with Delete Messages permission.")
                print(f"✅ Group added: {group_id}")
                print(f"📋 Allowed groups: {allowed_groups}")
            else:
                await message.reply("❌ Usage: /allow <group_id>\n\nGet group ID from @RawDataBot")
        
        # TEST DELETE COMMAND
        @app.on_message(filters.command("testdelete"))
        async def test_delete_handler(client, message: Message):
            if message.reply_to_message:
                try:
                    await message.reply_to_message.delete()
                    await message.reply("✅ Message deleted successfully!")
                    print("✅ Test delete successful")
                except Exception as e:
                    await message.reply(f"❌ Delete failed: {e}")
                    print(f"❌ Delete failed: {e}")
            else:
                await message.reply("❌ Reply to a message with /testdelete to test deletion")
        
        # SIMPLE MESSAGE HANDLER - DELETE ALL LINKS
        @app.on_message(filters.group)
        async def delete_links_handler(client, message: Message):
            try:
                group_id = str(message.chat.id)
                print(f"🔍 Checking message in group: {group_id}")
                print(f"📋 Allowed groups: {allowed_groups}")
                
                # Check if group is allowed
                if group_id not in allowed_groups:
                    print(f"❌ Group {group_id} not in allowed list")
                    return
                
                print(f"✅ Group {group_id} is allowed")
                
                # Don't process own messages
                me = await app.get_me()
                if message.from_user and message.from_user.id == me.id:
                    return
                
                message_text = message.text or message.caption or ""
                print(f"📝 Message text: {message_text}")
                
                # Check for links
                has_links = 't.me/' in message_text.lower() or 'http' in message_text.lower() or '@' in message_text
                
                if has_links:
                    print(f"🔗 Link detected in message")
                    try:
                        await message.delete()
                        print(f"🗑️ SUCCESS: Deleted link message in group {group_id}")
                        
                        # Notify in private (optional)
                        try:
                            await app.send_message(
                                "me", 
                                f"🗑️ Deleted link in group {group_id}\nMessage: {message_text[:100]}..."
                            )
                        except:
                            pass
                            
                    except Exception as e:
                        print(f"❌ DELETE FAILED: {e}")
                        # Send error to private
                        try:
                            await app.send_message(
                                "me",
                                f"❌ Delete failed in {group_id}\nError: {e}\nMake sure I have delete permissions!"
                            )
                        except:
                            pass
                
            except Exception as e:
                print(f"❌ Error in handler: {e}")
        
        print("🚀 Starting Telegram client...")
        await app.start()
        
        me = await app.get_me()
        print(f"🎉 BOT CONNECTED: {me.first_name} ({me.id})")
        
        # Send startup message with instructions
        try:
            await app.send_message("me", """
✅ **Bot Started with DELETE Feature!**

**To Setup:**
1. Get your group ID from @RawDataBot
2. Use `/allow <group_id>` 
3. Add me to group as ADMIN
4. Give me DELETE MESSAGES permission
5. Test with /testdelete

Bot will auto-delete links! 🚀
            """)
            print("✅ Startup message sent")
        except:
            print("⚠️ Could not send startup message")
        
        print("🤖 Bot is now running with DELETE FEATURE!")
        
        # Keep alive
        while True:
            await asyncio.sleep(10)
            
    except Exception as e:
        print(f"❌ Telegram Error: {e}")
        import traceback
        traceback.print_exc()

# Main execution
async def main():
    print("🔧 Starting main function...")
    await start_telegram()

if __name__ == "__main__":
    print("⭐ Bot Script Starting...")
    asyncio.run(main())
if __name__ == "__main__":
    print("⭐ Bot Script Starting...")
    asyncio.run(main())
