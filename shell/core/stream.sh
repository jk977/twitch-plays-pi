#!/bin/sh
# Starts streaming to Twitch.

. "$( dirname $0 )/../settings.sh"
. "$shldir/utils/tests.sh"

send_alarm() {
    # sends alarm to bot process if option is enabled
    bot_pid=$( pidof -x $botname 2>/dev/null )
    ! test_empty "$bot_pid" && kill -s ALRM "$bot_pid"
}

if test_readable_file "$audiosrc"; then
    # use audio from file
    audioargs="-i $streamaudio -c:a copy -ar 44100 -ac 2"
elif [ "$audiosrc" -eq $gameaudio ]; then
    # use audio from game
    audioargs="-thread_queue_size 64 -f pulse -ar 44100 -i default"
else
    audioargs=
fi

logdest=$(get_log_dest stream.log)
stream="${streamuri}${streamkey}"

while :; do
    ffmpeg \
        $audioargs \
        -threads 4 -f x11grab -r 30 -s 256x240 -i :1.0+0,91 \
        -c:v libx264 -preset medium -pix_fmt yuv420p \
        -shortest -f avi "$stream" 2>&1 | tee -a "$logdest"

    if ! $streamloops; then
        exit 0
    elif $streamsig; then
        send_alarm
    fi
done
