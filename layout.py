import gradio
import pandas as pd
import json

import schedule_sport

client = None
SPORT_ID = None

def start_layout(pr_client, pr_SPORT_ID):
    global client, SPORT_ID
    client = pr_client
    SPORT_ID = pr_SPORT_ID

    demo.launch(
        share=False,
    )


def personal_info(api_id, api_hash, phone_number):
    #TODO check that it does not rewrite the file
    with open(".env", "w") as f:
        f.write(f"API_ID='{api_id}'\n")
        f.write(f"API_HASH='{api_hash}'\n")
        f.write(f"PHONE_NUMBER='{phone_number}'\n")
    
    #TODO make the whole register system (with code from telegram)
    
    # return "Now you will receive a code, enter it please in the next window"

def generate_schedule(number_sports):
    try:
        number_sports = int(number_sports)
    except ValueError:
        return gradio.update(value="Invalid input, enter a number"), []
    
    schedule_data = [["", "", ""] for _ in range(number_sports)]
    return "", schedule_data

def save_schedule(schedule):
    schedule_df = pd.DataFrame(schedule, columns=["Day", "Sport", "Time"])
    print("Processing schedule")
    print(schedule_df)
    schedule_df = schedule_df.to_dict(orient="records")
    schedule_data = []
    for entry in schedule_df:
        schedule_data.append({
            "day": entry["Day"],
            "sport": entry["Sport"],
            "time": entry["Time"]
        })
    with open("schedule.json", "w") as file:
        json.dump({"schedule": schedule_data}, file, indent=4)
    print(SPORT_ID)
    schedule_sport.schedule_sport(client=client, SPORT_ID=SPORT_ID)
    return f"Processing {len(schedule)} sports entries"

def load_schedule():
    with open("schedule.json", "r") as file:
        schedule_data = json.load(file)
    schedule = [[entry["day"], entry["sport"], entry["time"]] for entry in schedule_data["schedule"]]
    
    return schedule


with gradio.Blocks() as demo:
    gradio.Markdown("# Telegram Bot")
    with gradio.Tab("Information"):
        api_id = gradio.Textbox(label="api_id")
        api_hash = gradio.Textbox(label="api_hash")
        phone_number = gradio.Textbox(label="phone_number")
        
        submit_button = gradio.Button("Submit")
        submit_button.click(fn=personal_info, inputs=[api_id, api_hash, phone_number])
        
        # code_from_tg = gradio.Textbox(label="code")
        # submit_button_2 = gradio.Button("Submit")

    with gradio.Tab("Schedule"):
        # descr_number = gradio.Markdown("Enter the number of sports you want to schedule")
        # number_sports = gradio.Textbox(label="Number of Sports")
        # submit_button_3 = gradio.Button("Generate Schedule")
        
        desc_schedule = gradio.Markdown("Enter the schedule below (in time write the start time of the sport)")
        
        schedule = gradio.Dataframe(
            headers=["Day", "Sport", "Time"],
            datatype=["str", "str", "str"],
            value=load_schedule(),
            col_count=(3, "fixed"),
        )
        
        schedule_state = gradio.State([])

        # submit_button_3.click(fn=generate_schedule, inputs=[number_sports], outputs=[number_sports, schedule])

        submit_button_4 = gradio.Button("Submit Schedule")
        submit_button_4.click(fn=save_schedule, inputs=[schedule], outputs=[gradio.Textbox(label="Schedule Output")])

