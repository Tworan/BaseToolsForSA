#!/bin/bash
#users=("wxd" "xlf" "czf" "rym")
users=("wsy")
for user in "${users[@]}"
do
        HOMEPATH="/home/${user}"
        echo $HOMEPATH
        sudo useradd -m -d $HOMEPATH -g seucs -s /bin/zsh "$user"
        cp -r /home/master/.oh-my-zsh /home/$user/
        cp /home/master/.zshrc /home/$user/
        echo "${user}:123456" | sudo chpasswd
done

