from django.shortcuts import render
from django.http import HttpResponse
from myplaylist.services.spotify import get_token, login_spotify


# Create your views here.
def hello(request):
    test = get_token()
    spotify_url = login_spotify()
    return render(request, "myplaylist/index.html",{
        "test": test,
        "spotify_url": spotify_url
    })
