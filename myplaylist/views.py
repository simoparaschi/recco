from django.shortcuts import render
from django.http import HttpResponse
from myplaylist.services.spotify import login_spotify, callback


# Create your views here.
def spotify_login(request):
    spotify_url = login_spotify()

    return render(request, "myplaylist/index.html",{
        "spotify_url": spotify_url
    })

def spotify_callback(request):
    response = callback(request)
    print(f"RESPONSE {response}")
    return render(request, "myplaylist/dashboard.html",{
        "response": response
    })
