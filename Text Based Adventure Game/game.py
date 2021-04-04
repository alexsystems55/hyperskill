class Game:
    def __init__(self, title: str, user: str):
        self.title = title
        self._difficulty = 2
        self.level = 1
        self.user = user
        self.saves_path = f"saves/{user}.txt"

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


class Character:
    def __init__(self, name: str, species: str, gender: str):
        self.name = name
        self.species = species
        self.gender = gender
        self.bag = {}

    def __str__(self):
        return f"{self.name}, {self.species}, {self.gender}"


def new_game():
    print("Starting a new game...")
    user_name = input(
        "Enter a user name to save your progress or type '/b' to go back "
    )
    if user_name != "/b":
        game = Game("Journey to Mount Qaf", user_name)
        print("Create your character:")
        char_name = input("Name ")
        char_spec = input("Species ")
        char_gender = input("Gender ")
        hero = Character(char_name, char_spec, char_gender)
        print("Pack your bag for the journey:")
        snack = input("Favourite Snack ")
        weapon = input("A weapon for the journey ")
        tool = input("A traversal tool ")
        hero.bag.update({"snack": snack, "weapon": weapon, "tool": tool})
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
        print(f"Your character: {hero}")
        print(f"Your inventory: {', '.join(hero.bag.values())}")
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
