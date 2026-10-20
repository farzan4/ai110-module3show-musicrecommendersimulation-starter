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

    user_profiles = [
        {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.9,
        },
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 1.5,
        },
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "likes_acoustic": True,
        },
    ]

    for profile_number, user_prefs in enumerate(user_profiles, start=1):
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nProfile {profile_number}: {user_prefs}")
        print(f"Top {len(recommendations)} recommendations")
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
