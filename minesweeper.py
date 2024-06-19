board = [
   ["-", "-", "*", "-",],
   ["-", "-", "*", "-",],
   ["-", "-", "-", "-",],
   ["-", "-", "-", "-",]
]


def reveal(board, row, col, flood=False):
    if board[row][col] == "*":
        if flood:
            return

        print_board(board)
        print("you lose")
        exit()

    num_rows = len(board)
    num_cols = len(board[0])

    search_min_y = max(row - 1, 0)
    search_max_y = min(row + 1,  num_rows - 1)
    search_min_x = max(col - 1, 0)
    search_max_x = min(col + 1, num_cols - 1)

    num_mines = 0
    adjacent_unseen_cells = []
    for y, search_row in enumerate(board):
        if y < search_min_y or y > search_max_y:
            continue

        for x, search_cell in enumerate(search_row):
            if x < search_min_x or x > search_max_x:
                continue

            if search_cell == "*":
                num_mines += 1

            elif search_cell == "-":
                # A value other than "*" or "-" indicates the cell has been
                # revealed already. This prevents infinite recursion.
                adjacent_unseen_cells.append((y, x))

    board[row][col] = num_mines

    if num_mines == 0:
        for adjacent_cell in adjacent_unseen_cells:
            reveal(board, adjacent_cell[0], adjacent_cell[1], flood=True)


def is_win(board):
    for row in board:
        if "-" in row:
            return False

    return True


def print_board(board):
    for row in board:
        for cell in row:
            print(cell, end=" ")

        print("\n")


print_board(board)


while True:

    user_input = input("Enter coordinates (x, y): ")

    coords = user_input.split(',')
    if len(coords) != 2:
        print("Invalid input. Try again.")
        continue

    row = int(coords[0]) - 1
    col = int(coords[1]) - 1

    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
        print("Coordinate out of range. Please try again.")

    reveal(board, row, col)
    print_board(board)

    if is_win(board):
        print("you win")
        exit()
