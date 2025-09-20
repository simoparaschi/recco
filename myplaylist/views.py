from django.shortcuts import render, redirect
from myplaylist.services.spotify import login_spotify, get_token_spotify, get_playlist_spotify, refresh_token_spotify # check all of these, long
from myplaylist.services.session import save_access_tokens, get_user_tokens, check_token_expiration, update_tokens
from myplaylist.services.playlist import sync_playlist, ExtractPlaylistIdError
from django.contrib.auth.decorators import login_required



# Create your views here.
def spotify_login(request):
    spotify_url = login_spotify()

    return render(request, "myplaylist/index.html",{
        "spotify_url": spotify_url
    })


def spotify_callback(request):
    tokens = get_token_spotify(request)

    # Save access tokens in session
    save_access_tokens(request, tokens)

    return redirect("dashboard")


@login_required
def dashboard(request):
    tokens = get_user_tokens(request)

    if not tokens["access_token"]:
        return redirect("")

    # Check if the token has expired
    if check_token_expiration(request):
        new_tokens = refresh_token_spotify(tokens["refresh_token"])
        update_tokens(request, new_tokens)


    # Get user's playlists
    playlists = get_playlist_spotify(tokens["access_token"])


    # Display user's playlists
    try:
        list_playlist = sync_playlist(playlists, request)
     except ExtractPlaylistIdError as e:
        print("Could not extract playlist. {e}")


    return render(request, "myplaylist/dashboard.html",{
        "list_playlist": list_playlist
    })
