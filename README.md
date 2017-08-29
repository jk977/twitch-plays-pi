# Twitch Plays Bot

A 3-piece set of scripts to host a Twitch Plays style bot on a Raspberry Pi 3 Model B. Note that this is intended for private use, and may not work on different systems without tweaking code.

## Requirements

* Python 3
* Lua 5.1+
* ffmpeg with libx264 and libmp3lame enabled
* FCEUX 2.2.3 compiled with:
    * SDL 1.2.15
    * GTK 3.14.5

## Usage

Intended for private use. To run it yourself, make the following changes:

* Project root/
    * run.sh
        * Replace lxterminal with appropriate command if necessary
* bot/
    * cfg.py
        * Assign PASS to Twitch oauth
        * Assign CHAN to host channel
* shell/
    * streamkey.cfg
        * Store Twitch stream key in file
    * config.sh
        * Update paths if necessary
    * core/
        * stream.sh
            * Update ffmpeg audio and video settings as needed
        
To start, execute run.sh by itself or shell/bot.sh, shell/nes.sh, and shell/stream.sh concurrently. For performance reasons, the resulting emulator window is not fullscreen, and should be positioned in the spot captured by ffmpeg (default is 36px from the top of the screen)

Once running, Twitch users can type an input in the following format (case-insensitive, space optional): {button} {presscount}

{button} corresponds to any of "A", "B", "start", "select", "up", "down", "left", or "right", and {presscount} is a number between 1 and 9.
