import gradio
import pandas as pd
import json
import subprocess
import os
from dotenv import load_dotenv
from time import sleep

import schedule_sport

load_dotenv()

running_process = None

def start_layout():
    demo.launch(
        share=False,
    )

def get_data():
    try:
        api_id = os.environ.get('API_ID')
        api_hash = os.environ.get('API_HASH')
        phone_number = os.environ.get('PHONE_NUMBER')
        password = os.environ.get('PASSWORD')
    except KeyError:
        return "", "", "", ""
    return api_id, api_hash, phone_number, password

def personal_info(api_id, api_hash, phone_number, password):
    with open(".env", "w") as f:
        f.write(f"API_ID='{api_id}'\n")
        f.write(f"API_HASH='{api_hash}'\n")
        f.write(f"PHONE_NUMBER='{phone_number}'\n")
        f.write(f"PASSWORD='{password}'\n")
    
    registration_process(phone_number)
    
    return "Now you will receive a code, enter it please in the next window"

def registration_process (phone_number):
    global running_process
    
    # Start tg_client
    running_process = subprocess.Popen(
        ["python", "tg_client.py", "--func", "initialize"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    prompt_found = False
    while True:
        line = running_process.stdout.readline()
        if not line:  # Process exited
            break
        print("Subprocess Output:", line.strip())  # Optional: log output
        
        # Check for the prompt (case-insensitive)
        if "phone" in line.lower():
            prompt_found = True
            break
    
    if not prompt_found:
        raise RuntimeError("Prompt 'enter your phone' not found!")
    
    # Send the phone number
    print("Sending phone number:", phone_number)
    running_process.stdin.write(f"{phone_number}\n")
    running_process.stdin.flush()
    
    # Send phone number
    # TODO check problem with inserting phone number
    
    print("Exit Code:", running_process.returncode)

def send_ver_code (ver_code):
    global running_process
    
    # Send verification code
    running_process.stdin.write(f"{ver_code}\n")
    running_process.stdin.flush()
    
    # Get password
    password = os.environ.get('PASSWORD')
    print(password)
    
    # Send password
    running_process.stdin.write(f"{password}\n")
    running_process.stdin.flush()
    
    return f"Registration completed"

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
    
    schedule_sport.schedule_sport()
    return f"Processing {len(schedule)} sports entries"

def load_schedule():
    with open("schedule.json", "r") as file:
        schedule_data = json.load(file)
    schedule = [[entry["day"], entry["sport"], entry["time"]] for entry in schedule_data["schedule"]]
    
    return schedule


with gradio.Blocks() as demo:
    gradio.Markdown("# Telegram Bot")
    # with gradio.Tab("Information"):
    #     gradio.Markdown("Enter your personal information")
    #     api_id, api_hash, phone_number, password = get_data()
    #     api_id = gradio.Textbox(label="api_id", value=api_id)
    #     api_hash = gradio.Textbox(label="api_hash", value=api_hash)
    #     phone_number = gradio.Textbox(label="phone_number", value=phone_number)
    #     password = gradio.Textbox(label="password", value=password)
        
    #     submit_button = gradio.Button("Submit")
    #     submit_button.click(fn=personal_info, inputs=[api_id, api_hash, phone_number, password], outputs=[gradio.Markdown()])
        
    #     code_from_tg = gradio.Textbox(label="code")
    #     submit_button_2 = gradio.Button("Submit")
    #     submit_button_2.click(fn=send_ver_code, inputs=[code_from_tg], outputs=[gradio.Markdown()])

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

