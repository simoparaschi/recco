from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class PlaylistSpotify(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    spotify_url = models.CharField()

    def __str__(self):
        return f"playlist {self.name}"

class Track(models.Model):
    name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    album = models.CharField(max_length=50)
    spotify_url = models.CharField()

    def __str__(self):
        return f"Track {self.name}"

# JOIN table
class PlaylistSearched(models.Model):
    playlist_spotify = models.ForeignKey(PlaylistSpotify, on_delete=models.CASCADE, related_name="playlist_searched")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="track_searched")



class Recco(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    playlist_spotify = models.ForeignKey(PlaylistSpotify, on_delete=models.CASCADE, related_name="playlist_spotify")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recco {self.name}"



# JOIN table
class ReccoTracks(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="track_spotify")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searcher")


# JOIN table
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favouriter")
    recco_tracks = models.ForeignKey(ReccoTracks, on_delete=models.CASCADE, related_name="reccomended_tracks")
