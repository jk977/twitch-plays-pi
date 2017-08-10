# Twitch Plays Bot

A 3-piece set of scripts to host a Twitch Plays style bot on a Raspberry Pi 3 Model B. Note that this is intended for private use, and may not work on different systems.

## Requirements

* Python 3.4.2
* Lua 5.2.3
* FCEUX 2.2.3 compiled with:
    * SDL 1.2.15
    * GTK 3.14.5

## Usage

Intended for private use. To run it yourself, make the following changes:
    * Project root
        * run.sh
            * Replace lxterminal with appropriate command if necessary
    * twitch-bot
        * cfg.py
            * Assign PASS to Twitch oauth
            * Assign CHAN to host channel
    * shell
        * streamkey.cfg
            * Store Twitch stream key in file
        * config.sh
            * Update paths if necessary
        
To start, execute run.sh by itself or shell/bot.sh, shell/nes.sh, and shell/stream.sh concurrently. For performance reasons, the resulting emulator window is not fullscreen, and should be positioned in the top-left corner of the screen.
