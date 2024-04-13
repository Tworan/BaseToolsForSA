#/bin/zsh
users=("wxd" "czf" "xlf" "xzh_temp" "rym")

for user in "${users[@]}"
do
        echo $user
        # sudo chsh -s /bin/zsh $user
        # cp -r /home/master/.oh-my-zsh /home/$user/
        # cp /home/master/.zshrc /home/$user/
	chown -R $user:seucs /home/$user/.oh-my-zsh /home/$user/.zshrc
done

