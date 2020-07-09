from math import ceil, floor, log, pow
from sys import argv


class CreditCalc:
    def __init__(self, arguments: list):
        self.mode = "annuity"
        self.payment = 0
        self.principal = 0
        self.periods = 0
        self.interest = 0
        self.payments_sum = 0
        if self.parse_args(arguments):
            self.calculate()
        else:
            print("Incorrect parameters")

    @staticmethod
    def humanize_period(months_in: int) -> str:
        """
        Converts months count to 'X years and Y months' form

        :param months_in: month count
        :return: humanized representation
        """

        def format_num(number: int, unit: str) -> str:
            """
            Formats number using unit name and plural form when needed

            :param number:
            :param unit:
            :return: formatted string
            """
            if number == 0:
                return ""
            elif number == 1:
                return f"1 {unit}"
            else:
                return f"{number} {unit}s"

        years = months_in // 12
        months = months_in % 12
        return (
            f"{format_num(years, 'year')}"
            f"{' and ' if months and years else ''}"
            f"{format_num(months, 'month')}"
        )

    def parse_args(self, arguments: list) -> bool:
        """
        Parses and checks command line arguments

        :param arguments: Command line arguments
        :return: True if parsed Ok
        """
        # we need exactly 4 arguments (+ argv[0])
        if len(arguments) != 5:
            return False
        for arg in arguments[1:]:
            # check arguments format
            if "=" not in arg or not arg.startswith("--"):
                return False
            param, value = arg.split("=")
            # payment type
            if param == "--type":
                if value == "diff":
                    self.mode = "diff"
                elif value != "annuity":
                    return False
            # payment size
            elif param == "--payment":
                try:
                    self.payment = float(value)
                except ValueError:
                    return False
            # credit principal
            elif param == "--principal":
                try:
                    self.principal = float(value)
                except ValueError:
                    return False
            # periods count
            elif param == "--periods":
                try:
                    self.periods = int(value)
                except ValueError:
                    return False
            # credit interest
            elif param == "--interest":
                try:
                    self.interest = float(value) / 12 / 100
                except ValueError:
                    return False
        # border conditions
        if (
            self.principal < 0
            or self.payment < 0
            or self.periods < 0
            or self.interest <= 0
        ):
            return False
        # arguments compatibility
        if self.mode == "diff" and self.payment:
            return False
        return True

    def diff_payment(self):
        """
        Calculates differentiated payment

        :return:
        """
        p_div_n = self.principal / self.periods
        for month in range(1, self.periods + 1):
            monthly_payment = ceil(
                p_div_n
                + self.interest
                * (self.principal - self.principal * (month - 1) / self.periods)
            )
            self.payments_sum += monthly_payment
            print(f"Month {month}: paid out {monthly_payment}")

    def count_of_periods(self):
        """
        Counts periods (months) to repay credit

        :return:
        """
        count = ceil(
            log(
                self.payment / (self.payment - self.interest * self.principal),
                1 + self.interest,
            )
        )
        self.payments_sum = count * self.payment
        print(f"You need {self.humanize_period(count)} to repay this credit!")

    def annuity_payment(self):
        """
        Calculates annuity payment

        :return:
        """
        power = pow(1 + self.interest, self.periods)
        payment = ceil(self.principal * self.interest * power / (power - 1))
        self.payments_sum = self.periods * payment
        print(f"Your annuity payment = {payment}!")

    def credit_principal(self):
        """
        Calculates credit principal

        :return:
        """
        power = pow(1 + self.interest, self.periods)
        self.principal = floor(self.payment / (self.interest * power / (power - 1)))
        self.payments_sum = self.payment * self.periods
        print(f"Your credit principal = {self.principal}!")

    def overpayment(self):
        """
        Calculates overpayment

        :return:
        """
        print(f"Overpayment = {round(self.payments_sum - self.principal)}")

    def calculate(self):
        """
        Calculator engine =)

        :return:
        """
        if self.mode == "diff" and self.principal and self.periods:
            self.diff_payment()
        elif self.principal and self.payment:
            self.count_of_periods()
        elif self.principal and self.periods:
            self.annuity_payment()
        elif self.payment and self.periods:
            self.credit_principal()
        self.overpayment()


calc = CreditCalc(argv)
