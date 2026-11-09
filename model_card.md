# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

This is a small classroom recommender. The name is just a label for the scoring recipe in this project.

---

## 2. Intended Use

The goal is to turn one listener profile into a ranked list of songs and to show why each song scored the way it did.

VibeFinder 1.0 is for a student exploring how a content-based recommender works. It assumes the listener can name one favorite genre, one favorite mood, a target energy between 0 and 1, and whether they like acoustic music. It returns the top 5 songs in a 20-song catalog, with a score and short reasons.

It is not for a real music service. It should not be used to choose what a real person hears, to decide which artists get promoted, or to judge whether a song is good. The songs are made-up examples. The score is a match to a profile, not a measure of quality.

---

## 3. How the Model Works

Each song starts at zero. A matching genre adds 2.0 points. A matching mood adds 1.0 point. Energy is a closeness score: the song can earn up to 1.5 points when its energy equals the target, and it earns less as the gap grows. A song that is too high does not beat a song that is the same distance too low. Acoustic taste nudges the score by a fraction of a point, up or down.

The program scores every song, sorts from highest to lowest, and keeps five. The starter code returned the first songs in the file. This version scores the whole catalog and can explain each pick with strings such as `genre match (+2.0)`.

---

## 4. Data

The catalog has 20 songs. The starter file had 10, and I added 10 more. The new genres include folk, r&b, metal, country, electronic, blues, latin, classical, and hip hop. The new moods include sad, romantic, angry, nostalgic, dreamy, and peaceful.

Each song has a title, an artist, a genre, a mood, energy, tempo, valence, danceability, and acousticness. The score uses genre, mood, energy, and acousticness. Tempo, valence, and danceability are saved and then ignored.

The limits are easy to see. There is one rock song and two pop songs. The only sad songs are slow. There is no listening history and no lyrics. The songs are not from a real chart.

---

## 5. Strengths

High-Energy Pop puts Sunrise City first. That song is pop, happy, and close to energy 0.90, so the result matches the profile.

Chill Lofi puts Library Rain first. Its energy is 0.35, the same as the target, and it is lofi, chill, and acoustic. Midnight Coding, the other chill lofi song, is second.

Deep Intense Rock puts Storm Runner first with 4.9, well ahead of Gym Hero at 3.0. Storm Runner is the only rock song, and it is intense with energy 0.91.

The reasons add up to the printed score. For Sunrise City on the pop profile, 2.0 + 1.0 + 1.4 + 0.3 = 4.7. That made the list easy to trust when it was right.

---

## 6. Limitations and Bias

The clearest weakness is that a genre bonus plus a hole in the catalog can erase a mood request. Restless Sad asks for pop songs that feel sad at energy 0.90, and the catalog has no song that is pop and sad. The only sad songs are Blue Window (folk, energy 0.30) and Rain On The Platform (blues, energy 0.33), so they earn the +1.0 mood point and then lose on energy. Gym Hero is intense, not sad, but the +2.0 pop bonus and a near-perfect energy score give it 4.0 and first place, while Rain On The Platform scores 1.3 and lands at rank 10. Doubling the energy weight in the sensitivity run pushed those sad songs even lower, to ranks 11 and 12, so a bigger energy weight did not fix the hole.

Other limits showed up too. `indie pop` does not count as `pop`, so Rooftop Lights misses the genre bonus. Equal scores are broken by title, which is why Iron Horizon appears as the fifth High-Energy Pop song ahead of Storm Runner at the same 1.9. Chill Lofi also ranks two LoRoom songs in a row. An optional diversity switch can drop the second LoRoom song. I leave it off, because the song that replaced it was Coffee Shop Stories, which is jazz rather than lofi.

---

## 7. Evaluation

I tested four profiles with `python -m src.main`: High-Energy Pop (pop, happy, energy 0.90, acoustic no), Chill Lofi (lofi, chill, energy 0.35, acoustic yes), Deep Intense Rock (rock, intense, energy 0.90, acoustic no), and Restless Sad (pop, sad, energy 0.90, acoustic no). I looked at the top 5 titles, the scores, and the reason strings. I also halved the genre weight and doubled the energy weight, compared the lists, and put the original weights back. `python -m pytest` checks loading, the genre and mood points, energy closeness, sort order, and the `k` limit.

What surprised me is that Restless Sad and Deep Intense Rock returned the same five songs in a different order. I changed the genre from rock to pop and the mood from intense to sad, and a sad song still did not appear. The shared energy target of 0.90, plus a dislike of acoustic music, kept the loud songs in the list.

High-Energy Pop compared with Chill Lofi: the lists do not share a title. Pop opens with Sunrise City (4.7) and Gym Hero (4.0). Lofi opens with Library Rain (4.9) and Midnight Coding (4.6). The profiles disagree on genre, mood, energy, and acoustic taste, so the recipe points at opposite ends of the catalog. That split makes sense.

High-Energy Pop compared with Deep Intense Rock: Sunrise City leads the pop list because it is happy pop near energy 0.90. Storm Runner leads the rock list at 4.9 because it is intense rock at energy 0.91. Gym Hero is on each list. The pop profile pays it for genre, and the rock profile pays it for the intense mood. The different winners make sense because the genre bonus is large, and the shared energy target explains the overlap.

High-Energy Pop compared with Restless Sad: genre, energy, and acoustic taste stay the same, and only the mood changes from happy to sad. The winner changes from Sunrise City (4.7, with a mood match) to Gym Hero (4.0, with no mood match). No sad song enters the top 5. The score math explains the swap, and it also shows the hole in the catalog.

Chill Lofi compared with Deep Intense Rock: there is no shared title. Library Rain is a slow acoustic lofi match at 4.9. Storm Runner is a loud rock match at 4.9. One target energy is 0.35 and the other is 0.90, and the acoustic preference is flipped. A strong song for one profile is a weak song for the other. That distance makes sense.

Chill Lofi compared with Restless Sad: there is no shared title. Library Rain is slow, acoustic, and lofi. Gym Hero is fast, not acoustic, and pop. All four preferences differ, so the lists should not look alike. They do not.

Deep Intense Rock compared with Restless Sad: the top 5 titles are the same five songs, ordered differently. Storm Runner is first for rock (4.9) because genre and mood match. It falls to fourth for Restless Sad (1.9) because those bonuses disappear. Gym Hero and Sunrise City rise on the sad list only because they are pop and close to energy 0.90. The reorder makes sense. The missing sad songs do not.

---

## 8. Future Work

I would use tempo or valence in the score. Those columns are already in the file, and they could separate two songs that share a genre and a mood.

I would treat a near genre as a partial match. Rooftop Lights is tagged `indie pop`, so a pop listener gets no genre points for it.

The diversity switch now exists, and it stays off unless a caller turns it on. A useful next step is to decide when that penalty should turn on by itself. On Chill Lofi it removed the extra LoRoom song, and it also let a jazz song into the top 5.

---

## 9. Personal Reflection

### What was your biggest learning moment?

My biggest learning moment was the Restless Sad run. I thought a sad mood would pull sad songs to the top. It did not. Gym Hero, an intense pop song, scored 4.0 and won, and the sad songs stayed at ranks 10 and 11. I could see why once I added the points: genre is worth 2.0, mood is worth 1.0, and I never added a sad pop song with high energy. The list was following my recipe and my file, not a hidden sense of mood.

### How did using AI tools help you, and when did you need to double-check them?

An AI coding assistant helped me draft the scoring function, the command-line layout, and the tests. I still double-checked the work. I ran `python -m src.main` and `python -m pytest`, and I added the printed reasons by hand. Sunrise City's 2.0 + 1.0 + 1.4 + 0.3 really is 4.7. I also did not trust the idea that a bigger energy weight would help the sad profile. The new ranks showed the opposite, so I put the original weights back.

### What surprised you about how simple algorithms can still feel like recommendations?

The Chill Lofi list felt like a real playlist: Library Rain, then Midnight Coding, then another lofi track. The program does not understand music. It only matches genre, mood, energy, and acousticness. It felt personal because those tags are the same words I would use to describe the songs. The simple points were enough to imitate a taste, as long as the tags and the weights agreed.

### What would you try next?

After the first Chill Lofi list, I saw two LoRoom songs in a row. I added an optional diversity penalty for a repeated artist or a repeated genre. With the switch on, Focus Flow dropped out and Coffee Shop Stories, a jazz song, took the last spot, so I left the switch off for the normal profiles. Next I would use the tempo and valence columns, which are loaded and still ignored, and I would try a partial point when the genre is close, such as indie pop for a pop listener. The weight experiment taught me to print the before and after lists before I keep a change.
