#!/bin/bash
# Starts streaming to twitch.
# TODO add audio (avconv -f alsa doesn't seem to work)

dir="$( dirname $0 )"
source "$dir/config.sh"
stream="rtmp://live.twitch.tv/app/$( cat "$shldir/streamkey.cfg" )"

avconv -f x11grab -r 25 -s 1184x624 -i :0.0 -c:v libx264 -preset fast -pix_fmt yuv420p -s 390x360 -threads 0 -b 30k -f flv "$stream" 2>&1 | tee "$logdir/stream.log"
