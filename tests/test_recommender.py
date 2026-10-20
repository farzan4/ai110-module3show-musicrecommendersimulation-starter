import pytest

from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    recommend_songs,
    score_song,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)


def test_score_song_applies_genre_mood_and_energy_weights():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "POP", "mood": "HAPPY", "energy": 0.6}

    score, reasons = score_song(user, song)

    assert score == pytest.approx(3.6)
    assert reasons == [
        "Genre match (+1.0)",
        "Mood match (+1.0)",
        "Energy similarity (+1.60)",
    ]


def test_score_song_includes_tempo_similarity_when_target_is_provided():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8, "target_tempo_bpm": 120}
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 110,
    }

    score, reasons = score_song(user, song)

    assert score == 4.9
    assert reasons[-1] == "Tempo similarity (+0.90)"


def test_oop_recommender_uses_target_tempo_in_explanation():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        target_tempo_bpm=120,
    )
    rec = make_small_recommender()

    explanation = rec.explain_recommendation(user, rec.songs[0])

    assert "Tempo similarity (+1.00)" in explanation


def test_recommend_songs_ranks_by_weighted_score():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    genre_match = {"title": "Genre match", "genre": "pop", "mood": "calm", "energy": 0.2}
    mood_and_energy_match = {
        "title": "Mood and energy match",
        "genre": "jazz",
        "mood": "happy",
        "energy": 0.8,
    }

    recommendations = recommend_songs(user, [mood_and_energy_match, genre_match], k=2)

    assert recommendations[0][0] is mood_and_energy_match
    assert recommendations[0][1] > recommendations[1][1]
    assert all(explanation.strip() for _, _, explanation in recommendations)
