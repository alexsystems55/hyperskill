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

    def add_item(self, item: dict, silent: bool = False):
        self.inventory.update(item)
        if not silent:
            print(f"A new item has been added to your inventory: {item.values()}")

    def add_life(self):
        self.lives += 1
        print(f"You gained an extra life! Lives remaining: {self.lives}\n")

    def sub_life(self):
        self.lives -= 1
        print(f"You died! Lives remaining: {self.lives}\n")

    def show_inventory(self):
        print(f"Your inventory: {', '.join(self.inventory.values())}")

    def show_traits(self, show_lives: bool = True):
        print(f"Your character: {self.name}, {self.species}, {self.gender}")
        if show_lives:
            print(f"Lives remaining: {self.lives}\n")
