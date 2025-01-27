from telethon import TelegramClient, events
import os
import re
from dotenv import load_dotenv, dotenv_values
from bot_commands import handle_group_messages, get_commands
import schedule
import asyncio
import json


import voice 
import sport_reg as sport

load_dotenv() 

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')

ME = int(os.environ.get('ME'))
GEOS_ID = int(os.environ.get('GEOS_ID'))
PENIS_PENIS_ID = int(os.environ.get('PENIS_PENIS_ID'))
BADM_ID = int(os.environ.get('BADM_ID'))
SGLIPA_ID = int(os.environ.get('SGLIPA_ID'))
STRUGALNYA_ID = int(os.environ.get('STRUGALNYA'))
SPORT_ID = int(os.environ.get('IU_SPORT'))

client = TelegramClient(
    'session.exp0.v1',
    API_ID,
    API_HASH,
    # device_model="iPhone 5s", 
    system_version="4.16.30-vxExpZero",)

commands = get_commands(client, ME)

ids = {
    "ME": ME,
    "GEOS": GEOS_ID,
    "PENIS_PENIS": PENIS_PENIS_ID,
    "BADM": BADM_ID,
    "SGLIPA": SGLIPA_ID,
    "STRUGALNYA": STRUGALNYA_ID,
    "SPORT": SPORT_ID
}

def get_id(name):
    return ids[name]

with open("schedule.json", "r") as file:
    schedule_data = json.load(file)

print(schedule_data)

async def main():
    print("Connecting to Telegram...")
    await client.start()
    print("Connected!")
    
    for entry in schedule_data["schedule"]:
        day = entry["day"]
        sport = entry["sport"]
        time_str = entry["time"].strip() 

        if not re.match(r"^\d{2}:\d{2}(:\d{2})?$", time_str):
            print(f"Invalid time format: {time_str}. Skipping.")
            continue

        schedule.every().day.at(time_str).do(
            lambda d=day, s=sport, t=time_str: asyncio.create_task(
                sport.sport_reg(client, SPORT_ID, d, s, t)
            )
        )


    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
    

async def get_chats():
    chats = await client.get_dialogs()
    for i in range(10):
        print(chats[i].name, chats[i].id)

# Optional: Do not use, cuz it may cause ban in tg

# async def sync(from_id, to_id, start, end):
#     print("Fetching messages...")
#     messages = await client.get_messages(from_id, limit=end)
#     for i, message in enumerate(messages, start=start):
#         print(f"Message {i}: {message.text or message}")
#         try:
#             await client.send_message(to_id, message)
#             print("Message forwarded successfully!")
#         except Exception as e:
#             print(f"Failed to forward message: {e}")
#         sleep(0.1)
#     print("Messages fetched successfully!")

# Geos chat
@client.on(events.NewMessage(chats=GEOS_ID))
async def handle_and_resend_messages(event):
    message = event.message
    # print(f"in chat of geos: {message.reply_to.reply_to_msg_id}")
    print(f"Message: {message.text or '<Non-text content>'}")
    # print(message)
    try:
        if message.reply_to_msg_id:
            original_reply_message = await event.get_reply_message()
            if "ева" == message.text or "Ева" in message.text or "ребро адама" in message.text:
                working_text = original_reply_message.text
                if "[СГЛЫПА]" in original_reply_message.text:
                    working_text = working_text.replace("[СГЛЫПА]", "")
                l = bool(re.search(r'[a-zA-Z]', original_reply_message.text))  
                if l:
                    status = voice.generate_audio(working_text, "en")
                else:
                    status = voice.generate_audio(working_text, "ru")
                
                # if "Error" in status:
                #     await client.send_message(
                #         GEOS_ID, 
                #         status,  
                #         reply_to=original_reply_message.id
                #     )
                #     return
                voice_msg = './output.ogg'
                
                await client.send_file(
                    GEOS_ID,
                    file=voice_msg,
                    voice_note=True,
                    reply_to=original_reply_message.id
                )
                return
            if "[СГЛЫПА]" in original_reply_message.text:
                await client.send_message(
                PENIS_PENIS_ID, 
                message,  
                reply_to=original_reply_message.id - 1
                )
            else:
                await client.send_message(
                    PENIS_PENIS_ID, 
                    message,  
                    reply_to=original_reply_message.id + 1
                )
            print("Message forwarded as a reply successfully!")
        else:
            await client.send_message(PENIS_PENIS_ID, message)
            print("Message forwarded successfully!")
    except Exception as e:
        print(f"Failed to forward message: {e}")

# handle messages from sglipa and resend to PM geos
@client.on(events.NewMessage(chats=PENIS_PENIS_ID))
async def handle_message_sglipa(event):
    message = event.message
    # print(f"in chat of penis penis: {message.reply_to.reply_to_msg_id}")
    # print("Message from sglipa")
    if message.from_id.user_id == SGLIPA_ID:
        
        if message.text:
            message.text = f"[СГЛЫПА] {message.text}"
        try:
            if event.message.media:
                await client.forward_messages(GEOS_ID, event.message)
            elif message.reply_to_msg_id:
                original_reply_message = await event.get_reply_message()
                await client.send_message(
                    GEOS_ID, 
                    message,  
                    reply_to=original_reply_message.id - 1
                )
                print("Message forwarded as a reply successfully!")
            else:
                await client.send_message(GEOS_ID, message)
                print("Message forwarded successfully!")
        except Exception as e:
            print(f"Failed to forward message: {e}")

# Handle commands from me
@client.on(events.NewMessage(chats=ME))
async def handle_command(event):
    message = event.message.text.strip()
    if message.startswith("/"):
        command = message[1:]
        print(f"Command received: {command}")
        if "schedule" in command:
            schedule_data = []  
            lines = command.split("\n") 

            for line in lines:
                if not line.strip():
                    continue

                parts = line.split(" ")
                if len(parts) != 3:
                    print(f"Invalid format in line: {line}")
                    continue

                day, sport, time = parts
                schedule_data.append({
                    "day": day,
                    "sport": sport,
                    "time": time
                })

            with open("schedule.json", "w") as file:
                json.dump({"schedule": schedule_data}, file, indent=4) 

            print("Schedule updated.")
            return
        if command in commands:
            try:
                await commands[command]()
            except Exception as e:
                print(f"Error executing command '{command}': {e}")
        else:
            print(f"Unknown command: {command}")

# Handle polls from badminton group
@client.on(events.NewMessage(chats=BADM_ID))
async def handle_group(event):
    await handle_group_messages(event, client)

with client:
    print("Bot is running...")
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
    