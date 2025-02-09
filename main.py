import os
from dotenv import load_dotenv
from layout import start_layout
import tg_client
import asyncio

load_dotenv()

async def tg_client_initialize():
    print("Initializing Telegram client...")
    await tg_client.initialize()

async def start_layout_initialize():
    print("Starting layout...")
    await start_layout()

async def main():
    print("Start")
    try :
        API_ID = os.environ.get('API_ID')
        API_HASH = os.environ.get('API_HASH')
    except Exception as e:
        print(f"error {e}")
    if API_ID is None:
        api_id = int(input("print ur api id: " ))
        with open(".env", "a") as env_file:
            env_file.write(f"API_ID='{api_id}'\n")
    if API_HASH is None:
        api_hash = input("print ur api hash: ")
        with open(".env", "a") as env_file:
            env_file.write(f"API_HASH='{api_hash}'\n")
    
    await tg_client.initialize()
    # tg_client_task = asyncio.create_task(tg_client_initialize())
    # start_layout_task = asyncio.create_task(start_layout_initialize())
    
    # await asyncio.gather(tg_client_task, start_layout_task)
    # start_layout()
    # print("Bot is running...")


if __name__ == "__main__":
    asyncio.run(main())