#!/bin/sh
# Starts twitch bot to read chat inputs.

. "$( dirname $0 )/../settings.sh"
. "$shldir/utils/tests.sh"

trap "exit" INT TERM
trap "echo Exiting bot.sh; kill 0" EXIT

cd "$botdir" # for PYTHONPATH reasons
logdest=$(get_log_dest bot.log)
status=0

# lets bot be restarted by calling sys.exit(0) in python script
while test_zero "$status"; do
    echo "Starting chat bot"
    python3 -u "$botname" 2>&1 | tee -a "$logdest"
    status=$?
done
