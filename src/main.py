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


def _print_profile(name: str, user_prefs: dict, songs: list[dict]) -> None:
    """Print the top recommendations for a single named user profile."""
    _print_header(name)
    print(f"Genre : {user_prefs['genre']}")
    print(f"Mood  : {user_prefs['mood']}")
    print(f"Energy: {user_prefs['energy']:.2f}")
    if "likes_acoustic" in user_prefs:
        print(f"Acoustic preference: {user_prefs['likes_acoustic']}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop Recommendations")
    print("-------------------")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Final score: {score:.2f}")
        print(f"   Reasons    : {explanation}")
        print()


def _print_header(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def main() -> None:
    songs = load_songs("data/songs_v2_adapted.csv")
    print("Music Recommender Simulation")
    print("============================")
    print(f"Loaded songs: {len(songs)}")

    test_profiles = [
        ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.90}),
        ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.35}),
        ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.95}),
        ("Adversarial: Sad But Max Energy", {"genre": "R&B", "mood": "sad", "energy": 0.90}),
        (
            "Adversarial: Acoustic Dancefloor",
            {"genre": "electronic", "mood": "dreamy", "energy": 0.85, "likes_acoustic": True},
        ),
    ]

    _print_header("System Evaluation Profiles")
    for name, _ in test_profiles:
        print(f"- {name}")

    for name, user_prefs in test_profiles:
        _print_profile(name, user_prefs, songs)


if __name__ == "__main__":
    main()
