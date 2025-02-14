import os
from dotenv import load_dotenv
from components.layout import start_layout
from components import tg_client
import asyncio

from components import schedule_sport

load_dotenv()

async def tg_client_initialize():
    print("Initializing Telegram client...")
    await tg_client.initialize()

def get_loop():
    return asyncio.get_running_loop()

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
    # TODO make initialization tg_client from layout
    # start_layout()
    # tg_client_task = asyncio.create_task(tg_client_initialize())
    # layout_task = asyncio.create_task(start_layout_initialize())
    
    # await asyncio.gather(tg_client_task, layout_task) 


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())