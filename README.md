# Generate historic Dutch city names

I run a D&D campaign inspired by Dutch history, and I'm often in need of names for people and places. With this generator, I'm trying out the idea of procedurally generating city names.

The generator creates a character-based language model based on a selection of place names from the _Atlas Nouveau des Dix-sept Provinces des Pais-Bas_ by Pierre Mortier, published around 1700.

I have created an ngram model, which seems to work best with fourgrams. I have also done some work on a recurrent neural network, but this still performs worse than the ngram model.
