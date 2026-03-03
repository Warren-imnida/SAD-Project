# EmoTune Setup Guide (Flutter Web + Django)

## 1) Backend setup (Django)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SPOTIFY_CLIENT_ID="1274dd22dc0d4d25a46fe1554fc5b33e"
export SPOTIFY_CLIENT_SECRET="01b3d65862b04203acb19326f052718e"
export SPOTIFY_REDIRECT_URI="http://localhost:3000/callback"
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Optional admin user:
```bash
python manage.py createsuperuser
```

## 2) Frontend setup (Flutter Web)
```bash
cd flutter_application_pagatpat
flutter pub get
flutter run -d chrome --dart-define=API_URL=http://127.0.0.1:8000/api
```

## 3) Main App Features Implemented
- Prompt-to-emotion pipeline + AI supportive response.
- Spotify-based track search recommendation endpoint.
- Artist preference in request/profile.
- Favorites, History, Profile endpoints + UI tabs.
- Adaptive behavior: repeated songs prioritized for repeated emotion.
- Long listening handling API returns **"Feel better?"** uplift message.
- Light/Night mode toggle.
- 5 app menus: Home, Favorite, Recommendation, History, Profile.

## 4) Admin Web Features
Open `http://127.0.0.1:8000/admin/` and use dashboard API:
- `GET /api/admin/dashboard/` for:
  - active users estimate
  - total users
  - monthly playlists generated
  - most common moods
  - mood distribution
  - account list

## 5) Notes on Spotify Login & In-App Playback
- Endpoint `GET /api/auth/spotify-login/` returns OAuth URL.
- Playback in-app is implemented via `audioplayers` using Spotify `preview_url` when available.
- Full account playback control requires Spotify Premium + Web Playback SDK token exchange flow.
