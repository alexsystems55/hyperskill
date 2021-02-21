from collections import Counter, defaultdict
from random import choices
from nltk.tokenize import regexp_tokenize
from nltk import bigrams


# Data input
file_path = input()
try:
    with open(file_path, "r", encoding="utf-8") as text_file:
        tokens = regexp_tokenize(text_file.read(), r"\S+")
except OSError as error:
    print(error)

# Get bigrams
bigrams_ = list(bigrams(tokens))

# Build Markov chain model
chains = defaultdict(Counter)
for head, tail in bigrams_:
    chains[head][tail] += 1

# Generate text
SENTENCES_NUMBER = 10
END_MARKERS = [".", "!", "?"]
MIN_WORDS = 5
for _ in range(SENTENCES_NUMBER):
    sentence = []
    # Get the first word of the sentence
    while True:
        first_word = choices(bigrams_)[0][0]
        # Only capitalized and without sentence-ending punctuation marks
        if first_word[0].isupper() and first_word[-1] not in END_MARKERS:
            break
    sentence.append(first_word)
    # Get next words
    while True:
        next_word = choices(
            list(chains[first_word].keys()), list(chains[first_word].values())
        )[0]
        sentence += [next_word]
        # End sentence with punctuation mark after at least MIN_WORDS
        if next_word[-1] in END_MARKERS and len(sentence) >= MIN_WORDS:
            break
        first_word = next_word
    print(" ".join(sentence))
