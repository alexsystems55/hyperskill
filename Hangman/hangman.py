from random import choice


def dash_the_word(word: str) -> str:
    """
    Replaces unopened letters with dashes

    :param word: Source word
    :return: Word with replaced letters
    """
    return "".join(["-" if letter not in open_letters else letter for letter in word])


def check_input() -> str:
    """
    Prompts user for input and validates it

    :return: User input or empty string if input is incorrect
    """
    user_input = input("Input a letter: ")
    if user_input in typed_letters:
        print("You already typed this letter")
        return ""
    if len(user_input) != 1:
        print("You should input a single letter")
        return ""
    if not user_input.islower() or not user_input.isalpha():
        print("It is not an ASCII lowercase letter")
        return ""
    return user_input


print("H A N G M A N")
while True:
    command = input('Type "play" to play the game, "exit" to quit: ')
    if command == "play":
        break
    elif command == "exit":
        exit()

word_list = ["python", "java", "kotlin", "javascript"]
tries = 8
word_to_guess = choice(word_list)
open_letters = set()
typed_letters = set()

word_to_show = dash_the_word(word_to_guess)
while tries:
    print()
    print(word_to_show)
    user_letter = check_input()
    if not user_letter:
        continue
    else:
        typed_letters.add(user_letter)
    if user_letter not in word_to_guess:
        print("No such letter in the word")
        tries -= 1
    else:
        open_letters.add(user_letter)
        word_to_show = dash_the_word(word_to_guess)
        if word_to_show == word_to_guess:
            print(f"You guessed the word {word_to_guess}!")
            print("You survived!")
            exit()
print("You are hanged!")
