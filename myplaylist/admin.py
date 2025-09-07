from django.contrib import admin
from .models import PlaylistSpotify, Track, PlaylistSearched, Recco, ReccoTracks

# Register your models here.
admin.site.register(PlaylistSpotify)
admin.site.register(Track)
admin.site.register(PlaylistSearched)
admin.site.register(Recco)
admin.site.register(ReccoTracks)
