#!/bin/bash
# Starts streaming to Twitch.
# TODO:
#   * Add audio (avconv -f alsa doesn't seem to work)
#   * Find out if Twitch freezing is caused by server or client (likely latter)

dir="$( dirname $0 )"
source "$dir/config.sh"
stream="rtmp://live.twitch.tv/app/$( cat "$shldir/streamkey.cfg" )"

avconv -f x11grab -r 30 -s 384x340 -i :0.0 -c:v libx264 -preset fast -pix_fmt yuv420p -s 384x340 -threads 4 -b 30k -f flv "$stream" 2>&1 | tee "$logdir/stream.log"
