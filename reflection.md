# Reflection on Profile Comparisons

## High-Energy Pop vs Chill Lofi

`High-Energy Pop` returned bright, upbeat songs that matched pop, happy mood, and high energy all at once. `Chill Lofi` shifted toward calmer songs with low energy, but because the dataset does not contain many explicit lofi labels, the results were driven more by the `chill` mood and energy score than by genre.

## High-Energy Pop vs Deep Intense Rock

Both profiles prefer high-energy songs, so the biggest change came from genre and mood. The pop profile surfaced upbeat mainstream pop tracks, while the rock profile moved toward louder, heavier songs because the `rock` and `intense` labels pushed those songs to the top.

## High-Energy Pop vs Adversarial: Sad But Max Energy

The pop profile rewarded songs that felt energetic and cheerful, while the `sad but max energy` profile exposed a tension in the scoring system. Even though the user asked for very high energy, songs still ranked highly when they matched the `R&B` and `sad` labels, which shows that label matches can beat the energy target.

## High-Energy Pop vs Adversarial: Acoustic Dancefloor

These two profiles both wanted relatively high energy, but the acoustic-electronic profile added a new filter through `likes_acoustic`. That pushed the output toward songs that were still energetic but also had higher acousticness, which made the results feel more textured and less purely dance-pop.

## Chill Lofi vs Deep Intense Rock

These two profiles produced the clearest contrast. `Chill Lofi` favored slower, softer songs with low energy, while `Deep Intense Rock` favored aggressive high-energy tracks because the desired mood changed from `chill` to `intense` and the target energy moved from `0.35` to `0.95`.

## Chill Lofi vs Adversarial: Sad But Max Energy

Both profiles moved away from upbeat music, but in very different ways. `Chill Lofi` preferred gentle low-energy songs, while `sad but max energy` showed that the recommender will still choose sad songs with only moderate energy if the mood and genre labels line up strongly enough.

## Chill Lofi vs Adversarial: Acoustic Dancefloor

The lofi profile mostly tested low energy and calm mood, while the acoustic-electronic profile tested whether the system could keep energy high and still reward acousticness. This comparison shows that the acoustic preference does change the list, but it works best when the dataset already has enough songs in that genre family.

## Deep Intense Rock vs Adversarial: Sad But Max Energy

Both profiles can surface emotionally heavy songs, but they do it for different reasons. The rock profile is driven by genre plus intensity, while the R&B/sad profile is driven by mood and genre even when the energy target is not a close match.

## Deep Intense Rock vs Adversarial: Acoustic Dancefloor

These profiles both ask for strong energy, but the output changes because one wants heavy rock intensity and the other wants dreamy electronic songs with some acoustic quality. That difference makes sense because the same energy level can still feel completely different depending on genre and mood.

## Adversarial: Sad But Max Energy vs Adversarial: Acoustic Dancefloor

These two edge cases test different weaknesses. `Sad But Max Energy` shows that the scoring system can be pulled toward label matches even when the energy target conflicts, while `Acoustic Dancefloor` shows that adding acousticness creates a narrower and more specialized recommendation pattern.
