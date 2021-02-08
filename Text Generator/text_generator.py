from nltk.tokenize import regexp_tokenize
from nltk import bigrams

text_file_path = input("Enter text file name: ")
tokens = []
try:
    with open(text_file_path, "r", encoding="utf-8") as text_file:
        for line in text_file:
            tokens += regexp_tokenize(line, r"\S+")
except OSError as error:
    print(error)

# print("Corpus statistics")
# print(f"All tokens: {len(tokens)}")
# print(f"Unique tokens: {len(set(tokens))}")

bigrams_ = list(bigrams(tokens))
print(f"Number of bigrams: {len(bigrams_)}")

while True:
    index = input()
    if index == "exit":
        exit()
    try:
        index = int(index)
        # print(tokens[index])
        print(f"Head: {bigrams_[index][0]}\tTail: {bigrams_[index][1]}")
    except IndexError:
        print(
            "Index Error. Please input an integer that is in the range of the corpus."
        )
    except ValueError:
        print("Type Error. Please input an integer.")
