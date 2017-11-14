#!/bin/bash
# Runs the 3 twitch-plays scripts concurrently. Configurable options are listed in the help command.

. shell/settings.sh

getflag() {
    # param $1: Masked number to check for flag
    # param $2: Flag to check number for
    # returns success if flag found or $1 is 0, otherwise fails

    [ $(( $1 & $2 )) -ne 0 ] || [ $1 -eq 0 ]
}

# script flags
bot=1
nes=2
stream=4

scriptdir=shell/core/

scripts=0               # mask of scripts to run; if 0, all will run
dryrun=false            # whether or not to actually execute the target scripts
myterm=gnome-terminal   # terminal to use for executing scripts

while getopts "ht:bnsd" opt; do
    case $opt in
        h)
            # whitespace type is important here
            # leading tabs are ignored but not leading spaces
            cat <<-EOF
			Usage: ./run.sh [-h] [-t TERMINAL] [-bns] [-d]
			Options:
			    -h      Show this help message and exit.
			    -t      Specify a terminal to use for scripts.
			    -b      Start the bot script.
			    -n      Start the NES script.
			    -s      Start the streaming script.
			    -d      Debug (don't execute core scripts, dump status).

			If any of [-bns] are used, only the specified scripts will run.
			Otherwise, all scripts will run.
			EOF

            exit 0
            ;;
        t)
            myterm=$OPTARG
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
        d)
            dryrun=true
            ;;
    esac
done

if ! $dryrun; then
    # run each script indicated by flags in $scripts.

    if getflag $scripts $bot; then
        echo "Starting bot script"
        $myterm -e "$scriptdir/bot.sh"
    fi

    if getflag $scripts $nes; then
        echo "Starting NES script"
        $myterm -e "$scriptdir/nes.sh"
    fi

    if getflag $scripts $stream; then
        echo "Starting stream script"
        $myterm -e "$scriptdir/stream.sh"
    fi
else
    echo "Terminal: $myterm"
    echo "Enabled scripts:"
    getflag $scripts $bot && printf "\t* Bot\n"
    getflag $scripts $nes && printf "\t* NES\n"
    getflag $scripts $stream && printf "\t* Stream\n"
fi
