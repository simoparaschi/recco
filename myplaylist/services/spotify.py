import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
from urllib.parse import urlencode


# get Spotify client id and secret safely
load_dotenv(find_dotenv())

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']



# Request Spotify authorization
# Using Authorization Code Flow
# https://developer.spotify.com/documentation/web-api/tutorials/code-flow

# Request User Authorization
def login_spotify():
    scope = "user-read-private user-read-email"
    auth_url = "https://accounts.spotify.com/authorize?"
    redirect_uri = "http://127.0.0.1:8000/callback"


    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": redirect_uri,
        "show_dialog": True
    }
    test = f"{auth_url}{urlencode(params)}"
    print("***********************************")
    print(test)
    return f"{auth_url}{urlencode(params)}"



# Request Access Token
def callback():
    pass
    # body {
    #     "code": request.GET.get("code")
    # }


# Old code
def get_token():
    auth_string = f"{CLIENT_ID }:{CLIENT_SECRET}"
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

    # Get the access token specifically
    token = data["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def get_playlist(token):
    url = "https://api.spotify.com/v1/users/"
    headers = get_auth_header(token)
