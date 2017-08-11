#!/bin/bash
# Starts nes emulator with lua input script loaded.

dir="$( dirname $0 )"
source "$dir/../config.sh"

fceux "$romdir" \
    --opengl 0
    --loadlua "$emudir/twitch.lua" \
    --xscale 1 \
    --yscale 1 \
    2>&1 | tee "$logdir/nes.log"
