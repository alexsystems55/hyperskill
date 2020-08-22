class GameField:
    def __init__(self, size=3):
        self.size = size
        self.field = []
        self.fill()
        self.state = "Game not finished"

    def check_state(self) -> str:
        def is_complete(line: list) -> bool:
            if "_" in line:
                return False
            if len(set(line)) == 1:
                return True
            return False

        # Check rows
        for row in self.field:
            if is_complete(row):
                return f"{row[0]} wins"
        # Check columns
        for row in zip(*self.field):
            if is_complete(list(row)):
                return f"{row[0]} wins"
        # Check diagonals
        diagonal = [self.get_cell(x, x) for x in range(1, self.size + 1)]
        if is_complete(diagonal):
            return f"{diagonal[0]} wins"
        diagonal = [
            self.get_cell(x, self.size - x + 1) for x in range(1, self.size + 1)
        ]
        if is_complete(diagonal):
            return f"{diagonal[0]} wins"
        # Check for empty cells
        for row in self.field:
            if "_" in row:
                return "Game not finished"
        return "Draw"

    def fill(self):
        for i in range(self.size):
            self.field.append(list("_" * self.size))

    def get_cell(self, x: int, y: int) -> str:
        return self.field[-y][x - 1]

    def set_cell(self, x: int, y: int, char: str):
        self.field[-y][x - 1] = char
        self.state = self.check_state()

    def show(self):
        print("-" * self.size * 3)
        for row in self.field:
            print("|", *row, "|")
        print("-" * self.size * 3)


def get_coordinates() -> list:
    coord = input("Enter the coordinates: ").split()
    try:
        x = int(coord[0])
        y = int(coord[1])
    except (ValueError, IndexError):
        print("You should enter numbers!")
        return []
    if x not in range(1, FIELD_SIZE + 1) or y not in range(1, FIELD_SIZE + 1):
        print(f"Coordinates should be from 1 to {FIELD_SIZE}!")
        return []
    if battlefield.get_cell(x, y) != "_":
        print("This cell is occupied! Choose another one!")
        return []
    return [x, y]


FIELD_SIZE = 3
battlefield = GameField(FIELD_SIZE)
battlefield.show()
player = "X"
while battlefield.state == "Game not finished":
    coord = []
    while not coord:
        coord = get_coordinates()
    battlefield.set_cell(coord[0], coord[1], player)
    battlefield.show()
    if player == "X":
        player = "O"
    else:
        player = "X"
print(battlefield.state)
