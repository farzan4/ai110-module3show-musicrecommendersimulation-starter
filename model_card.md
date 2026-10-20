# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**TuneTrail**

---

## 2. Intended Use

TuneTrail ranks songs by how well they match a listener's chosen genre, mood, energy, and optional tempo. It assumes the listener can describe some preferences. It is for classroom exploration, not a real music service.

---

## 3. How the Model Works

The recommender gives points when a song's genre or mood matches the listener's choice. It gives more energy points when a song's energy is closer to the target. If the listener gives a target tempo, closer tempos earn more points too. It ranks songs by their total score. Acoustic preference is not used in the ranking.

---

## 4. Data

The catalog contains 20 songs with genre, mood, energy, tempo, valence, danceability, and acousticness data. It includes genres such as pop, rock, jazz, folk, and classical, and moods such as happy, chill, intense, and relaxed. The catalog is small and cannot represent every genre or listener. Valence, danceability, and acousticness are recorded but not used in the score.

---

## 5. Strengths

It gives sensible results when a listener's genre, mood, and energy preferences match songs in the catalog. Happy pop songs, for example, rank well for someone who wants happy pop. The optional tempo preference can help find songs with a similar beat speed.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

In my experiment with a target energy of 1.5, the energy preference was outside the range represented by the songs (0.22–0.96). Because the score uses the raw difference between target and song energy, even the most energetic song earned only 0.92 of the possible 2 energy points, so genre and mood matches had more influence than expected. This can make recommendations less responsive to users whose preferred energy is outside the catalog's range; validating or normalizing the energy scale could help.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

I tried three profiles and checked whether the songs near the top matched the preferences each profile described:

- **Profile 1:** likes pop, wants a sad mood, and prefers energy around 0.9. This checks what happens when the chosen genre and mood do not line up well with the catalog.
- **Profile 2:** likes pop and happy songs, with an energy target of 1.5. This checks an energy preference beyond the songs' range (0.22–0.96).
- **Profile 3:** likes pop and happy songs, prefers energy around 0.8, and says they like acoustic music. This checks whether the acoustic preference changes the results.

### Comparing the profiles

- **Profiles 1 and 2:** The first profile puts _Gym Hero_ and _Sunrise City_ at the top, while the second puts _Sunrise City_ first and brings happy _Rooftop Lights_ into the top three. That makes sense: the second profile asks for a happy mood, which _Sunrise City_ and _Rooftop Lights_ match. Its energy target is also beyond anything in the catalog, so even the most energetic songs cannot match it closely and receive fewer energy points.
- **Profiles 1 and 3:** _Gym Hero_ leads for Profile 1, but _Sunrise City_ leads for Profile 3 and _Rooftop Lights_ moves up. Profile 3 asks for a happy mood, which those songs match, and its energy target is close to theirs. The acoustic preference did not push acoustic songs higher because this version of the recommender does not use that preference when ranking songs.
- **Profiles 2 and 3:** Both profiles want pop and happy music, so _Sunrise City_ and _Rooftop Lights_ rank near the top for both. With Profile 3's more moderate energy target, songs such as _Open Road_ and _Neon Shuffle_ enter the top five; Profile 2 instead favors the catalog's more energetic choices, such as _Iron Comet_ and _Paper Crown_. This is sensible because Profile 3's energy target is closer to those mid-to-high energy songs, while Profile 2 asks for more energy than any song provides.

The biggest surprise was that saying “I like acoustic music” did not change the ranking. That is a useful finding rather than a successful match: it shows that the profile accepts this preference, but the scoring currently ignores it. I also found that an out-of-range energy target still returns recommendations, but their scores are lower because none of the songs can fully satisfy it.

---

## 8. Future Work

- Use acousticness, valence, or danceability in the score.
- Add more songs and genres to broaden the catalog.
- Include more variety in the top recommendations.

---

## 9. Personal Reflection

My biggest learning moment was seeing how score weights and the song catalog shape the rankings. AI tools helped me understand the code and organize ideas, but I checked their suggestions against the actual scoring rules and test results. I was surprised that simple matches for genre, mood, and energy can still make recommendations feel personal, even when the system ignores preferences like acoustic music. Next, I would score more song features, add more songs, and test more listener profiles.
