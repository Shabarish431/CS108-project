import numpy as np
board = np.full((10, 10), ' ')
def print_board(board, row=0):
    if row == 10:
        print("   1   2   3   4   5   6   7   8   9   10")
        return
    print(f"{row+1:2} " + " | ".join(board[row]))
    print_board(board, row + 1)
def place_move(board, row, col, player):
    if board[row, col] != ' ':
        return False
    board[row, col] = player
    return True
def check_win(board, player):
    horizontal = np.any(
        (board[:, :-4] == player) &
        (board[:, 1:-3] == player) &
        (board[:, 2:-2] == player) &
        (board[:, 3:-1] == player) &
        (board[:, 4:] == player)
    )
    vertical = np.any(
        (board[:-4, :] == player) &
        (board[1:-3, :] == player) &
        (board[2:-2, :] == player) &
        (board[3:-1, :] == player) &
        (board[4:, :] == player)
    )
    diag1 = np.any(
        (board[:-4, :-4] == player) &
        (board[1:-3, 1:-3] == player) &
        (board[2:-2, 2:-2] == player) &
        (board[3:-1, 3:-1] == player) &
        (board[4:, 4:] == player)
    )
    diag2 = np.any(
        (board[4:, :-4] == player) &
        (board[3:-1, 1:-3] == player) &
        (board[2:-2, 2:-2] == player) &
        (board[1:-3, 3:-1] == player) &
        (board[:-4, 4:] == player)
    )
    return horizontal or vertical or diag1 or diag2
def check_draw(board):
    return not np.any(board == ' ')
def play_game(board, player):
    print_board(board)
    try:
        row = input(f"Player {player}, enter row (1-10): ")
        if row == "Exit" :
            return
        col = input(f"Player {player}, enter col (1-10): ")
        if col == "Exit":
            return
        row = int(row) - 1
        col = int(col) - 1
    except:
        print("Invalid input!")
        return play_game(board, player)
    if row < 0 or row > 9 or col < 0 or col > 9 or not place_move(board, row, col, player):
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