#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"

. "$shldir/menu/common.sh"
. "$shldir/menu/stream/capture.sh"

change_framerate() {
    update_data s_framerate

    show_window -sl inputbox \
        -t "Stream Framerate" \
        -p "Enter the stream's framerate, in FPS:" \
        -- "$s_framerate"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_number_input "$result"; then
        set_data s_framerate $result
    fi

    return 0
}

change_display() {
    update_data s_display

    show_window -sl inputbox \
        -t "Stream Display" \
        -p "Enter the display number to capture from.\nIf you're not sure, try setting this to 0 or 1:" \
        -- "$s_display"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_number_input "$result"; then
        set_data s_display $result
    fi

    return 0
}

change_screen() {
    update_data s_screen

    show_window -sl inputbox \
        -t "Stream Screen" \
        -p "Enter the screen number to capture from.\nIf you're not sure, try setting this to 0 or 1:" \
        -- "$s_screen"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_number_input "$result"; then
        set_data s_screen $result
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

advanced_menu() {
    while
        show_window -sl menu \
            -t "Advanced Stream Configuration" \
            -p "Configure which option?" \
            -- 5 \
            1 "Framerate" \
            2 "Capture Area" \
            3 "Display Number" \
            4 "Screen Number" \
            5 "End-of-Stream Signal"

        [ $? -eq 0 ] &&
            case "$(get_result)" in
                1)
                    change_framerate
                    ;;
                2)
                    capture_menu
                    ;;
                3)
                    change_display
                    ;;
                4)
                    change_screen
                    ;;
                5)
                    change_signal
                    ;;
            esac
    do :; done

    return 0
}
