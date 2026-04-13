import pygame
import sys
import numpy as np
#declaring the players
username1 = sys.argv[1]
username2 = sys.argv[2]
player = 'Y' #game is gonna start with Yellow color
winner = ' ' #used to check if winner is declared, if declared then who is winner 
loading_time = 0 #used to set the loading page time
pygame.init() #initializing the pygame
screen = pygame.display.set_mode((700, 700)) #declaring the size of the screen
pygame.display.set_caption("CONNECT4") 
board = np.full((7, 7), ' ') #declaring the gameboard
#loading all the required images
empty = pygame.transform.scale(pygame.image.load("games/conempty.png"), (100, 100))
yellow = pygame.transform.scale(pygame.image.load("games/conyellow.png"), (100, 100))
red = pygame.transform.scale(pygame.image.load("games/conred.png"), (100, 100))
loading = pygame.transform.scale(pygame.image.load("games/connect4_loading.jpg"),(700,700))
clock = pygame.time.Clock()
time = np.random.randint(15,20)
def check_win(board, player):
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
count = 0 #to print username onto terminal to let game.py know which player is the winner
board_count = 0 #to count how many cells are occupied
while True:
    #display loading page
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
                print("It's Draw")
                pygame.quit()
                sys.exit()                
    else:
        #display the game page 
        #display the gameboard
        for i in range(0, 700, 100):
            for j in range(0, 700, 100):
                if board[j//100][i//100] == ' ':
                    screen.blit(empty, (i, j))
                if board[j//100][i//100] == 'Y':
                    screen.blit(yellow, (i, j))
                if board[j//100][i//100] == 'R':
                    screen.blit(red, (i, j))
        if winner == 'Y' or winner == 'R':
            #drawing a line if the winner is declared 
            cell = 100
            draw_r = 6 - r
            if win_type == "horizontal":
                start = (c*cell + cell//2, draw_r*cell + cell//2)
                end = ((c+3)*cell + cell//2, draw_r*cell + cell//2)
            elif win_type == "vertical":
                start = (c*cell + cell//2, draw_r*cell + cell//2)
                end = (c*cell + cell//2, (draw_r-3)*cell + cell//2)
            elif win_type == "diag1":
                start = (c*cell + cell//2, draw_r*cell + cell//2)
                end = ((c+3)*cell + cell//2, (draw_r+3)*cell + cell//2)
            elif win_type == "diag2":
                start = (c*cell + cell//2, draw_r*cell + cell//2)
                end = ((c+3)*cell + cell//2, (draw_r-3)*cell + cell//2)
            color = (255,242,0) if winner == 'Y' else (136,0,21)
            pygame.draw.line(screen, color, start, end, 20)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #selecting the cell
                x, y = pygame.mouse.get_pos()
                col = min(x//100, 6)
                for i in range(6, -1, -1):
                    if board[i][col] == ' ' and winner == ' ':
                        board[i][col] = player
                        won, info = check_win(board, player)
                        if won:
                            winner = player
                            win_type, (r, c) = info
                        player = 'Y' if player == 'R' else 'R'
                        board_count += 1
                        break
            #to decalre the opponent as winner if teh current player exits before game is completed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if player == 'Y' and winner == ' ':
                        winner = 'R'
                        print(username2)
                    elif player == 'R' and winner == ' ':
                        winner = 'Y'
                        print(username1)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                if player == 'Y' and winner == ' ':
                    winner = 'R'
                    print(username2)
                elif player == 'R' and winner == ' ':
                    winner = 'Y'
                    print(username1)
                pygame.quit()
                sys.exit()
        if winner != ' ' or board_count == 49:
            if count == 0:
                #to print the winner username on terminal
                if winner == 'Y':
                    print(username1)
                elif winner == 'R':
                    print(username2)
                elif board_count == 49:
                    print("It's Draw")
                count += 1
                #blurring and dimming the image
            small = pygame.transform.smoothscale(screen, (150, 150))
            blurred = pygame.transform.smoothscale(small, (700, 700))
            screen.blit(blurred, (0, 0))
            overlay = pygame.Surface((700, 700))
            overlay.set_alpha(75)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            font = pygame.font.Font(None, 200)
            #displaying the winner text
            if winner == 'R' or winner == 'Y':
                winner_text = f"{winner} Wins!"
            elif board_count == 49:
                winner_text = "It's Draw"
            text = font.render(winner_text, True, (255, 255, 255))
            screen.blit(text, (50, 250))
            font = pygame.font.Font(None, 80)
            text2 = font.render("Press E to Exit", True, (200, 200, 200))
            screen.blit(text2, (100, 420))
    clock.tick(60)
    pygame.display.update()