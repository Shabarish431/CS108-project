#game
import pygame
import numpy as np
import sys
import csv
import os
from datetime import datetime
import subprocess
if len(sys.argv) < 3:
    print("Usage: python3 game.py <user1> <user2>")
    sys.exit()
status = None
winner = None
sort_active = False #to determine whether sort menu should be shown or not
base_path = os.path.dirname(__file__) #to get the directory of the current file
# loading all the required images
wi = pygame.image.load(os.path.join(base_path,"MW.png"))
li = pygame.image.load(os.path.join(base_path,"ML.png"))
di = pygame.image.load(os.path.join(base_path,"MD.png"))
ri = pygame.image.load(os.path.join(base_path,"MR.png"))
pu = pygame.image.load(os.path.join(base_path,"P.png"))
epu = pygame.image.load(os.path.join(base_path,"EP.png"))
nss = pygame.image.load(os.path.join(base_path,"MWS.png"))
image = nss #default image for main menu
clock = pygame.time.Clock()
def recording(status,winner,loser,game): #function to record the game result in history.csv file
    date = datetime.today().strftime("%d-%m-%Y")
    with open("history.csv",mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([status,winner,loser,date,game])
def load_image(screen): #to load the selected image on the screen and the variable image is global which decides which image to be loaded
    screen.blit(image,(0,0))
    font = pygame.font.Font(None,35)
    text1 = font.render(username1,True,"white") #print usernames on the screen
    screen.blit(text1,(70,70))
    text2 = font.render(username2,True,"white")
    screen.blit(text2,(270,70))
    pygame.display.update()
class Game(): #created a class Game which will be inherited by all the games to be played in the gaming hub
    # screen = None #pygame.display.set_mode((800,600))
    def init_screen(self,w=800,h=600):#to initialize the screen for the game
        Game.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption("Mini Gaming Hub")
        global screen
        screen = self.screen
        load_image(screen)
    def render_user(self,x1, y1, y2, y3, y4, username1, username2, color, u1i, u2i, screen): #function to render the user information on the screen
        font=pygame.font.Font(None,36)
        screen.blit(u1i,(x1,y1))
        userename1_display = font.render(username1,True,color)
        screen.blit(userename1_display,(x1,y2))
        screen.blit(u2i,(x1,y3))
        username2_display = font.render(username2,True,color)
        screen.blit(username2_display,(x1,y4))
    def switch_turn(self,player,a,b): #function to switch the turn of the player after every move
        return b if player == a else a
    def check_win(self,board,player): #function to check whether the player has won the game or not, this function will be overridden by each game class as the winning conditions are different for each game
        pass
    def load(self,screen,a,b,c,loading): #function to display the loading screen for every game while starting the game
        time = np.random.randint(15,20)
        clock.tick(time)
        screen.blit(a,(0,0))
        fs = "." * (loading % 3 + 1)
        spaces = " " * (2 - (loading % 3))
        loading_text = "Loading" + fs + ' ' + spaces + str(loading) + "%"
        loading = loading + 1
        font = pygame.font.Font(None,50)
        text = font.render(loading_text,True,"white")
        screen.blit(text,(b,c))
        return loading
    def apply_move(self): #function to apply the move of the player on the board, this function will be overridden by each game class as the move application is different for each game
        pass
    def play_game(self): #this function acts as game loop until game is over and returns the status of the game
        pass
    def __init__(self,player1,player2):
        self.board = None
        self.fm = None
        self.sm = None
        self.winner = None
        global username1,username2
        username1, self.username1 = player1,player1 # first player starts game
        username2, self.username2 = player2,player2
sortby = 1 #to determine the sorting criteria for the leaderboard, 1 for wins, 2 for losses, 3 for wins/losses ratio
def pop_up(): #to display the pop up screen for player selection for the selected game 
    screen.fill("black")
    screen.blit(pu,(100,150))
    font = pygame.font.Font(None,35)
    text = font.render(username1,True,"white")
    screen.blit(text,(140,190))
def leaderboard(sortby): #run the leaderboard.sh script to display the leaderboard according to the sorting criteria selected by the user
    subprocess.Popen(["bash","./leaderboard.sh",str(sortby)])
def analysis(): #run the analysis.py script to display the analysis of the games played by the users
    subprocess.Popen(["python3","./analysis.py"])
def main_menu(): #
    global sortby,image,username1,username2,sort_active,pa,gs
    pygame.init() #initializing the pygame
    G = Game(sys.argv[1],sys.argv[2])
    G.init_screen()
    pa = False
    running = True
    GNS = True # this variable is used to determine whether game is selected or not (initially game is not selected so it is true)
    gs = True
    p1f = False
    gid = None
    def end(): #to decide whethere user wants to play another game or quit the gaming hub
        nonlocal p1f, GNS,gid,running
        global gs
        if pa:
            GNS = True
            p1f = False
            gid = None
            gs = True
        else:
            running = False
            pygame.quit()
            sys.exit()
    def pg(game,gn): #function to play the selected game and record the result after the game is over, this function will be called when the game is over
        global sortby,gs
        nonlocal p1f, GNS,gid,running
        pygame.display.set_caption(gn)
        status, winner, loser = game.play_game()
        if status != 3 : 
            recording(status,winner,loser,gn)
            leaderboard(sortby)
            analysis()
        G.init_screen()
        screen.blit(epu,(100,150))
        gs = False
    while running:
        # gid = 2
        if GNS and gs:
            load_image(screen)
        if not GNS and gs:
            pop_up()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                i,j = pygame.mouse.get_pos()
                if gs: #if game is not ended or the user decided to play another game
                    if not GNS:
                        screen.fill("black")
                        clock.tick(30)
                    if i in range(680,750) and j in range(20,50) and GNS:
                        running = False
                        pygame.quit()
                        sys.exit()
                    if i in range(540,760) and j in range(70,120) and GNS: # to change whether sort menu is shown or not
                        sort_active = not sort_active
                    if sort_active and GNS: # allow the user to change the sorting criteria for the leaderboard when the sort menu is active
                        if sortby == 1:
                            image = wi
                            load_image(screen)
                        elif sortby == 2:
                            image = li
                            load_image(screen)
                        elif sortby == 3:
                            image = di
                            load_image(screen)
                        elif sortby == 4:
                            image = ri
                            load_image(screen)
                        if i in range(560,741) and GNS:
                            if j in range(120,170):
                                sortby = 1
                                image = wi
                                load_image(screen)
                            elif j in range(171,220):
                                sortby = 2
                                image = li
                                load_image(screen)
                            elif j in range(221,270):
                                sortby = 3
                                image = di
                                load_image(screen)
                            elif j in range(271,320):
                                sortby = 4
                                image = ri
                                load_image(screen)
                    if sort_active == False and GNS:
                        image = nss
                        load_image(screen)
                    if i in range(50,450) and GNS: #to select the game
                        if j in range(160,260):
                            GNS = False
                            gid = 3
                            pop_up()
                        elif j in range(300,400):
                            GNS = False
                            pop_up()
                            gid = 1
                        elif j in range(440,540):
                            GNS = False
                            pop_up()
                            gid = 2
                    elif j in range(350,400) and (not p1f) and (not GNS) : #after selecting the game, in pop-out if we select yes then usernames remain same otherwise they exchange
                        if i in range(200,300):
                            p1f = True
                        elif i in range(500,600):
                            username1,username2 = username2,username1
                            p1f = True
                    if i in range(540,760) and GNS: #for leaderboard and analysis options in the main menu
                        if j in range(350,450):
                            leaderboard(sortby)
                        if j in range(480,580):
                            analysis()
                else:  #if game is ended then it would show the pop-up for user to decide whether they want to play another game or quit the gaming hub
                    if j in range(350,400):
                        if i in range(200,300):
                            pa = False
                            end()
                        elif i in range(500,600):
                            pa = True
                            end()
        if gid==2 and p1f and gs: #to select the game and run the selected game
            from games.tictactoe import TTT
            tictactoe = TTT(username1,username2)
            pg(tictactoe,"TIC-TAC-TOE")
        elif gid == 1 and p1f and gs:
            from games.othello import OT
            othello = OT(username1,username2)
            pg(othello,"OTHELLO")
        elif gid == 3 and p1f and gs:
            from games.connect4 import CO
            connect4 = CO(username1,username2)
            pg(connect4,"CONNECT4")
        clock.tick(60)
        pygame.display.update()
if __name__ == "__main__":
    main_menu()