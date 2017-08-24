#!/bin/bash
# Starts nes emulator with lua input script loaded.

dir="$( dirname $0 )"
source "$dir/../config.sh"

fceux "$romdir" \
    --opengl 0 \
    --loadlua "$emudir/main.lua" \
    --xscale 1 \
    --yscale 1 \
    --sound 0 \
    2>&1 | tee -a "$logdir/nes.log"
