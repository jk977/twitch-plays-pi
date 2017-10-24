#!/bin/bash
# Runs the 3 twitch-plays scripts concurrently

bot=1
nes=2
stream=4

scripts=0 # mask of scripts to run; if 0, all will run

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

if [ -z "$dryrun" ] || [ "$dryrun" -ne 1 ]; then
    for i in $(seq 0 2); do
        val=$(( 2**i ))         # value of current flag
        mask=$(( scripts & val ))  # 0 if $scripts doesn't contain flag

        # run each script indicated by flags in $scripts.
        # if $scripts is 0, run all

        if [ $mask -eq $bot ] || [ $scripts -eq 0 ]; then
            echo "Starting bot script"
            $myterm -e shell/core/bot.sh
        fi

        if [ $mask -eq $nes ] || [ $scripts -eq 0 ]; then
            echo "Starting NES script"
          $myterm -e shell/core/nes.sh
        fi

        if [ $mask -eq $stream ] || [ $scripts -eq 0 ]; then
            echo "Starting stream script"
            $myterm -e shell/core/stream.sh
        fi
    done
else
    echo "Terminal: $myterm"
    echo "Scripts: $scripts"
    echo "Dry run: $dryrun"
fi
