#!/bin/bash
# Starts streaming to Twitch.
#
# Usage: stream.sh [-ds]
# Options:
#   -d      Does a dry run of the stream - saves file locally rather than streaming to Twitch.
#   -s      Enables stream sound. If not set, uses whatever is in $audiofile as background.

dir="$( dirname $0 )"
source "$dir/../config.sh"

audiofile="$audiodir/dq.mp3"

if [ -e $audiofile ]; then
    # uses $audiofile as background audio if it exists
    soundargs="-i $audiofile -c:a copy -ar 44100 -ac 2"
else
    soundargs=
fi

while getopts "ds" opt; do
    case $opt in
        d)
            stream="$basedir/stream.avi"
            ;;
        s)
            soundargs="-thread_queue_size 64 -f pulse -ar 44100 -i default"
            ;;
    esac
done

ffmpeg \
    $soundargs \
    -threads 4 -f x11grab -r 30 -s 256x240 -i :1.0+0,91 \
    -c:v libx264 -preset medium -pix_fmt yuv420p \
    -f avi "$stream" 2>&1 | tee -a "$logdir/stream.log"
