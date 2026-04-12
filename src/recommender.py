import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

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
        """Store the song catalog for later recommendation queries."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a user ranked by score."""
        ranked_songs = sorted(
            self.songs,
            key=lambda song: score_song(
                {
                    "favorite_genre": user.favorite_genre,
                    "favorite_mood": user.favorite_mood,
                    "target_energy": user.target_energy,
                    "likes_acoustic": user.likes_acoustic,
                },
                _song_to_dict(song),
            )[0],
            reverse=True,
        )
        return ranked_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Summarize why a given song matches a user's profile."""
        _, reasons = score_song(
            {
                "favorite_genre": user.favorite_genre,
                "favorite_mood": user.favorite_mood,
                "target_energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            _song_to_dict(song),
        )
        return "; ".join(reasons) if reasons else "No strong match."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": int(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs


def _song_to_dict(song: Song | Dict) -> Dict:
    """Convert a Song object to a dictionary if needed."""
    if isinstance(song, dict):
        return song

    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def _get_pref(user_prefs: Dict, *keys: str, default=None):
    """Return the first available preference value from the given keys."""
    for key in keys:
        if key in user_prefs and user_prefs[key] is not None:
            return user_prefs[key]
    return default


def _closeness(value: float, target: float, scale: float = 1.0) -> float:
    """Compute a 0-to-1 closeness score between a value and target."""
    return max(0.0, 1.0 - abs(value - target) / scale)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against a user profile and return the score plus reasons."""
    score = 0.0
    reasons: List[str] = []

    genre = str(_get_pref(user_prefs, "favorite_genre", "genre", default="")).strip().lower()
    mood = str(_get_pref(user_prefs, "favorite_mood", "mood", default="")).strip().lower()
    target_energy = _get_pref(user_prefs, "target_energy", "energy")
    target_tempo = _get_pref(user_prefs, "target_tempo_bpm", "tempo_bpm")
    target_valence = _get_pref(user_prefs, "target_valence", default=None)
    target_danceability = _get_pref(user_prefs, "target_danceability", default=None)
    target_acousticness = _get_pref(user_prefs, "target_acousticness", default=None)
    likes_acoustic = bool(_get_pref(user_prefs, "likes_acoustic", default=False))

    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()

    if genre and song_genre == genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if mood and song_mood == mood:
        score += 1.5
        reasons.append("mood match (+1.5)")

    if target_energy is not None:
        energy_score = 2.0 * _closeness(float(song.get("energy", 0.0)), float(target_energy))
        score += energy_score
        reasons.append(f"energy closeness (+{energy_score:.2f})")

    if target_tempo is not None:
        tempo_score = 1.0 * _closeness(float(song.get("tempo_bpm", 0.0)), float(target_tempo), scale=100.0)
        score += tempo_score
        reasons.append(f"tempo closeness (+{tempo_score:.2f})")

    if target_valence is not None:
        valence_score = 0.75 * _closeness(float(song.get("valence", 0.0)), float(target_valence))
        score += valence_score
        reasons.append(f"valence closeness (+{valence_score:.2f})")

    if target_danceability is not None:
        danceability_score = 0.75 * _closeness(float(song.get("danceability", 0.0)), float(target_danceability))
        score += danceability_score
        reasons.append(f"danceability closeness (+{danceability_score:.2f})")

    if likes_acoustic or target_acousticness is not None:
        acoustic_target = target_acousticness
        if acoustic_target is None:
            acoustic_target = 1.0

        acousticness_score = 1.0 * _closeness(float(song.get("acousticness", 0.0)), float(acoustic_target))
        score += acousticness_score
        reasons.append(f"acousticness closeness (+{acousticness_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs with scores and explanations."""
    scored_songs = sorted(
        (
            (
                song,
                score,
                "; ".join(reasons) if reasons else "No strong match.",
            )
            for song in songs
            for score, reasons in [score_song(user_prefs, song)]
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    return scored_songs[:k]
