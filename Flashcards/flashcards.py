class DuplicateError(Exception):
    def __init__(self, entry: str, entry_type: str):
        self.message = f'The {entry_type} "{entry}" already exists.\n'
        super().__init__(self.message)


class OtherTermError(Exception):
    def __init__(self, term: str, other_term: str):
        self.message = f'Wrong. The right answer is "{term}", but your definition is correct for "{other_term}".'
        super().__init__(self.message)


class Cards:
    def __init__(self):
        self.cards = {}

    def add_card(self, term: str, definition: str, errors: int = 0) -> None:
        self.cards[term] = {"definition": definition, "errors": errors}

    def check_term(self, term: str) -> str:
        if term in self.cards.keys():
            raise DuplicateError(term, "card")
        return term

    def check_definition(self, definition: str) -> str:
        for value in self.cards.values():
            if value["definition"] == definition:
                raise DuplicateError(definition, "definition")
        return definition

    @property
    def cards_count(self):
        return len(self.cards)

    def check_result(self, term: str, definition: str) -> bool:
        if self.cards[term]["definition"] == definition:
            return True
        else:
            other_term = self.get_term_by_definition(definition)
            if other_term:
                raise OtherTermError(term, other_term)
            return False

    def get_definition_by_term(self, term: str) -> str:
        return self.cards[term]["definition"]

    def get_term_by_definition(self, definition: str) -> str:
        for term, value in self.cards.items():
            if value["definition"] == definition:
                return term
        return ""

    def remove_card(self, term: str) -> None:
        del self.cards[term]

    def export_cards(self, file_name: str) -> None:
        from json import dump

        file = open(file_name, "w")
        dump(self.cards, file)
        file.close()

    def import_cards(self, file_name: str) -> int:
        from json import load

        file = open(file_name, "r")
        data = load(file)
        self.cards.update(data)
        file.close()
        return len(data)


def data_input(prompt: str) -> str:
    check = {
        "card": flash_cards.check_term,
        "definition": flash_cards.check_definition,
    }
    result = ""
    while True:
        print(prompt)
        try:
            func_name = prompt.split()[1].strip(":")
            result = check[func_name](input())
        except DuplicateError as error:
            print(error)
        if result:
            return result


def menu() -> None:
    while True:
        print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        action = input()
        # Add card
        if action == "add":
            card_term = data_input("The card:")
            card_definition = data_input("The definition of the card:")
            flash_cards.add_card(card_term, card_definition)
            print(f'The pair ("{card_term}":"{card_definition}") has been added.\n')
        # Remove card
        elif action == "remove":
            print("Which card?")
            card_term = input()
            try:
                flash_cards.remove_card(card_term)
                print("The card has been removed.\n")
            except KeyError:
                print(f'Can\'t remove "{card_term}": there is no such card.\n')
        # Import cards from file
        elif action == "import":
            print("File name:")
            file_name = input()
            try:
                print(f"{flash_cards.import_cards(file_name)} cards have been loaded.")
            except FileNotFoundError:
                print("File not found.")
            except IOError as error:
                print(error)
        # Export cards to file
        elif action == "export":
            print("File name:")
            file_name = input()
            try:
                flash_cards.export_cards(file_name)
                print(f"{flash_cards.cards_count} cards have been saved.")
            except IOError as error:
                print(error)
        # Ask definition for a card
        elif action == "ask":
            from random import choice

            print("How many times to ask?")
            try:
                times = int(input())
                for _ in range(times):
                    card = choice(list(flash_cards.cards))
                    print(f'Print the definition of "{card}":')
                    user_def = input()
                    try:
                        if flash_cards.check_result(card, user_def):
                            print("Correct!\n")
                        else:
                            print(
                                f'Wrong. The right answer is "{flash_cards.get_definition_by_term(card)}".'
                            )
                    except OtherTermError as error:
                        print(error)
            except ValueError as error:
                print(error)
        elif action == "exit":
            print("Bye bye!")
            exit()


# Initialization
flash_cards = Cards()
menu()
