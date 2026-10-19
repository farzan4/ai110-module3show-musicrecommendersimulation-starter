"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

from recommender import load_songs, recommend_songs


def main() -> None:
    songs_path = Path(__file__).resolve().parent.parent / "data" / "songs.csv"
    songs = load_songs(str(songs_path))
    print(f"Loaded songs: {len(songs)}")

    # Example listener: prefers pop and happy songs, high energy, and
    # does not specifically prefer acoustic music.
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "target_tempo_bpm": 120,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations")
    print("=" * 40)
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"\n{rank}. {song['title']}")
        print(f"   Final score: {score:.2f}")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
