class Character:
    def __init__(self):
        self.lives = 3
        self.inventory = {}  # {"item_type": "item_name"}
        self.name = "Unknown Hero"
        self.species = "unknown"
        self.gender = "unknown"

    def __str__(self):
        return f"{self.name}, {self.species}, {self.gender}."

    def add_item(self, item: dict, silent: bool = False):
        self.inventory.update(item)
        if not silent:
            print(f"A new item has been added to your inventory: {list(item.values())[0]}\n")

    def remove_item(self, item: str):
        try:
            removed_item = self.inventory.pop(item)
            print(f"An item has been removed from your inventory: {removed_item}\n")
        except KeyError:
            pass

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
