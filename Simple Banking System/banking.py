import sqlite3


class Card:
    def __init__(self, iin: str, number: str = None, pin: str = None, balance: int = 0):
        """
        Initializes Card object with specified or random parameters

        :param iin: Issuer identification number
        :param number: Card number
        :param pin: Card PIN
        :param balance: Card balance
        """
        self.balance = balance
        self.iin = iin
        self.number = number if number else self.gen_card_number()
        self.pin = pin if pin else self.gen_rand_seq(4)

    def gen_card_number(self) -> str:
        """
        Generates a card number

        :return: Card number
        """
        account = self.gen_rand_seq(9)
        checksum = self.luhn_checksum(f"{self.iin}{account}")
        return f"{self.iin}{account}{checksum}"

    @staticmethod
    def gen_rand_seq(length: int) -> str:
        """
        Generates random numbers sequence of specified length

        :param length: Sequence length
        :return: Random numbers sequence as a string
        """
        from random import randint

        return "".join(str(randint(0, 9)) for _ in range(length))

    @staticmethod
    def luhn_checksum(card_number: str) -> int:
        """
        Calculates checksum for a card number with the Luhn algorithm

        :param card_number:
        :return: Checksum
        """
        sum_ = 0
        for idx in range(1, len(card_number) + 1):
            digit = int(card_number[idx - 1])
            if idx % 2:
                digit *= 2
                if digit > 9:
                    digit -= 9
            sum_ += digit
        return 10 - sum_ % 10 if sum_ % 10 else 0

    def validate_number(self, card_number: str) -> bool:
        """
        Checks if the card number is valid

        :param card_number: Card number
        :return: Check result
        """
        if not card_number.isnumeric():
            return False
        return card_number[-1] == str(self.luhn_checksum(card_number[:-1]))


class CardDB:
    def __init__(self, iin: str):
        """
        Initialize card database

        """
        self.db = sqlite3.connect("card.s3db")
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT UNIQUE NOT NULL,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0
            )
        """
        )
        self.iin = iin

    def __del__(self):
        """
        Closes database connection

        :return:
        """
        self.db.close()

    def insert(self, card: Card) -> bool:
        """
        Inserts a card into the database

        :param card: Card object
        :return: Operation result
        """
        try:
            with self.db:
                self.db.execute(
                    "INSERT INTO card (number, pin) VALUES (?, ?)",
                    (card.number, card.pin),
                )
        except sqlite3.IntegrityError:
            return False
        return True

    def get_by_number(self, number: str) -> Card or None:
        """
        Searches Card object by its number

        :param number: Card number
        :return: Card object or None if no such number in the database
        """
        self.db.row_factory = sqlite3.Row
        result = self.db.execute(
            "SELECT pin, balance FROM card WHERE number = ?", (number,),
        ).fetchone()
        return Card(self.iin, number, result[0], result[1]) if result else None

    def delete(self, card: Card):
        """
        Deletes card record from the database

        :param card: Card object
        :return:
        """
        with self.db:
            self.db.execute("DELETE FROM card WHERE number = ?", (card.number,))

    def update_balance(self, card: Card):
        """
        Updates card record in the database

        :param card: Card object
        :return:
        """
        with self.db:
            self.db.execute(
                "UPDATE card set balance = ? WHERE number = ?",
                (card.balance, card.number),
            )


class Bank:
    def __init__(self, iin: str):
        """
        Initializes Bank object with corresponding IIN and card database

        :param iin:
        """
        self.cards = CardDB(iin)
        self.iin = iin

    def account_create(self):
        """
        Creates a new card and adds it to the database

        :return:
        """
        while True:  # Generate a new card until its number is unique
            card = Card(self.iin)
            if self.cards.insert(card):
                break
        print(
            "Your card has been created\n"
            "Your card number:\n"
            f"{card.number}\n"
            "Your card PIN:\n"
            f"{card.pin}\n"
        )

    def account_menu(self, card: Card):
        """
        Implements account menu

        :param card: Card to work with
        :return:
        """
        print("You have successfully logged in!\n")
        while True:
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            user_input = input()
            if user_input == "0":
                print("Bye!")
                exit()
            elif user_input == "1":
                print(f"Balance: {card.balance}\n")
            elif user_input == "2":
                self.add_income(card)
            elif user_input == "3":
                self.do_transfer(card)
            elif user_input == "4":
                self.close_account(card)
                break
            elif user_input == "5":
                print("You have successfully logged out!\n")
                break
            else:
                print("Invalid input!")

    def account_login(self) -> bool:
        """
        Implements account login menu

        :return: Login attempt result
        """
        print("Enter your card number:")
        card_number = input()
        print("Enter your PIN:")
        pin = input()
        if not Card(self.iin).validate_number(card_number):
            return False
        card = self.cards.get_by_number(card_number)
        if not card:
            return False
        if card.pin == pin:
            self.account_menu(card)
            return True
        return False

    def add_income(self, card: Card):
        """
        Adds requested amount of money to the card

        :param card: Card to work with
        :return:
        """
        print("Enter income:")
        income = int(input())
        card.balance += income
        self.cards.update_balance(card)
        print("Income was added!")

    def close_account(self, card: Card):
        """
        Deletes the account

        :param card: Card to work with
        :return:
        """
        self.cards.delete(card)
        print("The account has been closed!")

    def do_transfer(self, card: Card):
        """
        Transfers money from one card to another

        :param card: Card to transfer money from
        :return:
        """
        print("Transfer\nEnter card number:")
        recv_card_number = input()
        if not Card(self.iin).validate_number(recv_card_number):
            print("Probably you made mistake in the card number. Please try again!")
        elif recv_card_number == card.number:
            print("You can't transfer money to the same account!")
        else:
            recv_card = self.cards.get_by_number(recv_card_number)
            if not recv_card:
                print("Such a card does not exist.")
            else:
                print("Enter how much money you want to transfer:")
                amount = int(input())
                if amount > card.balance:
                    print("Not enough money!")
                else:
                    card.balance -= amount
                    self.cards.update_balance(card)
                    recv_card.balance += amount
                    self.cards.update_balance(recv_card)
                    print("Success!")

    def main_menu(self):
        """
        Implements main menu

        :return:
        """
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
            user_input = input()
            if user_input == "0":
                print("Bye!")
                exit()
            elif user_input == "1":
                self.account_create()
            elif user_input == "2":
                if not self.account_login():
                    print("Wrong card number or PIN!")
            else:
                print("Invalid input!")


# Main program
hyper_bank = Bank("400000")
hyper_bank.main_menu()
