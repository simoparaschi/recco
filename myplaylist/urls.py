from django.urls import path
from . import views
from myplaylist.services.spotify import get_token


urlpatterns = [
    path("", views.spotify_login, name="spotify_login"),
    path("callback/", views.spotify_callback, name="spotify_callback"),
    path("dashboard/", views.dashboard, name="dashboard")
]
