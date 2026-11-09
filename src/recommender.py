"""Score songs against a listener profile and return the top matches."""

import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple

# Default Algorithm Recipe weights. A sensitivity run may change these
# temporarily, but the shipped values stay here.
GENRE_MATCH = 2.0
MOOD_MATCH = 1.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 1.0

INT_FIELDS = ("id", "tempo_bpm")
FLOAT_FIELDS = ("energy", "valence", "danceability", "acousticness")


@dataclass
class Song:
    """One catalog song and the attributes stored for it."""

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
    """A listener's favorite genre, mood, energy, and acoustic taste."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Rank songs for one user with the shared scoring recipe."""

    def __init__(self, songs: List[Song]):
        """Store the songs this recommender is allowed to rank."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for this user, highest score first."""
        picked = recommend_songs(
            _prefs_from_profile(user),
            [_song_to_dict(song) for song in self.songs],
            k=k,
        )
        by_id = {song.id: song for song in self.songs}
        return [by_id[item[0]["id"]] for item in picked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain one song's score as a single reason string."""
        _, reasons = score_song(_prefs_from_profile(user), song)
        if not reasons:
            return "no matching preferences"
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            song = dict(row)
            for key in INT_FIELDS:
                song[key] = int(float(song[key]))
            for key in FLOAT_FIELDS:
                song[key] = float(song[key])
            songs.append(song)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a numeric score and the reason strings for one song."""
    song = _as_song_dict(song)
    reasons: List[str] = []
    score = 0.0

    genre = str(song.get("genre", "")).strip().casefold()
    mood = str(song.get("mood", "")).strip().casefold()
    wanted_genre = str(user_prefs.get("genre", "")).strip().casefold()
    wanted_mood = str(user_prefs.get("mood", "")).strip().casefold()

    if genre and genre == wanted_genre:
        score += _add_reason(reasons, "genre match", GENRE_MATCH)
    if mood and mood == wanted_mood:
        score += _add_reason(reasons, "mood match", MOOD_MATCH)

    gap = abs(float(song["energy"]) - float(user_prefs["energy"]))
    closeness = max(0.0, 1.0 - gap)
    score += _add_reason(
        reasons,
        "energy closeness",
        ENERGY_WEIGHT * closeness,
        keep_zero=True,
    )

    if "likes_acoustic" in user_prefs and user_prefs["likes_acoustic"] is not None:
        acousticness = float(song.get("acousticness", 0.5))
        if user_prefs["likes_acoustic"]:
            raw = ACOUSTIC_WEIGHT * (acousticness - 0.5)
        else:
            raw = ACOUSTIC_WEIGHT * (0.5 - acousticness)
        score += _add_reason(reasons, "acoustic preference", raw)

    return round(score, 1), reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k from highest to lowest."""
    if k <= 0:
        return []
    ranked = []
    for song in songs:
        song_dict = _as_song_dict(song)
        points, reasons = score_song(user_prefs, song_dict)
        ranked.append((song_dict, points, reasons))
    ranked.sort(key=lambda item: (-item[1], str(item[0].get("title", "")).casefold()))
    chosen = ranked[:k]
    return [(song, points, "; ".join(reasons)) for song, points, reasons in chosen]


def _song_to_dict(song: Song) -> Dict:
    """Copy a Song dataclass into a plain dictionary."""
    return asdict(song)


def _as_song_dict(song) -> Dict:
    """Accept either a Song or a dictionary and return a dictionary."""
    if isinstance(song, Song):
        return asdict(song)
    return song


def _prefs_from_profile(user: UserProfile) -> Dict:
    """Map a UserProfile onto the keys score_song reads."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


def _add_reason(
    reasons: List[str], label: str, points: float, keep_zero: bool = False
) -> float:
    """Append one reason and return the points that were added."""
    points = round(float(points), 1)
    if points == 0 and not keep_zero:
        return 0.0
    reasons.append(f"{label} ({points:+.1f})")
    return points
