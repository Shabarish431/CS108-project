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
sort_active = False
base_path = os.path.dirname(__file__)
wi = pygame.image.load(os.path.join(base_path,"MW.png"))
li = pygame.image.load(os.path.join(base_path,"ML.png"))
di = pygame.image.load(os.path.join(base_path,"MD.png"))
ri = pygame.image.load(os.path.join(base_path,"MR.png"))
pu = pygame.image.load(os.path.join(base_path,"P.png"))
epu = pygame.image.load(os.path.join(base_path,"EP.png"))
nss = pygame.image.load(os.path.join(base_path,"MWS.png"))
image = nss
clock = pygame.time.Clock()
def recording(status,winner,loser,game):
    date = datetime.today().strftime("%d-%m-%Y")
    with open("history.csv",mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([status,winner,loser,date,game])
def load_image(screen):
    screen.blit(image,(0,0))
    font = pygame.font.Font(None,35)
    text1 = font.render(username1,True,"white")
    screen.blit(text1,(70,70))
    text2 = font.render(username2,True,"white")
    screen.blit(text2,(270,70))
class Game():
    # screen = None #pygame.display.set_mode((800,600))
    def init_screen(self,w=800,h=600):
        Game.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption("Mini Gaming Hub")
        global screen
        screen = self.screen
        load_image(screen)
    def render_user(self,x, y, title, label, username, color):
        font = pygame.font.Font(None, 36)
        t1 = font.render(title, True, color)
        t2 = font.render(label, True, color)
        if len(username) > 13:
            username1 = username[:11] + "..."
        else :
            username1 = username
        t3 = font.render(username1, True, color)
        self.screen.blit(t1, (x, y))
        self.screen.blit(t2, (x, y + 27))
        self.screen.blit(t3, (x, y + 54))
    def switch_turn(self,player,a,b):
        return b if player == a else a
    def check_win(self,board,player):
        pass
    def load(self,screen,a,b,c,loading):
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
    def apply_move(self):
        pass
    def play_game(self):
        pass
    def __init__(self,player1,player2):
        self.board = None
        self.fm = None
        self.sm = None
        self.winner = None
        global username1,username2
        username1, self.username1 = player1,player1 # first player starts game
        username2, self.username2 = player2,player2
sortby = 1
def pop_up():
    screen.fill("black")
    screen.blit(pu,(100,150))
    font = pygame.font.Font(None,35)
    text = font.render(username1,True,"white")
    screen.blit(text,(140,190))
def leaderboard(sortby):
    subprocess.Popen(["bash","./leaderboard.sh",str(sortby)])
def analysis():
    subprocess.Popen(["python3","./analysis.py"])
def main_menu():
    global sortby,image,username1,username2,sort_active,pa,gs
    pygame.init() #initializing the pygame
    G = Game(sys.argv[1],sys.argv[2])
    G.init_screen()
    pa = False
    running = True
    GNS = True
    gs = True
    p1f = False
    gid = None
    def end():
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
    def pg(game,gn):
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
                if gs:
                    if not GNS:
                        screen.fill("black")
                        clock.tick(30)
                    if i in range(680,750) and j in range(20,50) and GNS:
                        running = False
                        pygame.quit()
                        sys.exit()
                    if i in range(540,760) and j in range(70,120) and GNS:
                        sort_active = not sort_active
                        print(sort_active)
                    if sort_active and GNS:
                        if sortby == 1:
                            image = wi
                            load_image(screen)
                            pygame.display.update()
                        elif sortby == 2:
                            image = li
                            load_image(screen)
                            pygame.display.update()
                        elif sortby == 3:
                            image = di
                            load_image(screen)
                            pygame.display.update()
                        elif sortby == 4:
                            image = ri
                            load_image(screen)
                            pygame.display.update()
                        if i in range(560,741) and GNS:
                            if j in range(120,170):
                                sortby = 1
                                image = wi
                                load_image(screen)
                                pygame.display.update()
                            elif j in range(171,220):
                                sortby = 2
                                image = li
                                load_image(screen)
                                pygame.display.update()
                            elif j in range(221,270):
                                sortby = 3
                                image = di
                                load_image(screen)
                                pygame.display.update()
                            elif j in range(271,320):
                                sortby = 4
                                image = ri
                                load_image(screen)
                                pygame.display.update()
                    if sort_active == False and GNS:
                        image = nss
                        load_image(screen)
                        pygame.display.update()
                    if i in range(50,450) and GNS:
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
                    elif j in range(350,400) and (not p1f) and (not GNS) :
                        if i in range(200,300):
                            p1f = True
                        elif i in range(500,600):
                            username1,username2 = username2,username1
                            p1f = True
                    if i in range(540,760) and GNS:
                        if j in range(350,450):
                            leaderboard(sortby)
                        if j in range(480,580):
                            analysis()
                else:
                    if j in range(350,400):
                        if i in range(200,300):
                            pa = False
                            end()
                        elif i in range(500,600):
                            pa = True
                            end()
        if gid==2 and p1f and gs:
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