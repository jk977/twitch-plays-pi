#!/bin/bash
# Starts nes emulator with lua input script loaded. If called with -s, enables sound.

soundargs="--sound 0"

while getopts "s" opt; do
    case $opt in
        s)
            soundargs="--sound 1 --soundrate 44100 --soundq 1 --soundbufsize 200"
            ;;
    esac
done

dir="$( dirname $0 )"
source "$dir/../config.sh"
game="$romdir/fire.nes"

fceux "$game" \
    $soundargs \
    --opengl 0 \
    --loadlua "$emudir/main.lua" \
    --xscale 1 \
    --yscale 1 \
    2>&1 | tee -a "$logdir/nes.log"
