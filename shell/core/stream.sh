#!/bin/bash
# Starts streaming to Twitch.

dir="$( dirname $0 )"
source "$dir/../config.sh"

# uncomment to save stream to a file
#stream="/home/pi/Desktop/stream.flv"

ffmpeg \
    -thread_queue_size 64 -threads 4 -f x11grab -r 30 -s 256x240 -i :0.0+0,36 \
    -thread_queue_size 64 -f alsa -ar 22050 -i default \
    -c:v libx264 -preset medium -pix_fmt yuv420p -b:v 20k \
    -f flv "$stream" 2>&1 | tee -a "$logdir/stream.log"
