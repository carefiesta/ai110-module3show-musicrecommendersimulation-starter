# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version is a small content-based music recommender. It loads a catalog of 20 songs, scores every song against a listener profile, and prints the top 5 with the reasons behind each score.

---

## How The System Works

Real platforms usually recommend music in one of two ways. Collaborative filtering uses other users' behavior, such as likes, skips, and playlists, and suggests songs that people with similar habits enjoyed. Content-based filtering uses the song's own attributes, such as tempo, mood, and energy, and suggests songs that resemble what one listener already likes. This project is content-based only. The catalog does not contain other listeners, so there is no collaborative step.

The input data, the user preferences, and the ranking step stay separate. The input data is the song catalog in `data/songs.csv`. The user preferences are one profile: a favorite genre, a favorite mood, a target energy, and whether that person likes acoustic music. The ranking step scores every song with the recipe below, sorts those scores from highest to lowest, and keeps the top 5.

```text
catalog + listener profile -> score every song -> sort high to low -> top 5
```

### Features the objects use

`Song` stores `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The score uses `genre`, `mood`, `energy`, and `acousticness`. `title` and `artist` are shown in the results. `tempo_bpm`, `valence`, and `danceability` are loaded with the catalog and do not change the score.

`UserProfile` stores `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`. The command-line profiles use those same four ideas with the keys `genre`, `mood`, `energy`, and `likes_acoustic`.

### Algorithm Recipe

These are the default weights:

- Genre match: **+2.0** when the song genre equals the favorite genre.
- Mood match: **+1.0** when the song mood equals the favorite mood.
- Energy closeness: **+1.5 × (1 − |song energy − target energy|)**, rounded to one decimal. A song nearer the target earns more points. A higher energy does not beat a lower energy when the two songs sit the same distance from the target.
- Acoustic preference: **+1.0 × (acousticness − 0.5)** when the listener likes acoustic music, and **+1.0 × (0.5 − acousticness)** when they do not. The term is rounded to one decimal. A zero result is left off the reason list.

Each rule that changes the score adds a reason such as `genre match (+2.0)`.

### Expected bias

The genre bonus is the largest single step, so the recipe over-prioritizes genre. A song in the favorite genre can outrank a song that fits the mood and the energy target more closely. Genre labels are exact, so `indie pop` does not count as `pop`.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



