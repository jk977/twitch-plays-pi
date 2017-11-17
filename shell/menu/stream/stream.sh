#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"
. "$shldir/menu/stream/audio.sh"
. "$shldir/menu/stream/destination.sh"

change_stream_loop() {
    if $streamloops; then
        default=
    else
        default="--defaultno"
    fi

    prompt="Enable stream looping? This will make the stream restart instead of terminating once the end of the stream audio file is reached. If the stream uses emulator audio, setting this option does nothing."

    show_submenu \
        --title "Stream Loop" $default \
        --yesno "$prompt" \
        $(dimensions)

    if [ $? -eq 0 ]; then
        set_data streamloops "true"
    else
        set_data streamloops "false"
    fi
}

change_stream_signal() {
    if $streamsig; then
        default=
    else
        default="--defaultno"
    fi

    prompt="Enable end-of-stream signal? This will send a SIGALRM to the Twitch bot's process every time the stream restarts."

    show_submenu \
        --title "Stream Signal" $default \
        --yesno "$prompt" \
        $(dimensions)

    if [ $? -eq 0 ]; then
        set_data streamsig "true"
    else
        set_data streamsig "false"
    fi
}

stream_menu() {
    status=0

    while [ $status -eq 0 ]; do
        show_submenu \
            --title "Stream" --notags \
            --menu "Configure which option?" \
            $(dimensions) 4 \
            1 "Audio" \
            2 "Destination" \
            3 "Looping" \
            4 "End-of-Stream Signal"
        status=$?

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
    done

    main_menu
}
