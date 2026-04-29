users=("" "") 
i=0

echo "2 users are required to play any game"
# if anywhere user didn't met the conditions required to login or regester again this loop runs from the beginning
# iterates the loop till 2 users are logged in to play the game
# 'i' stores the value of number of users logged in

while ((i<2)); do 
    echo "Enter 1 to register or 2 to login or other valid keys to terminate"
    read -e option
    totallines=$(awk 'END{print NR}' users.tsv) # total no of lines in the users.tsv to iterate over each and every line
    
    if (( option == 1)); then 
        read -ep "Enter Username: " un
        b=1 # b is used as boolean to check if the username has not met the required conditions
        # b is changed to 0 if the conditions aren't met, based on this we go to check the password

        iter=1 # iter is used to check if we are supposed to iterate over all the lines in the file(just like 'b' used as boolean for different purpose)
        # this is to avoid checking all over the file if the other conditions on the username are not met already 

        if [[ ${un} == '' ]]; then
            iter=0
            b=0
            echo "Username shall be of atleast 4 charecters"
        elif echo "${un}" | grep -Eq " "; then
            iter=0
            b=0
            echo "Username should not contain spaces"
        elif echo "${un}" | grep -Eq ","; then
            iter=0
            b=0
            echo "Username should not contain commas"
        elif [[ ${#un} -lt 4 ]]; then
            iter=0
            b=0
            echo "Username should contain atleast 4 charecters"
        elif ((${#un} > 12)); then
            iter=0
            b=0
            echo "Username shall be of atmost 12 charecters"
        fi
        if (( iter==1 ));then 
            l=1
            while (( l<=totallines )); do 
            # hun is storing the already present usernames at the 'l'th line in the file users.tsv
                hun=$(awk -v l="${l}" 'BEGIN{OFS="";FS="\t"} NR==l {print $1}' users.tsv)
                if [[ "$hun" == "$un" ]]; then
                    echo "Username already exists"
                    b=0
                    break
                fi
                ((l++))
            done
            # if all the username conditions are met then we shall ask for the password(i.e no where b is assigned to be 0)
            if ((b==1)); then
                read -ep "Enter Password: " pw
                if [[ ${pw} == '' ]]; then
                    echo "Password shall be of atleast 7 charecters"
                elif echo ${pw} | grep -Eq " " ; then
                    echo "Password should not contain spaces"
                elif echo "${pw}" | grep -Eq "[^A-Za-z0-9@]"; then
                    echo "Invalid charecters, use normal charecters"
                elif ! echo "${pw}" | grep -Eq "[A-Z]" || ! echo "${pw}" | grep -Eq "[a-z]" ; then
                    echo "Password should contain both upper and lower case letters"
                elif ! echo "${pw}" | grep -Eq "[0-9]"; then
                    echo "Password should contain atleast 1 number"
                elif ! echo ${pw} | grep -Eq "^[A-Za-z0-9]*@[A-Za-z0-9]*$"; then
                    echo "Password should contain exactly 1 @" 
                elif (( ${#pw} >= 7 && ${#pw} < 15)); then
                # if all the password conditions are met the entered password is hashed and stored in the 'pass' variable
                    pass=$(echo ${pw} | sha256sum | awk '{print $1}')
                    # username and password entered is stored in the users.tsv
                    echo -e "${un}\t${pass}">>users.tsv
                    echo "${un} Registered successfully"
                    echo "Do you want to login too? Enter yes or no"
                    # user is able to just regester if he/she doesn't want to play
                    read -e decision
                    if [[ "$decision" == "yes" ]]; then
                        # if user decided to play then the user count increases and the username is stored in the 'users' array
                        users[i]=${un}
                        ((i++))
                        echo "Player ${i}: ${un} logged in successfully"
                    fi
                else
                    echo "Password should be of atleast 7 and atmost 14 charecters"
                fi
            fi

        fi
        # if user wanted to login
    elif (( option == 2)); then 
        read -ep "Enter Username: " un
        totallines=$(awk 'END{print NR}' users.tsv)
        l=1 # line number in the users.tsv as we iterate over the file
        # here 'it' is used as boolean to check if to iterate over the whole file or not
        # here 'b' is used as boolean to check if the username matches with one of the username in the file or not (if no remains b=1)
        b=1 
        it=1
        # same person can't login twice
        if [[ "${un}" == "${users[0]}" && "${un}" != '' ]]; then
            echo "${un} have logged in already"
            b=0
            it=0
        fi
        while (( l<=totallines && it == 1 )); do 
            hun=$(awk -v l="${l}" 'BEGIN{OFS="";FS="\t"} NR==l {print $1}' users.tsv)
            if [[ "$hun" = "$un" ]]; then
                read -ep "Enter Password: " pw
                # awk is used after hashing to avoid the extra column genrated by the sha256sum command
                pass=$(echo ${pw}|sha256sum|awk '{print $1}')
                hpw=$(awk -v l="${l}" 'BEGIN{OFS="";FS="\t"} NR==l {print $2}' users.tsv)
                # check the password entered(pass) against the correct password(hpw)
                if [[ ${hpw} == ${pass} ]]; then
                    # if the password matches then increase the number of users and store the username in 'users' array
                    users[i]=${un}
                    ((i++))
                    echo "Player ${i}: ${un} logged in successfully"
                else 
                    echo "Incorrect Password"
                fi

                b=0
                break
            fi
            ((l++))
        done
        # if somewhere 'b' value is not changed then the username doesn't exist in the file already
        if ((b==1)); then
            echo "Username doesn't exist, Register first!"
        fi
    else
    # if user don't want to register or login then terminate the loop
        break
    fi
done

# if there are 2 users logged in then send the usernames (in the order they have logged in) to the game.py as arguments

if ((i==2)); then 
    python3 game.py "${users[0]}" "${users[1]}"
fi
