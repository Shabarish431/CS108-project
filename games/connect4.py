#connect4
import pygame
import sys
import numpy as np
import os
#loading all the required images
base_path = os.path.dirname(__file__)
empty = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "conempty.png")), (100, 100))
yellow = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "conyellow.png")), (100, 100))
red = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "conred.png")), (100, 100))
quit = pygame.transform.smoothscale(pygame.image.load(os.path.join(base_path, "quit.png")), (100,50))
loadingpic = pygame.transform.smoothscale(pygame.image.load(os.path.join(base_path, "connect4_loading.jpg")), (700, 700))
sys.path.append(os.path.abspath(os.path.join(base_path,"..")))
from game import Game
clock = pygame.time.Clock()
time = np.random.randint(15,20)
class CO(Game):
    def check_win(self,board, player):
        #splicing all horizontal 
        horizontal = (
            (board[:, :-3] == player) &
            (board[:, 1:-2] == player) &
            (board[:, 2:-1] == player) &
            (board[:, 3:] == player)
        )
        #splicing all vertical
        vertical = (
            (board[:-3, :] == player) &
            (board[1:-2, :] == player) &
            (board[2:-1, :] == player) &
            (board[3:, :] == player)
        )
        #splicing all \
        diag1 = (
            (board[:-3, :-3] == player) &
            (board[1:-2, 1:-2] == player) &
            (board[2:-1, 2:-1] == player) &
            (board[3:, 3:] == player)
        )
        #splicing all /
        diag2 = (
            (board[3:, :-3] == player) &
            (board[2:-1, 1:-2] == player) &
            (board[1:-2, 2:-1] == player) &
            (board[:-3, 3:] == player)
        )
        #if there are any horizontal or vertical or / or \
        if np.any(horizontal):
            pos = np.argwhere(horizontal)[0]
            return True, ("horizontal", pos)
        elif np.any(vertical):
            pos = np.argwhere(vertical)[0]
            return True, ("vertical", pos)
        elif np.any(diag1):
            pos = np.argwhere(diag1)[0]
            return True, ("diag1", pos)
        elif np.any(diag2):
            pos = np.argwhere(diag2)[0]
            return True, ("diag2", pos)
        else:
            return False, None
    def apply_move(self):
        #display the gameboard
        for i in range(0, 700, 100):
            for j in range(0, 700, 100):
                img_map = {
                    ' ':empty,
                    'Y':yellow,
                    'R':red
                }
                screen.blit(img_map[board[j//100][i//100]], (i, j))
    def play_game(self):
        board_count = 0 #to count how many cells are occupied
        global loading,username1,username2,screen,board,winner
        board = self.board
        username1=self.username1
        username2=self.username2
        player = 'Y' #game is gonna start with Yellow color
        winner = ' ' #used to check if winner is declared, if declared then who is winner
        loading = 0
        self.screen = pygame.display.set_mode((900,700))
        screen = self.screen
        while True:
            screen.fill((255,255,255)) #background color
            #display loading page
            if loading <= 100:
                loading = self.load(screen,loadingpic,330,530,loading)
                for event in pygame.event.get(): # if quit button on loading screen is selected
                    if event.type == pygame.QUIT :
                        return 3,username1,username2
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 750 <= x <= 850 and 550 <= y <= 600:
                            return 3,username1,username2
            else:
                screen.fill('Blue')
                #display the game page 
                self.apply_move()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #selecting the cell
                        x, y = pygame.mouse.get_pos()
                        if x <= 700:
                            col = min(x//100, 6)
                            for i in range(6, -1, -1):
                                if board[i][col] == ' ' and winner == ' ':
                                    board[i][col] = player
                                    won, info = self.check_win(board, player)
                                    if won:
                                        winner = player
                                        win_type, (r, c) = info
                                    player = self.switch_turn(player,"Y","R")
                                    board_count += 1
                                    break
                    #to decalre the opponent as winner if teh current player exits before game is completed
                    if event.type == pygame.QUIT:
                        if player == 'Y' and winner == ' ':
                            winner = 'R'
                            overlay = pygame.Surface((900,700))
                            overlay.set_alpha(75)
                            overlay.fill((0,0,0))
                            screen.blit(overlay,(0,0))
                            font = pygame.font.Font(None, 50)
                            winner_display = f"{username2} Wins!"
                            text = font.render(winner_display, True, ((255,0,0)))
                            screen.blit(text, (190, 500))
                            self.render_user(710, 30, 130, 171, 280, username1, username2, (0,0,0), red, yellow, screen)
                            pygame.display.update()
                            clock.tick(1)
                            return 1,username2,username1
                        elif player == 'R' and winner == ' ':
                            winner = 'Y'
                            overlay = pygame.Surface((900,700))
                            overlay.set_alpha(75)
                            overlay.fill((0,0,0))
                            screen.blit(overlay,(0,0))
                            font = pygame.font.Font(None, 50)
                            winner_display = f"{username1} Wins!"
                            text = font.render(winner_display, True, ((255,0,0)))
                            screen.blit(text, (190, 500))
                            pygame.display.update()
                            clock.tick(1)
                            return 1,username1,username2
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 750 <= x <= 850 and 550 <= y <= 600:
                            if player == 'Y' and winner == ' ':
                                winner = 'R'
                                overlay = pygame.Surface((900,700))
                                overlay.set_alpha(75)
                                overlay.fill((0,0,0))
                                screen.blit(overlay,(0,0))
                                font = pygame.font.Font(None, 50)
                                winner_display = f"{username2} Wins!"
                                text = font.render(winner_display, True, ((255,0,0)))
                                screen.blit(text, (190, 500))
                                self.render_user(710, 30, 130, 171, 280, username1, username2, (0,0,0), red, yellow, screen)
                                pygame.display.update()
                                clock.tick(1)
                                return 1,username2,username1
                            elif player == 'R' and winner == ' ':
                                winner = 'Y'
                                overlay = pygame.Surface((900,700))
                                overlay.set_alpha(75)
                                overlay.fill((0,0,0))
                                screen.blit(overlay,(0,0))
                                font = pygame.font.Font(None, 50)
                                winner_display = f"{username1} Wins!"
                                text = font.render(winner_display, True, ((255,0,0)))
                                screen.blit(text, (190, 500))
                                self.render_user(710, 30, 130, 171, 280, username1, username2, (0,0,0), red, yellow, screen)
                                pygame.display.update()
                                clock.tick(1)
                                return 1,username1,username2
                if winner == 'Y' or winner == 'R':
                    #drawing a line if the winner is declared 
                    self.apply_move()
                    cell = 100
                    if win_type == "horizontal":
                        start = (c*cell+cell//2,r*cell+cell//2)
                        end = ((c+3)*cell+cell//2,r*cell+cell//2)
                    elif win_type == "vertical":
                        start = (c*cell+cell//2,r*cell+cell//2)
                        end = (c*cell+cell//2,(r+3)*cell+cell//2)
                    elif win_type == "diag1":
                        start = (c*cell+cell//2,r*cell+cell//2)
                        end = ((c+3)*cell+cell//2,(r+3)*cell+cell//2)
                    elif win_type == "diag2":
                        start = (c*cell+cell//2,(r+3)*cell+cell//2)
                        end = ((c+3)*cell+cell//2,r*cell+cell//2)
                    color = (255,242,0) if winner == 'Y' else (136,0,21)
                    pygame.draw.line(screen, color, start, end, 20)
                    pygame.display.update()
                    clock.tick(1)
                if winner != ' ' or board_count == 49:
                    #blurring and dimming the image
                    small = pygame.transform.smoothscale(screen, (150, 150))
                    blurred = pygame.transform.smoothscale(small, (900, 700))
                    screen.blit(blurred, (0, 0))
                    overlay = pygame.Surface((900, 700))
                    overlay.set_alpha(75)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))
                    font = pygame.font.Font(None, 50)
                    #displaying the winner text
                    if winner == 'R' or winner == 'Y':
                        winner_text = f"{username1} Wins!" if winner == 'Y' else f"{username2} Wins!"
                    elif board_count == 49:
                        winner_text = "It's Draw"
                    text = font.render(winner_text, True, (255, 255, 255))
                    screen.blit(text, (190, 500))
                    self.render_user(710, 30, 130, 171, 280, username1, username2, (0,0,0), red, yellow, screen)
                    pygame.display.update()
                    clock.tick(1)
                    #to print the winner username on terminal
                    if winner == 'Y':
                        return 1,username1,username2
                    elif winner == 'R':
                        return 1,username2,username1
                    elif board_count == 49:
                        return 2,username1,username2
            #displaying the usernames of the players
            self.render_user(710, 30, 130, 171, 280, username1, username2, (0,0,0), red, yellow, screen)
            #when the winner is declared the text to pressing quit button to exit is already printed but when the winner is not declared it is shown in the column containing usernames
            if winner == ' ':
                screen.blit(quit,(750,550))
            clock.tick(60)
            pygame.display.update()
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.board = np.full((7, 7), ' ') #declaring the gameboard