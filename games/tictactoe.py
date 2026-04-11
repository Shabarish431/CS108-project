import pygame
import sys
import numpy as np
pygame.init()
screen=pygame.display.set_mode((600, 600))
pygame.display.set_caption("TIC TAC TOE")
empty=pygame.image.load("games/empty.png")
empty=pygame.transform.scale(empty,(60,60))
withx=pygame.image.load("games/withX.png")
withx=pygame.transform.scale(withx,(60,60))
withy=pygame.image.load("games/withO.png")
withy=pygame.transform.scale(withy,(60,60))
board=np.full((10,10),' ')
player = 'X'
winner = ''
loading=0
count = 0 
loadingpic=pygame.image.load("games/tictactoev2.png")
clock = pygame.time.Clock()
time = np.random.randint(10,20)
while True:
    #check win condition
    def check_win(board, player):
        horizontal = (
            (board[:, :-4] == player) &
            (board[:, 1:-3] == player) &
            (board[:, 2:-2] == player) &
            (board[:, 3:-1] == player) &
            (board[:, 4:] == player)
        )
        vertical = (
            (board[:-4, :] == player) &
            (board[1:-3, :] == player) &
            (board[2:-2, :] == player) &
            (board[3:-1, :] == player) &
            (board[4:, :] == player)
        )
        diag1 = (
            (board[:-4, :-4] == player) &
            (board[1:-3, 1:-3] == player) &
            (board[2:-2, 2:-2] == player) &
            (board[3:-1, 3:-1] == player) &
            (board[4:, 4:] == player)
        )
        diag2 = (
            (board[4:, :-4] == player) &
            (board[3:-1, 1:-3] == player) &
            (board[2:-2, 2:-2] == player) &
            (board[1:-3, 3:-1] == player) &
            (board[:-4, 4:] == player)
        )
        if np.any(horizontal):
            pos = np.argwhere(horizontal)[0]
            return True,("horizontal",pos)
        elif np.any(vertical):
            pos = np.argwhere(vertical)[0]
            return True,("vertical",pos)
        elif np.any(diag1):
            pos = np.argwhere(diag1)[0]
            return True,("diag1",pos)
        elif np.any(diag2):
            pos = np.argwhere(diag2)[0]
            return True,("diag2",pos)
        else:
            return False, None
    #game board display
    for i in range(0,600,60):
        for j in range(0,600,60):
            if board[i//60][j//60] == 'X':
                screen.blit(withx,(i,j))
            elif board[i//60][j//60] == 'O':
                screen.blit(withy,(i,j))
            else:
                screen.blit(empty,(i,j))
    #selecting the cell and substituting the value to that cell
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board=np.full((10,10),' ')
                player = 'X'
                winner = ''
            elif event.key == pygame.K_e:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            if player == 'X' and board[x//60][y//60] == ' ' and winner == '':
                board[x//60][y//60] = 'X'
                won, info = check_win(board, player)
                count += 1
                if won:
                    winner = player
                    win_type, (r,c) = info
                player = 'O'
            elif player == 'O' and board[x//60][y//60] == ' ' and winner == '':
                board[x//60][y//60] = 'O'
                won, info = check_win(board, player)
                count += 1
                if won:
                    winner = player
                    win_type, (r,c) = info
                player = 'X'
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if loading <= 100:
        clock.tick(time)
        if loading%3 == 0:
            screen.blit(loadingpic,(0,0))
            font = pygame.font.Font(None, 50)
            loading_text = f"Loading.   {loading}%"
            text = font.render(loading_text, True, (255, 255, 255))
            screen.blit(text, (200, 480))
        elif loading%3 == 1:
            screen.blit(loadingpic,(0,0))
            font = pygame.font.Font(None, 50)
            loading_text = f"Loading..  {loading}%"
            text = font.render(loading_text, True, (255, 255, 255))
            screen.blit(text, (200, 480))
        elif loading%3 == 2:
            screen.blit(loadingpic,(0,0))
            font = pygame.font.Font(None, 50)
            loading_text = f"Loading... {loading}%"
            text = font.render(loading_text, True, (255, 255, 255))
            screen.blit(text, (200, 480))
    if loading <= 100:
        loading += 1
    if winner != '' or count == 100:
        cell = 60
        if win_type == "horizontal":
            start = (r*cell+cell//2,c*cell)
            end = (r*cell+cell//2,(c+5)*cell)
        elif win_type == "vertical":
            start = (r*cell,c*cell+cell//2)
            end = ((r+5)*cell,c*cell+cell//2)
        elif win_type == "diag1":
            start = (r*cell,c*cell)
            end = ((r+5)*cell,(c+5)*cell)
        elif win_type == "diag2":
            start = ((r+5)*cell,c*cell)
            end = (r*cell,(c+5)*cell)
        pygame.draw.line(screen, (255, 255, 255), start, end, 5)
        small = pygame.transform.smoothscale(screen, (150, 150))
        blurred = pygame.transform.smoothscale(small, (600, 600))
        screen.blit(blurred, (0, 0))
        overlay = pygame.Surface((600, 600))
        overlay.set_alpha(75)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        font = pygame.font.Font(None, 200)
        winner_text = f"{winner} Wins!"
        text = font.render(winner_text, True, (255, 255, 255))
        winner_display=screen.blit(text, (50, 250))
        font = pygame.font.Font(None, 80)
        press_r_text = "Press R to Restart"
        text1 = font.render(press_r_text, True, (200, 200, 200))
        press_e_text = "Press E to Exit"
        text2 = font.render(press_e_text, True, (200, 200, 200))
        screen.blit(text1, (50, 370))
        screen.blit(text2, (100, 420))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board=np.full((10,10),' ')
                    player = 'X'
                    winner = ''
                elif event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()
    pygame.display.update()