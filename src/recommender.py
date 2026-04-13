import csv
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple


SCORING_MODES: dict[str, dict[str, float]] = {
    "balanced": {
        "genre": 2.0,
        "mood": 1.5,
        "energy": 2.0,
        "tempo": 1.0,
        "valence": 0.75,
        "danceability": 0.75,
        "acousticness": 1.0,
        "popularity": 0.8,
        "mood_tags": 1.2,
        "energy_band": 0.6,
        "acoustic_profile": 0.6,
        "intensity_level": 0.7,
        "dance_style": 0.6,
    },
    "genre_first": {
        "genre": 3.2,
        "mood": 1.2,
        "energy": 1.2,
        "tempo": 0.6,
        "valence": 0.4,
        "danceability": 0.5,
        "acousticness": 0.5,
        "popularity": 0.5,
        "mood_tags": 0.8,
        "energy_band": 0.5,
        "acoustic_profile": 0.4,
        "intensity_level": 0.5,
        "dance_style": 0.4,
    },
    "mood_first": {
        "genre": 1.4,
        "mood": 2.6,
        "energy": 1.4,
        "tempo": 0.5,
        "valence": 0.8,
        "danceability": 0.6,
        "acousticness": 0.7,
        "popularity": 0.4,
        "mood_tags": 1.5,
        "energy_band": 0.8,
        "acoustic_profile": 0.5,
        "intensity_level": 1.0,
        "dance_style": 0.4,
    },
    "energy_focused": {
        "genre": 1.1,
        "mood": 1.0,
        "energy": 3.0,
        "tempo": 1.2,
        "valence": 0.5,
        "danceability": 0.9,
        "acousticness": 0.4,
        "popularity": 0.3,
        "mood_tags": 0.6,
        "energy_band": 1.2,
        "acoustic_profile": 0.3,
        "intensity_level": 1.0,
        "dance_style": 0.7,
    },
}

ARTIST_DIVERSITY_PENALTY = 1.25
GENRE_DIVERSITY_PENALTY = 0.35


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
    popularity: float = 50.0
    mood_tags: str = ""
    energy_band: str = ""
    acoustic_profile: str = ""
    intensity_level: str = ""
    dance_style: str = ""


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

    def recommend(
        self,
        user: UserProfile,
        k: int = 5,
        mode: str = "balanced",
        apply_diversity: bool = True,
    ) -> List[Song]:
        """Return the top k songs for a user ranked by score."""
        ranked_songs = recommend_songs(
            {
                "favorite_genre": user.favorite_genre,
                "favorite_mood": user.favorite_mood,
                "target_energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            [_song_to_dict(song) for song in self.songs],
            k=k,
            mode=mode,
            apply_diversity=apply_diversity,
        )
        return [Song(**song) for song, _, _ in ranked_songs]

    def explain_recommendation(self, user: UserProfile, song: Song, mode: str = "balanced") -> str:
        """Summarize why a given song matches a user's profile."""
        _, reasons = score_song(
            {
                "favorite_genre": user.favorite_genre,
                "favorite_mood": user.favorite_mood,
                "target_energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            _song_to_dict(song),
            mode=mode,
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
                    "tempo_bpm": int(float(row["tempo_bpm"])),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                    "popularity": float(row.get("popularity", 50.0)),
                    "mood_tags": row.get("mood_tags", ""),
                    "energy_band": row.get("energy_band", ""),
                    "acoustic_profile": row.get("acoustic_profile", ""),
                    "intensity_level": row.get("intensity_level", ""),
                    "dance_style": row.get("dance_style", ""),
                }
            )

    return songs


def get_scoring_modes() -> List[str]:
    """Return the available scoring mode names."""
    return list(SCORING_MODES.keys())


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
        "popularity": song.popularity,
        "mood_tags": song.mood_tags,
        "energy_band": song.energy_band,
        "acoustic_profile": song.acoustic_profile,
        "intensity_level": song.intensity_level,
        "dance_style": song.dance_style,
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


def _normalize_tags(raw_tags) -> set[str]:
    """Split a tag list into normalized individual tags."""
    if raw_tags is None:
        return set()
    if isinstance(raw_tags, list):
        parts = raw_tags
    else:
        text = str(raw_tags).replace("|", ",").replace(";", ",")
        parts = text.split(",")
    return {part.strip().lower() for part in parts if part and part.strip()}


def _get_mode_weights(mode: str) -> dict[str, float]:
    """Return the weight map for the requested scoring mode."""
    return SCORING_MODES.get(mode, SCORING_MODES["balanced"])


def _append_closeness_reason(
    reasons: List[str],
    score: float,
    label: str,
    weight: float,
) -> float:
    """Append a reason for a closeness-based score contribution."""
    contribution = weight * score
    if contribution > 0:
        reasons.append(f"{label} (+{contribution:.2f})")
    return contribution


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score a single song against a user profile and return the score plus reasons."""
    weights = _get_mode_weights(mode)
    score = 0.0
    reasons: List[str] = [f"mode={mode}"]

    genre = str(_get_pref(user_prefs, "favorite_genre", "genre", default="")).strip().lower()
    mood = str(_get_pref(user_prefs, "favorite_mood", "mood", default="")).strip().lower()
    target_energy = _get_pref(user_prefs, "target_energy", "energy")
    target_tempo = _get_pref(user_prefs, "target_tempo_bpm", "tempo_bpm")
    target_valence = _get_pref(user_prefs, "target_valence", default=None)
    target_danceability = _get_pref(user_prefs, "target_danceability", default=None)
    target_acousticness = _get_pref(user_prefs, "target_acousticness", default=None)
    target_popularity = _get_pref(user_prefs, "target_popularity", default=None)
    preferred_mood_tags = _normalize_tags(_get_pref(user_prefs, "preferred_mood_tags", default=None))
    preferred_energy_band = str(_get_pref(user_prefs, "preferred_energy_band", default="")).strip().lower()
    preferred_acoustic_profile = str(_get_pref(user_prefs, "preferred_acoustic_profile", default="")).strip().lower()
    preferred_intensity = str(_get_pref(user_prefs, "preferred_intensity", default="")).strip().lower()
    preferred_dance_style = str(_get_pref(user_prefs, "preferred_dance_style", default="")).strip().lower()
    likes_acoustic = bool(_get_pref(user_prefs, "likes_acoustic", default=False))

    song_genre = str(song.get("genre", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    song_energy_band = str(song.get("energy_band", "")).strip().lower()
    song_acoustic_profile = str(song.get("acoustic_profile", "")).strip().lower()
    song_intensity_level = str(song.get("intensity_level", "")).strip().lower()
    song_dance_style = str(song.get("dance_style", "")).strip().lower()
    song_tags = _normalize_tags(song.get("mood_tags", ""))

    if genre and song_genre == genre:
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.2f})")

    if mood and song_mood == mood:
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.2f})")

    if target_energy is not None:
        score += _append_closeness_reason(
            reasons,
            _closeness(float(song.get("energy", 0.0)), float(target_energy)),
            "energy closeness",
            weights["energy"],
        )

    if target_tempo is not None:
        score += _append_closeness_reason(
            reasons,
            _closeness(float(song.get("tempo_bpm", 0.0)), float(target_tempo), scale=120.0),
            "tempo closeness",
            weights["tempo"],
        )

    if target_valence is not None:
        score += _append_closeness_reason(
            reasons,
            _closeness(float(song.get("valence", 0.0)), float(target_valence)),
            "valence closeness",
            weights["valence"],
        )

    if target_danceability is not None:
        score += _append_closeness_reason(
            reasons,
            _closeness(float(song.get("danceability", 0.0)), float(target_danceability)),
            "danceability closeness",
            weights["danceability"],
        )

    if likes_acoustic or target_acousticness is not None:
        acoustic_target = 1.0 if target_acousticness is None else float(target_acousticness)
        score += _append_closeness_reason(
            reasons,
            _closeness(float(song.get("acousticness", 0.0)), acoustic_target),
            "acousticness closeness",
            weights["acousticness"],
        )

    if target_popularity is not None:
        score += _append_closeness_reason(
            reasons,
            _closeness(float(song.get("popularity", 0.0)), float(target_popularity), scale=100.0),
            "popularity closeness",
            weights["popularity"],
        )

    if preferred_mood_tags:
        overlap = preferred_mood_tags & song_tags
        if overlap:
            tag_score = weights["mood_tags"] * (len(overlap) / len(preferred_mood_tags))
            score += tag_score
            reasons.append(f"mood tag overlap {sorted(overlap)} (+{tag_score:.2f})")

    if preferred_energy_band and song_energy_band == preferred_energy_band:
        score += weights["energy_band"]
        reasons.append(f"energy band match (+{weights['energy_band']:.2f})")

    if preferred_acoustic_profile and song_acoustic_profile == preferred_acoustic_profile:
        score += weights["acoustic_profile"]
        reasons.append(f"acoustic profile match (+{weights['acoustic_profile']:.2f})")

    if preferred_intensity and song_intensity_level == preferred_intensity:
        score += weights["intensity_level"]
        reasons.append(f"intensity match (+{weights['intensity_level']:.2f})")

    if preferred_dance_style and song_dance_style == preferred_dance_style:
        score += weights["dance_style"]
        reasons.append(f"dance style match (+{weights['dance_style']:.2f})")

    return score, reasons


def _apply_diversity_penalty(
    scored_songs: List[Tuple[Dict, float, List[str]]],
    k: int,
) -> List[Tuple[Dict, float, str]]:
    """Greedily select top results while penalizing repeated artists and genres."""
    remaining = list(scored_songs)
    selected: List[Tuple[Dict, float, str]] = []
    artist_counts: Counter[str] = Counter()
    genre_counts: Counter[str] = Counter()

    while remaining and len(selected) < k:
        best_index = 0
        best_adjusted_score = float("-inf")
        best_penalty_reasons: List[str] = []

        for index, (song, base_score, reasons) in enumerate(remaining):
            artist = str(song.get("artist", "")).strip().lower()
            genre = str(song.get("genre", "")).strip().lower()
            artist_penalty = artist_counts[artist] * ARTIST_DIVERSITY_PENALTY
            genre_penalty = genre_counts[genre] * GENRE_DIVERSITY_PENALTY
            adjusted_score = base_score - artist_penalty - genre_penalty
            penalty_reasons: List[str] = []

            if artist_penalty > 0:
                penalty_reasons.append(f"artist diversity penalty (-{artist_penalty:.2f})")
            if genre_penalty > 0:
                penalty_reasons.append(f"genre diversity penalty (-{genre_penalty:.2f})")

            if adjusted_score > best_adjusted_score:
                best_index = index
                best_adjusted_score = adjusted_score
                best_penalty_reasons = penalty_reasons

        song, _, reasons = remaining.pop(best_index)
        final_reasons = reasons + best_penalty_reasons
        selected.append((song, best_adjusted_score, "; ".join(final_reasons)))

        artist_counts[str(song.get("artist", "")).strip().lower()] += 1
        genre_counts[str(song.get("genre", "")).strip().lower()] += 1

    return selected


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    apply_diversity: bool = True,
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs with scores and explanations."""
    scored_songs = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song, mode=mode)]
    ]

    if apply_diversity:
        return _apply_diversity_penalty(scored_songs, k)

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return [
        (song, score, "; ".join(reasons) if reasons else "No strong match.")
        for song, score, reasons in scored_songs[:k]
    ]
