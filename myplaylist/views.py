from django.shortcuts import render, redirect
from myplaylist.services.spotify import login_spotify, get_token, get_playlist, refresh_token, get_playlist_id
from datetime import datetime
from .models import PlaylistSpotify

# Create your views here.
def spotify_login(request):
    spotify_url = login_spotify()

    return render(request, "myplaylist/index.html",{
        "spotify_url": spotify_url
    })


def spotify_callback(request):
    tokens = get_token(request)

    # Save access tokens in session
    request.session["access_token"] = tokens["access_token"]
    request.session["refresh_token"] = tokens["refresh_token"]
    request.session["expires_in"] = datetime.now().timestamp() + tokens["expires_in"]


    return redirect("dashboard")


def dashboard(request):
    access_token = request.session.get("access_token")
    refresh_token = request.session.get("refresh_token")
    expires_in = request.session.get("expires_in")


    if not access_token:
        return redirect("")

    # Check if the token has expired
    if datetime.now().timestamp() > expires_in:
        new_tokens = refresh_token(refresh_token)

        request.session["access_token"] = new_tokens["access_token"]
        request.session["expires_in"] = datetime.now().timestamp() + new_tokens["expires_in"]


    # Get user's playlists
    playlists = get_playlist(access_token)

    # Display user's playlists
    list_playlist = []
    for item in playlists["items"]:
        list_playlist.append(item["name"])
        spotify_url = item["external_urls"]["spotify"]
        spotify_id = get_playlist_id(spotify_url)
        PlaylistSpotify.objects.get_or_create(name=item["name"], spotify_id=spotify_id, spotify_url=spotify_url, user=request.user)




    return render(request, "myplaylist/dashboard.html",{
        "list_playlist": list_playlist
    })
