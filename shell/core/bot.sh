#!/bin/bash
# Starts twitch bot to read chat inputs.

dir="$( dirname $0 )"
source "$dir/../config.sh"
cd "$botdir"
python3 -u main.py 2>&1 | tee -a "$logdir/bot.log"
cd "$basedir"
