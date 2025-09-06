import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
from urllib.parse import urlencode
import requests
from django.http import JsonResponse



# Get Spotify client id and secret safely
load_dotenv(find_dotenv())

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = "http://127.0.0.1:8000/callback"


# Request Spotify authorization
# Using Authorization Code Flow
# https://developer.spotify.com/documentation/web-api/tutorials/code-flow

# Request User Authorization
def login_spotify():
    scope = "user-read-private user-read-email"
    auth_url = "https://accounts.spotify.com/authorize?"


    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True
    }
    test = f"{auth_url}{urlencode(params)}"
    print("***********************************")
    print(test)
    return f"{auth_url}{urlencode(params)}"



# Request Access Token
def callback(request):
    code = request.GET.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    auth_string = f"{CLIENT_ID }:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes).decode("utf-8"))

    payload = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, headers=headers, data=payload)


    return response.json()

def get_playlist(tokens):
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    expires_in = tokens["expires_in"]

    print(f"ACCE {access_token} -- REF {refresh_token} -- EXP {expires_in}")

    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()
