import numpy as np
board = np.full((7, 7), ' ')
def drop_piece(board, col, player):
    column = board[:, col]
    empty = np.where(column == ' ')[0]
    if len(empty) == 0:
        return False
    row = empty[-1]
    board[row, col] = player
    return True
def print_board(board):
    print("\n")
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("  1   2   3   4   5   6   7 ")
def check_win(board, player):
    horizontal = np.any(
        (board[:, :-3] == player) &
        (board[:, 1:-2] == player) &
        (board[:, 2:-1] == player) &
        (board[:, 3:] == player)
    )
    vertical = np.any(
        (board[:-3, :] == player) &
        (board[1:-2, :] == player) &
        (board[2:-1, :] == player) &
        (board[3:, :] == player)
    )
    diag1 = np.any(
        (board[:-3, :-3] == player) &
        (board[1:-2, 1:-2] == player) &
        (board[2:-1, 2:-1] == player) &
        (board[3:, 3:] == player)
    )
    diag2 = np.any(
        (board[3:, :-3] == player) &
        (board[2:-1, 1:-2] == player) &
        (board[1:-2, 2:-1] == player) &
        (board[:-3, 3:] == player)
    )
    return horizontal or vertical or diag1 or diag2
def check_draw(board):
    return not np.any(board == ' ')
def play_game(board, player):
    print_board(board)
    col = input(f"Player {player}, choose column (0-6): ")
    if col == "Exit":
        return
    col = int(col) - 1
    if col < 0 or col > 6 or not drop_piece(board, col, player):
        print("Invalid move! Try again.")
        return play_game(board, player)
    if check_win(board, player):
        print_board(board)
        print(f"🎉 Player {player} wins!")
        return
    if check_draw(board):
        print_board(board)
        print("It's a draw!")
        return
    next_player = 'O' if player == 'X' else 'X'
    play_game(board, next_player)
play_game(board, 'X')