#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_audio_dir() {
    if test_readable_file "$s_audio"; then
        default="$s_audio"
    else
        default="$basedir"
    fi

    prompt="Enter path to stream's audio file:"

    show_submenu \
        --title "Audio Directory" \
        --inputbox "$prompt" \
        $(dimensions) \
        "$default"

    if [ $? -ne 0 ]; then
        audio_menu
    fi

    set_file s_audio "$(get_result)"
    check_file_error
}

audio_menu() {
    prompt="Choose audio source. If File is selected, you will be prompted to enter a path to an audio file:"
    oldsrc="$s_audio" # in case of failure
    filetag="File"

    filestat="OFF"
    gamestat="OFF"
    nonestat="OFF"

    if test_readable_file "$s_audio"; then
        filetag="$filetag ($s_audio)"
    fi

    case "$s_audio" in
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

    show_submenu \
        --title "Stream Audio" \
        --radiolist "$prompt" \
        $(dimensions) 3 \
        1 "$filetag" $filestat \
        2 "Game Audio" $gamestat \
        3 "None" $nonestat

    if [ $? -ne 0 ]; then
        stream_menu
    fi

    case "$(get_result)" in
        1)
            change_audio_dir

            if [ $? -ne 0 ]; then
                s_audio="$oldsrc" # restores old value if invalid input
            fi
            ;;
        2)
            set_data s_audio $gameaudio
            ;;
        3)
            set_data s_audio $noaudio
            ;;
    esac
}
