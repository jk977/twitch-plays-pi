#!/bin/sh
# Contains project settings, such as resource locations and script settings.

# include guard
[ -n "$settings_included" ] && return
settings_included=true

. shell/tests.sh

# constant values
gameaudio=2
noaudio=3

datadir=~/.twitch-plays-pi/
botdata="$datadir/bot/"
shelldata="$datadir/shell/"

botname="bot.py"
streamname="stream.sh"
emuname="emu.lua"

logging_enabled() {
    test_writable_dir "$logdir" && [ "$loglevel" -ne 0 ] 2>/dev/null
}

get_log_dest() {
    # prepends log directory to filename if logging is enabled
    # and configured, otherwise echos /dev/null

    # $1: Name of log file

    if logging_enabled && [ -n "$1" ]; then
        echo "$logdir/$1"
    else
        echo /dev/null
    fi
}

load_data() {
    # retrieves variable value from data directory and assigns to variable

    # $1: Name of variable to load (searches for .dat file of same name)

    if [ -z "$1" ]; then
        return 1
    fi

    contents=$( cat "$shelldata/$1.dat" 2>/dev/null )
    eval "$1=$contents"
    [ -n "$contents" ] # return success if $contents isn't empty
}

load_and_warn() {
    # writes warning to stderr if variable load fails
    load_data $@

    if [ $? -ne 0 ] && [ -z "$1" ]; then
        echo "Warning: Variable \"$1\" is empty (searched directory $shelldata)." >&2
    else
        echo "Variable \"$1\" is set."
    fi
}

load_defaults() {
    if test_writable_dir "$logdir" && [ -n "$loglevel" ]; then :; else
        # disable logging if not configured
        set_data loglevel 0
    fi

    [ -z "$s_audio" ] && set_data s_audio $noaudio
    [ -z "$s_framerate" ] && set_data s_framerate 30

    [ -z "$s_loops" ] && set_data s_loops "false"
    [ -z "$s_sig" ] && set_data s_sig "true"

    [ -z "$s_display" ] && set_data s_display 0
    [ -z "$s_screen" ] && set_data s_screen 0

    [ -z "$s_capture_x" ] && set_data s_capture_x 0
    [ -z "$s_capture_y" ] && set_data s_capture_y 0

    [ -z "$s_dimensions_x" ] && set_data s_dimensions_x 240
    [ -z "$s_dimensions_y" ] && set_data s_dimensions_y 256
}

load_bot_vars() {
    : # placeholder function
}

load_nes_vars() {
    load_and_warn emurom
}

load_stream_vars() {
    load_and_warn s_uri
    load_and_warn s_dest

    load_data s_audio
    load_data s_framerate

    load_data s_loops
    load_data s_sig

    load_data s_display
    load_data s_screen

    load_data s_capture_x
    load_data s_capture_y

    load_data s_dimensions_x
    load_data s_dimensions_y
}

update_data() {
    if [ $# -ne 0 ]; then
        for var in $@; do
            load_and_warn $var
        done
    else
        load_bot_vars
        load_nes_vars
        load_stream_vars
    fi

    echo # for formatting
}

set_data() {
    # assigns value of $2 to variable named by $1

    # $1: Name of data
    # $2: Value of data

    echo "$2" >"$shelldata/$1.dat"
    update_data "$1" >/dev/null
}

set_file() {
    # checks to see if $2 is a readable file, and
    # assigns to variable named by $1 if true

    # $1: Name of data
    # $2: Filepath to assign data to

    # no ifs to allow function to return non-zero on test failure
     test_readable_file "$2" && set_data "$1" "$2"
}

set_directory() {
    # checks to see if $2 is a writable directory, and assigns to
    # variable named by $1 if true

    # $1: Name of data
    # $2: Directory to assign data to

    test_writable_dir "$2" && set_data "$1" "$2"
}

load_and_warn basedir
load_and_warn logdir
load_data loglevel

update_data
load_defaults

# constant paths relative to project root
if [ -n "$basedir" ]; then
    set_directory shldir "$basedir/shell/"
    set_directory botdir "$basedir/bot/"
    set_directory emudir "$basedir/emu/"
else
    echo "Error: basedir is empty" >&2
    exit 1
fi
