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

video_menu() {
    while
        show_window -sl menu \
            -t "Stream Video" \
            -p "Configure which option?" \
            -- 4 \
            1 "Framerate" \
            2 "Capture Area" \
            3 "Display Number" \
            4 "Screen Number"

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
            esac
    do :; done

    return 0
}
