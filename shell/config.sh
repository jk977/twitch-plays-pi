#!/bin/bash
# Contains project directories.

basedir=$( realpath ~/Desktop/twitch-plays )
botdir="$basedir/twitch-bot"
emudir="$basedir/emu"
logdir="$basedir/logs"
romdir="$basedir/roms/ff.nes"
shldir="$basedir/shell"

stream="rtmp://live.twitch.tv/app/$( cat "$basedir/streamkey.cfg" )"
