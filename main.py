from telethon import TelegramClient, events
import os
import re
from dotenv import load_dotenv, dotenv_values
import schedule
import asyncio
import json
from time import sleep


# import voice 
from components.sport import sport_reg as sport
from components.bot_commands import handle_group_messages, get_commands


load_dotenv() 

#TODO make a boolean variable to_register

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')

ME = int(os.environ.get('ME'))
SPORT_ID = int(os.environ.get('IU_SPORT'))
TO_HANDLED_GROUP_ID = int(os.environ.get('TO_HANDLED_GROUP_ID'))

client = TelegramClient(
    'session.exp0.v1',
    API_ID,
    API_HASH,
    # device_model="iPhone 5s", 
    system_version="4.16.30-vxExpZero",)

commands = get_commands(client, ME)

ids = {
    "ME": ME,
    "SPORT": SPORT_ID,
    "TO_HANDLED_GROUP_ID": TO_HANDLED_GROUP_ID
}

def get_ids():
    print(client.get_dialogs())

with open("schedule.json", "r") as file:
    schedule_data = json.load(file)


async def main():
    print("Connecting to Telegram...")
    await client.start()
    print("Connected!")
    schedule_sport()
    
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
    
def schedule_sport():
    schedule.clear()
    for entry in schedule_data["schedule"]:
        day = entry["day"]
        sport_name = entry["sport"]
        time_str = entry["time"].strip() 
        if not re.match(r"^\d{2}:\d{2}(:\d{2})?$", time_str):
            print(f"Invalid time format: {time_str}. Skipping.")
            continue

        schedule.every().day.at(time_str).do(
            lambda d=day, s=sport_name, t=time_str: asyncio.create_task(
                sport.sport_reg(client, SPORT_ID, d, s, t)
            )
        )

async def get_chats():
    chats = await client.get_dialogs()
    for i in range(10):
        print(chats[i].name, chats[i].id)

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
                
                parts = line.split(", ")
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
            schedule_sport()
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
@client.on(events.NewMessage(chats=TO_HANDLED_GROUP_ID))
async def handle_group(event):
    await handle_group_messages(event, client)

with client:
    print("Bot is running...")
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
    