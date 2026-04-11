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
player='X'
winner=''
loading=0
count=0
winner_count = 0
loadingpic=pygame.image.load("games/tictactoev2.png")
clock=pygame.time.Clock()
time=np.random.randint(10,20)
def check_win(board,player):
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
    if loading <= 100:
        clock.tick(time)
        screen.blit(loadingpic,(0,0))
        font = pygame.font.Font(None, 50)
        if loading%3 == 0:
            loading_text = f"Loading.   {loading}%"
        elif loading%3 == 1:
            loading_text = f"Loading..  {loading}%"
        else:
            loading_text = f"Loading... {loading}%"
        text = font.render(loading_text, True, (255, 255, 255))
        screen.blit(text, (200, 480))
        loading += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                pygame.quit()
                sys.exit() 
    else:
        for i in range(0,600,60):
            for j in range(0,600,60):
                if board[j//60][i//60]=='X':screen.blit(withx,(i,j))
                elif board[j//60][i//60]=='O':screen.blit(withy,(i,j))
                else:screen.blit(empty,(i,j))
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    board=np.full((10,10),' ')
                    player='X'
                    winner=''
                elif event.key==pygame.K_e:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if board[x//60][y//60] == ' ' and winner == '':
                    board[x//60][y//60] = player
                    won, info = check_win(board, player)
                    count += 1
                    if won:
                        winner = player
                        win_type, (r,c) = info
                    player = 'O' if player == 'X' else 'O'
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        if winner!='' or count==100:
            if winner_count == 0 :
                print(winner)
                winner_count += 1
            cell=60
            if win_type=="horizontal":
                start=(c*cell+cell//2,r*cell+cell//2)
                end=((c+4)*cell+cell//2,r*cell+cell//2)
            elif win_type=="vertical":
                start=(c*cell+cell//2,r*cell+cell//2)
                end=(c*cell+cell//2,(r+4)*cell+cell//2)
            elif win_type=="diag1":
                start=(c*cell+cell//2,r*cell+cell//2)
                end=((c+4)*cell+cell//2,(r+4)*cell+cell//2)
            elif win_type=="diag2":
                start=(c*cell+cell//2,(r+4)*cell+cell//2)
                end=((c+4)*cell+cell//2,r*cell+cell//2)
            pygame.draw.line(screen,(255,255,255),start,end,5)
            small=pygame.transform.smoothscale(screen,(150,150))
            blurred=pygame.transform.smoothscale(small,(600,600))
            screen.blit(blurred,(0,0))
            overlay=pygame.Surface((600,600))
            overlay.set_alpha(75)
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))
            font=pygame.font.Font(None,200)
            text=font.render(f"{winner} Wins!",True,(255,255,255))
            screen.blit(text,(50,250))
            font=pygame.font.Font(None,80)
            text2=font.render("Press E to Exit",True,(200,200,200))
            screen.blit(text2,(100,420))
    clock.tick(60)
    pygame.display.update()