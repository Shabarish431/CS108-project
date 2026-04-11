import pygame
import sys
import numpy as np
player = 'Y'
winner = ''
loading_time = 0
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("CONNECT4")
board = np.full((7, 7), ' ')
empty = pygame.transform.scale(pygame.image.load("games/conempty.png"), (100, 100))
yellow = pygame.transform.scale(pygame.image.load("games/conyellow.png"), (100, 100))
red = pygame.transform.scale(pygame.image.load("games/conred.png"), (100, 100))
loading = pygame.transform.scale(pygame.image.load("games/connect4_loading.jpg"),(700,700))
clock = pygame.time.Clock()
time = np.random.randint(10,20)
def check_win(board, player):
    horizontal = (
        (board[:, :-3] == player) &
        (board[:, 1:-2] == player) &
        (board[:, 2:-1] == player) &
        (board[:, 3:] == player)
    )
    vertical = (
        (board[:-3, :] == player) &
        (board[1:-2, :] == player) &
        (board[2:-1, :] == player) &
        (board[3:, :] == player)
    )
    diag1 = (
        (board[:-3, :-3] == player) &
        (board[1:-2, 1:-2] == player) &
        (board[2:-1, 2:-1] == player) &
        (board[3:, 3:] == player)
    )
    diag2 = (
        (board[3:, :-3] == player) &
        (board[2:-1, 1:-2] == player) &
        (board[1:-2, 2:-1] == player) &
        (board[:-3, 3:] == player)
    )
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
count = 0
while True:
    if loading_time <= 100:
        clock.tick(time)
        screen.blit(loading,(0,0))
        font = pygame.font.Font(None, 50)
        if loading_time%3 == 0:
            loading_text = f"Loading.   {loading_time}%"
        elif loading_time%3 == 1:
            loading_text = f"Loading..  {loading_time}%"
        else:
            loading_text = f"Loading... {loading_time}%"
        text = font.render(loading_text, True, (0, 0, 0))
        screen.blit(text, (250, 550))
        loading_time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                pygame.quit()
                sys.exit()                
    else:
        for i in range(0, 700, 100):
            for j in range(0, 700, 100):
                if board[j//100][i//100] == ' ':
                    screen.blit(empty, (i, j))
                if board[j//100][i//100] == 'Y':
                    screen.blit(yellow, (i, j))
                if board[j//100][i//100] == 'R':
                    screen.blit(red, (i, j))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i in range(6, -1, -1):
                    if board[i][x//100] == ' ' and winner != ' ':
                        board[i][x//100] = player
                        won, info = check_win(board, player)
                        if won:
                            winner = player
                            win_type, (r, c) = info
                        player = 'Y' if player == 'R' else 'R'
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()
                    if player == 'Y' and winner == ' ':
                        winner = 'R'
                    elif player == 'R' and winner == ' ':
                        winner = 'Y'
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if winner != '':
            if count == 0:
                print(winner)
                count += 1
            cell = 100
            if win_type == "horizontal":
                start = (c*cell + cell//2, r*cell + cell//2)
                end = ((c+3)*cell + cell//2, r*cell + cell//2)
            elif win_type == "vertical":
                start = (c*cell + cell//2, r*cell + cell//2)
                end = (c*cell + cell//2, (r+3)*cell + cell//2)
            elif win_type == "diag1":
                start = (c*cell + cell//2, r*cell + cell//2)
                end = ((c+3)*cell + cell//2, (r+3)*cell + cell//2)
            elif win_type == "diag2":
                start = (c*cell + cell//2, (r+3)*cell + cell//2)
                end = ((c+3)*cell + cell//2, r*cell + cell//2)
            if winner == 'R':
                pygame.draw.line(screen, (136, 0, 21), start, end, 20)
            if winner == 'Y':
                pygame.draw.line(screen, (255, 242, 0), start, end, 20)
            small = pygame.transform.smoothscale(screen, (150, 150))
            blurred = pygame.transform.smoothscale(small, (700, 700))
            screen.blit(blurred, (0, 0))
            overlay = pygame.Surface((700, 700))
            overlay.set_alpha(75)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            font = pygame.font.Font(None, 200)
            winner_text = f"{winner} Wins!"
            text = font.render(winner_text, True, (255, 255, 255))
            winner_display = screen.blit(text, (50, 250))
            font = pygame.font.Font(None, 80)
            press_e_text = "Press E to Exit"
            text2 = font.render(press_e_text, True, (200, 200, 200))
            screen.blit(text2, (100, 420))
    clock.tick(60)
    pygame.display.update()