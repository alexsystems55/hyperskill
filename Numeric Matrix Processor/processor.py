def input_matrix(matrix_num="") -> list:
    """
    Gets matrix from user's input

    :param matrix_num: Number of matrix to input ("first", "second"...)
    :return: Matrix as list of rows (lists as well) ([[1, 2], [3, 4]...])
    """
    if matrix_num:
        matrix_num += " "
    rows, cols = map(int, input(f"Enter size of {matrix_num}matrix: ").split())
    matrix = []
    print(f"Enter {matrix_num}matrix:")
    for _ in range(rows):
        matrix.append(list(map(float, input().split()[:cols])))
    return matrix


def print_matrix(matrix: list) -> None:
    print("The result is:")
    for row in matrix:
        print(" ".join(map(str, row)))


def add_matrices(m1: list, m2: list) -> None:
    matrix_s = []
    if len(m1) == len(m2) and len(m1[0]) == len(m2[0]):
        for row_idx in range(len(m1)):
            matrix_s.append([x + y for x, y in zip(m1[row_idx], m2[row_idx])])
        print_matrix(matrix_s)
    else:
        print("The operation cannot be performed.")


def mul_matrices(m1: list, m2: list) -> None:
    matrix_p = []
    if len(m1[0]) == len(m2):
        for m1_row_idx in range(len(m1)):
            matrix_p.append([])
            for m2_col_idx in range(len(m2[0])):
                sum_ = 0
                for m1_col_idx in range(len(m1[0])):
                    sum_ += m1[m1_row_idx][m1_col_idx] * m2[m1_col_idx][m2_col_idx]
                matrix_p[m1_row_idx].append(sum_)
        print_matrix(matrix_p)
    else:
        print("The operation cannot be performed.")


def mul_matrix_by_const(matrix: list, const: float) -> None:
    matrix_p = []
    for row in matrix:
        matrix_p.append([const * x for x in row])
    print_matrix(matrix_p)


def menu():
    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("0. Exit")
    choice = input("Your choice: ")
    # Exit
    if choice == "0":
        exit()
    # Add matrices
    elif choice == "1":
        matrix_1 = input_matrix("first")
        matrix_2 = input_matrix("second")
        add_matrices(matrix_1, matrix_2)
    # Multiply matrix by a constant
    elif choice == "2":
        matrix_1 = input_matrix()
        const = float(input("Enter constant: "))
        mul_matrix_by_const(matrix_1, const)
    # Multiply matrices
    elif choice == "3":
        matrix_1 = input_matrix("first")
        matrix_2 = input_matrix("second")
        mul_matrices(matrix_1, matrix_2)


# Main program
while True:
    menu()
