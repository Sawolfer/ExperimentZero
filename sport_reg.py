from telethon.tl.types import KeyboardButtonCallback
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

prev_button_data = None

async def sport_reg(client, chat_id, day, sport):
    print("start sport registration")
    last_message = await client.get_messages(chat_id, limit=1)
    last_message = last_message[0]
    message_buttons_rows = last_message.reply_markup.rows
    for row in message_buttons_rows:
        for button in row.buttons:
            # print(f"button: {button.text}")
            if day in button.text:
                print(f"in th: {button.text}")
                result = await client(GetBotCallbackAnswerRequest(
                        peer=chat_id,
                        msg_id=last_message.id,
                        data=button.data
                    ))
                print("Result of callback:", result)
                await session_reg(client, chat_id, sport)
                
async def session_reg(client, chat_id, sport):
    print("start session registration")

    last_message = await client.get_messages(chat_id, limit=1)
    last_message = last_message[0]
    message_buttons_rows = last_message.reply_markup.rows
    for row in message_buttons_rows:
        for button in row.buttons:
            if button.text == sport:
                print(f"in th: {button.text}")
                result = await client(GetBotCallbackAnswerRequest(
                        peer=chat_id,
                        msg_id=last_message.id,
                        data=prev_button_data
                    ))
                print("Result of callback:", result)
            prev_button_data = button.data



