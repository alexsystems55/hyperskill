from collections import Counter, defaultdict
from random import choices
from nltk.tokenize import regexp_tokenize
from nltk import trigrams


# Data input
file_path = input()
try:
    with open(file_path, "r", encoding="utf-8") as text_file:
        tokens = regexp_tokenize(text_file.read(), r"\S+")
except OSError as error:
    print(error)

# Get trigrams
trigrams_ = list(trigrams(tokens))

# Build Markov chain model
chains = defaultdict(Counter)
for head_1, head_2, tail in trigrams_:
    chains[f"{head_1} {head_2}"][tail] += 1

# Generate text
SENTENCES_NUMBER = 10
END_MARKERS = [".", "!", "?"]
MIN_WORDS = 5
for _ in range(SENTENCES_NUMBER):
    sentence = ""
    # Get the first word of the sentence
    while True:
        head = choices(list(chains.keys()))[0]
        # Only capitalized and without sentence-ending punctuation marks
        if (
            head[0].isupper()
            and head.split()[0][-1]
            not in END_MARKERS  # Check end of the first word in head
        ):
            break
    sentence += head
    # Get next words
    while True:
        next_word = choices(tuple(chains[head].keys()), tuple(chains[head].values()))[0]
        sentence += f" {next_word}"
        # End sentence with punctuation mark after at least MIN_WORDS
        if next_word[-1] in END_MARKERS and len(sentence.split()) >= MIN_WORDS:
            break
        head = " ".join(sentence.split()[-2:])
    print(sentence)
