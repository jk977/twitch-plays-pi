#!/bin/bash
# Starts nes emulator with lua input script loaded.

dir="$( dirname $0 )"
source "$dir/config.sh"
fceux "$romdir" --loadlua "$emudir/twitch.lua" --opengl 1 --xscale 1.5 --yscale 1.5 2>&1 | tee "$logdir/nes.log"
