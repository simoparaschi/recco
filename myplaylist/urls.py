from django.urls import path
from . import views


urlpatterns = [
    path("login", views.spotify_login, name="spotify_login"),
    path("callback/", views.spotify_callback, name="spotify_callback"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("playlist/<int:playlist_id>", views.see_playlist, name="playlist")
]
