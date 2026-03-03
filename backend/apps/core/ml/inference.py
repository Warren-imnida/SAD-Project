from collections import Counter
from dataclasses import dataclass

from apps.core.emotions import EMOTIONS


@dataclass
class MoodResult:
    emotion: str
    confidence: float


KEYWORDS = {
    'Happy': ['happy', 'joy', 'grateful', 'excited'],
    'Sad': ['sad', 'cry', 'down', 'heartbroken'],
    'Angry': ['angry', 'mad', 'furious', 'annoyed'],
    'Motivational': ['motivate', 'focus', 'grind', 'achieve'],
    'Fear': ['fear', 'anxious', 'scared', 'panic'],
    'Depressing': ['depress', 'hopeless', 'empty', 'numb'],
    'Surprising': ['surprise', 'wow', 'unexpected', 'shocked'],
    'Stressed': ['stress', 'pressure', 'burnout', 'overwhelmed'],
    'Calm': ['calm', 'peaceful', 'relaxed', 'serene'],
    'Lonely': ['lonely', 'alone', 'isolated', 'miss'],
    'Romantic': ['love', 'romantic', 'date', 'crush'],
    'Nostalgic': ['nostalgic', 'memories', 'old days', 'throwback'],
}


def predict_emotion(text: str) -> MoodResult:
    lowered = text.lower()
    counts = Counter()
    for emotion, words in KEYWORDS.items():
        for word in words:
            if word in lowered:
                counts[emotion] += 1

    if not counts:
        return MoodResult(emotion='Mixed', confidence=0.35)

    top = counts.most_common(1)[0]
    confidence = min(0.55 + 0.1 * top[1], 0.95)
    return MoodResult(emotion=top[0], confidence=confidence)


def ai_support_message(emotion: str) -> str:
    message = {
        'Happy': 'I love your positive energy. Here is a playlist to keep your joy alive.',
        'Sad': 'I hear you. Take your time, breathe, and listen to these comforting tracks.',
        'Angry': 'Let us release that tension safely with energetic songs.',
        'Motivational': 'You can do this. Here is a performance-boosting playlist.',
        'Fear': 'You are not alone. Try grounding music to regain a sense of safety.',
        'Depressing': 'Your feelings are valid. Let us start with gentle uplifting songs.',
        'Surprising': 'Unexpected emotions can be intense. Here are balancing tracks.',
        'Stressed': 'Slow down and reset with this stress-relief playlist.',
        'Calm': 'Let us preserve your calm with soothing music.',
        'Lonely': 'I am with you. These songs can make the moment feel less empty.',
        'Romantic': 'Here is a romantic mix that matches your vibe.',
        'Nostalgic': 'Let us revisit beautiful memories with nostalgic songs.',
        'Mixed': 'I sense mixed emotions. Here is a balanced playlist to support you.',
    }
    return message[emotion]
