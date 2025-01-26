import requests as req
import json


# URL = "https://coqui-xtts.hf.space/--replicas/1ycfn/file=/tmp/gradio/1fb634c95ee60911623727afa0a2ee3948de455b/female.wav"

# URL = "https://coqui-xtts.hf.space/api/predict/"
URL = "https://coqui-xtts.hf.space/--replicas/1ycfn/"

session_hash = {
    "fn_index": 1,
    "session_hash": "6q9kceqhz39"
}

response = req.post(URL, json=session_hash)

print(response)

data ={
    "data": [
        "привет как проходит твой день чем занят и что будешь сегодня делать ? ",
        "ru",
        {
            "name": "/tmp/gradio/1fb634c95ee60911623727afa0a2ee3948de455b/female.wav",
            "data": "https://coqui-xtts.hf.space/--replicas/1ycfn/file=/tmp/gradio/1fb634c95ee60911623727afa0a2ee3948de455b/female.wav",
            "is_file": True,
        },
        None,
        False,
        False,
        False,
        True,
    ],
    "fn_index": 1,
    "session_hash": "6q9kceqhz39"
}


response = req.post(URL, json=data)

print(response.status_code)
# Check the response
if response.status_code == 200:
    print("Response:", response.json())
    with open("tmp.json", "w") as f:
        json.dump(response.json(), f)
    # with open("test.wav", "wb") as f:
    #     response = req.get(response.json()["data"][0][0]["data"])
else:
    print(f"Error: {response.status_code} - {response.text}")
