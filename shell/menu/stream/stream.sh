#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"
. "$shldir/menu/stream/audio.sh"
. "$shldir/menu/stream/advanced.sh"
. "$shldir/menu/stream/destination.sh"

change_stream_loop() {
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

    stream_menu
}

change_stream_signal() {
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

    stream_menu
}

stream_menu() {
    show_window -sl menu \
        -t "Stream" \
        -p "Configure which option?" \
        -- 4 \
        1 "Audio" \
        2 "Destination" \
        3 "Looping" \
        4 "End-of-Stream Signal"

    if [ $? -eq 0 ]; then
        case "$(get_result)" in
            1)
                audio_menu
                ;;
            2)
                destination_menu
                ;;
            3)
                change_stream_loop
                ;;
            4)
                change_stream_signal
                ;;
        esac
    fi

    main_menu
}
