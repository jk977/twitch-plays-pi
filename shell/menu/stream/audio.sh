#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_audio_dir() {
    show_window -sl inputbox \
        -t "Audio Directory" \
        -p "Enter path to stream's audio file:" \
        -- "$s_audio_file"

    if [ $? -eq 0 ]; then
        result=$(get_result)

        if test_readable_file "$result"; then
            set_file s_audio_file "$result"
            set_data s_audio_type $fileaudio
        else
            show_error "Invalid file entered. No changes made."
        fi
    fi

    return 0
}

change_source() {
    oldsrc="$s_audio_file" # in case of failure
    filetag="File"

    filestat="OFF"
    gamestat="OFF"
    nonestat="OFF"

    update_data s_audio_type s_audio_file

    case $s_audio_type in
        $fileaudio)
            if test_readable_file "$s_audio_file"; then
                filetag="$filetag ($s_audio_file)"
                filestat="ON"
            else
                nonestat="ON"
            fi
            ;;
        $gameaudio)
            gamestat="ON"
            ;;
        $noaudio)
            nonestat="ON"
            ;;
    esac

    show_window -sl radiolist \
        -t "Audio Source" \
        -p "Choose audio source. If File is selected, you will be prompted to enter a path to an audio file:" \
        -- 3 \
        1 "$filetag" $filestat \
        2 "Game Audio" $gamestat \
        3 "None" $nonestat

    [ $? -eq 0 ] &&
        case "$(get_result)" in
            1)
                change_audio_dir
                ;;
            2)
                set_data s_audio_type $gameaudio
                ;;
            3)
                set_data s_audio_type $noaudio
                ;;
        esac

    return 0
}

audio_menu() {
    while
        show_window -sl menu \
            -t "Stream Audio" \
            -p "Configure which option?" \
            -- 1 \
            1 "Source"

        [ $? -eq 0 ] &&
            case "$(get_result)" in
                1)
                    change_source
                    ;;
            esac
    do :; done

    return 0
}
