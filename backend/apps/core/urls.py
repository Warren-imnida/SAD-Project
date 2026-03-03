from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.health),
    path('auth/spotify-login/', views.spotify_login),
    path('auth/register/', views.demo_register),
    path('mood/prompt/', views.mood_prompt),
    path('mood/play-event/', views.track_play_event),
    path('favorites/add/', views.add_favorite),
    path('favorites/<int:user_id>/', views.list_favorites),
    path('history/<int:user_id>/', views.list_history),
    path('profile/<int:user_id>/', views.profile),
    path('admin/dashboard/', views.dashboard),
]
