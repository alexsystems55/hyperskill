from collections import defaultdict
from nltk.tokenize import regexp_tokenize
from nltk import bigrams

# Data input
file_path = input("Enter text file name: ")
tokens = []
try:
    with open(file_path, "r", encoding="utf-8") as text_file:
        for line in text_file:
            tokens += regexp_tokenize(line, r"\S+")
except OSError as error:
    print(error)

# Get bigrams
bigrams_ = list(bigrams(tokens))

# Build Markov chain model
heads = defaultdict(dict)
for head, tail in bigrams_:
    if tail in heads[head]:
        heads[head][tail] += 1
    else:
        heads[head][tail] = 1

# Check
while True:
    head = input()
    if head == "exit":
        exit()
    print(f"Head: {head}")
    if head in heads:
        for tail in heads[head]:
            print(f"Tail: {tail}\tCount: {heads[head][tail]}")
    else:
        print("The requested word is not in the model. Please input another word.")
