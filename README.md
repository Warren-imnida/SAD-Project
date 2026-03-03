# EmoTune: Sentiment-Driven AI Music Recommender

Capstone scaffold with:
- **Frontend:** Flutter (Dart) runnable on browser
- **Backend:** Python Django + DRF
- **AI:** BERT training pipeline + live fallback emotion inference
- **Music:** Spotify API integration for recommendations

## Quick Start
Follow `docs/setup.md`.

## Project Structure
- `flutter_application_pagatpat/` → Flutter app (Home, Favorite, Recommendation, History, Profile)
- `backend/` → Django API and admin
- `datasets/` → mood prompt training dataset
- `docs/model_training.md` → training process and sample results

## Key Endpoints
- `POST /api/mood/prompt/`
- `POST /api/mood/play-event/`
- `POST /api/favorites/add/`
- `GET /api/favorites/<user_id>/`
- `GET /api/history/<user_id>/`
- `GET/PATCH /api/profile/<user_id>/`
- `GET /api/admin/dashboard/`
