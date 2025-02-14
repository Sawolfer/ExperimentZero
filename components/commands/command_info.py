import pandas as pd


def schedule():
    schedule_df = pd.read_json("schedule.json")
    if isinstance(schedule_df.iloc[0, 0], dict):
        schedule_df = pd.json_normalize(schedule_df['schedule'])

    # Rename columns to match desired output
    schedule_df.columns = ['Day', 'Sport', 'Time']
    print(schedule_df)
    return f"the schedule is:\n{schedule_df}"


def info(list_of_commands):
    to_return = "Available commands:\n"
    to_return += "\n".join(f"/{cmd}" for cmd in list_of_commands) + "\n\n"
    to_return += schedule()
    return f"{to_return}"