#!/bin/sh
# Contains project settings, such as resource locations and script settings.

[ -n "$settings_included" ] && return
settings_included=true

# constant values
gameaudio=2
noaudio=3

datadir=$( find . -type d -name data | grep -v bot )
botname="bot.py"
streamname="stream.sh"
emuname="emu.lua"

test_empty() {
    [ -z "$1" ]
}

load_data() {
    # $1: Name of variable to load (searches for .dat file of same name)

    test_empty "$1" && exit 1
    contents=$( cat "$datadir/$1.dat" 2>/dev/null )
    eval "$1=$contents"
    [ -n "$contents" ] # return success if $contents isn't empty
}

load_and_warn() {
    load_data $@

    if [ "$?" -ne 0 ]; then
        echo "Warning: Variable \"$1\" is empty." >&2
    else
        echo "Variable \"$1\" is set."
    fi
}

load_defaults() {
    if test_empty "$loglevel" && test_empty "$logdir"; then
        set_data loglevel 0
    fi

    test_empty "$audiosrc" && set_data audiosrc $noaudio
    test_empty "$streamloops" && set_data streamloops "false"
    test_empty "$streamsig" && set_data streamsig "true"
}

update_data() {
    if [ "$#" -ne 0 ]; then
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
}

set_data() {
    # assigns value of $2 to variable named by $1

    # $1: Name of data
    # $2: Value of data

    echo "$2" > "$datadir/$1.dat"
    update_data "$1" >/dev/null
}

test_readable_file() {
    ! [ -d "$1" ] && [ -r "$1" ]
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

    [ -d "$2" ] && [ -w "$2" ] && set_data $@
}

update_data
load_defaults

# constant paths relative to project root
set_directory shldir "$basedir/shell/"
set_directory botdir "$basedir/bot/"
set_directory emudir "$basedir/emu/"
