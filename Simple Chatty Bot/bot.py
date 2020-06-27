def greet(bot_name: str, birth_year: int):
    print(f"Hello! My name is {bot_name}.")
    print(f"I was created in {birth_year}.")


def remind_name():
    print("Please, remind me your name.")
    name = input("> ")
    print(f"What a great name you have, {name}!")


def guess_age():
    print("Let me guess your age.")
    print("Enter remainders of dividing your age by 3, 5 and 7.")

    rem3 = int(input("3> "))
    rem5 = int(input("5> "))
    rem7 = int(input("7> "))
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

    print(f"Your age is {age}; that's a good time to start programming!")


def count():
    print("Now I will prove to you that I can count to any number you want.")
    number = int(input())
    for num in range(number + 1):
        print(f"{num}!")


def test():
    # test configuration
    QUESTION = "WTF???"
    OPTIONS = ("One...", "Two...", "Three...", "PROFIT!!!")
    CORRECT_ANSWER = "4"

    print("Let's test your programming knowledge.")
    print(QUESTION)
    for num, opt in enumerate(OPTIONS):
        print(f"{num + 1}. {opt}")

    while True:
        answer = input("> ")
        if answer == CORRECT_ANSWER:
            break
        else:
            print("Please, try again.")

    print("Completed, have a nice day!")


def end():
    print("Congratulations, have a nice day!")


greet("HyperBot", 2020)
remind_name()
guess_age()
count()
test()
end()
