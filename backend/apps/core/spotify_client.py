import os
from typing import Any

import requests
from django.conf import settings

EMOTION_GENRE_HINTS = {
    'Happy': ['pop', 'dance'],
    'Sad': ['acoustic', 'piano'],
    'Angry': ['rock', 'metal'],
    'Motivational': ['work-out', 'hip-hop'],
    'Fear': ['ambient', 'chill'],
    'Depressing': ['sad', 'indie'],
    'Surprising': ['alternative', 'electronic'],
    'Stressed': ['chill', 'sleep'],
    'Calm': ['ambient', 'study'],
    'Lonely': ['singer-songwriter', 'indie'],
    'Romantic': ['r-n-b', 'romance'],
    'Nostalgic': ['classics', 'oldies'],
    'Mixed': ['pop', 'indie'],
}


def get_client_token() -> str:
    cid = settings.SPOTIFY_CLIENT_ID
    csecret = settings.SPOTIFY_CLIENT_SECRET
    if not cid or not csecret:
        return ''
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        auth=(cid, csecret),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()['access_token']


def search_recommendations(emotion: str, artists: list[str] | None = None, limit: int = 10) -> list[dict[str, Any]]:
    token = get_client_token()
    if not token:
        return []

    genres = ','.join(EMOTION_GENRE_HINTS.get(emotion, ['pop'])[:2])
    q_terms = [f'genre:{g}' for g in genres.split(',') if g]
    if artists:
        q_terms.append(f'artist:{artists[0]}')
    query = ' '.join(q_terms)

    response = requests.get(
        'https://api.spotify.com/v1/search',
        headers={'Authorization': f'Bearer {token}'},
        params={'q': query, 'type': 'track', 'limit': limit},
        timeout=10,
    )
    response.raise_for_status()
    tracks = response.json().get('tracks', {}).get('items', [])

    normalized = []
    for track in tracks:
        normalized.append({
            'id': track['id'],
            'name': track['name'],
            'artist': ', '.join(a['name'] for a in track.get('artists', [])),
            'image_url': track.get('album', {}).get('images', [{}])[0].get('url', ''),
            'preview_url': track.get('preview_url') or '',
            'spotify_url': track.get('external_urls', {}).get('spotify', ''),
        })
    return normalized


def build_auth_url() -> str:
    cid = settings.SPOTIFY_CLIENT_ID
    redirect = settings.SPOTIFY_REDIRECT_URI
    scope = 'user-read-email user-read-private streaming user-modify-playback-state user-read-playback-state'
    return (
        'https://accounts.spotify.com/authorize'
        f'?client_id={cid}&response_type=code&redirect_uri={redirect}&scope={scope.replace(" ", "%20")}'
    )
