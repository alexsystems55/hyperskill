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
        """
        Add item to player's inventory

        :param item: {"item_type": "item_name"}
        :param silent: Don't show message if True
        """
        self.inventory.update(item)
        if not silent:
            print(
                f"A new item has been added to your inventory: {list(item.values())[0]}\n"
            )

    def remove_item(self, item: str):
        """
        Remove item from player's inventory

        :param item: Item type
        """
        try:
            removed_item = self.inventory.pop(item)
            print(f"An item has been removed from your inventory: {removed_item}\n")
        except KeyError:
            print(f"There's no {item} in your inventory!\n")

    def add_life(self):
        """
        Add one more life
        """
        self.lives += 1
        print(f"You gained an extra life! Lives remaining: {self.lives}\n")

    def sub_life(self):
        """
        Subtract a life
        """
        self.lives -= 1
        print(f"You died! Lives remaining: {self.lives}\n")

    def show_inventory(self):
        """
        Show player's inventory
        """
        print(f"Your inventory: {', '.join(self.inventory.values())}")

    def show_traits(self, show_lives: bool = True):
        """
        Show player's stats

        :param show_lives: Show lives number if True
        """
        print(f"Your character: {self.name}, {self.species}, {self.gender}")
        if show_lives:
            print(f"Lives remaining: {self.lives}\n")
