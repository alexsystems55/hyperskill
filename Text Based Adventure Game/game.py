from collections import defaultdict
import json
import re

from character import Character


class Game:
    def __init__(self, title: str):
        self.is_running = True
        self.title = title
        # Set some defaults
        self.difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
        self._difficulty = 2
        self.level = 1
        self.chapter = 0
        self.user = "user"
        self.hero = None
        self.saves_path = f"saves/{self.user}.json"
        self.story = defaultdict(list)
        # Let's go!
        self.load_data_from_file()
        self.main_menu()

    @property
    def difficulty_str(self) -> str:
        return self.difficulty_map[self._difficulty]

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
        rx_level = re.compile(r"Level (?P<level>\d+)\n")
        try:
            with open("story/choices.txt", "r") as data_file:
                choices = data_file.read().splitlines()
            with open("story/outcomes.txt", "r") as data_file:
                outcomes = data_file.read().split("*")
            with open("story/story.txt", "r") as data_file:
                for stage in data_file.read().split("+"):
                    match = rx_level.search(stage)
                    if match:
                        level = int(match.group("level"))
                        continue
                    self.story[level].append(
                        {"story": stage.strip(), "choices": {}, "outcomes": {}}
                    )
                    for index in range(1, 4):
                        self.story[level][-1]["choices"][index] = choices.pop(0)
                        self.story[level][-1]["outcomes"][index] = [
                            outcomes.pop(0).strip()
                        ]
                        if "option" in self.story[level][-1]["outcomes"][index][0]:
                            try:
                                while "option" in outcomes[0]:
                                    self.story[level][-1]["outcomes"][index].append(
                                        outcomes.pop(0).strip()
                                    )
                            except IndexError:
                                pass
        except OSError as error:
            print(error)

    def game_loop(self):
        while self.is_running:
            if self.chapter == 0:
                print(f"Level {self.level}\n")
                if self.level == 2:
                    self.is_running = False
                    break
            print(self.story[self.level][self.chapter]["story"], "\n")
            choice = self.get_user_choice(
                self.story[self.level][self.chapter]["choices"].values(),
                "What will you do? Type the number of the option or type '/h' to show help.",
            )
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
            elif choice in ("1", "2", "3"):  # @todo: hardcoded choices = bad idea
                self.parse_story(choice)
            else:
                print("Unknown input! Please enter a valid one.")
            if self.hero.lives < 1:
                print("You've run out of lives! Game over!")
                break

    def get_user_choice(self, choices: list, prompt: str) -> str:
        rx_action = re.compile(r"'(?P<action>.+?)'")
        print(prompt)
        print()
        # Some default actions
        actions = {"/c", "/h", "/i", "/q"}
        for index, choice in enumerate(choices, start=1):
            # Search available actions in given choices
            for match in rx_action.finditer(choice):
                actions.add(match.group("action").lower())
            actions.add(str(index))  # Choices numbers usable as actions, too
            print(f"{index}- {self.replace_inventory_items(choice)}")
        user_choice = input().lower()
        if user_choice not in actions:
            return ""
        return user_choice

    def main_menu(self):
        choices = [
            "Press key '1' or type 'start' to start a new game",
            "Press key '2' or type 'load' to load your progress",
            "Press key '3' or type 'quit' to quit the game",
        ]
        while self.is_running:
            choice = self.get_user_choice(
                choices, f"***Welcome to the {self.title}!***"
            )
            if choice in ("1", "start"):
                self.start_new_game()
            elif choice in ("2", "load"):
                print("No save data found!")
            elif choice in ("3", "quit"):
                self.is_running = False
            else:
                print("Unknown input! Please enter a valid one.\n")
        print("Goodbye!")

    def parse_story(self, choice: str):
        rx_action = re.compile(r"\((?P<action>.+?)\)")
        text = self.story[self.level][self.chapter]["outcomes"][int(choice)][0]
        parsed_text = re.sub(rx_action, "", text)
        parsed_text = self.replace_inventory_items(parsed_text)
        print(parsed_text, "\n")

        for match in rx_action.finditer(text):
            if "move" in match.group("action"):
                self.chapter += 1
            if "life+1" in match.group("action"):
                self.hero.add_life()
            elif "life-1" in match.group("action"):
                self.hero.sub_life()
                self.chapter = 0
            if "save" in match.group("action"):
                self.level += 1
                self.chapter = 0
                self.save_progress()

    def replace_inventory_items(self, text: str) -> str:
        rx_inventory = re.compile(r"{(?P<item>\S+)}")
        for match in rx_inventory.finditer(text):
            if match.group("item") in self.hero.inventory:
                text = re.sub(
                    rx_inventory, self.hero.inventory[match.group("item")], text
                )
        return text

    def save_progress(self):
        save_dict = {
            "char_attrs": {
                "name": self.hero.name,
                "species": self.hero.species,
                "gender": self.hero.gender
            },
            "inventory": self.hero.inventory,
            "difficulty": self.difficulty_str,
            "lives": self.hero.lives,
            "level": self.level
        }
        with open(self.saves_path, "w") as save_file:
            json.dump(save_dict, save_file)

    def start_new_game(self):
        print("Starting a new game...")
        user_name = input(
            "Enter a user name to save your progress or type '/b' to go back "
        )
        # user_name = "test_user"
        if user_name != "/b":
            # User settings
            self.user = user_name
            self.saves_path = f"saves/{self.user}.json"
            # Create our Hero
            self.hero = Character()
            # Set up game difficulty
            while True:
                difficulty = self.get_user_choice(
                    [f"'{dfclt_val}'" for dfclt_val in self.difficulty_map.values()],
                    "Choose your difficulty: ",
                )
                if difficulty.capitalize() in self.difficulty_map.values():
                    self.difficulty = difficulty
                    break
                print("Unknown input! Please enter a valid one.")
            # Show summary and start the game
            print("Good luck on your journey!")
            self.hero.show_traits(show_lives=False)
            self.hero.show_inventory()
            print(f"Difficulty: {self.difficulty_str}\n")
            self.game_loop()
        else:
            print("Going back to menu...\n")


game = Game("Journey to Mount Qaf")
