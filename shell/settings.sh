#!/bin/sh
# Contains project settings, such as resource locations and script settings.

# include guard
[ -n "$settings_included" ] && return
settings_included=true

. shell/utils/tests.sh

# constant values
gameaudio=2
noaudio=3

datadir=~/.twitch-plays-pi/
botdata=$datadir/bot/
shelldata=$datadir/shell/

botname="bot.py"
streamname="stream.sh"
emuname="emu.lua"

get_log_dest() {
    # $1: Name of log file

    if test_empty "$1" || test_empty "$logdir" || test_zero "$loglevel"; then
        echo /dev/null
    else
        echo "$logdir/$1"
    fi
}

load_data() {
    # $1: Name of variable to load (searches for .dat file of same name)

    test_empty "$1" && exit 1
    contents=$( cat "$shelldata/$1.dat" 2>/dev/null )
    eval "$1=$contents"
    ! test_empty "$contents" # return success if $contents isn't empty
}

load_and_warn() {
    load_data $@

    if ! test_zero "$?"; then
        echo "Warning: Variable \"$1\" is empty (searched directory $shelldata)." >&2
    else
        echo "Variable \"$1\" is set."
    fi
}

load_defaults() {
    if test_empty "$loglevel" || test_empty "$logdir"; then
        # only allow logging if directory is specified
        set_data loglevel 0
    fi

    test_empty "$audiosrc" && set_data audiosrc $noaudio
    test_empty "$streamloops" && set_data streamloops "false"
    test_empty "$streamsig" && set_data streamsig "true"
}

update_data() {
    if ! test_zero "$#"; then
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

    echo "$2" > "$shelldata/$1.dat"
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

    test_writable_dir "$2" && set_data $@
}

update_data
load_defaults

# constant paths relative to project root
set_directory shldir "$basedir/shell/"
set_directory botdir "$basedir/bot/"
set_directory emudir "$basedir/emu/"
