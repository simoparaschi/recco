from myplaylist.services.spotify import get_playlist_id# Raised when an regex input validation error occurs
from myplaylist.models import PlaylistSpotify

class CleanError(Exception):
    pass

def sync_playlist(playlists, request):
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
    return list_playlist
