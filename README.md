# Twitch Plays Pi

A 3-piece set of scripts originally intended to host a Twitch Plays style bot on a Raspberry Pi 3 Model B, but tested to work on Ubuntu as well. Note that the project may require some tweaks to work on systems that haven't been tested.

## Dependencies

* Python 3
* whiptail (used by config.sh)
* FCEUX 2.1.2 or higher (for built-in Lua)
* FFmpeg with libx264, librtmp, and libmp3lame (optional if using another audio library) enabled
    * Files other than mp3's for audio will not work unless the stream script is manually changed and your version of FFmpeg supports the file type
* PulseAudio (if using emulator audio instead of a music file)
    * Although this is an option, emulator audio on the Pi results in poor performance and is not recommended

## Usage

To configure the program, run the following commands:

```
cd /path/to/project/root/
./config
```

Once the configuration script is running, completely fill out all information for each category.

To start, execute 

```
./run
```

To stop the script, press the Enter key in the terminal that the script was started in. Use the script's -h option for more details on parameters, or run without parameters for default behavior. For performance reasons, the resulting emulator window is not fullscreen, and should be positioned in the spot captured by ffmpeg (default is in the top left corner of the screen).

Once running, Twitch users can type a case-insensitive input corresponding to a valid emulator input, optionally followed by the number of times to press the input. The choice is voted for, and once a choice has enough votes, the input is sent to the emulator.
