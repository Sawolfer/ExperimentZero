from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
import schedule
import asyncio
import argparse

from components import schedule_sport
from components.commands import manager


load_dotenv()

USER = None

async def telegram_main():
    
    print("Connecting to Telegram...")
    await client.start()
    print("Connected!")
    
    SPORT_ID = 6343627526
    await find_my()

    schedule_sport.schedule_sport(client)
    
    client.add_event_handler(handle_message, events.NewMessage(from_users=USER))

    
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

async def find_my():
    global USER 
    user = await client.get_me()
    print(f"User ID: {user.id}")
    USER = user.id

# initialize()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--func", type=str, help="Function to run (e.g., func1, func2)")
    args = parser.parse_args()
    
    if args.func == "initialize":
        initialize()
    else:
        print(f"Unknown function: {args.func}")

async def handle_message(event):
    print(f"Received message: {event.message.text}")
    commands = manager.get_list_of_commands()
    
    if event.message.text.startswith("/") and event.message.text.split("\n")[0][1:] in commands:
        await manager.manager(client, USER, event.message.text)