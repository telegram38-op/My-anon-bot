import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import hashlib

# --- 1. Render Dummy Server ---
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b"Bot is Running Safely!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('', port), handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# --- 2. Bot Configuration ---
api_id = 30052784
api_hash = 'd293751024445d1d9d56d75e9bd80c01'
bot_token = '8213579010:AAFZJoJ_M5DOt_VlDKYuEuyHhiwYxUVSYN8'
target_groups = [-1003684964048, -1001902540748] 

client = TelegramClient('anon_session', api_id, api_hash)

# User ID se ek chota unique code banane ke liye function
def get_unique_name(user_id):
    readable_hash = hashlib.md5(str(user_id).encode()).hexdigest()[:5].upper()
    return f"Member_{readable_hash}"

@client.on(events.NewMessage(chats=target_groups))
async def handler(event):
    if event.sender_id == (await client.get_me()).id:
        return

    # 1. Admin/Owner Check
    # Agar admin message karega toh bot ignore karega
    try:
        permissions = await client.get_permissions(event.chat_id, event.sender_id)
        if permissions.is_admin or permissions.is_creator:
            return 
    except:
        pass # Agar permissions check na ho payein toh normal process karega

    # 2. Duplicate Fix
    if event.text and "👤 **Member_" in event.text:
        return
    
    if event.text:
        user_code = get_unique_name(event.sender_id)
        msg_text = event.text
        try:
            await event.delete()
            # Ab ye dikhayega: 👤 Member_A1B2: Message
            await client.send_message(event.chat_id, f"👤 **{user_code}:**\n\n{msg_text}")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("✅ Bot is online with Admin Bypass & Unique IDs!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
