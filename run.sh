#!/bin/bash
# Runs the 3 twitch-plays scripts concurrently. Configurable options are listed in the help command.

. shell/settings.sh
cd "$basedir"

# script flags
bot=1
nes=2
stream=4

scriptdir=$( find . -type d -name core )
scripts=0               # mask of scripts to run; if 0, all will run
dryrun=false            # whether or not to actually execute the target scripts
out_dest=/dev/stdout    # destination of script output

getflag() {
    # $1: Masked number to check for flag
    # $2: Flag to check number for
    # returns success if flag found or $1 is 0, otherwise fails

    [ $(( $1 & $2 )) -ne 0 ] || [ $1 -eq 0 ]
}

start_script() {
    # $1: script path
    "$1" >$out_dest 2>&1
}

while getopts "hqbnsd" opt; do
    case $opt in
        h)
            # whitespace type is important here
            # leading tabs are ignored but not leading spaces
            cat <<-EOF
			Usage: ./run.sh [-h] [-bns] [-q] [-d]
			Options:
			    -h      Show this help message and exit.
			    -b      Start the bot script.
			    -n      Start the NES script.
			    -s      Start the streaming script.
			    -q      Suppress script outputs (quiet).
			    -d      Debug (don't execute core scripts, dump status).

			If any of [-bns] are used, only the specified scripts will run.
			Otherwise, all scripts will run.
			EOF

            exit 0
            ;;
        q)
            out_dest=/dev/null
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

if $dryrun; then
    echo "Output destination: $out_dest"
    echo "Enabled scripts:"
    getflag $scripts $bot && printf "\t* Bot\n"
    getflag $scripts $nes && printf "\t* NES\n"
    getflag $scripts $stream && printf "\t* Stream\n"
    exit 0
fi

# run each script indicated by flags in $scripts.
# PIDs are saved in .{name}id if manual killing necessary

signals="INT TERM"

if getflag $scripts $bot; then
    echo "Starting bot script"
    start_script "$scriptdir/bot.sh" &
    echo $! > .botid
fi

if getflag $scripts $nes; then
    echo "Starting NES script"
    start_script "$scriptdir/nes.sh" &
    echo $! > .nesid
fi

if getflag $scripts $stream; then
    echo "Starting stream script"
    start_script "$scriptdir/stream.sh" &
    echo $! > .streamid
fi

trap "exit" $signals
trap "kill 0" EXIT
wait
