#!/bin/bash
# Runs the 3 twitch-plays scripts concurrently

lxterminal -e shell/core/nes.sh -t NES &
lxterminal -e shell/core/bot.sh -t Bot &
lxterminal -e shell/core/stream.sh -t Stream &
wait
