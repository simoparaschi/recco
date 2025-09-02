from django.shortcuts import render
from django.http import HttpResponse
from myplaylist.services.spotify import test_spotify, get_token


# Create your views here.
def hello(request):
    test = get_token()
    return render(request, "myplaylist/index.html",{
        "test": test
    })
