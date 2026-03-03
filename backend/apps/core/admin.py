from django.contrib import admin

from .models import FavoriteTrack, PromptHistory, TrackPlayEvent, UserProfile

admin.site.register(UserProfile)
admin.site.register(PromptHistory)
admin.site.register(FavoriteTrack)
admin.site.register(TrackPlayEvent)
