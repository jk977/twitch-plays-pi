#!/bin/bash
# Starts streaming to Twitch.

dir="$( dirname $0 )"
source "$dir/../config.sh"

# uncomment to save stream to a file
#stream="/home/jk/Desktop/stream.avi"

ffmpeg \
    -thread_queue_size 64 -threads 4 -f x11grab -r 30 -s 256x240 -i :1.0+0,91 \
    -thread_queue_size 64 -f pulse -ar 44100 -i default \
    -c:v libx264 -preset medium -pix_fmt yuv420p \
    -f avi "$stream" 2>&1 | tee -a "$logdir/stream.log"
