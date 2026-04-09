metric="$1" #metric id
declare -A games
declare -A gn #game_name
declare -A users
gn["othello"]=1
gn["tictactoe"]=2
gn["connect4"]=3
n=0
dr=0
d=0
ratio=0
he(){
    if [[ "$1" == "" ]]; then
        echo "0"
    else
        echo "$1"
    fi
}
while IFS=',' read -r status win los date game; do
    game=$(echo "$game" | tr -d '\r')
    if [[ ${users[${win}]} == '' ]]; then 
        users[${win}]=1
    fi
    if [[ ${users[${los}]} == '' ]]; then 
        users[${los}]=1
    fi
    if (($status == 1)); then
        ((games["0,1,$win"]++))
        ((games["0,2,$los"]++))
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
        ((games["0,3,$win"]++))
        ((games["0,3,$los"]++))
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
done < history.csv

((m=metric+1))
pi(){ # print info
    sort -k "${m}" -r ginfo > ginfo1
    awk '{printf "%-25s %-8s %-8s %-8s %-8s\n", $1, $2, $3, $4, $5 }' ginfo1
    rm ginfo ginfo1
    echo ""
}
cv(){ # calculate values
    local user="$1"
    local gid="$2"
    n=$(he "${games["${gid},1,${user}"]}")
    d=$(he "${games["${gid},2,${user}"]}")
    dr=$(he "${games["${gid},3,${user}"]}")
    if ((d != 0)); then
        ratio=$(echo "scale=2; $n / $d"| bc -l)
    else
        ratio="pro"
    fi
}
for gam in "${!gn[@]}"; do
    echo "For Game ${gam}:"
    gid=${gn["${gam}"]}
    for user in "${!users[@]}"; do
        cv "${user}" "${gid}"
        echo -e "${user}\t${n}\t${d}\t${dr}\t${ratio}">> ginfo
    done
    printf "%-25s %-8s %-8s %-8s %-8s\n" "Username" "Wins" "Loses" "Draws" "Win/Lose"
    pi
done
for user in "${!users[@]}"; do
    echo "For User ${user}:"
    for gam in "${!gn[@]}"; do
        gid=${gn["${gam}"]}
        cv "${user}" "${gid}"
        echo -e "${gam}\t${n}\t${d}\t${dr}\t${ratio}">> ginfo
    done
    printf "%-25s %-8s %-8s %-8s %-8s\n" "Game" "Wins" "Loses" "Draws" "Win/Lose"
    pi
done
