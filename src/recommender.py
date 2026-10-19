from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_MATCH_POINTS = 2.0
MOOD_MATCH_POINTS = 1.0
MAX_ENERGY_SIMILARITY_POINTS = 1.0


def _score_attributes(
    preferred_genre: str,
    preferred_mood: str,
    target_energy: float,
    song_genre: str,
    song_mood: str,
    song_energy: float,
) -> Tuple[float, List[str]]:
    """Apply the shared genre, mood, and energy weighting strategy."""
    score = 0.0
    reasons = []

    if preferred_genre.strip().casefold() == song_genre.strip().casefold():
        score += GENRE_MATCH_POINTS
        reasons.append(f"Genre match (+{GENRE_MATCH_POINTS:.1f})")

    if preferred_mood.strip().casefold() == song_mood.strip().casefold():
        score += MOOD_MATCH_POINTS
        reasons.append(f"Mood match (+{MOOD_MATCH_POINTS:.1f})")

    energy_similarity = max(
        0.0,
        1.0 - abs(float(song_energy) - float(target_energy)),
    )
    energy_points = MAX_ENERGY_SIMILARITY_POINTS * energy_similarity
    score += energy_points
    reasons.append(f"Energy similarity (+{energy_points:.2f})")
    return score, reasons


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked_songs = sorted(
            self.songs,
            key=lambda song: _score_attributes(
                user.favorite_genre,
                user.favorite_mood,
                user.target_energy,
                song.genre,
                song.mood,
                song.energy,
            )[0],
            reverse=True,
        )
        return ranked_songs[:max(0, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = _score_attributes(
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            song.genre,
            song.mood,
            song.energy,
        )
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    return _score_attributes(
        str(user_prefs.get("genre", "")),
        str(user_prefs.get("mood", "")),
        float(user_prefs.get("energy", 0.0)),
        str(song.get("genre", "")),
        str(song.get("mood", "")),
        float(song.get("energy", 0.0)),
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda recommendation: recommendation[1], reverse=True)
    return scored_songs[:max(0, k)]
