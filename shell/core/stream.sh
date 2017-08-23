#!/bin/bash
# Starts streaming to Twitch.

dir="$( dirname $0 )"
source "$dir/../config.sh"

#stream="/home/pi/Desktop/stream.flv"

ffmpeg \
    -stream_loop -1 -f mp3 -i "$audiodir/all.mp3" \
    -thread_queue_size 64 -threads 4 -f x11grab -r 30 -s 256x240 -i :0.0+0,36 \
    -c:v libx264 -preset fast -pix_fmt yuv420p \
    -c:a copy -ar 44100 -ac 2 \
    -f flv "$stream" 2>&1 | tee "$logdir/stream.log"
