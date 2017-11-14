#!/bin/bash
# Usage: nes.sh [-s]
# Options:
#   -s      Enables emulator sound.

dir="$( dirname $0 )"
. "$dir/../settings.sh"

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
    2>&1 | tee -a "$logdir/nes.log"
