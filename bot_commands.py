from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendVoteRequest
from telethon.tl.types import MessageMediaPoll

poll_handling_enabled = True
bot_shutdown = False  

async def enable_poll_handling():
    global poll_handling_enabled
    poll_handling_enabled = True
    print("Poll handling enabled.")

async def disable_poll_handling():
    global poll_handling_enabled
    poll_handling_enabled = False
    print("Poll handling disabled.")

async def turn_off(client):
    global bot_shutdown
    print("Bot is shutting down...")
    bot_shutdown = True
    await client.disconnect()

async def info(client, chat_id, commands):
    message = f"Poll handling: {poll_handling_enabled}\n"
    message += "Available commands:\n" + "\n".join(f"/{cmd}" for cmd in commands.keys())
    try:
        await client.send_message(chat_id, message)
    except Exception as e:
        print(f"Failed to send info: {e}")

async def handle_group_messages(event, client):
    
    if not poll_handling_enabled:
        print("Poll handling is disabled.")
        return

    if isinstance(event.message.media, MessageMediaPoll):
        poll = event.message.media.poll
        print(f"Poll received: {poll.question}")
        if poll.answers:
            selected_option = poll.answers[0].option
            try:
                await client(SendVoteRequest(
                    peer=event.chat_id,
                    msg_id=event.message.id,
                    options=[selected_option]
                ))
                print("Vote cast successfully!")
            except Exception as e:
                print(f"Failed to vote: {e}")

def get_commands(client, me_id):
    return {
        "badm_on": lambda: enable_poll_handling(),
        "badm_off": lambda: disable_poll_handling(),
        "turn_off": lambda: turn_off(client),
        "info": lambda: info(client, me_id, get_commands(client, me_id)),
    }

__all__ = [
    "poll_handling_enabled",
    "bot_shutdown",
    "handle_group_messages",
    "get_commands",
]