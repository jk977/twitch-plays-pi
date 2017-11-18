# Twitch Plays Pi

A 3-piece set of scripts originally intended to host a Twitch Plays style bot on a Raspberry Pi 3 Model B, but tested to work on Ubuntu as well. Note that the project may require some tweaks to work on systems that haven't been tested.

## Dependencies

* Python 3
* [whiptail](https://linux.die.net/man/1/whiptail) (used by config.sh)
* FCEUX 2.1.2 or higher (for built-in Lua)
* ffmpeg with libx264,librtmp, and libmp3lame (optional if using another audio library) enabled
    * Enable encoders/muxers and other libraries as needed, depending on what type of input/output you use

## Usage

To configure the program, run the following commands:

```
cd /path/to/project/root/
./config
```

Once the configuration script is running, completely fill out all information for each category. You may also need to adjust the ffmpeg capture area offset manually, as there are no options for it in the menu (yet). To do this, edit $capture\_x and $capture\_y in shell/core/stream to contain the x- and y-offsets, respectively.

To start, execute 

```
./run
```

To stop the script, press the Enter key in the terminal that the script was started in. Use the script's -h option for more details on parameters, or run without parameters for default behavior. For performance reasons, the resulting emulator window is not fullscreen, and should be positioned in the spot captured by ffmpeg (default is in the top left corner of the screen).

Once running, Twitch users can type a case-insensitive input corresponding to a valid emulator input, optionally followed by the number of times to press the input. The choice is voted for, and once a choice has enough votes, the input is sent to the emulator.
