class DuplicateError(Exception):
    def __init__(self, entry: str, entry_type: str):
        self.message = f'The {entry_type} "{entry}" already exists. Try again:'
        super().__init__(self.message)


class Cards:
    def __init__(self):
        self.cards = {}

    def add_card(self, term: str, definition: str):
        self.cards[term] = definition

    def check_duplicate(self, entry: str) -> bool:
        if entry in self.cards.keys():
            raise DuplicateError(entry, "term")
        if entry in self.cards.values():
            raise DuplicateError(entry, "definition")
        return True

    def check_card(self, term: str, definition: str) -> bool:
        return self.cards[term] == definition

    def get_definition_by_term(self, term: str) -> str:
        return self.cards[term]

    def get_term_by_definition(self, definition: str) -> str:
        for term, def_ in self.cards.items():
            if def_ == definition:
                return term
        return ""


def input_data(prompt: str) -> str:
    print(prompt)
    while True:
        user_input = input()
        try:
            if flash_cards.check_duplicate(user_input):
                return user_input
        except DuplicateError as error:
            print(error)


# Initialization
cards_number = int(input("Input the number of cards:\n"))
flash_cards = Cards()
# Input
for number in range(1, cards_number + 1):
    card_term = input_data(f"The term for card #{number}:")
    card_definition = input_data(f"The definition for card #{number}:")
    flash_cards.add_card(card_term, card_definition)
# Check
for card in flash_cards.cards:
    user_def = input(f'Print the definition of "{card}":\n')
    if flash_cards.check_card(card, user_def):
        print("Correct!")
    elif user_def in flash_cards.cards.values():
        print(
            f'Wrong. The right answer is "{flash_cards.get_definition_by_term(card)}", '
            f'but your definition is correct for "{flash_cards.get_term_by_definition(user_def)}". '
        )
    else:
        print(
            f'Wrong. The right answer is "{flash_cards.get_definition_by_term(card)}".'
        )
