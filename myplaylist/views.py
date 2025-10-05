from django.shortcuts import render, redirect
from django.contrib import messages
from myplaylist.services.spotify import login_spotify, get_token_spotify, get_playlist_spotify, refresh_token_spotify, SpotifyAPIError, get_playlist_items_spotify # check all of these, long
from myplaylist.services.session import save_access_tokens, get_user_tokens, check_token_expiration, update_tokens
from myplaylist.services.playlist import save_playlist, get_playlist_total_nb, save_playlist_songs
from django.contrib.auth.decorators import login_required
from myplaylist.models import PlaylistSpotify

LOGIN_SCREEN = "/login"

# Create your views here.
def spotify_login(request):
    spotify_url = login_spotify()

    return render(request, "myplaylist/index.html",{
        "spotify_url": spotify_url
    })


def spotify_callback(request):
    redirect_target = "dashboard"
    try:
        tokens = get_token_spotify(request)

        # Check if user canceled during Auth, if so redirect to login
        if tokens.get("error"):
            messages.error(request, f"Spotify authorization failed - {tokens.get("error")}")
            redirect_target = LOGIN_SCREEN
        else:
            # Save access tokens in session
            save_access_tokens(request, tokens)

    except SpotifyAPIError as e:
        messages.error(request, f"Error: {e}")
        redirect_target = LOGIN_SCREEN

    return redirect(redirect_target)


@login_required
def dashboard(request):
    tokens = get_user_tokens(request)

    # Check if we have expiration token, if not redirect to login
    if not tokens.get("expires_in"):
        return redirect(LOGIN_SCREEN)

    # Check if the token has expired, if so request new one
    if check_token_expiration(request):
        new_tokens = refresh_token_spotify(tokens["refresh_token"])
        update_tokens(request, new_tokens)


    # Get user's playlists
    try:
        playlists_data = get_playlist_spotify(tokens["access_token"])
    except SpotifyAPIError as e:
        messages.error(request, f"Error: {e}")
        return redirect(LOGIN_SCREEN)


    # Get total nb of playlists
    nb_playlists = get_playlist_total_nb(playlists_data)

    # Save playlits in db
    save_playlist(playlists_data, request)


    return render(request, "myplaylist/dashboard.html",{
        "nb_playlists": nb_playlists,
        "playlists": PlaylistSpotify.objects.all()
    })

@login_required
def see_playlist(request, playlist_id):
    tokens = get_user_tokens(request)

    # Check if we have expiration token, if not redirect to login
    if not tokens.get("expires_in"):
        return redirect(LOGIN_SCREEN)

    # Check if the token has expired, if so request new one
    if check_token_expiration(request):
        new_tokens = refresh_token_spotify(tokens["refresh_token"])
        update_tokens(request, new_tokens)


    playlist = PlaylistSpotify.objects.get(id=playlist_id, user=request.user)

    # Get user's songs per playlist
    try:
        playlist_data = get_playlist_items_spotify(tokens["access_token"], playlist.spotify_id)
    except SpotifyAPIError as e:
        messages.error(request, f"Error: {e}")
        return redirect(LOGIN_SCREEN)

    # Save playlit's songs in db
    save_playlist_songs(playlist_data, playlist)

    return render(request, "myplaylist/playlist.html",{
        "playlist": playlist
    })
