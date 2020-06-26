class CoffeeMachine:
    # Possible machine states
    ST_WAIT = 0
    ST_SELL_DRINK = 10
    ST_GIVE_CASH = 20
    ST_LOAD_SUPPLIES = 30
    ST_SHOW_STATUS = 40
    ST_TURN_OFF = 99

    def __init__(self, init_supplies: dict, available_drinks: dict):
        """
        Machine initialization

        @param init_supplies: {"water": 400, "milk": 540, "beans": 120, "cups": 9, "money": 550}
        @param available_drinks: {"latte": {"water": -350, "milk": -75, "beans": -20, "cups": -1, "money": 7,}, ...}
        """
        self.state = CoffeeMachine.ST_WAIT
        self.supplies = dict(water=0, milk=0, beans=0, cups=0, money=0)
        self.drinks = available_drinks
        self.fill_supplies(init_supplies)

    def parse_supplies(self, supplies_string: str) -> dict:
        """
        Converts supplies string into dict

        @param supplies_string: "100 50 10 1"
        @return: {"water": 100, "milk": 50, "beans": 10, "cups": 1}
        """
        parsed_supplies = {}
        for key, value in zip(self.supplies.keys(), supplies_string.split()):
            try:
                parsed_supplies[key] = int(value)
            except ValueError:
                print(f"Sorry, invalid value of {key}.")
        return parsed_supplies

    def check_supplies_amount(self, needed_supplies: dict) -> bool:
        """
        Checks if supplies amount is enough for requested needs

        @param needed_supplies: {"water": 400, "milk": 540, "beans": 120, "cups": 9, "money": 550}
        @return: Check result
        """
        out_of = []
        for item in needed_supplies:
            if self.supplies[item] + needed_supplies[item] < 0:
                out_of.append(item)
        if out_of:
            print(f"Sorry, not enough {','.join(out_of)}!")
            return False
        else:
            return True

    def fill_supplies(self, loaded_supplies: dict):
        """
        Load or unload specified amount of supply

        @param loaded_supplies: {"water": 400, "milk": 540, "beans": 120, "cups": 9, "money": 550}
        """
        if self.check_supplies_amount(loaded_supplies):
            for item in loaded_supplies:
                self.supplies[item] += loaded_supplies[item]

    def parse_drink_code(self, drink_code: str) -> str:
        """
        Converts drink code from user input to drink name from the list

        @param drink_code:
        @return:
        """
        try:
            return list(self.drinks.keys())[int(drink_code) - 1]
        except (ValueError, IndexError):
            print("Sorry, no such drink.")
            return ""

    def make_drink(self, drink_code: str):
        """
        Makes you a hot drink :)

        @param drink_code:
        @return:
        """
        drink = self.parse_drink_code(drink_code)
        if drink:
            if self.check_supplies_amount(
                    self.drinks[drink]
            ):  # @todo: avoid double check
                print("I have enough resources, making you a coffee!")
                self.fill_supplies(self.drinks[drink])

    def process_command(self, command: str):
        """
        Changes machine state according to received command

        @param command: Command from menu
        """
        if command == "remaining":
            self.state = CoffeeMachine.ST_SHOW_STATUS
        elif command == "buy":
            self.state = CoffeeMachine.ST_SELL_DRINK
        elif command == "take":
            # first switch to GIVE_CASH state to show corresponding message
            if self.state != CoffeeMachine.ST_GIVE_CASH:
                self.state = CoffeeMachine.ST_GIVE_CASH
            else:
                # then give money and go back to main menu
                cm.fill_supplies({"money": -cm.supplies["money"]})
                cm.state = CoffeeMachine.ST_WAIT
        elif command == "fill":
            self.state = CoffeeMachine.ST_LOAD_SUPPLIES
        elif command == "exit":
            self.state = CoffeeMachine.ST_TURN_OFF
        elif command == "back":
            self.state = CoffeeMachine.ST_WAIT
        else:
            if self.state == CoffeeMachine.ST_LOAD_SUPPLIES:
                # parse string as loaded supplies amount
                self.fill_supplies(self.parse_supplies(command))
                self.state = CoffeeMachine.ST_WAIT
            elif self.state == CoffeeMachine.ST_SELL_DRINK:
                # parse string as drink code
                self.make_drink(command)
                self.state = CoffeeMachine.ST_WAIT
            else:
                print("Sorry, unknown command.")


# Main program

# "menu_name": ["menu_item", "menu_item", ...]
MENU_STRINGS = {
    "main": ["Write action (buy, fill, take, remaining, exit):"],
    # @todo: dynamic drinks list
    "buy": [
        "What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:"
    ],
    "fill": [
        "Write how many ml of water do you want to add:",
        "Write how many ml of milk do you want to add:",
        "Write how many grams of coffee beans do you want to add:",
        "Write how many disposable cups do you want to add:",
    ],
    "take": ["I gave you ${}"],
    "remaining": [
        "The coffee machine has:\n"
        "{} ml of water\n"
        "{} ml of milk\n"
        "{} g of coffee beans\n"
        "{} disposable cups\n"
        "${} of money\n"
    ],
}


def show_menu(menu: str, need_input: bool = False, data: list = None) -> list:
    """
    Shows selected menu from MENU_STRINGS and return user input if any

    @param menu: Name of menu to show
    @param data: List of data to show in message
    @param need_input: True if user input needed
    @return: List of data entered by user
    """
    user_input = []
    for item in MENU_STRINGS[menu]:
        if data:
            print(item.format(*data))
        else:
            print(item)
        if need_input:
            user_input.append(input(">").lower())
    return user_input


# initial supplies
supplies = {
    "water": 400,
    "milk": 540,
    "beans": 120,
    "cups": 9,
    "money": 550,
}
# available drinks
drinks = {
    "espresso": {"water": -250, "milk": 0, "beans": -16, "cups": -1, "money": 4, },
    "latte": {"water": -350, "milk": -75, "beans": -20, "cups": -1, "money": 7, },
    "cappuccino": {"water": -200, "milk": -100, "beans": -12, "cups": -1, "money": 6, },
}
# init the machine
cm = CoffeeMachine(supplies, drinks)

while cm.state != CoffeeMachine.ST_TURN_OFF:
    if cm.state == CoffeeMachine.ST_WAIT:
        cm.process_command(*show_menu("main", True))
    elif cm.state == CoffeeMachine.ST_SHOW_STATUS:
        show_menu("remaining", False, list(cm.supplies.values()))
        cm.process_command("back")
    elif cm.state == CoffeeMachine.ST_SELL_DRINK:
        cm.process_command(*show_menu("buy", True))
    elif cm.state == CoffeeMachine.ST_GIVE_CASH:
        show_menu("take", False, [cm.supplies["money"]])
        cm.process_command("take")
    elif cm.state == CoffeeMachine.ST_LOAD_SUPPLIES:
        cm.process_command(" ".join(show_menu("fill", True)))
