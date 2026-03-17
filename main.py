import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telethon import TelegramClient, events
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
bot_token = '8679827577:AAE3tjUf0p_qiBBfUfO9b_2sNjITMt0FXuQ'
target_groups = [-1003684964048, -1001902540748] 

# Aapki dono Whitelisted IDs
WHITELISTED_IDS = [5960920349, 7720568554]

client = TelegramClient('anon_session', api_id, api_hash)

# Member ke naam se unique code banane ke liye function
def get_member_identity(user):
    first_name = user.first_name if user.first_name else "User"
    # Naam ko clean karke uppercase mein lena
    clean_name = "".join(x for x in first_name if x.isalnum()).upper()[:8]
    # Ek unique hash suffix taaki same naam ke log alag dikhein
    unique_suffix = hashlib.md5(str(user.id).encode()).hexdigest()[:4].upper()
    return f"Member_{clean_name}_{unique_suffix}"

@client.on(events.NewMessage(chats=target_groups))
async def handler(event):
    if not event.sender_id:
        return

    # 1. Bot ke apne message ignore karein
    me = await client.get_me()
    if event.sender_id == me.id:
        return

    # 2. ADMIN/OWNER BYPASS
    # Agar aap dono message karenge toh bot touch nahi karega
    if event.sender_id in WHITELISTED_IDS:
        return

    # 3. Duplicate check (Anonymous format ignore)
    if event.text and "👤 **Member_" in event.text:
        return
    
    if event.text:
        sender = await event.get_sender()
        user_identity = get_member_identity(sender)
        msg_text = event.text
        try:
            # Check permissions for other admins
            perms = await client.get_permissions(event.chat_id, event.sender_id)
            if perms.is_admin or perms.is_creator:
                return

            await event.delete()
            # Naya Format: 👤 Member_NAME_CODE: Message
            await client.send_message(event.chat_id, f"👤 **{user_identity}:**\n\n{msg_text}")
        except Exception as e:
            print(f"Error: {e}")
            # Agar permissions check fail ho toh safety ke liye anonymous kar dena
            try:
                await event.delete()
                await client.send_message(event.chat_id, f"👤 **{user_identity}:**\n\n{msg_text}")
            except: pass

async def main():
    await client.start(bot_token=bot_token)
    print("✅ Bot is online with Personalized IDs!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
