# 🎧 Model Card: VibeMap 1.0

## Model Name

**VibeMap 1.0**

## Goal / Task

This recommender suggests songs that match a user's taste profile.  
It tries to rank songs by how well they fit a requested genre, mood, energy level, and acoustic preference.  
It does not predict what a real person will definitely like.  
It gives a simple classroom example of how recommendation logic works.

## Data Used

The system uses `data/songs_v2_adapted.csv`.  
The dataset has 41,574 songs.  
Each song has an id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.  
The adapted data came from `songs_v2.csv`, then it was cleaned to match the schema used by the project.  
The biggest limit is that the catalog is not balanced. It contains much more rock and metal than pop, lofi, or dreamy music.

## Algorithm Summary

The model gives points when a song matches the user's genre and mood.  
It also gives points when the song's energy is close to the target energy.  
If the user wants acoustic songs, it adds another score for acousticness.  
Songs with the highest total score move to the top of the list.  
The system also returns short reasons so the ranking is easier to understand.

## Observed Behavior / Biases

The recommender works best when the dataset has many songs in the requested genre.  
It struggles when a user asks for a less common genre such as `lofi`, because there are not many clear genre matches in the dataset.  
In those cases, the model falls back to mood and energy, so the recommendations may feel only partly right.  
I also found that genre and mood matches can overpower the energy target.  
That means a song can still rank highly even when its energy is not very close to what the user asked for.

## Evaluation Process

I tested five profiles: `High-Energy Pop`, `Chill Lofi`, `Deep Intense Rock`, `Adversarial: Sad But Max Energy`, and `Adversarial: Acoustic Dancefloor`.  
I compared the top 5 songs for each profile and checked whether the reasons matched the profile settings.  
The strongest results were the pop and rock profiles, because those songs matched genre, mood, and energy at the same time.  
The biggest surprise was the `Chill Lofi` profile, because it mostly matched calm mood and low energy instead of true lofi songs.  
The `Sad But Max Energy` profile also showed a weakness: mood and genre matches stayed strong even when the energy target was a poor fit.

## Intended Use and Non-Intended Use

This system is for classroom exploration and simple experiments.  
It is useful for showing how a recommender turns user preferences into rankings.  
It is not meant for real music apps, real users, or business decisions.  
It should not be used to make claims about a person's identity, emotions, or long-term taste.  
It should also not be treated as fair or complete, because the catalog and mood labels are limited.

## Ideas for Improvement

- Build a smaller but more balanced dataset across genres and moods.
- Let users enter more than one favorite genre or mood.
- Add a diversity rule so the top 5 results are not all nearly identical songs.

## Personal Reflection

My biggest learning moment was seeing how much the dataset shapes the results, even when the scoring logic seems reasonable.  
At first, the rules looked simple and fair, but the tests showed that a skewed catalog can quietly push the system toward certain genres again and again.  
AI tools helped me move faster when I was refactoring code, formatting output, and brainstorming evaluation profiles.  
I still had to double-check the results, because the code could look clean while the recommendations were still biased or surprising.  
What surprised me most is that a simple scoring system can still feel like a real recommender when the labels and explanations line up.  
If I extended this project, I would improve the data balance first, then test softer weighting so one strong label match does not dominate everything else.
