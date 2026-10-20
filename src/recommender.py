import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_MATCH_POINTS = 1.0
MOOD_MATCH_POINTS = 1.0
MAX_ENERGY_SIMILARITY_POINTS = 2.0
MAX_TEMPO_SIMILARITY_POINTS = 1.0
TEMPO_SIMILARITY_RANGE_BPM = 100.0


def _score_attributes(
    preferred_genre: str,
    preferred_mood: str,
    target_energy: float,
    song_genre: str,
    song_mood: str,
    song_energy: float,
    target_tempo_bpm: Optional[float] = None,
    song_tempo_bpm: Optional[float] = None,
) -> Tuple[float, List[str]]:
    """Score genre, mood, energy, and optional tempo matches."""
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

    if target_tempo_bpm is not None and song_tempo_bpm is not None:
        tempo_similarity = max(
            0.0,
            1.0 - abs(float(song_tempo_bpm) - float(target_tempo_bpm))
            / TEMPO_SIMILARITY_RANGE_BPM,
        )
        tempo_points = MAX_TEMPO_SIMILARITY_POINTS * tempo_similarity
        score += tempo_points
        reasons.append(f"Tempo similarity (+{tempo_points:.2f})")

    return score, reasons


@dataclass
class Song:
    """Represent a song and its attributes."""
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
    """Represent a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo_bpm: Optional[float] = None

class Recommender:
    """Provide an object-oriented interface for song recommendations."""
    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a song collection."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs ranked for the user's preferences."""
        ranked_songs = sorted(
            self.songs,
            key=lambda song: _score_attributes(
                user.favorite_genre,
                user.favorite_mood,
                user.target_energy,
                song.genre,
                song.mood,
                song.energy,
                user.target_tempo_bpm,
                song.tempo_bpm,
            )[0],
            reverse=True,
        )
        return ranked_songs[:max(0, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song matches the user's preferences."""
        _, reasons = _score_attributes(
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            song.genre,
            song.mood,
            song.energy,
            user.target_tempo_bpm,
            song.tempo_bpm,
        )
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load and convert song data from a CSV file."""
    integer_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    with open(csv_path, mode="r", newline="", encoding="utf-8") as csv_file:
        songs = []
        for row in csv.DictReader(csv_file):
            for field in integer_fields:
                if row.get(field) not in (None, ""):
                    row[field] = int(row[field])
            for field in float_fields:
                if row.get(field) not in (None, ""):
                    row[field] = float(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against the user's preferences and return reasons."""
    return _score_attributes(
        str(user_prefs.get("genre", "")),
        str(user_prefs.get("mood", "")),
        float(user_prefs.get("energy", 0.0)),
        str(song.get("genre", "")),
        str(song.get("mood", "")),
        float(song.get("energy", 0.0)),
        (
            float(user_prefs.get("target_tempo_bpm", user_prefs.get("tempo_bpm")))
            if user_prefs.get("target_tempo_bpm", user_prefs.get("tempo_bpm")) is not None
            else None
        ),
        float(song["tempo_bpm"]) if song.get("tempo_bpm") is not None else None,
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k song recommendations with scores and explanations."""
    scored_songs = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    top_songs = sorted(scored_songs, key=lambda recommendation: recommendation[1], reverse=True)

    return [
        (song, score, "; ".join(reasons))
        for song, score, reasons in top_songs[:max(0, k)]
    ]
