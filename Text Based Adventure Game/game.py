from collections import defaultdict
import json
from os import listdir
from os.path import dirname
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
        self.saves_path = f"game/saves/{self.user}.json"
        self.story = defaultdict(list)
        # Let's go!
        self.load_data_from_file()
        self.main_menu()

    @property
    def difficulty_str(self) -> str:
        """
        :return: Game difficulty as a string
        """
        return self.difficulty_map[self._difficulty]

    @property
    def difficulty(self) -> int:
        """
        :return: Game difficulty as an int
        """
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        """
        Set game difficulty

        :param value: Difficulty as a word or number
        """
        difficulty_rev_map = {"easy": 1, "medium": 2, "hard": 3, "1": 1, "2": 2, "3": 3}
        difficulty_to_lives_map = {1: 5, 2: 3, 3: 1}
        try:
            self._difficulty = difficulty_rev_map[value.lower()]
            self.hero.lives = difficulty_to_lives_map[self._difficulty]
        except KeyError:
            raise ValueError

    def load_data_from_file(self):
        """
        Load game data to structure like:

        {  # dict of levels
            1: [  # level is a list of chapters
                {
                    "story": "You saw a door with a lock. You also saw a human-sized bird in front of it.",
                    "choices": {
                        1: "Walk up to the unattached door.",
                        2: "Examine the strange bird from afar.",
                        3: "Walk towards the path and face the bird.",
                    },
                    "outcomes": {
                        1: [
                            "You tried the key on the lock and the door opened. (inventory-'key' and move option1)",
                            "You don't have a key to open the lock. (repeat option2)",
                        ],
                        2: ["Its eyes are following you, interested. (repeat)"],
                        3: ["You take out your weapon and attack the bird. It's too fast... (life-1)"],
                    },
                }
            ],
        }
        """
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
        """
        Main game loop
        """
        while self.is_running:
            if self.chapter == 0:
                print(f"Level {self.level}\n")
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
        """
        Show menu (choices) and ask for user input

        :param choices: Available choices
        :param prompt: Prompt or hint
        :return: User choice
        """
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
        """
        Show main menu
        """
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
                self.load_progress()
            elif choice in ("3", "quit"):
                self.is_running = False
            else:
                print("Unknown input! Please enter a valid one.\n")
        print("Goodbye!")

    def parse_story(self, choice: str):
        """
        Parse story and make according actions

        :param choice: User choice
        """
        rx_action = re.compile(r"\((?P<action>.+?)\)")
        rx_item = re.compile(r"inventory(?P<action>[-+])'(?P<item>.+?)'")
        # rx_option = re.compile(r"option(?P<option>\d+)")
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
            if "inventory" in match.group("action"):
                inv_match = rx_item.search(match.group("action"))
                if inv_match.group("action") == "+":
                    self.hero.add_item(
                        {inv_match.group("item"): inv_match.group("item")}
                    )
                else:
                    self.hero.remove_item(inv_match.group("item"))
            # if "option" in match.group("action"):
            #    opt_match = rx_option.search(match.group("action"))
            if "save" in match.group("action"):
                self.level += 1
                self.chapter = 0
                self.save_progress()
            if "game_won" in match.group("action"):
                print("Congratulations! You beat the game!")
                self.is_running = False

    def replace_inventory_items(self, text: str) -> str:
        """
        Replace placeholders with inventory item names

        :param text: Text with placeholders
        :return: Cleared text
        """
        rx_inventory = re.compile(r"{(?P<item>\S+)}")
        for match in rx_inventory.finditer(text):
            if match.group("item") in self.hero.inventory:
                text = re.sub(
                    rx_inventory, self.hero.inventory[match.group("item")], text
                )
        return text

    def load_progress(self):
        """
        Load from save file

        :return:
        """
        saves_dir = dirname(self.saves_path)
        files = [file for file in listdir(saves_dir) if file.endswith(".json")]
        if files:
            print("Type your user name from the list:")
            for file in files:
                print(file[:-5])
            username = input()
            if f"{username}.json" in files:
                print("Loading your progress...")
                with open(f"{saves_dir}/{username}.json", "r") as save_file:
                    data = json.load(save_file)
                try:
                    self.hero = Character()
                    self.hero.name = data["char_attrs"]["name"]
                    self.hero.species = data["char_attrs"]["species"]
                    self.hero.gender = data["char_attrs"]["gender"]
                    self.hero.inventory = data["inventory"]
                    self.hero.lives = data["lives"]
                    self.difficulty = data["difficulty"]
                    self.level = data["level"]
                    self.game_loop()
                except KeyError:
                    print("Save file is corrupted!")
            else:
                print("No save data found!")
        else:
            print("No save data found!")

    def save_progress(self):
        """
        Save game progress to file
        """
        save_dict = {
            "char_attrs": {
                "name": self.hero.name,
                "species": self.hero.species,
                "gender": self.hero.gender,
            },
            "inventory": self.hero.inventory,
            "difficulty": self.difficulty_str,
            "lives": self.hero.lives,
            "level": self.level,
        }
        with open(self.saves_path, "w") as save_file:
            json.dump(save_dict, save_file)

    def start_new_game(self):
        """
        Initialize new game
        """
        print("Starting a new game...")
        user_name = input(
            "Enter a user name to save your progress or type '/b' to go back "
        )
        if user_name != "/b":
            # User settings
            self.user = user_name
            self.saves_path = f"game/saves/{self.user}.json"
            # Create our Hero
            self.hero = Character()
            print("Create your character:")
            self.hero.name = input("Name ")
            self.hero.species = input("Species ")
            self.hero.gender = input("Gender ")
            print("Pack your bag for the journey:")
            snack = input("Favourite Snack ")
            weapon = input("A weapon for the journey ")
            tool = input("A traversal tool ")
            self.hero.add_item(
                {"snack": snack, "weapon": weapon, "tool": tool}, silent=True
            )
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
