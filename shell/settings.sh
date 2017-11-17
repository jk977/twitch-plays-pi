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

    [ -z "$1" ] && return 1
    contents=$( cat "$shelldata/$1.dat" 2>/dev/null )
    eval "$1=$contents"
    [ -n "$contents" ] # return success if $contents isn't empty
}

load_and_warn() {
    # writes warning to stderr if variable load fails
    load_data $@

    if [ $? -ne 0 ]; then
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

    [ -z "$audiosrc" ] && set_data audiosrc $noaudio
    [ -z "$streamloops" ] && set_data streamloops "false"
    [ -z "$streamsig" ] && set_data streamsig "true"
}

update_data() {
    if [ $# -ne 0 ]; then
        for var in $@; do
            load_and_warn $var
        done
    else
        load_and_warn basedir
        load_and_warn emurom

        load_and_warn logdir
        load_data loglevel

        load_data audiosrc
        load_data streamloops
        load_data streamsig
        load_and_warn streamuri
        load_and_warn streamdest
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

update_data
load_defaults

# constant paths relative to project root
set_directory shldir "$basedir/shell/"
set_directory botdir "$basedir/bot/"
set_directory emudir "$basedir/emu/"
