from django.shortcuts import render
from django.http import HttpResponse
from myplaylist.services.spotify import login_spotify, callback, get_playlist


# Create your views here.
def spotify_login(request):
    spotify_url = login_spotify()

    return render(request, "myplaylist/index.html",{
        "spotify_url": spotify_url
    })

def spotify_callback(request):
    response = callback(request)
    playlists = get_playlist(response)


    list_playlist = []

    for item in playlists["items"]:
        print(item["name"])
        list_playlist.append(item["name"])



    return render(request, "myplaylist/dashboard.html",{
        "response": response,
        "list_playlist": list_playlist
    })
