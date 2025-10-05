import os
from dotenv import load_dotenv, find_dotenv
import base64
import requests
from urllib.parse import urlencode
import requests
import json




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
# Credits to Imdad Codes for the tutorial
# https://youtu.be/olY_2MW4Eik?feature=shared

class SpotifyAPIError(Exception):
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
        "show_dialog": True # DELETE - Only here for testing purposes so we force login each time
    }

    return f"{auth_url}{urlencode(params)}"



# Request Access Token
def get_token_spotify(request):
    code = request.GET.get("code")
    error = request.GET.get("error")
    # Check whether user gives access or cancels process
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
        data = make_api_call("POST", TOKEN_URL, headers=headers, data=payload)

    elif error:
        data = {
            "error": error
        }

    return data


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
    data = make_api_call("POST", TOKEN_URL, headers=headers, data=payload)
    return data


# https://developer.spotify.com/documentation/web-api/reference/get-list-users-playlists
def get_playlist_spotify(token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = make_api_call("GET", url, headers=headers)
    return data


def get_playlist_items_spotify(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = make_api_call("GET", url, headers=headers)

    return data


def make_api_call(method, url, headers=None, data=None):
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, data=data)

        elif method == "GET":
            response = requests.get(url, headers=headers, data=data)
        response.raise_for_status() # to raise HTTPErrors
    except requests.ConnectionError:
        raise SpotifyAPIError("Network error - Unable to connect to the API.")
    except requests.Timeout:
        raise SpotifyAPIError("Request timed out - Please try again later.")
    except requests.HTTPError as http_err:
        raise SpotifyAPIError(f"HTTP error occurred - {http_err}")

    try:
        data = response.json()
    except (AttributeError, json.JSONDecodeError):
        raise SpotifyAPIError("Failed to parse response as JSON")
    return data
