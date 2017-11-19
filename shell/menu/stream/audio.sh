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

    show_window -sl inputbox \
        -t "Audio Directory" \
        -p "Enter path to stream's audio file:" \
        -- "$default"

    if [ $? -eq 0 ]; then
        set_file s_audio "$(get_result)"
        check_file_error
    fi

    audio_menu
}

audio_menu() {
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

    show_window -sl radiolist \
        -t "Stream Audio" \
        -p "Choose audio source. If File is selected, you will be prompted to enter a path to an audio file:" \
        -- 3 \
        1 "$filetag" $filestat \
        2 "Game Audio" $gamestat \
        3 "None" $nonestat

    if [ $? -eq 0 ]; then
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
    fi

    stream_menu
}
