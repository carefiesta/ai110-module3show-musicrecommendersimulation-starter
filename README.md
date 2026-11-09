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

From the project folder, run:

```bash
python -m pytest
```

The tests cover `load_songs`, the genre and mood points in `score_song`, energy closeness, ranking order, and the `k` limit. This is the passing output from that command:

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
rootdir: /workspace
collected 9 items

tests/test_recommender.py .........                                      [100%]

============================== 9 passed in 0.01s ===============================
```

---

## Sample Recommendation Output

These blocks are copied from a real `python -m src.main` run. The program first prints `Loaded songs: 20`.

### High-Energy Pop

```text
Profile: High-Energy Pop
Preferences: genre=pop, mood=happy, energy=0.90, likes_acoustic=no
1. Sunrise City — Neon Echo
   Score: 4.7
   Reasons: genre match (+2.0); mood match (+1.0); energy closeness (+1.4); acoustic preference (+0.3)
2. Gym Hero — Max Pulse
   Score: 4.0
   Reasons: genre match (+2.0); energy closeness (+1.5); acoustic preference (+0.5)
3. Carnival Lights — Sol Mar
   Score: 2.7
   Reasons: mood match (+1.0); energy closeness (+1.4); acoustic preference (+0.3)
4. Rooftop Lights — Indigo Parade
   Score: 2.5
   Reasons: mood match (+1.0); energy closeness (+1.3); acoustic preference (+0.2)
5. Iron Horizon — Grave Circuit
   Score: 1.9
   Reasons: energy closeness (+1.4); acoustic preference (+0.5)
```

### Chill Lofi

```text
Profile: Chill Lofi
Preferences: genre=lofi, mood=chill, energy=0.35, likes_acoustic=yes
1. Library Rain — Paper Lanterns
   Score: 4.9
   Reasons: genre match (+2.0); mood match (+1.0); energy closeness (+1.5); acoustic preference (+0.4)
2. Midnight Coding — LoRoom
   Score: 4.6
   Reasons: genre match (+2.0); mood match (+1.0); energy closeness (+1.4); acoustic preference (+0.2)
3. Focus Flow — LoRoom
   Score: 3.7
   Reasons: genre match (+2.0); energy closeness (+1.4); acoustic preference (+0.3)
4. Pine Smoke — Cedar Line
   Score: 2.8
   Reasons: mood match (+1.0); energy closeness (+1.5); acoustic preference (+0.3)
5. Spacewalk Thoughts — Orbit Bloom
   Score: 2.8
   Reasons: mood match (+1.0); energy closeness (+1.4); acoustic preference (+0.4)
```

### Deep Intense Rock

```text
Profile: Deep Intense Rock
Preferences: genre=rock, mood=intense, energy=0.90, likes_acoustic=no
1. Storm Runner — Voltline
   Score: 4.9
   Reasons: genre match (+2.0); mood match (+1.0); energy closeness (+1.5); acoustic preference (+0.4)
2. Gym Hero — Max Pulse
   Score: 3.0
   Reasons: mood match (+1.0); energy closeness (+1.5); acoustic preference (+0.5)
3. Iron Horizon — Grave Circuit
   Score: 1.9
   Reasons: energy closeness (+1.4); acoustic preference (+0.5)
4. Carnival Lights — Sol Mar
   Score: 1.7
   Reasons: energy closeness (+1.4); acoustic preference (+0.3)
5. Sunrise City — Neon Echo
   Score: 1.7
   Reasons: energy closeness (+1.4); acoustic preference (+0.3)
```

### Restless Sad

```text
Profile: Restless Sad
Preferences: genre=pop, mood=sad, energy=0.90, likes_acoustic=no
Note: edge case: energy 0.90 with a sad mood
1. Gym Hero — Max Pulse
   Score: 4.0
   Reasons: genre match (+2.0); energy closeness (+1.5); acoustic preference (+0.5)
2. Sunrise City — Neon Echo
   Score: 3.7
   Reasons: genre match (+2.0); energy closeness (+1.4); acoustic preference (+0.3)
3. Iron Horizon — Grave Circuit
   Score: 1.9
   Reasons: energy closeness (+1.4); acoustic preference (+0.5)
4. Storm Runner — Voltline
   Score: 1.9
   Reasons: energy closeness (+1.5); acoustic preference (+0.4)
5. Carnival Lights — Sol Mar
   Score: 1.7
   Reasons: energy closeness (+1.4); acoustic preference (+0.3)
```

---

## Experiments You Tried

I ran one sensitivity experiment. I halved the genre weight from +2.0 to +1.0 and doubled the energy weight from +1.5 to +3.0. The mood weight stayed at +1.0, and the acoustic weight stayed at +1.0. I ranked the same four profiles again, then put the original weights back. The code in `src/recommender.py` still uses the defaults, because this run did not show a clear improvement.

### High-Energy Pop

Before: Sunrise City 4.7, Gym Hero 4.0, Carnival Lights 2.7, Rooftop Lights 2.5, Iron Horizon 1.9.

After: Sunrise City 5.1, Gym Hero 4.4, Carnival Lights 4.1, Rooftop Lights 3.8, Storm Runner 3.4.

The first four songs stayed in the same order. Fifth place changed from Iron Horizon (metal, angry, energy 0.96) to Storm Runner (rock, intense, energy 0.91). Storm Runner is only 0.01 away from the target, and Iron Horizon is 0.06 away, so the heavier energy term picked the nearer song. The two pop songs still led the list.

### Chill Lofi

Before: Library Rain 4.9, Midnight Coding 4.6, Focus Flow 3.7, Pine Smoke 2.8, Spacewalk Thoughts 2.8.

After: Library Rain 5.4, Midnight Coding 5.0, Pine Smoke 4.3, Spacewalk Thoughts 4.2, Focus Flow 4.1.

Focus Flow is lofi, but its mood is focused rather than chill. Pine Smoke is folk and chill, and its energy is 0.36 against a target of 0.35. With a smaller genre bonus, those closer chill songs moved ahead of the extra lofi track. That follows the new weights. It is a worse list for someone whose favorite genre is lofi, because a folk song jumped over a lofi song.

### Deep Intense Rock

Before: Storm Runner 4.9, Gym Hero 3.0, Iron Horizon 1.9, Carnival Lights 1.7, Sunrise City 1.7.

After: Storm Runner 5.4, Gym Hero 4.4, Iron Horizon 3.3, Carnival Lights 3.1, Sunrise City 3.1.

The order did not change. The scores rose because Storm Runner and Gym Hero were already very close to energy 0.90.

### Restless Sad

Before: Gym Hero 4.0, Sunrise City 3.7, Iron Horizon 1.9, Storm Runner 1.9, Carnival Lights 1.7. The sad songs were lower: Rain On The Platform at rank 10 with 1.3, and Blue Window at rank 11 with 1.2.

After: Gym Hero 4.4, Sunrise City 4.1, Storm Runner 3.4, Iron Horizon 3.3, Carnival Lights 3.1. Rain On The Platform fell to rank 11 with 2.0, and Blue Window fell to rank 12 with 1.8.

The top 5 still contains no sad song. Those two songs are slow (energy 0.33 and 0.30), so a heavier energy weight pushes them further down. Cutting the genre bonus in half was not enough to unseat Gym Hero or Sunrise City.

I kept the default weights. The new mix did not repair the sad high-energy profile, and it made the chill list less loyal to lofi.

---

## Limitations and Risks

The catalog has 20 songs. Several genres appear only once, so a rock listener gets a single true genre match and the rest of the list is filler. The model does not read lyrics, language, or anyone's play history. `tempo_bpm`, `valence`, and `danceability` are stored and then ignored. Genre labels have to match exactly, so `indie pop` is not `pop`.

The biggest scoring risk is the +2.0 genre bonus. On the Restless Sad profile the request is pop, sad, and energy 0.90, and the top 5 are still intense or happy songs with high energy. The only sad songs in the catalog land outside the top 5. Equal scores are also broken by title, which is why Iron Horizon can appear ahead of Storm Runner when the points match. The model card goes into more detail.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I learned that this recommender does not hear the music. It turns each song into tags and a few numbers, adds points when those tags match a profile, and sorts the list. The printed reasons made that visible. On High-Energy Pop, Sunrise City scores 4.7 because 2.0 + 1.0 + 1.4 + 0.3 adds up.

The unfair part showed up on a profile I expected to be sad. Restless Sad still recommended Gym Hero, an intense pop song, and left the two sad songs outside the top 5. Genre was worth more than mood, and the catalog had no sad pop song with high energy. Raising the energy weight did not fix that. It pushed the slow sad songs further down. The longer reflection is in the model card.



