from nltk.tokenize import regexp_tokenize

text_file_path = input("Enter text file name: ")
tokens = []
try:
    with open(text_file_path, "r", encoding="utf-8") as text_file:
        for line in text_file:
            tokens += regexp_tokenize(line, r"\S+")
except OSError as error:
    print(error)
print("Corpus statistics")
print(f"All tokens: {len(tokens)}")
print(f"Unique tokens: {len(set(tokens))}")

while True:
    index = input()
    if index == "exit":
        exit()
    try:
        index = int(index)
        try:
            print(tokens[index])
        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
    except ValueError:
        print("Type Error. Please input an integer.")
