#!/bin/sh
# Starts streaming to Twitch.

dir="$( dirname $0 )"
. "$dir/../settings.sh"

if [ "$loglevel" -gt 0 ]; then
    logdest="$logdir/stream.log"
else
    logdest=/dev/null
fi

stream="${streamuri}${streamkey}"

if [ -r "$audiosrc" ]; then
    # use audio from file
    audioargs="-i $streamaudio -c:a copy -ar 44100 -ac 2"
elif [ "$audiosrc" -eq $gameaudio ]; then
    # use audio from game
    audioargs="-thread_queue_size 64 -f pulse -ar 44100 -i default"
else
    audioargs=
fi

while :; do
    ffmpeg \
        $audioargs \
        -threads 4 -f x11grab -r 30 -s 256x240 -i :1.0+0,91 \
        -c:v libx264 -preset medium -pix_fmt yuv420p \
        -shortest -f avi "$stream" 2>&1 | tee -a "$logdest"

    if $streamsig; then
        # send SIGALRM to bot process
        bot_pid=$( pidof -x $botname 2>/dev/null )
        [ -n "$bot_pid" ] && kill -s ALRM "$bot_pid"
    fi

    if ! $streamloops; then
        exit 0
    fi
done
