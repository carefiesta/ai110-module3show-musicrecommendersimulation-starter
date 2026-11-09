"""Command line runner for the Music Recommender Simulation."""

from pathlib import Path

from src.recommender import load_songs, recommend_songs

# Three taste profiles, plus one edge case whose mood and energy disagree.
PROFILES = [
    {
        "name": "High-Energy Pop",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    {
        "name": "Chill Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    {
        "name": "Deep Intense Rock",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    {
        "name": "Restless Sad",
        "genre": "pop",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": False,
        "note": "edge case: energy 0.90 with a sad mood",
    },
]


def _preference_line(profile: dict) -> str:
    """Format the four preferences on one line."""
    acoustic = "yes" if profile["likes_acoustic"] else "no"
    return (
        f"genre={profile['genre']}, mood={profile['mood']}, "
        f"energy={profile['energy']:.2f}, likes_acoustic={acoustic}"
    )


def _print_recommendations(recommendations) -> None:
    """Print the title, score, and reasons for one ranked list."""
    if not recommendations:
        print("No recommendations.")
        return
    for index, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{index}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.1f}")
        print(f"   Reasons: {reasons}")


def main() -> None:
    """Load the catalog and print the top 5 songs for each profile."""
    csv_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    songs = load_songs(str(csv_path))
    print(f"Loaded songs: {len(songs)}")
    for profile in PROFILES:
        print()
        print(f"Profile: {profile['name']}")
        print(f"Preferences: {_preference_line(profile)}")
        if profile.get("note"):
            print(f"Note: {profile['note']}")
        recommendations = recommend_songs(profile, songs, k=5)
        _print_recommendations(recommendations)


if __name__ == "__main__":
    main()
