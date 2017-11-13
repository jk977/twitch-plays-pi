#!/bin/bash
# Starts streaming to Twitch.
#
# Usage: stream.sh [-ds]
# Options:
#   -a      Enables stream audio. If not set, uses whatever is in $audiofile as background.
#   -d      Does a dry run of the stream - saves file locally rather than streaming to Twitch.
#   -s      Send SIGALRM to twitch bot when the stream restarts, if it loops.

dir="$( dirname $0 )"
source "$dir/../config.sh"

audiofile="$audiodir/dq.mp3"
streamloops=true
sendalarm=false

if [ -e $audiofile ]; then
    # uses $audiofile as background audio if it exists
    soundargs="-i $audiofile -c:a copy -ar 44100 -ac 2"
else
    soundargs=
fi

while getopts "ads" opt; do
    case $opt in
        a)
            soundargs="-thread_queue_size 64 -f pulse -ar 44100 -i default"
            streamloops=false
            ;;
        d)
            stream="$basedir/stream.avi"
            ;;
        s)
            sendalarm=true
            ;;
    esac
done

while :; do
    ffmpeg \
        $soundargs \
        -threads 4 -f x11grab -r 30 -s 256x240 -i :1.0+0,91 \
        -c:v libx264 -preset medium -pix_fmt yuv420p \
        -shortest -f avi "$stream" 2>&1 | tee -a "$logdir/stream.log"

    if $streamloops; then
        kill -s ALRM $( pidof -x $botname )
    else
        exit 0
    fi
done
