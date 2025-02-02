from telethon import TelegramClient, events
import os
import re
from dotenv import load_dotenv, dotenv_values
import threading
import schedule
import asyncio
import json
from time import sleep


# import voice 
from layout import start_layout
import schedule_sport
from components.sport import sport_reg as sport
from components.bot_commands import get_commands


load_dotenv() 

#TODO make a boolean variable to_register

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')

ME = int(os.environ.get('ME'))
SPORT_ID = int(os.environ.get('IU_SPORT'))
# TO_HANDLED_GROUP_ID = int(os.environ.get('TO_HANDLED_GROUP_ID'))

client = TelegramClient(
    'session.exp0.v1',
    int(API_ID),
    API_HASH,
    # device_model="iPhone 5s", 
    system_version="4.16.30-vxExpZero",)


async def get_ids():
    if os.environ.get('IU_SPORT'):
        return
    dialogs = await client.get_dialogs()
    important_chats = []
    for dialog in dialogs:
        if dialog.name == "IU Sport":
            print(dialog.id)
            with open(".env", "a") as file:
                file.write(f"IU_SPORT={dialog.id}\n")
            os.environ["IU_SPORT"] = str(dialog.id)
            important_chats.append(dialog.id)
            break

async def telegram_main():
    print("Connecting to Telegram...")
    await client.start()
    print("Connected!")
    
    await get_ids()
    
    # ME = int(os.environ.get('ME'))
    SPORT_ID = int(os.environ.get('IU_SPORT'))
    
    # await sport.sport_reg(client, SPORT_ID, "Monday", "Boxing", "19:30")
    schedule_sport.schedule_sport(client=client, SPORT_ID=SPORT_ID)
    
    while True:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, schedule.run_pending)
        await asyncio.sleep(1)

def load_layout():
    # loop = asyncio.get_running_loop()
    # await loop.run_in_executor(None, start_layout)
    start_layout(client, SPORT_ID)

async def main():
    # task_telegram = asyncio.create_task((telegram_main()))
    # task_gradio = asyncio.create_task(load_layout())
    gradio_thread = threading.Thread(target=load_layout, daemon=True)
    gradio_thread.start()
    
    # await asyncio.gather(task_telegram, task_gradio)
    await telegram_main()

commands = get_commands(client, ME)

async def get_chats():
    chats = await client.get_dialogs()
    for i in range(10):
        print(chats[i].name, chats[i].id)

# # Handle commands from me
# @client.on(events.NewMessage(chats=ME))
# async def handle_command(event):
#     message = event.message.text.strip()
#     if message.startswith("/"):
#         command = message[1:]
#         print(f"Command received: {command}")
#         if "schedule" in command:
#             schedule_data = []  
#             lines = command.split("\n") 

#             for line in lines:
#                 if not line.strip():
#                     continue
                
#                 parts = line.split(", ")
#                 if len(parts) != 3:
#                     print(f"Invalid format in line: {line}")
#                     continue

#                 day, sport, time = parts
#                 schedule_data.append({
#                     "day": day,
#                     "sport": sport,
#                     "time": time
#                 })

#             with open("schedule.json", "w") as file:
#                 json.dump({"schedule": schedule_data}, file, indent=4) 
#             schedule_sport()
#             print("Schedule updated.")
            
#             return
#         if command in commands:
#             try:
#                 await commands[command]()
#             except Exception as e:
#                 print(f"Error executing command '{command}': {e}")
#         else:
#             print(f"Unknown command: {command}")

# Handle polls from badminton group
# @client.on(events.NewMessage(chats=TO_HANDLED_GROUP_ID))
# async def handle_group(event):
#     await handle_group_messages(event, client)

with client:
    print("Bot is running...")
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
    