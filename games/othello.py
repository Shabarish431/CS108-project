import numpy as np
board = np.full((8, 8), ' ')
board[3,3], board[3,4] = 'O', 'X'
board[4,3], board[4,4] = 'X', 'O'
def print_board(board, row=0):
    if row == 8:
        print("   1   2   3   4   5   6   7   8")
        return
    print(f"{row+1:2} " + " | ".join(board[row]))
    print_board(board, row + 1)
def check_direction(board, r, c, dr, dc, player, found_opponent=False):
    r += dr
    c += dc
    if r < 0 or r >= 8 or c < 0 or c >= 8:
        return False
    if board[r, c] == ' ':
        return False
    opponent = 'O' if player == 'X' else 'X'
    if board[r,c] == opponent:
        return check_direction(board, r, c, dr, dc, player, True)
    if board[r, c] == player:
        return found_opponent
    return False
def flip_direction(board, r, c, dr, dc, player, cells=None):
    if cells is None:
        cells = []
    opponent = 'O' if player == 'X' else 'X'
    r += dr
    c += dc
    if r < 0 or r >= 8 or c < 0 or c >= 8:
        return
    if board[r][c] == ' ':
        return
    if board[r][c] == opponent:
        cells.append((r, c))
        flip_direction(board, r, c, dr, dc, player, cells)
        return
    if board[r][c] == player:
        for rr, cc in cells:
            board[rr][cc] = player
        return
def is_valid_move(board, r, c, player):
    if board[r, c] != ' ':
        return False
    opponent = 'O' if player == 'X' else 'X'
    return (
        check_direction(board, r, c, -1, 0, player) or
        check_direction(board, r, c, 1, 0, player) or
        check_direction(board, r, c, 0, -1, player) or
        check_direction(board, r, c, 0, 1, player) or
        check_direction(board, r, c, -1, -1, player) or
        check_direction(board, r, c, -1, 1, player) or
        check_direction(board, r, c, 1, -1, player) or
        check_direction(board, r, c, 1, 1, player)
    )
def apply_move(board, r, c, player):
    directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    def apply_dir(i=0):
        if i == len(directions):
            return
        dr, dc = directions[i]
        # CHECK before placing
        if check_direction(board, r, c, dr, dc, player):
            flip_direction(board, r, c, dr, dc, player)
        apply_dir(i + 1)
    apply_dir()
    board[r, c] = player
def has_valid_move(board, player, r=0, c=0):
    if r == 8:
        return False
    if c == 8:
        return has_valid_move(board, player, r+1, 0)
    if is_valid_move(board, r, c, player):
        return True
    return has_valid_move(board, player, r, c+1)
def count_score(board):
    x = np.sum(board == 'X')
    o = np.sum(board == 'O')
    return x, o
def check_win(board,player):
    next_player = 'O' if player == 'X' else 'X'
    if not has_valid_move(board,player) and not has_valid_move(board,next_player):
        print(f"Game Over!")
        x, o = count_score(board)
        if x == o :
            print(f"It's Draw")
            return True
        elif x>o :
            print(f"player X is winner")
            return True
        elif o>x :
            print(f"player O is winner")
            return True
    elif not has_valid_move(board, player) and has_valid_move(board,next_player):
        print(f"No valid moves for {player}, skipping turn.")
        return "skip"
def play_game(board, player):
    print_board(board)
    result=check_win(board,player)
    if result == True:
        return
    if result == "skip":
        next_player = 'O' if player == 'X' else 'X'
        return play_game(board,player)
    try:
        r = input(f"{player} row (1-8): ")
        if r == 'Exit':
            return
        c = input(f"{player} col (1-8): ")
        if c == 'Exit':
            return
        r = int(r) - 1
        c = int(c) - 1
    except:
        print("Invalid input!")
        return play_game(board, player)
    if r < 0 or r > 7 or c < 0 or c > 7 or not is_valid_move(board, r, c, player):
        print("Invalid move!")
        return play_game(board, player)
    apply_move(board, r, c, player)
    next_player = 'O' if player == 'X' else 'X'
    play_game(board, next_player)
play_game(board, 'X')