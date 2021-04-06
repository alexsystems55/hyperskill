from collections import defaultdict
import re


class Character:
    def __init__(self):
        self.lives = 3
        self.inventory = {}  # {"item_type": "item_name"}

        print("Create your character:")
        self.name = "Desmond"  # input("Name ")
        self.species = "Half-elf"  # input("Species ")
        self.gender = "Male"  # input("Gender ")

        print("Pack your bag for the journey:")
        snack = "bread"  # input("Favourite Snack ")
        weapon = "staff"  # input("A weapon for the journey ")
        tool = "magic"  # input("A traversal tool ")
        self.add_item({"snack": snack, "weapon": weapon, "tool": tool}, silent=True)

    def __str__(self):
        return f"{self.name}, {self.species}, {self.gender}."

    def add_item(self, item: dict, silent: bool = False):
        self.inventory.update(item)
        if not silent:
            print(f"A new item has been added to your inventory: {item.values()}")

    def show_inventory(self):
        print(f"Your inventory: {', '.join(self.inventory.values())}")

    def show_traits(self, show_lives: bool = True):
        print(f"Your character: {self.name}, {self.species}, {self.gender}")
        if show_lives:
            print(f"Lives remaining: {self.lives}\n")


class Game:
    def __init__(self, title: str):
        self.is_running = True
        self.title = title
        # Set some defaults
        self._difficulty = 2
        self.level = 1
        self.user = "user"
        self.hero = None
        self.saves_path = f"saves/user.txt"
        self.story = defaultdict(list)
        self.choices = []
        self.outcomes = []
        # Let's go!
        self.load_data_from_file()
        self.main_menu()

    @property
    def difficulty_str(self) -> str:
        difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
        return difficulty_map[self._difficulty]

    @property
    def difficulty(self) -> int:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        difficulty_rev_map = {"easy": 1, "medium": 2, "hard": 3, "1": 1, "2": 2, "3": 3}
        difficulty_to_lives_map = {1: 5, 2: 3, 3: 1}
        try:
            self._difficulty = difficulty_rev_map[value.lower()]
            self.hero.lives = difficulty_to_lives_map[self._difficulty]
        except KeyError:
            raise ValueError

    def load_data_from_file(self):
        rx_story = re.compile(r"Level (?P<level>\d+)\n")
        try:
            with open("story/story.txt", "r") as data_file:
                for line in data_file.read().split("+"):
                    match = rx_story.search(line)
                    if match:
                        level = int(match.group("level"))
                        continue
                    self.story[level].append(line.strip())
            with open("story/choices.txt", "r") as data_file:
                self.choices = data_file.read().splitlines()
        except OSError as error:
            print(error)

    def game_loop(self):
        while True:
            if self.hero.lives < 1:
                print("You've run out of lives! Game over!")
                break
            print(self.story[self.level].pop(0), "\n")
            for index, line in enumerate(self.choices[:3], start=1):
                print(f"{index} - {line}")
            print()
            print(
                "What will you do? Type the number of the option or type '/h' to show help."
            )
            choice = input().lower()
            if choice == "/q":
                exit_confirmation = input(
                    "You sure you want to quit the game? Y/N "
                ).lower()
                if exit_confirmation == "y":
                    print("Goodbye!")
                    exit(0)
            elif choice == "/h":
                print("Type the number of the option you want to choose.")
                print("Commands you can use:")
                print("/i => Shows inventory.")
                print("/q => Exits the game.")
                print("/c => Shows the character traits.")
                print("/h => Shows help.")
            elif choice == "/c":
                self.hero.show_traits()
            elif choice == "/i":
                self.hero.show_inventory()
            #        elif choice in
            else:
                print("Unknown input! Please enter a valid one.")

    def main_menu(self):
        while self.is_running:
            print(f"*** Welcome to the {self.title}! ***\n")
            print("Press key '1' or type 'start' to start a new game")
            print("Press key '2' or type 'load' to load your progress")
            print("Press key '3' or type 'quit' to quit the game")

            choice = input().lower()
            if choice in ("1", "start"):
                self.start_new_game()
            elif choice in ("2", "load"):
                print("No save data found!")
            elif choice in ("3", "quit"):
                print("Goodbye!")
                self.is_running = False
            else:
                print("Unknown input! Please enter a valid one.\n")

    def start_new_game(self):
        print("Starting a new game...")
#        user_name = input(
#            "Enter a user name to save your progress or type '/b' to go back "
#        )
        user_name = "test_user"
        if user_name != "/b":
            # User settings
            self.user = user_name
            self.saves_path = f"saves/{self.user}.txt"
            # Create our Hero
            self.hero = Character()
            # Set up game difficulty
#            while True:
#                print("Choose your difficulty:")
#                print("1 - Easy")
#                print("2 - Medium")
#                print("3 - Hard")
#                try:
#                    self.difficulty = input()
#                    break
#                except ValueError:
#                    print("Unknown input! Please enter a valid one.")
            self.difficulty = "2"

            # Show summary and start the game
            print("Good luck on your journey!")
            self.hero.show_traits(show_lives=False)
            self.hero.show_inventory()
            print(f"Difficulty: {self.difficulty_str}")
            self.game_loop()
        else:
            print("Going back to menu...\n")


game = Game("Journey to Mount Qaf")
