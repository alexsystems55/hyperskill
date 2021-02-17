from collections import Counter, defaultdict
from random import choices
from nltk.tokenize import regexp_tokenize
from nltk import bigrams

# Data input
file_path = input()
tokens = []
try:
    with open(file_path, "r", encoding="utf-8") as text_file:
        tokens = regexp_tokenize(text_file.read(), r"\S+")
except OSError as error:
    print(error)

# Get bigrams
bigrams_ = list(bigrams(tokens))

# Build Markov chain model
heads = defaultdict(Counter)
for head, tail in bigrams_:
    heads[head][tail] += 1

# Generate text
for sentence in range(10):
    text = [choices(bigrams_)[0][0]]
    start_word = text[0]
    for step in range(9):
        text += choices(
            list(heads[start_word].keys()), list(heads[start_word].values())
        )
        start_word = text[-1]
    print(" ".join(text))
