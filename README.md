# Twitch Plays Bot

A 3-piece set of scripts to host a Twitch Plays style bot on a Raspberry Pi 3 Model B. Note that this is intended for private use, and may not work on different systems.

## Requirements

* Python 3.4.2
* Lua 5.2.3
* FCEUX 2.2.3 compiled with:
    * SDL 1.2.15
    * GTK 3.14.5

## Usage

Intended for private use. To run it yourself, assign PASS in twitch-bot/cfg.py to the Twitch oauth and bot owner, respectively. Assign the name of the channel from which chat commands are taken to CHAN. Store the Twitch stream key in shell/streamkey.cfg, and update $basedir in config.sh to match the project's base directory. To start the bot, run bot.sh, stream.sh, and nes.sh (found in the shell directory).
