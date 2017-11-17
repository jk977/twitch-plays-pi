#!/bin/sh

[ -n "$common_included" ] && return
common_included=true

tmpfile=".output"
menu_buttons="--yes-button Yes --no-button No --ok-button Select --cancel-button Quit"
submenu_buttons="--yes-button Yes --no-button No --ok-button Select --cancel-button Back"

width() {
    tput cols
}

height() {
    tput lines
}

dimensions() {
    # gets dimensions of current terminal window
    echo $(height) $(width)
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

show_submenu() {
    show_window $submenu_buttons "$@"
}

show_menu() {
    show_window $menu_buttons "$@"
}

show_error() {
    whiptail --msgbox "$@" $(dimensions)
}

check_file_error() {
    if [ $? -ne 0 ]; then
        show_error "Invalid file or directory entered. No changes made."
    fi
}

get_result() {
    result="$(cat $tmpfile)"
    rm $tmpfile 2>/dev/null
    echo "$result"
}
