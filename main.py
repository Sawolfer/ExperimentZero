import os
from dotenv import load_dotenv
from layout import start_layout
import tg_client

load_dotenv()

if __name__ == "__main__":
    print("Start")
    try :
        API_ID = os.environ.get('API_ID')
        API_HASH = os.environ.get('API_HASH')
        print(API_ID, API_HASH)
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
    
    tg_client.initialize()
    
    start_layout()
    print("Bot is running...")
    