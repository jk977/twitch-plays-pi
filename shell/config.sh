#!/bin/bash
# Contains project directories.

mkdirs_if_absent () {
    shopt -s nocasematch

    for dir in $@; do
        if ! [ -e "$dir" ]; then
            echo "$dir is absent. Create it? [y/N]"
            read confirm
            echo

            if [ "$confirm" = y ]; then
                echo "Making directory $dir"
                mkdir "$dir"
            fi
        fi
    done

    shopt -u nocasematch
}

basedir=$( realpath ~/Desktop/cs/projects/twitch-plays )
audiodir="/media/usb1/audio/"

botdir="$basedir/bot/"
emudir="$basedir/emu/"
logdir="$basedir/logs/"
romdir="$basedir/roms/"
shldir="$basedir/shell/"

if ! [ -e "$basedir" ]; then
    echo "Error: Could not find project root."
    exit 1
fi

stream="rtmp://live.twitch.tv/app/$( cat "$basedir/streamkey.cfg" )"
mkdirs_if_absent "$logdir" "$romdir"
