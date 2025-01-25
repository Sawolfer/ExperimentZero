import requests as req


URL = "https://coqui-xtts.hf.space/api/predict"

def get_data(url):
    response = req.get(url)
    return response.json()


def post_data(url, data):
    response = req.post(url, json=data)
    return response.json()

data ={
    "data": [
        "hello",
        "ru",
        {
            "is_file": True,
            "name": "female.wav",
            "orig_name": "female.wav"
        },
        None,
        False,
        False,
        False,
        True,
    ],
    "fn_index": 1
}

files = {
    "file": open("female.wav", "rb")  
}

response = req.post(URL)
print(response.status_code)
# Check the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")