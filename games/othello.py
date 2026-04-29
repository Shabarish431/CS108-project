#othello
import sys
import pygame
import numpy as np
import os
# pygame.init()
# screen=pygame.display.set_mode((800, 600))#settign the screen size
# pygame.display.set_caption("OTHELLO")
# username1 = sys.argv[1]#decalringm the players
# username2 = sys.argv[2]
winner_display = ' ' #to dispay at the end of the game
winner = ' ' #who is the winner
#declared all the images needed
base_path = os.path.dirname(__file__)
empty = pygame.image.load(os.path.join(base_path, "othelloempty.png"))
empty = pygame.transform.scale(empty, (75, 75))
white = pygame.image.load(os.path.join(base_path, "othellowhite.png"))
white = pygame.transform.scale(white, (75, 75))
black = pygame.image.load(os.path.join(base_path, "othelloblack.png"))
black = pygame.transform.scale(black, (75, 75))
loading_i = pygame.image.load(os.path.join(base_path, "othelloloading.png"))
loading_i = pygame.transform.scale(loading_i, (600, 600))
valid = pygame.image.load(os.path.join(base_path,"othellovalid.png"))
valid = pygame.transform.scale(valid, (75,75))
quit = pygame.image.load(os.path.join(base_path,"quit.png"))
quit = pygame.transform.scale(quit, (100, 50))
clock = pygame.time.Clock()
time = np.random.randint(15,20)
#this function is used to declare whether teh opponent is on that direction
sys.path.append(os.path.abspath(os.path.join(base_path,"..")))
from game import Game
def get_valid_moves(board, player):
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == ' ':
                found=False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr != 0 or dc != 0:
                            if check_direction(board, r, c, dr, dc, player):
                                moves.append((r, c))  # for user display
                                found=True
                                break
                    if found == True :
                        break
    return moves
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
#this function is used to declare which cells have to be flipped
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
#this function is declared to say whether the selected cell is valid or not
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
#this function is used to say whether teh player has valid moves or not 
def has_valid_move(board, player, r=0, c=0):
    if r == 8:
        return False
    if c == 8:
        return has_valid_move(board, player, r+1, 0)
    if is_valid_move(board, r, c, player):
        return True
    return has_valid_move(board, player, r, c+1)
#this function is used to store the no of B and W on the board
def count_score(board):
    x = np.sum(board == 'B')
    o = np.sum(board == 'W')
    return x, o
class OT(Game):
    def check_win(self,board,player):
        global winner_display,winner,username1,username2
        next_player = self.switch_turn(player,"W","B")
        if not has_valid_move(board,player) and not has_valid_move(board,next_player):
            x, o = count_score(board)
            if x == o :
                winner_display="It's Draw"
                winner = "Draw"
                return True
            elif x>o :
                winner_display=f"{username1} is winner"
                winner = "B"
                return True
            elif o>x :
                winner_display=f"{username2} is winner"
                winner = "W"
                return True
        elif not has_valid_move(board, player) and has_valid_move(board,next_player):
            return "skip"
    #this function is used to make the move if the selected cell is valid and flips the opponent cells
    def apply_move(self,board, r, c, player):
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
    def play_game(self):
        username1 = self.username1
        username2 = self.username2
        global loading,screen,winner_display  #used to set the time of the loading page
        self.screen = pygame.display.get_surface()
        screen = self.screen
        loading = 0
        board = self.board
        player = 'B' #game is gonna start with B
        message_display = ' ' #used to decalre the message to be delivered if needed
        message_timer = 0 #used to set the timer of the messager
        while True:
            screen.fill((15,79,34))
            #this is for loading page
            if loading <= 100:
                loading = self.load(screen,loading_i,200,550,loading)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT  and loading <=100 :
                        return 3,username1,username2
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y=pygame.mouse.get_pos()
                        if 650 <= x <= 750 and 450 <= y <= 500 and loading <=100:
                            return 3,username1,username2
            else:
                #game screen displayig 
                #game board display
                valid_moves = get_valid_moves(board,player)
                for i in valid_moves:
                    if board[i[0]][i[1]] == ' ':
                        board[i[0]][i[1]] = 'V'
                for i in range(0,600,75):
                    for j in range(0,600,75):
                        img_map = {
                            ' ':empty,
                            'W':white,
                            'B':black,
                            'V':valid
                        }
                        screen.blit(img_map[board[i//75][j//75]], (i, j))
                for i in valid_moves:
                    if board[i[0]][i[1]] == 'V':
                        board[i[0]][i[1]] = ' '
                result = self.check_win(board, player)
                if result == True :
                    self.render_user(610, 10, 100, 131, 220, username1, username2, (255,255,255), black, white, screen)
                    overlay = pygame.Surface((800,600))
                    overlay.set_alpha(75)
                    overlay.fill((0,0,0))
                    screen.blit(overlay,(0,0))
                    font = pygame.font.Font(None,50)
                    text = font.render(winner_display, True, (255, 0, 0))
                    screen.blit(text, (190, 500))
                    pygame.display.update()
                    clock.tick(1)
                    if winner == 'W':
                        return 1,username2,username1
                    if winner == 'B':
                        return 1,username1,username2
                    if winner == "Draw":
                        return 2,username1,username2
                elif result == "skip": #this is for skipping turn if the player does not have valid moves
                    message_display = f"No valid moves for {player}, skipping turn."
                    message_timer = 30
                    player = self.switch_turn(player,"W","B")
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y=pygame.mouse.get_pos()
                        if message_timer > 0 or result == True:
                            continue
                        if x <= 600 :
                            if board[x//75][y//75] != ' ':
                                #display occupied cell
                                message_display = "Cell Occupied!"
                                message_timer = 30
                            elif not is_valid_move(board, x//75, y//75, player):
                                #display invalid move
                                    message_display = "Invalid Move!"
                                    message_timer = 30
                            else:
                                self.apply_move(board, x//75, y//75, player)
                                player = self.switch_turn(player,"W","B")
                        elif 650 <= x <= 750 and 450 <= y <= 500:
                            if winner == ' ':
                                if player == 'B':
                                    overlay = pygame.Surface((800,600))
                                    overlay.set_alpha(75)
                                    overlay.fill((0,0,0))
                                    screen.blit(overlay,(0,0))
                                    font = pygame.font.Font(None,50)
                                    winner_display = f"{username2} is winner"
                                    text = font.render(winner_display, True, (255, 0, 0))
                                    screen.blit(text, (190, 500))
                                    pygame.display.update()
                                    clock.tick(1)
                                    return 1,username2,username1
                                if player == 'W':
                                    overlay = pygame.Surface((800,600))
                                    overlay.set_alpha(75)
                                    overlay.fill((0,0,0))
                                    screen.blit(overlay,(0,0))
                                    font = pygame.font.Font(None,50)
                                    winner_display = f"{username1} is winner"
                                    text = font.render(winner_display, True, (255, 0, 0))
                                    screen.blit(text, (190, 500))
                                    pygame.display.update()
                                    clock.tick(1)
                                    return 1,username1,username2
                    if event.type == pygame.QUIT: #to decalre the opponent as winner if teh current player exits before game is completed
                        if winner == ' ':
                            if player == 'B':
                                overlay = pygame.Surface((800,600))
                                overlay.set_alpha(75)
                                overlay.fill((0,0,0))
                                screen.blit(overlay,(0,0))
                                font = pygame.font.Font(None,50)
                                winner_display = f"{username2} is winner"
                                text = font.render(winner_display, True, (255, 0, 0))
                                screen.blit(text, (190, 500))
                                pygame.display.update()
                                clock.tick(1)
                                return 1,username2,username1
                            if player == 'W':
                                overlay = pygame.Surface((800,600))
                                overlay.set_alpha(75)
                                overlay.fill((0,0,0))
                                screen.blit(overlay,(0,0))
                                font = pygame.font.Font(None,50)
                                winner_display = f"{username1} is winner"
                                text = font.render(winner_display, True, (255, 0, 0))
                                screen.blit(text, (190, 500))
                                pygame.display.update()
                                clock.tick(1)
                                return 1,username1,username2
                if message_display != " " and message_timer > 0: #used to display the message if the selected cell is invalid or occupied
                    font = pygame.font.Font(None,50)
                    text = font.render(message_display, True, (255, 0, 0))
                    if message_display == "Cell Occupied!" or message_display == "Invalid Move!":
                        screen.blit(text, (200, 550))
                    else:
                        screen.blit(text,(100, 550))
                    message_timer -= 1
                    if message_timer == 0:
                        message_display = " "
            #displaying the usernames of the players
            self.render_user(610, 10, 100, 131, 220, username1, username2, (255,255,255), black, white, screen)
            #when the winner is declared the text to press e to exit is already printed but when the winner is not declared it is shown in the column containing usernames
            if winner == ' ' :
                screen.blit(quit,(650,450))
                if loading > 100:    
                    font = pygame.font.Font(None,28)
                    show_valid = ["The cells which","are in brighter green","are valid moves of","current player"]
                    for i in range(4):
                        show_valid[i] = font.render(show_valid[i],True,(200,200,200))
                        screen.blit(show_valid[i],(605,245+(i*25)))
            clock.tick(60)
            pygame.display.update()

    def __init__(self,player1,player2):
        super().__init__(player1,player2)
        self.board=np.full((8,8),' ')#initializing the board game
        self.board[3,3], self.board[3,4] = 'W', 'B'#initial set up of the game board
        self.board[4,3], self.board[4,4] = 'B', 'W'