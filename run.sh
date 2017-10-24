#!/bin/bash
# Runs the 3 twitch-plays scripts concurrently. Configurable options are listed in the help command.

getflag() {
    # param $1: Masked number to check for flag
    # param $2: Flag to check number for
    # returns success if flag found or $1 is 0, otherwise fails

    [ $(( $1 & $2 )) -eq $2 ] || [ $1 -eq 0 ]
}

bot=1
nes=2
stream=4

scripts=0   # mask of scripts to run; if 0, all will run
dryrun=0    # whether or not to actually execute the target scripts

while getopts ":ht:dbns" opt; do
    case $opt in
        h)
            cat <<-EOF
			Usage: ./run.sh [-h] [-t TERMINAL] [-bns] [-d]
			Options:
			    -h      Show this help message and quit.
			    -t      Specify a terminal to use for scripts.
			    -b      Start the bot script.
			    -n      Start the NES script.
			    -s      Start the streaming script.
			    -d      Debug (don't execute core scripts, dump status).

			If any of [-bns] are used, only the specified scripts will be ran.
			Otherwise, all scripts will run.
			EOF

            exit 0
            ;;
        t)
            myterm=$OPTARG
            ;;
        d)
            dryrun=1
            ;;
        b)
            scripts=$((scripts | bot))
            ;;
        n)
            scripts=$((scripts | nes))
            ;;
        s)
            scripts=$((scripts | stream))
            ;;
    esac
done

if [ -z $myterm ]; then
    myterm=gnome-terminal
fi

if [ "$dryrun" -eq 0 ]; then
    # run each script indicated by flags in $scripts.

    if getflag $scripts $bot; then
        echo "Starting bot script"
        $myterm -e shell/core/bot.sh
    fi

    if getflag $scripts $nes; then
        echo "Starting NES script"
      $myterm -e shell/core/nes.sh
    fi

    if getflag $scripts $stream; then
        echo "Starting stream script"
        $myterm -e shell/core/stream.sh
    fi
else
    echo "Terminal: $myterm"
    echo "Enabled scripts:"
    getflag $scripts $bot && printf "\t* Bot\n"
    getflag $scripts $nes && printf "\t* NES\n"
    getflag $scripts $stream && printf "\t* Stream\n"
fi
