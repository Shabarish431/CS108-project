metric="$1" # metric id

declare -A games # works as 3D array, stores the no of loses, wins, draws for a specific game and user
# can be acessed by the game ID, win/lose/draw ID (1,2,3 respectively), username

declare -A gn #game_name
# used to iterate efficiently, stores the gameID corresponding to the game name

declare -A users
# Stores all the usernames(as keys) present in the history.csv, as all users don't play all games

mid=("" "Win count" "Lose count" "Draw count" "Win/Lose Ratio")

gn["OTHELLO"]=1
gn["TIC-TAC-TOE"]=2
gn["CONNECT4"]=3
w=0 # win count
l=0 # lose count
# both are used for the ratio

dr=0 # draw count
ratio=0 # win/lose ratio

e2z(){
    # used to return the empty string as 0, as arrays default value stored is empty string
    # takes 1 argument-value of the associate array
    if [[ "$1" == "" ]]; then
        echo "0"
    else
        echo "$1"
    fi
}
while IFS=',' read -r status win los date game; do
    # status tells if the game is draw (status=2)
    # since csv file is being used carriage return shall be avoided
    game=$(echo "$game" | tr -d '\r')

    # if username is not present in users array already, it assings value as 1(marking as true,present)

    if [[ ${users[${win}]} == '' ]]; then 
        users[${win}]=1
    fi
    if [[ ${users[${los}]} == '' ]]; then 
        users[${los}]=1
    fi

    if (($status == 1)); then # if the game isn't draw
        if [[ ${game} == "OTHELLO" ]]; then
        # games["(gameID),(win/lose/draw ID),(Username)"]
            ((games["1,1,${win}"]++))
            ((games["1,2,${los}"]++))
        elif [[ ${game} == "CONNECT4" ]]; then
            ((games["3,1,${win}"]++))
            ((games["3,2,${los}"]++))
        elif [[ ${game} == "TIC-TAC-TOE" ]]; then
            ((games["2,1,${win}"]++))
            ((games["2,2,${los}"]++))
        fi
    else # if the game is draw
        if [[ ${game} == "OTHELLO" ]]; then
            ((games["1,3,${win}"]++))
            ((games["1,3,${los}"]++))
        elif [[ ${game} == "CONNECT4" ]]; then
            ((games["3,3,${win}"]++))
            ((games["3,3,${los}"]++))
        elif [[ ${game} == "TIC-TAC-TOE" ]]; then
            ((games["2,3,${win}"]++))
            ((games["2,3,${los}"]++))
        fi
    fi
done < history.csv

((f=metric+1)) # converting metric ID into the field number

pi(){ # print info
    # sorted based on the field and printed to the terminal
    if ((f < 5)); then
        sort -k "${f}" -rn ginfo > ginfo1
    # to sort the instances where no losses occured
    elif ((f==5)); then
        sort -k "${f}" -rn ginfo > temp
        awk ' $5 =="Pro" {printf "%-25s %-8s %-8s %-8s %-8s\n", $1, $2, $3, $4, $5 }' temp >>ginfo1
        awk ' $5 != "Pro" && $5 != "-" {printf "%-25s %-8s %-8s %-8s %-8s\n", $1, $2, $3, $4, $5 }' temp >> ginfo1
        awk ' $5 == "-" {printf "%-25s %-8s %-8s %-8s %-8s\n", $1, $2, $3, $4, $5} ' temp >> ginfo1
        rm temp
    fi
    awk '{printf "%-25s %-8s %-8s %-8s %-8s\n", $1, $2, $3, $4, $5 }' ginfo1
    # removing the files to ensure there is no file already present for later use
    rm ginfo ginfo1
    echo ""
}
cv(){ # calculate values
    # takes 2 arguments username and gameID
    local user="$1"
    local gid="$2"
    # reassigning win, lose, draw count 
    w=$(e2z "${games["${gid},1,${user}"]}")
    l=$(e2z "${games["${gid},2,${user}"]}")
    dr=$(e2z "${games["${gid},3,${user}"]}")
    if ((l != 0)); then
        ratio=$(echo "scale=2; $w / $l"| bc -l)
    elif ((w != 0)); then
        ratio="Pro" # declaring the gameplay as pro level if there is only winning streak
    else
        ratio="-" # Haven't played yet/ only draw matches
    fi
}
# print info for games (each game individually)
echo -e "Leaderboards: sorted based on the ${mid[${metric}]}"
for gam in "${!gn[@]}"; do
    echo "For Game ${gam}:"
    gid=${gn["${gam}"]}
    # iterating over all the keys(usernames) of the users array to ensure no user is missed, even though they didn't play the game
    for user in "${!users[@]}"; do
        # calling cv for the values of w, l, dr, ratio
        cv "${user}" "${gid}"
        # sent to the file "ginfo" each line is appended to sort later, based on the metric
        echo -e "${user}\t${w}\t${l}\t${dr}\t${ratio}">> ginfo
    done
    printf "%-25s %-8s %-8s %-8s %-8s\n" "Username" "Wins" "Loses" "Draws" "Win/Lose"
    # calling print info function to print the sorted information from the ginfo file
    pi
done
for user in "${!users[@]}"; do
    # iterating over each username
    echo "For User ${user}:"
    for gam in "${!gn[@]}"; do
        # iterating over each game
        gid=${gn["${gam}"]}
        # calling cv for the values of w, l, dr, ratio
        cv "${user}" "${gid}"
        # sent to the file "ginfo" each line is appended to sort later, based on the metric
        echo -e "${gam}\t${w}\t${l}\t${dr}\t${ratio}">> ginfo
    done
    printf "%-25s %-8s %-8s %-8s %-8s\n" "Game" "Wins" "Loses" "Draws" "Win/Lose"
    # calling print info function to print the sorted information from the ginfo file
    pi
done
