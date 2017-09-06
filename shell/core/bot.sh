#!/bin/bash
# Starts twitch bot to read chat inputs.

dir="$( dirname $0 )"
source "$dir/../config.sh"
cd "$botdir"
status=0

# lets bot be restarted by calling sys.exit(0)
while [[ $status -eq 0 ]]; do
    echo "Starting chat bot"
    python3 -u main.py 2>&1 | tee -a "$logdir/bot.log"
    status=$?
done

cd "$basedir"
