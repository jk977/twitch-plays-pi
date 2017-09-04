#!/bin/bash
# Finds all todo notes in code files. Doesn't work well with multiline todos.

dir="$( dirname $0 )"
source "$dir/../config.sh"

find "$basedir" -type f \( -name "*.py" -or -name "*.lua" -or -name "*.sh" \) -print0 | \
    xargs -0 grep -P '(#|(--))\s+TODO' | \
    sed 's_/home/pi/Desktop/twitch-plays/__' | \
    sed -r 's/(#|(--))\s+TODO:?//' | \
    tr -s [:space:] | \
    sort -u
