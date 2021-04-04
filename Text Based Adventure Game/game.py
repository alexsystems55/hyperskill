class Character:
    def __init__(self):
        self.lives = 3
        self.inventory = {}  # {"item_type": "item_name"}

        print("Create your character:")
        self.name = input("Name ")
        self.species = input("Species ")
        self.gender = input("Gender ")

        print("Pack your bag for the journey:")
        snack = input("Favourite Snack ")
        weapon = input("A weapon for the journey ")
        tool = input("A traversal tool ")
        self.add_item({"snack": snack, "weapon": weapon, "tool": tool}, silent=True)

    def __str__(self):
        return f"{self.name}, {self.species}, {self.gender}."

    def add_item(self, item: dict, silent: bool=False):
        self.inventory.update(item)
        if not silent:
            print(f"A new item has been added to your inventory: {item.values()}")

    def show_inventory(self):
        print(f"Inventory: {', '.join(self.inventory.values())}")

    def show_traits(self, show_lives: bool=True):
        print(self)
        if show_lives:
            print(f"Lives remaining: {self.lives}\n")


class Game:
    def __init__(self, title: str, user: str):
        self.title = title
        self._difficulty = 2
        self.level = 1
        self.user = user
        self.saves_path = f"saves/{user}.txt"
        self.hero = Character()

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
        try:
            self._difficulty = difficulty_rev_map[value.lower()]
        except KeyError:
            raise ValueError

    @staticmethod
    def load_data_from_file(self, path: str) -> str:
        try:
            with open(path, "r") as data_file:
                return data_file.read()
        except OSError as error:
            print(error)

    @staticmethod
    def get_user_input(self, message: str):
        print(message)
        choice = input().lower()
        if choice == "/q":
            exit_confirmation = input("You sure you want to quit the game? Y/N ").lower()
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


def new_game():
    print("Starting a new game...")
    user_name = input(
        "Enter a user name to save your progress or type '/b' to go back "
    )
    if user_name != "/b":
        game = Game("Journey to Mount Qaf", user_name)
        while True:
            print("Choose your difficulty:")
            print("1 - Easy")
            print("2 - Medium")
            print("3 - Hard")
            difficulty = input()
            try:
                game.difficulty = difficulty
                break
            except ValueError:
                print("Unknown input! Please enter a valid one.")
        print("Good luck on your journey!")
        game.hero.show_traits(show_lives=False)
        game.hero.show_inventory()
        print(f"Difficulty: {game.difficulty_str}")
    else:
        print("Going back to menu...\n")


def main_menu():
    game_is_running = True
    while game_is_running:
        print("*** Welcome to the Journey to Mount Qaf! ***\n")
        print("Press key '1' or type 'start' to start a new game")
        print("Press key '2' or type 'load' to load your progress")
        print("Press key '3' or type 'quit' to quit the game")

        choice = input().lower()
        if choice in ("1", "start"):
            new_game()
        elif choice in ("2", "load"):
            print("No save data found!")
        elif choice in ("3", "quit"):
            print("Goodbye!")
            game_is_running = False
        else:
            print("Unknown input! Please enter a valid one.")


main_menu()
