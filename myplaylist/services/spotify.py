import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
import json

# get Spotify client id and secret safely
load_dotenv(find_dotenv())

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def test_spotify():
    return f"{client_id } - {client_secret }"

def get_token():
    auth_string = f"{client_id }:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes).decode("utf-8"))

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    print(data)
    return data
