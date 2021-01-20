class DuplicateError(Exception):
    def __init__(self, entry: str, entry_type: str):
        self.message = f'The {entry_type} "{entry}" already exists.\n'
        super().__init__(self.message)


class OtherTermError(Exception):
    def __init__(self, term: str, other_term: str):
        self.message = f'Wrong. The right answer is "{term}", but your definition is correct for "{other_term}".\n'
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

    def cards_count(self) -> int:
        return len(self.cards)

    def check_result(self, term: str, definition: str) -> bool:
        if self.cards[term]["definition"] == definition:
            return True
        else:
            self.cards[term]["errors"] += 1
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

    def hardest_cards(self) -> list:
        max_errors = 0
        if self.cards:
            max_errors = max(self.cards[card]["errors"] for card in self.cards)
        if max_errors:
            return [max_errors] + [card for card in self.cards if self.cards[card]["errors"] == max_errors]
        return [max_errors]

    def remove_card(self, term: str) -> None:
        del self.cards[term]

    def export_cards(self, file_name: str) -> None:
        from json import dump

        with open(file_name, "w") as file:
            dump(self.cards, file)

    def import_cards(self, file_name: str) -> int:
        from json import load

        with open(file_name, "r") as file:
            data = load(file)
        self.cards.update(data)
        return len(data)

    def reset_stats(self) -> None:
        for card in self.cards:
            self.cards[card]["errors"] = 0


def output(message: (str, Exception)) -> None:
    if isinstance(message, Exception):
        message = str(message)
    print(message)
    log.append(message)


def get_file_name() -> str:
    output("File name:")
    file_name = input()
    return file_name


def card_data_input(prompt: str) -> str:
    check = {
        "card": flash_cards.check_term,
        "definition": flash_cards.check_definition,
    }
    result = ""
    while True:
        output(prompt)
        try:
            func_name = prompt.split()[1].strip(":")
            result = check[func_name](input())
        except DuplicateError as error:
            output(error)
        if result:
            return result


def save_log(file_name: str) -> None:
    with open(file_name, "w") as file:
        for line in log:
            print(line, file=file)


def menu() -> None:
    while True:
        output(
            "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"
        )
        action = input()
        # Add card
        if action == "add":
            card_term = card_data_input("The card:")
            card_definition = card_data_input("The definition of the card:")
            flash_cards.add_card(card_term, card_definition)
            output(f'The pair ("{card_term}":"{card_definition}") has been added.\n')
        # Remove card
        elif action == "remove":
            output("Which card?")
            card_term = input()
            try:
                flash_cards.remove_card(card_term)
                output("The card has been removed.\n")
            except KeyError:
                output(f'Can\'t remove "{card_term}": there is no such card.\n')
        # Import cards from file
        elif action == "import":
            file_name = get_file_name()
            try:
                output(f"{flash_cards.import_cards(file_name)} cards have been loaded.")
            except FileNotFoundError:
                output("File not found.")
            except IOError as error:
                output(error)
        # Export cards to file
        elif action == "export":
            file_name = get_file_name()
            try:
                flash_cards.export_cards(file_name)
                output(f"{flash_cards.cards_count()} cards have been saved.")
            except IOError as error:
                output(error)
        # Ask definition for a card
        elif action == "ask":
            from random import choice

            output("How many times to ask?")
            try:
                times = int(input())
                for _ in range(times):
                    card = choice(list(flash_cards.cards))
                    output(f'Print the definition of "{card}":')
                    user_def = input()
                    try:
                        if flash_cards.check_result(card, user_def):
                            output("Correct!\n")
                        else:
                            output(
                                f'Wrong. The right answer is "{flash_cards.get_definition_by_term(card)}".\n'
                            )
                    except OtherTermError as error:
                        output(error)
            except ValueError as error:
                output(error)
        # Exit program
        elif action == "exit":
            output("Bye bye!")
            exit()
        # Save log file
        elif action == "log":
            file_name = get_file_name()
            save_log(file_name)
            output("The log has been saved.")
        # Show the hardest card
        elif action == "hardest card":
            hardest = flash_cards.hardest_cards()
            if len(hardest) == 1:
                output("There are no cards with errors.\n")
            elif len(hardest) == 2:
                output(f'The hardest card is "{hardest[1]}". You have {hardest[0]} errors answering it.\n')
            else:
                hard_str = ", ".join(f'"{item}"' for item in hardest[1:])
                output(f'The hardest cards are {hard_str}\n')
        # Reset stats
        elif action == "reset stats":
            flash_cards.reset_stats()
            output("Card statistics have been reset.\n")


# Initialization
flash_cards = Cards()
log = []
menu()
