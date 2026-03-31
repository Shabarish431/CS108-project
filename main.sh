users=("" "")
i=0

while ((i<2)); do 
    echo "Press 1 to register or 2 to login and other keys to terminate"
    read -e option
    totallines=$(awk 'END{print NR}' users.tsv)
    if (( option == 1)); then 
        read -ep "Enter Username: " un
        word=${un}
        len=0
        b=1
        iter=1
        while [[ $word != '' ]]; do
            ((len++))
            word=${word:1}
        done
        if ((len < 4)); then
            iter=0
            b=0
            echo "Username should contain atleast 4 charecters"
        elif echo "${un}" | grep -Eq " "; then
            iter=0
            b=0
            echo "Username should not contain spaces"
        fi
        if (( iter==1 ));then 
            l=1
            while (( l<=totallines )); do 
                hun=$(awk -v l="${l}" 'BEGIN{OFS="";FS="\t"} NR==l {print $1}' users.tsv)
                if [[ "$hun" = "$un" ]]; then
                    echo "Username already exists"
                    b=0
                    break
                fi
                ((l++))
            done
            if ((b==1)); then
                read -ep "Enter Password: " pw
                len=0
                word=${pw}
                while [[ $word != '' ]]; do
                    ((len++))
                    word=${word:1}
                done
                if echo ${pw} | grep -Eq " " ; then
                    echo "Password should not contain spaces"
                elif ((len<7)); then
                    echo "Password should be of atleast 7 charecters length" 
                elif echo ${pw} | grep -Eq "@"; then
                    pass=$(echo ${pw} | sha256sum | awk '{print $1}')
                    echo -e "${un}\t${pass}">>users.tsv
                    users[i]=${un}
                    ((i++))
                    echo "${un} Registered and logged in successfully"
                else
                    echo "Password should contain atleast 1 @"
                fi
            fi

        fi

    elif (( option == 2)); then 
        read -ep "Enter Username: " un
        totallines=$(awk 'END{print NR}' users.tsv)
        l=1
        b=1
        it=1
        if [[ "${un}" = "${users[0]}" && "${un}" != '' ]]; then
            echo "${un} have logged in already"
            b=0
            it=0
        fi
        while (( l<=totallines && it == 1 )); do 
            hun=$(awk -v l="${l}" 'BEGIN{OFS="";FS="\t"} NR==l {print $1}' users.tsv)
            if [[ "$hun" = "$un" ]]; then
                read -ep "Enter Password: " pw
                pass=$(echo ${pw}|sha256sum|awk '{print $1}')
                hpw=$(awk -v l="${l}" 'BEGIN{OFS="";FS="\t"} NR==l {print $2}' users.tsv)
                if [[ ${hpw} = ${pass} ]]; then
                    users[i]=${un}
                    ((i++))
                    echo "${un} logged in successfully"
                else 
                    echo "Incorrect Password"
                fi
                b=0
                break
            fi
            ((l++))
        done
        if ((b==1)); then
            echo "Username doesn't exist"
        fi
    else
        break
    fi
done

if ((i==2)); then 
    python3 game.py "${users[0]}" "${users[1]}"
fi
