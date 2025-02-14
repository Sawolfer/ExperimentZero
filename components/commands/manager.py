
from components.commands import command_schedule, command_info

list_of_commands = ["schedule", "info"]

def get_list_of_commands():
    return list_of_commands

async def manager(client, chat_id, message):
    if "/schedule" in message:
        print("schedule")
        message = message.replace("/schedule", "")
        new_schedule = command_schedule.change_schedule(message)
        await send_message(client, chat_id, new_schedule)
    elif "/info" in message:
        print("info")
        info = command_info.info(list_of_commands)
        await send_message(client, chat_id, info)


async def send_message(client, chat_id, message):
    try: 
        await client.send_message(
            chat_id,
            message
        )
    except Exception as e:
        print(f"Error: {e}")