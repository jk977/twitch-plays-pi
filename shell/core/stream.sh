#!/bin/bash
# Starts streaming to Twitch.

dir="$( dirname $0 )"
source "$dir/../config.sh"

audiofile="$audiodir/all.mp3"

# uncomment to save stream to a file
#stream="/home/pi/Desktop/stream.flv"

while :
do
    ffmpeg \
        -i "$audiofile" \
        -threads 4 -f x11grab -r 30 -s 256x240 -i :0.0+0,36 \
        -c:a copy -ar 44100 -ac 2 \
        -c:v libx264 -preset medium -pix_fmt yuv420p \
        -shortest -f flv "$stream" 2>&1 | tee -a "$logdir/stream.log"
done
