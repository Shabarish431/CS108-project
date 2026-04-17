import pygame
import sys
import numpy as np
import os

base_path = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(base_path,"..")))

# pygame.init() #initializing the pygame
# screen=pygame.display.set_mode((800, 600)) #declaring the size of the screen
# #loading all the required images
# pygame.display.set_caption("TIC TAC TOE")
empty = pygame.image.load(os.path.join(base_path, "empty.png"))
print(os.path.join(base_path, "empty.png"))
empty = pygame.transform.scale(empty, (60, 60))
withx = pygame.image.load(os.path.join(base_path, "withX.png"))
withx = pygame.transform.scale(withx, (60, 60))
witho = pygame.image.load(os.path.join(base_path, "withO.png"))
witho = pygame.transform.scale(witho, (60, 60))
loadingpic = pygame.image.load(os.path.join(base_path, "tictactoev2.png"))
loadingpic = pygame.transform.scale(loadingpic, (600, 600))
#declaring the players
# username1 = sys.argv[1]
# username2 = sys.argv[2]
clock = pygame.time.Clock()
time = np.random.randint(15,20)

from game import Game
class TTT(Game):
    username1 = None
    username2 = None

    def __init__(self,player1,player2):
        super().__init__(player1,player2)
        self.board = np.full((10,10),' ') #declaring the gameboard
        # nonlocal username1


    def check_win(self,board,player):
        #splicing all horizontal 
        horizontal = (
            (board[:, :-4] == player) &
            (board[:, 1:-3] == player) &
            (board[:, 2:-2] == player) &
            (board[:, 3:-1] == player) &
            (board[:, 4:] == player)
        )
        #splicing all vertical
        vertical = (
            (board[:-4, :] == player) &
            (board[1:-3, :] == player) &
            (board[2:-2, :] == player) &
            (board[3:-1, :] == player) &
            (board[4:, :] == player)
        )
        #splicing all \
        diag1 = (
            (board[:-4, :-4] == player) &
            (board[1:-3, 1:-3] == player) &
            (board[2:-2, 2:-2] == player) &
            (board[3:-1, 3:-1] == player) &
            (board[4:, 4:] == player)
        )
        #splicing all /
        diag2 = (
            (board[4:, :-4] == player) &
            (board[3:-1, 1:-3] == player) &
            (board[2:-2, 2:-2] == player) &
            (board[1:-3, 3:-1] == player) &
            (board[:-4, 4:] == player)
        )
        #if there are any horizontal or vertical or / or \
        if np.any(horizontal):
            return True,("horizontal",np.argwhere(horizontal)[0])
        elif np.any(vertical):
            return True,("vertical",np.argwhere(vertical)[0])
        elif np.any(diag1):
            return True,("diag1",np.argwhere(diag1)[0])
        elif np.any(diag2):
            return True,("diag2",np.argwhere(diag2)[0])
        else:
            return False,None
    def load(self):
        global loading
        clock.tick(time)
        screen.blit(loadingpic,(0,0))
        font = pygame.font.Font(None, 50)
        dots = "." * (loading % 3 + 1)
        spaces = " " * (2 - loading % 3)
        loading_text = f"Loading{dots}{spaces} {loading}%"
        text = font.render(loading_text, True, (255, 255, 255))
        screen.blit(text, (200, 480))
        loading += 1
    def apply_move(self):
        for i in range(0,600,60):
            for j in range(0,600,60):
                img_map = {
                    ' ':empty,
                    'X':withx,
                    'O':witho
                }
                screen.blit(img_map[self.board[j//60][i//60]], (i, j))
    def play_game(self):
        player = 'X' #game is gonna start with X
        winner = ' ' #used to check if winner is declared, if declared then who is winner 
        global loading,screen
        self.screen = pygame.display.get_surface()
        screen = self.screen
        loading = 0 #used to set the loading page time
        count = 0 #used to check whether the board is full or any place is remained empty to declare whether its Draw or not 
        winner_count = 0 #used to print the winner onto the terminal for game.py to append the winner data in to history.csv
        message_display = ' ' #used if the occupied cell is selected
        message_timer = 0 #used to display the iamge for a second tentatively
        username1 = self.username1
        username2 = self.username2
        while True:
            screen.fill((7,71,80))
            if winner == ' ':
                self.render_user(610, 10, "Username Of", "Player X:", username1, (255,255,255))
                self.render_user(610, 101, "Username Of", "Player O:", username2, (255,255,255))
            #displaying the loading page
            if loading <= 100:
                self.load()
                for event in pygame.event.get():
                    #if they press e to exit and the game is declared as draw
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        return 3,username1,username2
            else:
                #screening the game page
                #displaying the game board
                self.apply_move()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y=pygame.mouse.get_pos()
                        if message_timer > 0:
                            continue
                        if self.board[y//60][x//60] == ' ' and winner == ' ':
                            self.board[y//60][x//60] = player
                            won, info = self.check_win(self.board, player)
                            count += 1
                            if won:
                                winner = player
                                win_type, (r,c) = info
                            player = self.switch_turn(player,'X','O')
                        elif self.board[y//60][x//60] != ' ' and winner == ' ':
                            message_display = "Cell Occupied!"
                            message_timer = 30
                    #pressing e to exit the game and declaring the result of the game
                    if event.type==pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                        if player == 'X' and winner == ' ':
                            winner = 'O'
                            overlay = pygame.Surface((800,600))
                            overlay.set_alpha(75)
                            overlay.fill((0,0,0))
                            screen.blit(overlay,(0,0))
                            font = pygame.font.Font(None, 200)
                            winner_display = "O Wins!"
                            text = font.render(winner_display, True, (255,255,255))
                            screen.blit(text, (50, 250))
                            self.render_user(610, 10, "Username Of", "Player X:", username1, (255,255,255))
                            self.render_user(610, 101,"username of", "player O:", username2, (255,255,255))
                            pygame.display.update()
                            clock.tick(1)
                            return 1,username2,username1
                        elif player == 'O' and winner == ' ':
                            winner = 'X'
                            overlay = pygame.Surface((800,600))
                            overlay.set_alpha(75)
                            overlay.fill((0,0,0))
                            screen.blit(overlay,(0,0))
                            font = pygame.font.Font(None, 200)
                            winner_display = "X wins!"
                            text = font.render(winner_display, True, (255,255,255))
                            screen.blit(text, (50, 250))
                            self.render_user(610, 10, "Username Of", "Player X:", username1, (255,255,255))
                            self.render_user(610, 101,"username of", "player O:", username2, (255,255,255))
                            pygame.display.update()
                            clock.tick(1)
                            return 1,username1,username2
                if winner != ' ' or count == 100:
                    self.render_user(610, 10, "Username Of", "Player X:", username1, (255,255,255))
                    self.render_user(610, 101, "Username Of", "Player O:", username2, (255,255,255))
                    if winner == 'O' or winner == 'X':
                        cell = 60
                        if win_type == "horizontal":
                            start = (c*cell+cell//2,r*cell+cell//2)
                            end = ((c+4)*cell+cell//2,r*cell+cell//2)
                        elif win_type == "vertical":
                            start = (c*cell+cell//2,r*cell+cell//2)
                            end = (c*cell+cell//2,(r+4)*cell+cell//2)
                        elif win_type == "diag1":
                            start = (c*cell+cell//2,r*cell+cell//2)
                            end = ((c+4)*cell+cell//2,(r+4)*cell+cell//2)
                        elif win_type == "diag2":
                            start = (c*cell+cell//2,(r+4)*cell+cell//2)
                            end = ((c+4)*cell+cell//2,r*cell+cell//2)
                        self.apply_move()
                        pygame.display.update()
                        pygame.draw.line(screen,(255,255,255),start,end,5)
                    pygame.display.update()
                    clock.tick(1)
                    small = pygame.transform.smoothscale(screen,(150,150))
                    blurred = pygame.transform.smoothscale(small,(800,600))
                    screen.blit(blurred,(0,0))
                    overlay = pygame.Surface((800,600))
                    overlay.set_alpha(75)
                    overlay.fill((0,0,0))
                    screen.blit(overlay,(0,0))
                    font = pygame.font.Font(None,200)
                    if winner == 'O' or winner == 'X':
                        text = font.render(f"{winner} Wins!",True,(255,255,255))
                    elif count == 100:
                        text = font.render(f"It's Draw",True,(255,255,255))
                    screen.blit(text,(50,250))
                    pygame.display.update()
                    clock.tick(0.5)
                    if winner == 'X':
                        return 1,username1,username2
                    elif winner == 'O':
                        return 1,username2,username1
                    elif count == 100:
                        return 2,username1,username2
                if message_display != " " and message_timer > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(message_display, True, (255, 0, 0))
                    screen.blit(text, (200, 550))
                    message_timer -= 1
                    if message_timer == 0:
                        message_display = " "
            #when the winner is declared the text to press e to exit is already printed but when the winner is not declared it is shown in the column containing usernames
            font=pygame.font.Font(None,36)
            if winner == ' ':
                press_e = "Press E to exit."
                press_e = font.render(press_e,True,(200,200,200))
                screen.blit(press_e,(610,192))
            clock.tick(60)
            pygame.display.update()
        
                    