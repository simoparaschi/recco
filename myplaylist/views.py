from django.shortcuts import render, redirect
from myplaylist.services.spotify import login_spotify, callback, get_playlist
from datetime import datetime



# Create your views here.
def spotify_login(request):
    spotify_url = login_spotify()

    return render(request, "myplaylist/index.html",{
        "spotify_url": spotify_url
    })

def spotify_callback(request):
    tokens = callback(request)

    # Save access tokens in session
    request.session["access_token"] = tokens["access_token"]
    request.session["refresh_token"] = tokens["refresh_token"]
    request.session["expires_in"] = datetime.now().timestamp() + tokens["expires_in"]


    # Get and display list of playlists
    # playlists = get_playlist(tokens)

    # list_playlist = []
    # for item in playlists["items"]:
    #     list_playlist.append(item["name"])

    # ToDo save playlists in db


    return redirect("dashboard")

def dashboard(request):
    access_token = request.session.get("access_token")
    refresh_token = request.session.get("refresh_token")
    expires_in = request.session.get("expires_in")


    if not access_token:
        return redirect("")

    # Check if the token has expired
    if datetime.now().timestamp() > expires_in:
        return redirect("")

    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    playlists = get_playlist(tokens)

    list_playlist = []
    for item in playlists["items"]:
        list_playlist.append(item["name"])


    return render(request, "myplaylist/dashboard.html",{
        "list_playlist": list_playlist
    })
