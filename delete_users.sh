#!/bin/zsh
users=("wxd" "xlf" "czf" "rym")

for user in "${users[@]}"
do
        echo $user
        sudo userdel -r $user

done


