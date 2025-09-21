import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
from urllib.parse import urlencode
import requests




# Get Spotify client id and secret safely
load_dotenv(find_dotenv())

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = "http://127.0.0.1:8000/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"
AUTH_STRING = f"{CLIENT_ID }:{CLIENT_SECRET}"
AUTH_BYTES = AUTH_STRING.encode("utf-8")
AUTH_BASE64 = str(base64.b64encode(AUTH_BYTES).decode("utf-8"))

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

    return f"{auth_url}{urlencode(params)}"



# Request Access Token
def get_token_spotify(request):
    code = request.GET.get("code")
    if code:
        payload = {
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }

        headers = {
            "Authorization": f"Basic {AUTH_BASE64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(TOKEN_URL, headers=headers, data=payload)

    return response.json()


# A refresh token is a security credential that allows client applications to obtain new access tokens
# without requiring users to reauthorize the application

def refresh_token_spotify(token):
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": token,
        "client_id": CLIENT_ID
    }

    headers = {
        "Authorization": f"Basic {AUTH_BASE64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=payload)
    return response.json()



def get_playlist_spotify(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()
