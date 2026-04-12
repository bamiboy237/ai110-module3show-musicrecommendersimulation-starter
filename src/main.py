"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def _print_header(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def main() -> None:
    songs = load_songs("data/songs.csv")
    print("Music Recommender Simulation")
    print("============================")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    _print_header("Default User Profile")
    print(f"Genre : {user_prefs['genre']}")
    print(f"Mood  : {user_prefs['mood']}")
    print(f"Energy: {user_prefs['energy']:.2f}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    _print_header("Top Recommendations")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Final score: {score:.2f}")
        print(f"   Reasons    : {explanation}")
        print()


if __name__ == "__main__":
    main()
