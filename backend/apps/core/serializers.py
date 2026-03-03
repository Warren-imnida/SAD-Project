from django.contrib.auth.models import User
from rest_framework import serializers

from .models import FavoriteTrack, PromptHistory, TrackPlayEvent, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'spotify_user_id', 'preferred_artists', 'dark_mode']


class PromptHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptHistory
        fields = '__all__'


class FavoriteTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTrack
        fields = '__all__'


class TrackPlayEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPlayEvent
        fields = '__all__'
