#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"

. "$shldir/menu/common.sh"
. "$shldir/menu/stream/audio.sh"
. "$shldir/menu/stream/video.sh"
. "$shldir/menu/stream/destination.sh"

change_loop() {
    update_data s_loops

    if $s_loops; then
        default=
    else
        default="--defaultno"
    fi

    show_window -sl yesno \
        -t "Stream Loop" \
        -p "Enable stream looping? This will make the stream restart instead of terminating once the end of the stream audio file is reached. If the stream uses emulator audio, setting this option does nothing." \
        -- $default

    if [ $? -eq 0 ]; then
        set_data s_loops "true"
    else
        set_data s_loops "false"
    fi

    return 0
}

change_signal() {
    update_data s_sig

    if $s_sig; then
        default=
    else
        default="--defaultno"
    fi

    show_window -sl yesno \
        -t "Stream Signal" \
        -p "Enable end-of-stream signal? This will send a SIGALRM to the Twitch bot's process every time the stream restarts." \
        -- $default 

    if [ $? -eq 0 ]; then
        set_data s_sig "true"
    else
        set_data s_sig "false"
    fi

    return 0
}

stream_menu() {
    while
        show_window -sl menu \
            -t "Stream" \
            -p "Configure which option?" \
            -- 5 \
            1 "Video" \
            2 "Audio" \
            3 "Destination" \
            4 "Looping" \
            5 "End-of-Stream Signal"

        [ $? -eq 0 ] &&
            case "$(get_result)" in
                1)
                    video_menu
                    ;;
                2)
                    audio_menu
                    ;;
                3)
                    destination_menu
                    ;;
                4)
                    change_loop
                    ;;
                5)
                    change_signal
                    ;;
            esac
    do :; done

    return 0
}
