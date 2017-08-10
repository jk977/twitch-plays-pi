#!/bin/bash
# Starts streaming to Twitch.
# TODO fix audio to fully work instead of alternating on and off every ~0.5 seconds 

dir="$( dirname $0 )"
source "$dir/config.sh"
audio_opts="-f alsa -ar 22050 -i default"
video_opts="-f x11grab -r 60 -s 256x240 -i :0.0 -c:v libx264 -preset medium -pix_fmt yuv420p -s 256x240 -threads 4 -b 30k -f flv"

avconv $audio_opts $video_opts "$stream" 2>&1 | tee "$logdir/stream.log"
