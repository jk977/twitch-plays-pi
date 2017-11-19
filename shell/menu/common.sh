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
    # prints $1 to stdout if non-empty, otherwise prints the project root

    if [ -n "$1" ]; then
        echo "$1"
    else
        echo "$basedir"
    fi
}

show_error() {
    whiptail --msgbox "$@" $(dimensions)
}

check_file_error() {
    if [ $? -ne 0 ]; then
        show_error "Invalid file or directory entered. No changes made."
        return 1
    fi
}

check_number_input() {
    if test_number "$1"; then
        return 0
    else
        show_error "Invalid number entered. No changes made."
        return 1
    fi
}

base_window() {
    whiptail "$@" 2>$tmpfile
}

show_window() {
    # creates whiptail window with specified parameters.
    # all trailing (i.e., non-getopts) parameters are
    # passed to whiptail

    buttons="$menu_buttons"

    while getopts sl:t:p: opt; do
        case $opt in
            s)
                buttons="$submenu_buttons"
                ;;
            l)
                # window layout, such as yesno or msgbox
                layout="--$OPTARG"
                ;;
            t)
                title="$OPTARG"
                ;;
            p)
                prompt="$OPTARG"
                ;;
        esac
    done

    shift $((OPTIND - 1))

    base_window \
        $buttons \
        --title "$title" --notags \
        $layout "$prompt" \
        $(dimensions) \
        "$@"
}

get_result() {
    result="$( cat $tmpfile 2>/dev/null )"
    rm $tmpfile 2>/dev/null
    echo "$result"
}
