from telethon import TelegramClient
import os
from dotenv import load_dotenv
import schedule
import asyncio
import argparse


from components.sport import sport_reg as sport
from components import schedule_sport


load_dotenv()


async def telegram_main():
    
    print("Connecting to Telegram...")
    await client.start()
    print("Connected!")
    
    SPORT_ID = 6343627526
    
    schedule_sport.schedule_sport()
    
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

client = None

async def initialize():
    global client
    
    API_ID = os.environ.get('API_ID')
    API_HASH = os.environ.get('API_HASH')
    
    client = TelegramClient(
        'session.exp0.v1.light',
        int(API_ID),
        API_HASH,
        # device_model="iPhone 5s", 
        system_version="4.16.30-vxExpZero",
    )
    
    async with client:
        print("Bot is running...")
        # client.loop.run_until_complete(telegram_main())
        await telegram_main()
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