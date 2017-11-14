#!/bin/sh
[ -n "$common_included" ] && return

common_included=true
tmpfile=".output"

main_menu_buttons="--yes-button yes --no-button no --ok-button Ok --cancel-button Quit"
submenu_buttons="--yes-button yes --no-button no --ok-button Ok --cancel-button Back"

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

show_error() {
    whiptail --msgbox "$@" $(dimensions)
}

check_file_error() {
    if [ "$?" -ne 0 ]; then
        show_error "Invalid file or directory entered. No changes made."
    fi
}

get_result() {
    result="$(cat $tmpfile)"
    rm $tmpfile 2>/dev/null
    echo "$result"
}
