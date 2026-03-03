from django.contrib.auth.models import User
from django.db import models

from .emotions import EMOTIONS


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    spotify_user_id = models.CharField(max_length=128, blank=True)
    preferred_artists = models.JSONField(default=list, blank=True)
    dark_mode = models.BooleanField(default=True)


class PromptHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompts')
    text = models.TextField()
    emotion = models.CharField(max_length=32, choices=[(e, e) for e in EMOTIONS])
    ai_message = models.TextField()
    recommended_track_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


class FavoriteTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    spotify_track_id = models.CharField(max_length=128)
    track_name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image_url = models.URLField(blank=True)
    preview_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'spotify_track_id')


class TrackPlayEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plays')
    spotify_track_id = models.CharField(max_length=128)
    emotion = models.CharField(max_length=32, choices=[(e, e) for e in EMOTIONS])
    duration_seconds = models.PositiveIntegerField(default=0)
    repeated = models.BooleanField(default=False)
    played_at = models.DateTimeField(auto_now_add=True)
