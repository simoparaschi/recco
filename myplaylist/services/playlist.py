from myplaylist.models import PlaylistSpotify


def sync_playlist(playlists, request):
    list_playlist = []
    count = 0
    for item in playlists["items"]:
        list_playlist.append(item["name"])
        spotify_url = item["external_urls"]["spotify"]
        spotify_id = item["id"]
        count += 1
        PlaylistSpotify.objects.get_or_create(name=item["name"], spotify_id=spotify_id, spotify_url=spotify_url, user=request.user)

    return list_playlist, count
