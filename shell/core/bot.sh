#!/bin/sh
# Starts twitch bot to read chat inputs.

dir="$( dirname $0 )"
. "$dir/../settings.sh"

cd "$botdir" # for PYTHONPATH reasons
status=0

if [ "$loglevel" -gt 0 ] 2>/dev/null; then
    logdest="$logdir/bot.log"
else
    logdest=/dev/null
fi

# lets bot be restarted by calling sys.exit(0)
while [ $status -eq 0 ]; do
    echo "Starting chat bot"
    python3 -u "$botname" 2>&1 | tee -a "$logdest"
    status=$?
done

cd "$dir" # restore previous directory
