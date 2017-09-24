#!/bin/bash
# Contains project directories.

mkdirs_if_absent () {
    for dir in $@; do
        if [[ ! -e "$dir" ]]; then
            echo "Making directory $dir"
            mkdir "$dir"
        fi
    done
}

basedir=$( realpath ~/Desktop/twitch-plays )
botdir="$basedir/bot"
emudir="$basedir/emu"
logdir="/media/usb1/twitch-plays-logs/"
romdir="$basedir/roms/"
shldir="$basedir/shell"
audiodir="/media/usb1/audio"

stream="rtmp://live.twitch.tv/app/$( cat "$basedir/streamkey.cfg" )"

if [[ ! -e "$basedir" ]]; then
    echo "Error: Could not find project root."
    exit 1
fi

mkdirs_if_absent "$logdir" "$romdir" "$audiodir"
