def num_to_str(num: float) -> str:
    """
    Converts number to string, considering the number type

    :param num: Number to convert
    :return: Resulting string
    """
    if num == int(num):
        return str(int(num))
    else:
        return str(round(num, 3))


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
    """
    Outputs the result

    :param matrix: Matrix to print
    """
    print("The result is:")
    for row in matrix:
        print(" ".join(map(num_to_str, row)))


def add_matrices(m1: list, m2: list) -> None:
    """
    Adds matrix m1 to m2 and prints the result

    :param m1:
    :param m2:
    """
    matrix_s = []
    if len(m1) == len(m2) and len(m1[0]) == len(m2[0]):
        for row_idx in range(len(m1)):
            matrix_s.append([x + y for x, y in zip(m1[row_idx], m2[row_idx])])
        print_matrix(matrix_s)
    else:
        print("The operation cannot be performed.")


def mul_matrices(m1: list, m2: list) -> None:
    """
    Multiplies matrix m1 by m2 and prints the result

    :param m1:
    :param m2:
    """
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


def mul_matrix_by_const(matrix: list, const: float) -> list:
    """
    Multiplies matrix by a constant

    :param matrix:
    :param const:
    :return: Resulting matrix
    """
    matrix_p = []
    for row in matrix:
        matrix_p.append([const * x for x in row])
    return matrix_p


def transpose_matrix(matrix: list, trans_type: str) -> list:
    """
    Transposes matrix by specified way

    :param matrix: Original matrix
    :param trans_type: Kind of transposing
    :return: Transposed matrix
    """
    matrix_t = []
    # Main diagonal
    if trans_type == "1":
        matrix_t = [row for row in zip(*matrix)]
    # Side diagonal
    elif trans_type == "2":
        matrix_t = reversed([reversed(row) for row in zip(*matrix)])
    # Vertical line
    elif trans_type == "3":
        matrix_t = [reversed(row) for row in matrix]
    # Horizontal line
    elif trans_type == "4":
        matrix_t = reversed(matrix)
    return matrix_t


def cofactor(matrix: list, i: int, j: int) -> float:
    """
    Returns cofactor for matrix[i,j] element

    :param matrix:
    :param i:
    :param j:
    :return:
    """
    minor = []
    for row_idx, row in enumerate(matrix):
        if row_idx == i:
            continue
        minor.append(row[0:j] + row[j + 1 :])
    return pow(-1, i + j) * calculate_determinant(minor)


def calculate_determinant(matrix: list) -> float:
    """
    Recursive function for determinant calculation

    :param matrix:
    :return: Determinant
    """
    # 1 x 1 matrix case
    if len(matrix) == 1:
        return matrix[0][0]
    # 2 x 2 matrix case
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    # all bigger matrices
    determinant = 0
    calc_row = 0  # calculate for the first row
    for idx, x in enumerate(matrix[calc_row]):
        determinant += x * cofactor(matrix, calc_row, idx)
    return determinant


def matrix_determinant(matrix: list) -> None:
    """
    Calculates matrix determinant and prints the result

    :param matrix:
    :return:
    """
    if len(matrix) == len(matrix[0]):
        print(f"The result is:\n{calculate_determinant(matrix)}")
    else:
        print("The operation cannot be performed.")


def matrix_inverse(matrix: list) -> None:
    """
    Print matrix inverse if it exists

    :param matrix:
    :return:
    """
    det = calculate_determinant(matrix)
    if det != 0:
        c_matrix = []
        for i in range(len(matrix)):
            c_row = []
            for j in range(len(matrix[i])):
                c_row.append(cofactor(matrix, i, j))
            c_matrix.append(c_row)
        print_matrix(mul_matrix_by_const(transpose_matrix(c_matrix, "1"), 1 / det))
    else:
        print("This matrix doesn't have an inverse")


def menu() -> None:
    """
    Prints menu, gets user choices

    :return:
    """
    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate a determinant")
    print("6. Inverse matrix")
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
        print_matrix(mul_matrix_by_const(matrix_1, const))
    # Multiply matrices
    elif choice == "3":
        matrix_1 = input_matrix("first")
        matrix_2 = input_matrix("second")
        mul_matrices(matrix_1, matrix_2)
    # Transpose matrix
    elif choice == "4":
        print("1. Main diagonal")
        print("2. Side diagonal")
        print("3. Vertical line")
        print("4. Horizontal line")
        choice_t = input("Your choice: ")
        matrix_1 = input_matrix()
        print_matrix(transpose_matrix(matrix_1, choice_t))
    # Calculate a determinant
    elif choice == "5":
        matrix_1 = input_matrix()
        matrix_determinant(matrix_1)
    # Inverse matrix
    elif choice == "6":
        matrix_1 = input_matrix()
        matrix_inverse(matrix_1)


# Main program
while True:
    menu()
