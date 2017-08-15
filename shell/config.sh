#!/bin/bash
# Contains project directories.

basedir=$( realpath ~/Desktop/twitch-plays )
botdir="$basedir/bot"
emudir="$basedir/emu"
logdir="$basedir/logs"
romdir="$basedir/roms/ff.nes"
shldir="$basedir/shell"

stream="rtmp://live.twitch.tv/app/$( cat "$basedir/streamkey.cfg" )"

if [[ ! -e "$basedir" ]]
then
    echo "Error: Could not find project root."
    exit 1
fi

if [[ ! -e "$logdir" ]]
then
    mkdir "$basedir/logs"
fi

if [[ ! -e "$basedir/roms" ]]
then
    mkdir "$basedir/roms"
fi
