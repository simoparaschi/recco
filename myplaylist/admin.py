from django.contrib import admin
from .models import PlaylistSpotify, Track, Recco, ReccoTracks

# Register your models here.
admin.site.register(PlaylistSpotify)
admin.site.register(Track)
admin.site.register(Recco)
admin.site.register(ReccoTracks)
