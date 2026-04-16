import pygame
import numpy as np
import sys
import csv
from datetime import datetime
import subprocess

if len(sys.argv) < 3:
    print("Usage: python3 game.py <user1> <user2>")
    sys.exit()

status = None
winner = None
def recording(status,winner,loser,game):
    date = datetime.today().strftime("%d-%m-%Y")
    with open("history.csv",mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([status,winner,loser,date,game])
        

class Game():
    # screen = None #pygame.display.set_mode((800,600))
    def init_screen(self,w=800,h=600):
        Game.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption("Mini Gaming Hub")
        self.screen.fill('azure4')
        font = pygame.font.Font(None,50)
        text = font.render("Loading",True,"black")
        self.screen.blit(text,(100,100))
        
    def render_user(self,x, y, title, label, username, color):
        font = pygame.font.Font(None, 36)

        t1 = font.render(title, True, color)
        t2 = font.render(label, True, color)

        if len(username) > 13:
            username = username[:11] + "..."

        t3 = font.render(username, True, color)

        self.screen.blit(t1, (x, y))
        self.screen.blit(t2, (x, y + 27))
        self.screen.blit(t3, (x, y + 54))

    def switch_turn(self,player,a,b):
        return b if player == a else a
    def check_win(self,board,player):
        pass
    def load(self):
        pass
    def apply_move(self):
        pass
    def play_game(self):
        pass

    def __init__(self,player1,player2):
        self.board = None
        self.fm = None
        self.sm = None
        self.winner = None
        self.username1 = player1 # first player starts game
        self.username2 = player2

sortby = 1

def leaderboard(sortby):
    subprocess.Popen(["bash","./leaderboard.sh",str(sortby)])
def analysis():
    subprocess.Popen(["python3","./analysis.py"])
def main_menu():
    global sortby
    pygame.init() #initializing the pygame
    G = Game(sys.argv[1],sys.argv[2])
    #screen=G.screen #declaring the size of the screen
    G.init_screen()
    running = True
    def pg(game,gn):
        global sortby
        pygame.display.set_caption(gn)
        status, winner, loser = game.play_game()
        recording(status,winner,loser,gn)
        G.init_screen()
        leaderboard(sortby)
        analysis()

    while running:
        # gid = 2
        gid = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                leaderboard(sortby)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                analysis()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                gid = 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                gid = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                gid = 3
        if gid==2:
            from games.tictactoe import TTT
            tictactoe = TTT(G.username1,G.username2)
            pg(tictactoe,"TIC-TAC-TOE")
        elif gid == 1:
            from games.othello import OT
            othello = OT(G.username1,G.username2)
            pg(othello,"OTHELLO")
        elif gid == 3:
            from games.connect4 import CO
            connect4 = CO(G.username1,G.username2)
            pg(connect4,"CONNECT4")
            
        pygame.display.update()

if __name__ == "__main__":
    main_menu()