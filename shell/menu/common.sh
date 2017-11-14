#!/bin/sh
[ -n "$common_included" ] && return

common_included=true
tmpfile=".output"

width() {
    tput cols
}

height() {
    tput lines
}

get_default_dir() {
    if [ -n "$1" ]; then
        echo "$1"
    else
        echo "$basedir"
    fi
}

show_window() {
    whiptail "$@" 2>$tmpfile
}

show_error() {
    whiptail --msgbox "$@" $(height) $(width)
}

check_file_error() {
    if [ "$?" -ne 0 ]; then
        show_error "Invalid file entered. No changes made."
    fi
}

get_result() {
    result=$(cat $tmpfile)
    rm $tmpfile 2>/dev/null
    echo "$result"
}
