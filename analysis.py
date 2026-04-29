import matplotlib.pyplot as plt
import csv
games = [0,0,0]
players = {}
player_names = []
win_count = []
with open("history.csv",mode='r') as file:
    reader = csv.reader(file)
    
    for row in reader:
        if row[0]=="1":
            # to count no of wins for each player
            if row[1] in players: 
                players[row[1]] += 1
            else:
                players[row[1]] = 1
        # to count no of games played in the total playing history of this gaming hub
        if row[4]=="OTHELLO": games[0]+=1 
        if row[4]=="TIC-TAC-TOE": games[1]+=1
        if row[4]=="CONNECT4": games[2]+=1

tup = list(players.items())
#sorting the players according to their win count in descending order
tup.sort(key=lambda x: x[1], reverse=True)

player_names = [x[0] for x in tup]
win_count = [x[1] for x in tup]

# to consider only top 5 players for the bar graph

if len(win_count)>5 :
    player_names = player_names[0:5]
    win_count = win_count[0:5]
    
# to convert the games count into percentage for the pie chart
game_names = ["OTHELLO","TIC-TAC-TOE","CONNECT4"]
total = sum(games)
for i in range(0,3):
    games[i] = games[i]/total

def visualise():
    plt.figure(figsize=(12,6))

    pie = plt.subplot(1,2,1)
    pie.set_title("Popularity of Games")
    pie.pie(games,labels=game_names,autopct="%1.1f%%")
    
    bar = plt.subplot(1,2,2)
    bar.set_title("Top Players")
    bar.bar(player_names,win_count)
    bar.set_xlabel("UserName")
    bar.set_ylabel("WinCount")

    plt.tight_layout()
    plt.show()
visualise()