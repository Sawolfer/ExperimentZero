from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendVoteRequest
from telethon.tl.types import MessageMediaPoll
from time import sleep
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv() 

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')


geos_id = int(os.environ.get('GEOS_ID'))
penis_penis_id = int(os.environ.get('PENIS_PENIS_ID'))
badm_id = int(os.environ.get('BADM_ID'))
sglipa_id = int(os.environ.get('SGLIPA_ID'))
strugalnya_id = int(os.environ.get('STRUFALNYA'))


client = TelegramClient(
    'session.exp0.v1',
    API_ID,
    API_HASH,
    # device_model="iPhone 5s", 
    system_version="4.16.30-vxExpZero",)

print(geos_id)
print(penis_penis_id)
print(badm_id)
print(sglipa_id)

async def main():
    print("Connecting to Telegram...")
    await client.start()
    
    print("Connected!")

async def get_dialogs():
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(dialog.name, dialog.id)


# Optional: Do not use, cuz it may cause ban in tg
async def sync(from_id, to_id, start, end):
    print("Fetching messages...")
    messages = await client.get_messages(from_id, limit=end)
    for i, message in enumerate(messages, start=start):
        print(f"Message {i}: {message.text or message}")
        try:
            await client.send_message(to_id, message)
            print("Message forwarded successfully!")
        except Exception as e:
            print(f"Failed to forward message: {e}")
        sleep(0.1)
    print("Messages fetched successfully!")

@client.on(events.NewMessage(chats=badm_id))
async def handle_group_messages(event):
    if isinstance(event.message.media, MessageMediaPoll):
        poll = event.message.media.poll
        print(f"Poll received: {poll.question}")
        print(f'Options: {poll.answers}')
        if poll.answers:
            selected_option = poll.answers[0].option
            print(f"Selected option: {poll.answers[0].text}")
            try:
                print(f"Voting for option: {poll.answers[0].text}")
                await client(SendVoteRequest(
                    peer=badm_id,
                    msg_id=event.message.id,
                    options=[selected_option]
                ))
                print("Vote cast successfully!")
            except Exception as e:
                print(f"Failed to vote: {e}")
            print(f"Voted for option: {poll.answers[0].text}")
    else:
        print(f"New message: {event.message.text or '<Non-text content>'}")

@client.on(events.NewMessage(chats=geos_id))
async def handle_and_resend_messages(event):
    message = event.message
    print(f"Message: {message.text or '<Non-text content>'}")
    try:
        await client.send_message(penis_penis_id, message)
        print("Message forwarded successfully!")
    except Exception as e:
        print(f"Failed to forward message: {e}")

@client.on(events.NewMessage(chats=penis_penis_id))
async def handle_message_sglipa(event):
    message = event.message
    # print("Message from sglipa")
    print(message.from_id)
    if message.from_id.user_id == sglipa_id:
        print("Message from sglipa")
        if message.text:
            message.text= f'[СГЛЫПА] {message.text}'
            print(f"Message: {message.text or '<Non-text content>'}")
        try:
            await client.send_message(geos_id, message)
            print("Message forwarded successfully!")
        except Exception as e:
            print(f"Failed to forward message: {e}")



with client:
    print("Bot is running...")
    client.loop.run_until_complete(main())
    client.run_until_disconnected()