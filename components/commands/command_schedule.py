import json
import pandas as pd

from components import schedule_sport

valid_days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

def change_schedule(client, message):
    rows = [line.split(", ") for line in message.strip().split("\n") if line]

    schedule_df = pd.DataFrame(rows, columns=["Day", "Sport", "Time"])
    print("Processing schedule")
    print(schedule_df)
    schedule_df = schedule_df.to_dict(orient="records")
    schedule_data = []
    for entry in schedule_df:
        if entry["Day"] not in valid_days:
            print(f"Invalid day: {entry['Day']}. Skipping.")
            schedule_df.pop(schedule_df.index(entry))
            continue
        try: 
            schedule_data.append({
                "day": entry["Day"],
                "sport": entry["Sport"],
                "time": entry["Time"]
            })
        except Exception as e:
            print(f"Error: {e}")
    with open("schedule.json", "w") as file:
        json.dump({"schedule": schedule_data}, file, indent=4)
    
    schedule_sport.schedule_sport(client)
    schedule_df = pd.DataFrame(schedule_df, columns=["Day", "Sport", "Time"])
    return f"the new schedule is:\n  {schedule_df}"