# Twitch Plays Bot

A 3-piece set of scripts originally intended to host a Twitch Plays style bot on a Raspberry Pi 3 Model B, but tested to work on Ubuntu as well. Note that the project may require some tweaks to work on systems that haven't been tested.

## Requirements

* Python 3
* FCEUX 2.1.2 or higher (for built-in Lua)
* ffmpeg with libx264 and libmp3lame enabled

## Usage

Before starting the program, run config.sh and completely fill out the information for each category.
        
To start, execute run.sh (use the script's -h option for details, or run without parameters for default behavior). For performance reasons, the resulting emulator window is not fullscreen, and should be positioned in the spot captured by ffmpeg (default is in the top left corner of the screen).

Once running, Twitch users can type a case-insensitive input corresponding to a valid emulator input, optionally followed by the number of times to press the input. The choice is voted for, and once a choice has enough votes, the input is sent to the emulator.
