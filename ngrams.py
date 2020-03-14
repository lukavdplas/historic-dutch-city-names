# --------------------------------------------------------------------
# imports
# --------------------------------------------------------------------

#packages modules etc
import random
from generator import Generator

#pathnames
cities_file = 'city-names.txt'

#import cities

with open(cities_file) as file:
    cities = [line.strip() for line in file.readlines()]

#tokenise

def tokenize(name):
    """Turn a string into a list of character tokens."""
    #name = name.lower() #ignore cases
    characters = [c for c in name] #make a list of characters
    characters = ['<START>'] + characters + ['<STOP>'] #add beginning and end token
    return characters

tokenized_cities = [tokenize(city) for city in cities]

#make list of characters

characters_complete = list(set(char for city in tokenized_cities for char  in city))
characters = [c for c in characters_complete]
characters.remove('<START>')

#frequency function

def ngram_prob(ngram, all_ngrams):
    selection = [n for n in all_ngrams if n == ngram]
    p = len(selection) / len(all_ngrams)
    return p

# --------------------------------------------------------------------
#unigram generator
# --------------------------------------------------------------------

char_list = [char for city in tokenized_cities for char  in city if char != '<START>']

#make a dict with frequencies
unigram_dict = {char : ngram_prob(char, char_list) for char in characters}

def unigram(char, context):
    return unigram_dict[char]

unigram_generator = Generator(characters, unigram)

print('unigrams:')
unigram_generator.printSample(10)
print()

# --------------------------------------------------------------------
#bigram generator
# --------------------------------------------------------------------

def get_bigrams(charlist):
    #get the bigrams for a word

    bigrams = [(charlist[i], charlist[i + 1]) for i in range(len(charlist) - 1)]
    return bigrams

all_bigrams = [bigram for city in tokenized_cities for bigram in get_bigrams(city)]

bigram_dict = {b : ngram_prob(b, all_bigrams) for b in set(all_bigrams)}

def bigram(char, context):
    precedent = context[-1]
    if (precedent, char) in bigram_dict:
        p = bigram_dict[(precedent, char)]
    else:
        p = 0.0

    prior = sum(bigram_dict[b] for b in bigram_dict if b[0] == precedent)

    return p / prior

bigram_generator = Generator(characters, bigram)

print('bigrams:')
bigram_generator.printSample(10)
print()

# --------------------------------------------------------------------
# trigram generator
# --------------------------------------------------------------------

def get_ngrams(charlist, n):
    #get all ngrams for a word
    if len(charlist) < n:
        return []
    
    ngrams = [tuple(charlist[i : i + n]) for i in range(len(charlist) - (n - 1))]
    return ngrams

all_trigrams = [t for city in tokenized_cities for t in get_ngrams(city, 3)]
trigram_dict = {t : ngram_prob(t, all_trigrams) for t in set(all_trigrams)}

def trigram(char, context):
    if len(context) < 2:
        return bigram(char, context)

    precedent = context[-2:]
    token = (precedent[0], precedent[1], char)
    if token in trigram_dict:
        p = trigram_dict[token]
    else:
        p = 0.0

    prior = sum(trigram_dict[t] for t in trigram_dict if t[0] == precedent[0] and t[1] == precedent[1])
    return p / prior

trigram_generator = Generator(characters, trigram)

print('trigrams:')
trigram_generator.printSample(10)
print()
# --------------------------------------------------------------------
# fourgram generator
# --------------------------------------------------------------------

all_fourgrams = [t for city in tokenized_cities for t in get_ngrams(city, 4)]
fourgram_dict = {t : ngram_prob(t, all_trigrams) for t in set(all_trigrams)}

def fourgram(char, context):
    if len(context) < 3:
        return trigram(char, context)

    precedent = context[-3:]
    token = (precedent[0], precedent[1], precedent[2], char)
    if token in fourgram_dict:
        p = fourgram_dict[token]
    else:
        p = 0.0

    prior = sum(fourgram_dict[t] for t in fourgram_dict if all([t[0] == precedent[0], t[1] == precedent[1], t[2] == precedent[2]]))
    return p / prior

print('fourgrams:')
fourgram_generator = Generator(characters, trigram)
fourgram_generator.printSample(10)