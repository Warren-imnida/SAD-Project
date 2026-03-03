from collections import Counter

from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .ml.inference import ai_support_message, predict_emotion
from .models import FavoriteTrack, PromptHistory, TrackPlayEvent, UserProfile
from .serializers import FavoriteTrackSerializer, PromptHistorySerializer, UserProfileSerializer
from .spotify_client import build_auth_url, search_recommendations


@api_view(['GET'])
def health(_: object) -> Response:
    return Response({'status': 'ok'})


@api_view(['GET'])
def spotify_login(_: object) -> Response:
    return Response({'url': build_auth_url()})


@api_view(['POST'])
def demo_register(request) -> Response:
    username = request.data.get('username')
    email = request.data.get('email', '')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'username and password are required'}, status=400)
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    if created:
        user.set_password(password)
        user.save()
        UserProfile.objects.get_or_create(user=user)
    return Response({'user_id': user.id, 'created': created})


@api_view(['POST'])
def mood_prompt(request) -> Response:
    user_id = int(request.data.get('user_id', 1))
    text = request.data.get('text', '')
    selected_artist = request.data.get('selected_artist', '')

    user, _ = User.objects.get_or_create(id=user_id, defaults={'username': f'user{user_id}'})
    UserProfile.objects.get_or_create(user=user)

    mood = predict_emotion(text)
    ai_message = ai_support_message(mood.emotion)

    profile = user.profile
    tracks = search_recommendations(
        emotion=mood.emotion,
        artists=[selected_artist] if selected_artist else profile.preferred_artists,
        limit=12,
    )

    repeated = (
        TrackPlayEvent.objects.filter(user=user, emotion=mood.emotion)
        .values('spotify_track_id')
        .annotate(c=Count('id'))
        .order_by('-c')
        .first()
    )
    if repeated and tracks:
        repeated_id = repeated['spotify_track_id']
        tracks.sort(key=lambda t: t['id'] != repeated_id)

    prompt = PromptHistory.objects.create(
        user=user,
        text=text,
        emotion=mood.emotion,
        ai_message=ai_message,
        recommended_track_ids=[t['id'] for t in tracks],
    )

    return Response({
        'prompt_id': prompt.id,
        'emotion': mood.emotion,
        'confidence': mood.confidence,
        'ai_message': ai_message,
        'tracks': tracks,
    })


@api_view(['POST'])
def add_favorite(request) -> Response:
    serializer = FavoriteTrackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    favorite, _ = FavoriteTrack.objects.get_or_create(
        user_id=serializer.validated_data['user'].id,
        spotify_track_id=serializer.validated_data['spotify_track_id'],
        defaults=serializer.validated_data,
    )
    return Response(FavoriteTrackSerializer(favorite).data)


@api_view(['GET'])
def list_favorites(request, user_id: int) -> Response:
    favs = FavoriteTrack.objects.filter(user_id=user_id).order_by('-created_at')
    return Response(FavoriteTrackSerializer(favs, many=True).data)


@api_view(['GET'])
def list_history(request, user_id: int) -> Response:
    items = PromptHistory.objects.filter(user_id=user_id).order_by('-created_at')
    return Response(PromptHistorySerializer(items, many=True).data)


@api_view(['POST'])
def track_play_event(request) -> Response:
    user_id = int(request.data.get('user_id', 1))
    user, _ = User.objects.get_or_create(id=user_id, defaults={'username': f'user{user_id}'})
    event = TrackPlayEvent.objects.create(
        user=user,
        spotify_track_id=request.data.get('spotify_track_id', ''),
        emotion=request.data.get('emotion', 'Mixed'),
        duration_seconds=int(request.data.get('duration_seconds', 0)),
        repeated=bool(request.data.get('repeated', False)),
    )
    total_duration = sum(TrackPlayEvent.objects.filter(user=user).values_list('duration_seconds', flat=True))
    uplift = total_duration >= 1800
    uplift_message = 'Feel better? Here is one uplifting recommendation.' if uplift else None
    return Response({'event_id': event.id, 'uplift_message': uplift_message})


@api_view(['GET', 'PATCH'])
def profile(request, user_id: int) -> Response:
    user, _ = User.objects.get_or_create(id=user_id, defaults={'username': f'user{user_id}'})
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if request.method == 'PATCH':
        profile.preferred_artists = request.data.get('preferred_artists', profile.preferred_artists)
        profile.dark_mode = request.data.get('dark_mode', profile.dark_mode)
        if 'email' in request.data:
            user.email = request.data['email']
            user.save()
        profile.save()
    return Response(UserProfileSerializer(profile).data)


@api_view(['GET'])
def dashboard(_: object) -> Response:
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_playlists = PromptHistory.objects.filter(created_at__gte=month_start).count()
    mood_counts = Counter(PromptHistory.objects.values_list('emotion', flat=True))
    return Response({
        'active_users_estimate': User.objects.filter(last_login__date=now.date()).count(),
        'total_users': User.objects.count(),
        'monthly_playlists_generated': monthly_playlists,
        'most_common_moods': mood_counts.most_common(5),
        'mood_distribution': mood_counts,
        'accounts': list(User.objects.values('id', 'username', 'email')),
    })
