from telethon.tl.types import KeyboardButtonCallback
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from time import sleep

from tg_client import get_client

prev_button = None

async def sport_reg(chat_id, day, sport, time):
    client = get_client()
    print("start sport registration")
    last_message = await client.get_messages(chat_id, limit=1)
    last_message = last_message[0]
    message_buttons_rows = last_message.reply_markup.rows.copy()
    message_buttons_rows = message_buttons_rows[:-1]
    for row in message_buttons_rows:
        for button in row.buttons:
            if "All classes" in button.text:
                result = await client(GetBotCallbackAnswerRequest(
                        peer=chat_id,
                        msg_id=last_message.id,
                        data=button.data
                    ))
                print("Result of callback:", result)
                break
    await day_chooser(client, chat_id, day, sport, time)

async def day_chooser(client, chat_id, day, sport, time):
    # sleep(0.1)
    print("start day choosing")
    last_message = await client.get_messages(chat_id, limit=1)
    last_message = last_message[0]
    message_buttons_rows = last_message.reply_markup.rows.copy()
    message_buttons_rows = message_buttons_rows[:-1]
    for row in message_buttons_rows:
        for button in row.buttons:
            # print(f"button: {button.text}")
            if day in button.text:
                print(f"the day: {button.text}, is selected")
                result = await client(GetBotCallbackAnswerRequest(
                        peer=chat_id,
                        msg_id=last_message.id,
                        data=button.data
                    ))
                print("Result of callback:", result)
                await session_reg(client, chat_id, sport, time)
                
async def session_reg(client, chat_id, sport, time):
    # sleep(0.1)
    print("start session registration")
    last_message = await client.get_messages(chat_id, limit=1)
    last_message = last_message[0]
    message_buttons_rows = last_message.reply_markup.rows
    for row in message_buttons_rows:
        for button in row.buttons:
            # print(f"for {sport} and button {button.text}: {button.text==sport}")
            if button.text == sport and time in prev_button.text:
                print(f"sesion: {button.text}, time: {time}")
                try: 
                    result = await client(GetBotCallbackAnswerRequest(
                            peer=chat_id,
                            msg_id=last_message.id,
                            data=prev_button.data
                        ))
                    print("Result of callback:", result)
                except Exception as e:
                    print(f"Error: {e}")
            prev_button = button
    if row == message_buttons_rows[-1]:
        print("end of session registration")
        return

