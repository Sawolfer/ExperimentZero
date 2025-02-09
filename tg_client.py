from telethon import TelegramClient
import os
from dotenv import load_dotenv
import schedule
import asyncio
import argparse


from components.sport import sport_reg as sport
import schedule_sport


load_dotenv() 

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')
PASSWORD = os.environ.get('PASSWORD')

client = TelegramClient(
    'session.exp0.v1.light',
    int(API_ID),
    API_HASH,
    # device_model="iPhone 5s", 
    system_version="4.16.30-vxExpZero",)

async def telegram_main():
    print("Connecting to Telegram...")
    await client.start()
    print("Connected!")
    
    # await get_ids()
    
    # ME = int(os.environ.get('ME'))
    SPORT_ID = 6444735563
    
    # await sport.sport_reg(client, SPORT_ID, "Monday", "Boxing", "19:30")
    schedule_sport.schedule_sport()
    
    while True:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, schedule.run_pending)
        await asyncio.sleep(1)

async def initialize():
    with client:
        # print("Bot is running...")
        client.loop.run_until_complete(telegram_main())
        client.run_until_disconnected()

def get_client():
    return client

# initialize()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--func", type=str, help="Function to run (e.g., func1, func2)")
    args = parser.parse_args()
    
    if args.func == "initialize":
        initialize()
    else:
        print(f"Unknown function: {args.func}")