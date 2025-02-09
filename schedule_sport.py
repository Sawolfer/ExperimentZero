import asyncio
import schedule
import json
import re

from components.sport import sport_reg


with open("schedule.json", "r") as file:
    schedule_data = json.load(file)

def schedule_sport():
    SPORT_ID = int(6343627526)
    schedule.clear()
    for entry in schedule_data["schedule"]:
        day = entry["day"]
        sport_name = entry["sport"]
        time_str = entry["time"].strip() 
        if not sport_name:
            continue
        
        if not re.match(r"^\d{2}:\d{2}(:\d{2})?$", time_str):
            print(f"Invalid time format: {time_str}. Skipping.")
            continue
        
        # schedule.every().day.at(time_str).do(
        #     lambda d=day, s=sport_name, t=time_str: asyncio.create_task(
        #         sport_reg.sport_reg(SPORT_ID, d, s, t)
        #     )
        # )
        valid_days = {
            "monday": schedule.every().monday,
            "tuesday": schedule.every().tuesday,
            "wednesday": schedule.every().wednesday,
            "thursday": schedule.every().thursday,
            "friday": schedule.every().friday,
            "saturday": schedule.every().saturday,
            "sunday": schedule.every().sunday,
        }
        
        valid_days[day.lower()].at(time_str).do(
            lambda d=day, s=sport_name, t=time_str: asyncio.create_task(
                sport_reg.sport_reg(SPORT_ID, d, s, t)
            )
        )
    print(schedule.get_jobs())