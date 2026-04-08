metric="$1"
declare -A winn
declare -A lose
declare -A draw
declare -A games
nu=0
wb=1
lb=1
users=()
while IFS ',' read -r status win los date game; do
    for user in "${users[@]}"; do
        if [[ $user == $win ]]; then 
            wb=0
        fi
        if [[ $user == $los ]]; then
            lb=0
        fi
    done
    if ((wb==1)); then
        users[$nu]="$win"
        ((nu++))
    fi
    if ((lb==1)); then
        users[$nu]="$los"
        ((nu++))
    fi
    if (($status == 1)); then
        ((winn["$win"]++))
        ((lose["$los"]++))
        if [[ ${game} == "othello" ]]; then
            ((games["1,1,${win}"]++))
            ((games["1,2,${los}"]++))
        elif [[ ${game} == "connect4" ]]; then
            ((games["3,1,${win}"]++))
            ((games["3,2,${los}"]++))
        elif [[ ${game} == "tictactoe" ]]; then
            ((games["2,1,${win}"]++))
            ((games["2,2,${los}"]++))
        fi
    else
        ((draw["$win"]++))
        ((draw["$los"]++))
        if [[ ${game} == "othello" ]]; then
            ((games["1,3,${win}"]++))
            ((games["1,3,${los}"]++))
        elif [[ ${game} == "connect4" ]]; then
            ((games["3,3,${win}"]++))
            ((games["3,3,${los}"]++))
        elif [[ ${game} == "tictactoe" ]]; then
            ((games["2,3,${win}"]++))
            ((games["2,3,${los}"]++))
        fi
    fi
done
if (($metric==1)); then # Sort by win
    echo "GAMES:"
    for gam in "othello connect4 tictactoe"; do
        echo "For game ${gam}:"
        if [[ ${gam} == "othello" ]];then
            gid=1
        elif [[ ${gam} == "tictactoe" ]];then
            gid=2
        elif [[ ${gam} == "connect4" ]];then
            gid=3
        fi
        echo -E "Username\tWins\tLoses\tdraws\tWin/Lose"
        for user in "$users[@]"; do
            if ((games["gid,2,user"] != 0)); then
                ratio=((games["gid,1,user"]/games["gid,2,user"]))
            else
                ratio="no losses"
            fi
            echo -E "${user}\t${games["${gid},1,${user}"]}\t${games["${gid},2,${user}"]}\t${games["${gid},3,${user}"]}\t${ratio}"
        done
    done
elif (($metric==2)); then # sort by lose
    echo "GAMES:"
elif (($metric==3)); then # sort by w/l ratio
    echo "GAMES:"
fi
