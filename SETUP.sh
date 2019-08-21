# assuming python3 and pip3 is installed
user="qwezarty"
addr="34.92.195.41"
name="zna"

echo -e "\033[1m==> Checking latest commit and dependencies...\033[0m"
ssh -qt $user@$addr <<- EOF 1>/dev/null
    # checking python3 is installed
	if ! hash python3 2>/dev/null; then
        echo "you need python3 installed on your os" >&2
        exit 1
    fi
	if ! hash pip3 2>/dev/null; then
        echo "you need pip3 installed on your os" >&2
        exit 1
    fi
    # checking and pull latest code
    if [ ! -d ~/Apps/$name ]; then
        mkdir -p ~/Apps/$name && cd \$_ && cd ../
        git clone https://github.com/qwezarty/zju-news-alerts.git $name && cd $name
    else
        cd ~/Apps/$name
        git pull origin master
    fi
    # resolve dependencies
    pip3 install -r requirements.txt
EOF
[[ $? != "0" ]] && { echo "  --> Exiting with error..."; exit 1; }

echo -e "\033[1m==> Restarting service...\033[0m"
ssh $user@$addr <<- EOF 
    cd ~/Apps/$name
    python3 zju_news_alerts warmup
    [[ \$? != "0" ]] && { echo "  --> Exiting with warmup error..."; exit 1; }
	# kill existed service
	if [ -f run.pid ]; then
		kill \$(cat run.pid)
	fi
	# restart service
	nohup python3 -u zju_news_alerts serve > ./$name.log 2>&1 &
	echo \$! > run.pid
EOF
