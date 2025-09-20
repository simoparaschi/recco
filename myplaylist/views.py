from django.shortcuts import render, redirect
from myplaylist.services.spotify import login_spotify, get_token, get_playlist, spotify_refresh_token, get_playlist_id
from myplaylist.services.session import save_access_tokens, get_user_tokens, is_expired,update_tokens
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import PlaylistSpotify



# Raised when an regex input validation error occurs
class CleanError(Exception):
    pass


# Create your views here.
def spotify_login(request):
    spotify_url = login_spotify()

    return render(request, "myplaylist/index.html",{
        "spotify_url": spotify_url
    })


def spotify_callback(request):
    tokens = get_token(request)

    # Save access tokens in session
    save_access_tokens(request, tokens)

    return redirect("dashboard")


@login_required
def dashboard(request):
    tokens = get_user_tokens(request)

    if not tokens["access_token"]:
        return redirect("")

    # Check if the token has expired
    if is_expired(request):
        new_tokens = spotify_refresh_token(tokens["refresh_token"])
        update_tokens(request, new_tokens)



    # Get user's playlists
    playlists = get_playlist(tokens["access_token"])

    # Display user's playlists
    list_playlist = []
    for item in playlists["items"]:
        list_playlist.append(item["name"])
        spotify_url = item["external_urls"]["spotify"]
        try:
            spotify_id = get_playlist_id(spotify_url)
        except Exception as e:
            message = "Invalid Spotify URL format. Could not extract track ID." if isinstance(e, AttributeError) else "An error occurred while processing the input:"
            raise CleanError(f"{message}: {e}")

        PlaylistSpotify.objects.get_or_create(name=item["name"], spotify_id=spotify_id, spotify_url=spotify_url, user=request.user)

    return render(request, "myplaylist/dashboard.html",{
        "list_playlist": list_playlist
    })
