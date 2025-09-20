import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
from urllib.parse import urlencode
import requests
import re



# Get Spotify client id and secret safely
load_dotenv(find_dotenv())

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = "http://127.0.0.1:8000/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Request Spotify authorization
# Using Authorization Code Flow
# https://developer.spotify.com/documentation/web-api/tutorials/code-flow


# Raised when an regex input validation error occurs
class CleanError(Exception):
    pass


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
def get_token(request):
    code = request.GET.get("code")

    auth_string = f"{CLIENT_ID }:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes).decode("utf-8"))

    if code:
        payload = {
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }

        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(TOKEN_URL, headers=headers, data=payload)


    return response.json()


def refresh_token(token):
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": token,
        "client_id": CLIENT_ID
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
      },

    response = requests.post(TOKEN_URL, headers=headers, data=payload)

    return response.json()



def get_playlist(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def get_playlist_id(url):
    # Match the regex and extract the playlist ID
    matches = re.search(r'playlist/(\w*).*', url)
    return matches.group(1)  # This will raise an AttributeError if matches is None
