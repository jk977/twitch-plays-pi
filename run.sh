#!/bin/bash
# Runs the 3 twitch-plays scripts concurrently

lxterminal -e shell/nes.sh -t NES &
lxterminal -e shell/bot.sh -t Bot &
lxterminal -e shell/stream.sh -t Stream &
wait
