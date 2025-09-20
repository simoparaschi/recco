from myplaylist.models import PlaylistSpotify
import re

class ExtractPlaylistIdError(Exception):
    pass

def get_playlist_id(url):
    # Match the regex and extract the playlist ID
    matches = re.search(r'playlist/(\w+).*', url)
    if not matches:
        raise ExtractPlaylistIdError(f"Invalid playlist ID from: {url}")
    return matches.group(1)  # This will raise an AttributeError if matches is None



def sync_playlist(playlists, request):
    list_playlist = []
    for item in playlists["items"]:
        list_playlist.append(item["name"])
        spotify_url = item["external_urls"]["spotify"]
        spotify_id = get_playlist_id(spotify_url)

        PlaylistSpotify.objects.get_or_create(name=item["name"], spotify_id=spotify_id, spotify_url=spotify_url, user=request.user)
    return list_playlist
