from myplaylist.models import PlaylistSpotify, Track


def save_playlist(playlists, request):
    for item in playlists["items"]:
        spotify_url = item["external_urls"]["spotify"]
        spotify_id = item["id"]
        PlaylistSpotify.objects.get_or_create(name=item["name"], spotify_id=spotify_id, spotify_url=spotify_url, user=request.user)


def get_playlist_total_nb(playlists, request):
    return playlists["total"]

def save_playlist_songs(playlist, request):
    for song in playlist["items"]:
        song_name = song["track"]["name"]
        song_album = song["track"]["album"]["name"]
        song_artist = song["track"]["artists"][0]["name"]
        spotify_id = song["track"]["id"]
        spotify_url = song["track"]["external_urls"]["spotify"]
        Track.objects.get_or_create(name = song_name, artist=song_artist, album=song_album, spotify_id=spotify_id, spotify_url=spotify_url)



def recco():
    pass
