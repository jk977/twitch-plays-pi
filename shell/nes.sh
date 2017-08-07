#!/bin/bash
# Starts nes emulator with lua input script loaded.

dir="$( dirname $0 )"
source "$dir/config.sh"
fceux "$romdir" --loadlua "$emudir/twitch.lua" --fullscreen 1 2>&1 | tee "$logdir/nes.log"
