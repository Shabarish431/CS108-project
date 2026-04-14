import pygame
import sys
import numpy as np
import os
pygame.init() #initializing the pygame
screen=pygame.display.set_mode((800, 600)) #declaring the size of the screen
#loading all the required images
pygame.display.set_caption("TIC TAC TOE")
base_path = os.path.dirname(__file__)
empty = pygame.image.load(os.path.join(base_path, "empty.png"))
empty = pygame.transform.scale(empty, (60, 60))
withx = pygame.image.load(os.path.join(base_path, "withX.png"))
withx = pygame.transform.scale(withx, (60, 60))
witho = pygame.image.load(os.path.join(base_path, "withO.png"))
witho = pygame.transform.scale(witho, (60, 60))
loadingpic = pygame.image.load(os.path.join(base_path, "tictactoev2.png"))
loadingpic = pygame.transform.scale(loadingpic, (600, 600))
board = np.full((10,10),' ') #declaring the gameboard
#declaring the players
username1 = sys.argv[1]
username2 = sys.argv[2]
player = 'X' #game is gonna start with X
winner = ' ' #used to check if winner is declared, if declared then who is winner 
loading = 0 #used to set the loading page time
count = 0 #used to check whether the board is full or any place is remained empty to declare whether its Draw or not 
winner_count = 0 #used to print the winner onto the terminal for game.py to append the winner data in to history.csv
message_display = ' ' #used if the occupied cell is selected
message_timer = 0 #used to display the iamge for a second tentatively
clock = pygame.time.Clock()
time = np.random.randint(15,20)
def render_user(x, y, title, label, username, color):
    font = pygame.font.Font(None, 36)

    t1 = font.render(title, True, color)
    t2 = font.render(label, True, color)

    if len(username) > 13:
        username = username[:11] + "..."

    t3 = font.render(username, True, color)

    screen.blit(t1, (x, y))
    screen.blit(t2, (x, y + 27))
    screen.blit(t3, (x, y + 54))
def check_win(board,player):
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
while True:
    screen.fill((7,71,80))
    #displaying the loading page
    if loading <= 100:
        clock.tick(time)
        screen.blit(loadingpic,(0,0))
        font = pygame.font.Font(None, 50)
        dots = "." * (loading % 3 + 1)
        spaces = " " * (2 - loading % 3)
        loading_text = f"Loading{dots}{spaces} {loading}%"
        text = font.render(loading_text, True, (255, 255, 255))
        screen.blit(text, (200, 480))
        loading += 1
        for event in pygame.event.get():
            #if they press e to exit and the game is declared as draw
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                pygame.quit()
                sys.exit() 
    else:
        #screening the game page
        #displaying the game board
        for i in range(0,600,60):
            for j in range(0,600,60):
                img_map = {
                    ' ':empty,
                    'X':withx,
                    'O':witho
                }
                screen.blit(img_map[board[j//60][i//60]], (i, j))
        for event in pygame.event.get():
            #pressing e to exit the game and declaring the result of the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if winner == ' ':
                        if player == 'X':
                            winner = 'O'
                            print(username2)
                        elif player == 'O':
                            winner = 'X'
                            print(username1)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if message_timer > 0:
                    continue
                if board[y//60][x//60] == ' ' and winner == ' ':
                    board[y//60][x//60] = player
                    won, info = check_win(board, player)
                    count += 1
                    if won:
                        winner = player
                        win_type, (r,c) = info
                    player = 'O' if player == 'X' else 'X'
                elif board[y//60][x//60] != ' ' and winner == ' ':
                    message_display = "Cell Occupied!"
                    message_timer = 30
            if event.type==pygame.QUIT:
                if winner == ' ':
                    if player == 'X':
                        winner = 'O'
                        print(username2)
                    elif player == 'O':
                        winner = 'X'
                        print(username1)
                pygame.quit()
                sys.exit()
        if winner != ' ' or count == 100:
            if winner_count == 0 :
                if winner == 'X':
                    print(username1)
                elif winner == 'O':
                    print(username2)
                elif count == 100:
                    print("It's Draw")
                winner_count += 1
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
                pygame.draw.line(screen,(255,255,255),start,end,5)
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
            font = pygame.font.Font(None,80)
            text2 = font.render("Press E to Exit",True,(200,200,200))
            screen.blit(text2,(100,370))
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
        press_e = "press E to exit"
        press_e = font.render(press_e,True,(200,200,200))
        screen.blit(press_e,(610,192))
    #displaying the usernames of the players
    font=pygame.font.Font(None,36)
    render_user(610, 10, "Username Of", "Player X:", username1, (255,255,255))
    render_user(610, 101, "Username Of", "Player O:", username2, (255,255,255))
    clock.tick(60)
    pygame.display.update()