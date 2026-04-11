import sys
import pygame
import numpy as np
pygame.init()
screen=pygame.display.set_mode((600, 600))
pygame.display.set_caption("OTHELLO")
board=np.full((8,8),' ')
board[3,3], board[3,4] = 'W', 'B' #o,x
board[4,3], board[4,4] = 'B', 'W'
player = 'B'
winner_display = ''
loading = 0
message_display = ''
message_timer = 0
empty=pygame.image.load("games/othelloempty.png")
empty=pygame.transform.scale(empty,(75,75))
white=pygame.image.load("games/othellowhite.png")
white=pygame.transform.scale(white,(75,75))
black=pygame.image.load("games/othelloblack.png")
black=pygame.transform.scale(black,(75,75))
loading_i=pygame.image.load("games/othelloloading.png")
loading_i=pygame.transform.scale(loading_i,(600,600))
clock = pygame.time.Clock()
time = np.random.randint(10,20)
def check_direction(board, r, c, dr, dc, player, found_opponent=False):
    r += dr
    c += dc
    if r < 0 or r >= 8 or c < 0 or c >= 8:
        return False
    if board[r, c] == ' ':
        return False
    opponent = 'W' if player == 'B' else 'B'
    if board[r,c] == opponent:
        return check_direction(board, r, c, dr, dc, player, True)
    if board[r, c] == player:
        return found_opponent
    return False
def flip_direction(board, r, c, dr, dc, player, cells=None):
    if cells is None:
        cells = []
    opponent = 'W' if player == 'B' else 'B'
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
    opponent = 'W' if player == 'B' else 'B'
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
    x = np.sum(board == 'B')
    o = np.sum(board == 'W')
    return x, o
def check_win(board,player):
    global winner_display
    next_player = 'W' if player == 'B' else 'B'
    if not has_valid_move(board,player) and not has_valid_move(board,next_player):
        x, o = count_score(board)
        if x == o :
            winner_display="It's Draw"
            return True
        elif x>o :
            winner_display="player B is winner"
            return True
        elif o>x :
            winner_display="player W is winner"
            return True
    elif not has_valid_move(board, player) and has_valid_move(board,next_player):
        return "skip"
while True:
    #game board display
    for i in range(0,600,75):
        for j in range(0,600,75):
            if board[i//75][j//75] == 'W':
                screen.blit(white,(i,j))
            elif board[i//75][j//75] == 'B':
                screen.blit(black,(i,j))
            else:
                screen.blit(empty,(i,j))
    result = check_win(board, player)
    if result == True:
        font = pygame.font.Font(None, 36)
        text = font.render(winner_display, True, (255, 0, 0))
        screen.blit(text, (200, 550))
    elif result == "skip":
        message_display = f"No valid moves for {player}, skipping turn."
        message_timer = 60
        player = 'W' if player == 'B' else 'B'
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            if message_timer > 0 or result == True:
                continue
            if board[x//75][y//75] != ' ':
                #display occupied cell
                message_display = "Cell Occupied!"
                message_timer = 60 
            elif not is_valid_move(board, x//75, y//75, player):
                #display invalid move
                    message_display = "Invalid Move!"
                    message_timer = 60
            else:
                apply_move(board, x//75, y//75, player)
                player = 'W' if player == 'B' else 'B'
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if message_display != "" and message_timer > 0:
        font = pygame.font.Font(None, 36)
        text = font.render(message_display, True, (255, 0, 0))
        screen.blit(text, (200, 550))
        message_timer -= 1
        if message_timer == 0:
            message_display = ""
    if loading <= 100:
        clock.tick(time)
        if loading % 3 == 0:
            screen.blit(loading_i,(0,0))
            font = pygame.font.Font(None, 36)
            text = font.render(f"Loading.   {loading}", True, (255, 255, 255))
            screen.blit(text, (200, 550))
            loading += 1
        elif loading % 3 == 1:
            screen.blit(loading_i,(0,0))
            font = pygame.font.Font(None, 36)
            text = font.render(f"Loading..  {loading}", True, (255, 255, 255))
            screen.blit(text, (200, 550))
            loading += 1
        elif loading % 3 == 2:
            screen.blit(loading_i,(0,0))
            font = pygame.font.Font(None, 36)
            text = font.render(f"Loading... {loading}", True, (255, 255, 255))
            screen.blit(text, (200, 550))
            loading += 1
    clock.tick(60)
    pygame.display.update()