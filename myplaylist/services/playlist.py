from myplaylist.models import PlaylistSpotify, Track


def save_playlist(playlists_data, request):
    playlists = []
    for item in playlists_data["items"]:
        spotify_url = item["external_urls"]["spotify"]
        spotify_id = item["id"]
        playlist = PlaylistSpotify.objects.get_or_create(name=item["name"], spotify_id=spotify_id, spotify_url=spotify_url, user=request.user)
        playlists.append(playlist)
    return playlists


def get_playlist_total_nb(playlists):
    return playlists["total"]

def save_playlist_songs(playlist_data, playlist):
    songs = []
    for song in playlist_data["items"]:
        song_name = song["track"]["name"]
        song_album = song["track"]["album"]["name"]
        song_artist = song["track"]["artists"][0]["name"]
        spotify_id = song["track"]["id"]
        spotify_url = song["track"]["external_urls"]["spotify"]
        track, _ = Track.objects.get_or_create(name = song_name, artist=song_artist, album=song_album, spotify_id=spotify_id, spotify_url=spotify_url)
        playlist.tracks.add(track)
        songs.append(track)
    return songs



def recco():
    pass
