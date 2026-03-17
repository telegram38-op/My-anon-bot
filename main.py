from telethon import TelegramClient, events
import asyncio

# --- Aapki Details ---
api_id = 30052784
api_hash = 'd293751024445d1d9d56d75e9bd80c01'
bot_token = '8679827577:AAE3tjUf0p_qiBBfUfO9b_2sNjITMt0FXuQ'
target_group = -1003470297330  # Aapki Group ID

client = TelegramClient('anon_session', api_id, api_hash).start(bot_token=bot_token)

# Spam control: Ek user 3 second se pehle dusra message nahi kar payega
user_cooldown = {}

@client.on(events.NewMessage(chats=target_group))
async def handler(event):
    # Agar bot khud message bhej raha hai toh use ignore karein
    if event.sender_id == (await client.get_me()).id:
        return

    user_id = event.sender_id
    current_time = asyncio.get_event_loop().time()

    # --- Spam Control Logic ---
    if user_id in user_cooldown and current_time - user_cooldown[user_id] < 3:
        try:
            await event.delete()
        except Exception:
            pass
        return
    
    user_cooldown[user_id] = current_time

    # --- Identity Hiding Logic ---
    if event.text:
        msg_text = event.text
        try:
            # 1. Purana message delete karo
            await event.delete()
            # 2. Anonymous naam se naya message bhejo
            await client.send_message(event.chat_id, f"👤 **Anonymous:**\n\n{msg_text}")
        except Exception as e:
            print(f"Error: {e}")

print("✅ Aapka Anonymous Bot chalu ho gaya hai...")
client.run_until_disconnected()
