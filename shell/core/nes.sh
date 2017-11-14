#!/bin/sh

. "$( dirname $0 )/../settings.sh"

if [ "$loglevel" -gt 0 ]; then
    logdest="$logdir/nes.log"
else
    logdest=/dev/null
fi

if [ "$audiosrc" = $gameaudio ] >/dev/null; then
    soundargs="--sound 1 --soundrate 44100 --soundq 1 --soundbufsize 200"
else
    soundargs="--sound 0"
fi

fceux "$emugame" \
    $soundargs \
    --opengl 0 \
    --loadlua "$emudir/$emuname" \
    --xscale 1 \
    --yscale 1 \
    2>&1 | tee -a "$logdest"
