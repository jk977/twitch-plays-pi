# Twitch Plays Bot

A 3-piece set of scripts originally intended to host a Twitch Plays style bot on a Raspberry Pi 3 Model B, but tested to work on Ubuntu as well. Note that this is intended for private use, and may not work on different systems without tweaking configurations.

## Requirements

* Python 3
* FCEUX 2.1.2 or higher (for built-in Lua)
* ffmpeg with libx264 and libmp3lame enabled
## Usage

The following files may need to be changed or added before using the bot:

* Project root/
	* run.sh: Replace default terminal with appropriate command if necessary
	* streamkey.cfg: Store Twitch stream key in file (found in channel's Dashboard)
* bot/
	* info/
		* nick.cfg: Add bot username
		* oauth.cfg: Add oauth token for IRC connection
		* host.cfg: Add host channel
		* owner.cfg: Add name of bot owner (your username)
* shell/
	* config.sh
		* Update paths if necessary
	* core/
		* stream.sh
			* Update ffmpeg settings as needed
        * nes.sh
            * Update rom path as needed
        
To start, execute run.sh (use the script's -h option for details, or run without parameters for default behavior). For performance reasons, the resulting emulator window is not fullscreen, and should be positioned in the spot captured by ffmpeg (default is in the top left corner of the screen).

Once running, Twitch users can type a case-insensitive input corresponding to a valid emulator input, optionally followed by the number of times to press the input. The choice is voted for, and once a choice has enough votes, the input is sent to the emulator.
