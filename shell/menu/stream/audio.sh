#!/bin/sh
. shell/settings.sh
. shell/menu/common.sh

change_audio_dir() {
    if test_readable_file "$audiosrc" || [ -z "$audiosrc" ]; then
        default="$audiosrc"
    else
        default="$basedir"
    fi

    prompt="Enter path to stream's audio file:"

    show_window \
        --title "Audio Directory" \
        --inputbox "$prompt" \
        $(height) $(width) \
        "$default"

    if [ "$?" -eq 0 ]; then
        set_optional_file audiosrc "$(get_result)"
        check_file_error
    fi
}

shorten_path() {
    # Replaces /home/user with ~ in path
    # $1: Absolute path to a file

    pushd "$( dirname "$1" )" >/dev/null
    echo "$( dirs +0 )"
    popd >/dev/null
}

audio_menu() {
    oldsrc="$audiosrc" # in case of failure
    filetag="File"
    filestat="OFF"
    gamestat="OFF"
    nonestat="OFF"

    if test_readable_file "$audiosrc"; then
        filetag="$( shorten_path "$audiosrc" )"
    fi

    case "$audiosrc" in
        2)
            gamestat="ON"
            ;;
        3)
            nonestat="ON"
            ;;
        *)
            filestat="ON"
            ;;
    esac

    show_window \
        --title "Audio" --notags \
        --radiolist "Choose audio source:" \
        $(height) $(width) 3 \
        1 "$filetag" $filestat \
        2 "Game Audio" $gamestat \
        3 "None" $nonestat

    case $( get_result ) in
        1)
            change_audio_dir

            if [ "$?" -ne 0 ]; then
                audiosrc="$oldsrc"
            fi
            ;;
        2)
            set_data audiosrc $gameaudio
            ;;
        3)
            set_data audiosrc $noaudio
            ;;
    esac

    stream_menu
}
