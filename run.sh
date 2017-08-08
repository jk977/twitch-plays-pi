#!/bin/bash
# Runs the 3 twitch-plays scripts concurrently

lxterminal -e shell/nes.sh &
lxterminal -e shell/bot.sh &
lxterminal -e shell/stream.sh &
wait
