from django.urls import path
from . import views
from myplaylist.services.spotify import callback


urlpatterns = [
    path("", views.spotify_login, name="spotify_login"),
    path("callback/", views.spotify_callback, name="spotify_callback"),
]
