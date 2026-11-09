from pathlib import Path

import pytest

from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)

CATALOG = Path(__file__).resolve().parents[1] / "data" / "songs.csv"


def _song(**overrides):
    """Build one song dictionary, with overrides for the field under test."""
    song = {
        "id": 1,
        "title": "Sample",
        "artist": "Sample Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "tempo_bpm": 100,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.5,
    }
    song.update(overrides)
    return song

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
    assert explanation.strip() != ""
    assert "genre match (+2.0)" in explanation
    assert "mood match (+1.0)" in explanation


def test_load_songs_converts_numeric_fields(tmp_path):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "3,Tiny Tune,Ada Quinn,folk,sad,0.30,76,0.22,0.40,0.88\n",
        encoding="utf-8",
    )
    songs = load_songs(str(csv_path))
    assert len(songs) == 1
    song = songs[0]
    assert song["id"] == 3
    assert isinstance(song["id"], int)
    assert song["tempo_bpm"] == 76
    assert isinstance(song["tempo_bpm"], int)
    assert song["energy"] == pytest.approx(0.30)
    assert isinstance(song["energy"], float)
    assert isinstance(song["valence"], float)
    assert isinstance(song["danceability"], float)
    assert isinstance(song["acousticness"], float)


def test_load_songs_reads_the_full_catalog():
    songs = load_songs(str(CATALOG))
    assert len(songs) == 20
    assert songs[0]["title"] == "Sunrise City"
    assert songs[0]["energy"] == pytest.approx(0.82)
    for song in songs:
        assert song["title"]
        assert song["artist"]
        assert song["genre"]
        assert song["mood"]


def test_score_song_awards_genre_and_mood_points():
    prefs = {"genre": "rock", "mood": "intense", "energy": 0.4}
    matched = _song(genre="rock", mood="intense", energy=0.4, title="Matched")
    missed = _song(genre="jazz", mood="chill", energy=0.4, title="Missed")
    matched_score, reasons = score_song(prefs, matched)
    missed_score, missed_reasons = score_song(prefs, missed)
    assert "genre match (+2.0)" in reasons
    assert "mood match (+1.0)" in reasons
    assert "genre match (+2.0)" not in missed_reasons
    assert "mood match (+1.0)" not in missed_reasons
    assert matched_score - missed_score == pytest.approx(3.0)


def test_energy_closeness_rewards_the_nearer_song():
    prefs = {"genre": "jazz", "mood": "relaxed", "energy": 0.5}
    near = _song(title="Near", energy=0.5)
    higher = _song(title="Higher", energy=0.95)
    lower = _song(title="Lower", energy=0.05)
    near_score, near_reasons = score_song(prefs, near)
    higher_score, _ = score_song(prefs, higher)
    lower_score, _ = score_song(prefs, lower)
    assert near_score > higher_score
    assert near_score > lower_score
    assert any(reason.startswith("energy closeness") for reason in near_reasons)


def test_energy_closeness_treats_higher_and_lower_the_same():
    prefs = {"genre": "jazz", "mood": "relaxed", "energy": 0.5}
    above = _song(title="Above", energy=0.75)
    below = _song(title="Below", energy=0.25)
    above_score, above_reasons = score_song(prefs, above)
    below_score, below_reasons = score_song(prefs, below)
    assert above_score == below_score
    assert above_reasons == below_reasons


def test_recommend_songs_sorts_highest_first_and_limits_k():
    songs = [
        _song(id=1, title="Weak", genre="jazz", mood="sad", energy=0.1),
        _song(id=2, title="Best", genre="pop", mood="happy", energy=0.8),
        _song(id=3, title="Middle", genre="pop", mood="chill", energy=0.8),
    ]
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    ranked = recommend_songs(prefs, songs, k=3)
    limited = recommend_songs(prefs, songs, k=1)
    empty = recommend_songs(prefs, songs, k=0)
    assert [item[0]["title"] for item in ranked] == ["Best", "Middle", "Weak"]
    assert ranked[0][1] > ranked[1][1] > ranked[2][1]
    assert len(limited) == 1
    assert limited[0][0]["title"] == "Best"
    assert empty == []


def test_recommend_songs_caps_k_on_the_real_catalog():
    songs = load_songs(str(CATALOG))
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False}
    top_two = recommend_songs(prefs, songs, k=2)
    top_five = recommend_songs(prefs, songs, k=5)
    everything = recommend_songs(prefs, songs, k=100)
    assert len(top_two) == 2
    assert len(top_five) == 5
    assert len(everything) == len(songs)
    scores = [item[1] for item in top_five]
    assert scores == sorted(scores, reverse=True)
    assert top_two[0][0]["title"] == top_five[0][0]["title"]
