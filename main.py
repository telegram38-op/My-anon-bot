import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telethon import TelegramClient, events
import asyncio

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

# --- 2. Aapka Anonymous Bot Code ---
api_id = 30052784
api_hash = 'd293751024445d1d9d56d75e9bd80c01'
bot_token = '8679827577:AAE3tjUf0p_qiBBfUfO9b_2sNjITMt0FXuQ'
target_group = -1003470297330

client = TelegramClient('anon_session', api_id, api_hash)
user_cooldown = {}

@client.on(events.NewMessage(chats=target_group))
async def handler(event):
    if event.sender_id == (await client.get_me()).id:
        return
    
    user_id = event.sender_id
    current_time = asyncio.get_event_loop().time()

    if user_id in user_cooldown and current_time - user_cooldown[user_id] < 3:
        try: await event.delete()
        except: pass
        return
    
    user_cooldown[user_id] = current_time

    if event.text:
        msg_text = event.text
        try:
            await event.delete()
            await client.send_message(event.chat_id, f"👤 **Anonymous:**\n\n{msg_text}")
        except Exception as e:
            print(f"Error: {e}")

# --- Naye Python version ke liye Fix ---
async def main():
    await client.start(bot_token=bot_token)
    print("✅ Bot is online now!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
