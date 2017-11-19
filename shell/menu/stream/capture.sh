#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_width() {
    update_data s_dimensions_x

    show_window -sl inputbox \
        -t "Capture Width" \
        -p "Enter the width of the capture area:" \
        -- "$s_dimensions_x"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_number_input "$result"; then
        set_data s_dimensions_x $result
    fi

    capture_menu
}

change_height() {
    update_data s_dimensions_y

    show_window -sl inputbox \
        -t "Capture Height" \
        -p "Enter the height of the capture area:" \
        -- "$s_dimensions_y"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_number_input "$result"; then
        set_data s_dimensions_y $result
    fi

    capture_menu
}

change_x_offset() {
    update_data s_capture_x

    show_window -sl inputbox \
        -t "Capture X-Offset" \
        -p "Enter the distance of the capture area from the left edge of the screen:" \
        -- "$s_capture_x"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_number_input "$result"; then
        set_data s_capture_x $result
    fi

    capture_menu
}

change_y_offset() {
    update_data s_capture_y

    show_window -sl inputbox \
        -t "Capture Y-Offset" \
        -p "Enter the distance of the capture area from the top edge of the screen:" \
        -- "$s_capture_y"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_number_input "$result"; then
        set_data s_capture_y $result
    fi

    capture_menu
}

capture_menu() {
    show_window -sl menu \
        -t "Stream Capture Area" \
        -p "These settings adjust the area of the desktop recorded by ffmpeg. Please select an option:" \
        -- 4 \
        1 "Width" \
        2 "Height" \
        3 "X-Offset" \
        4 "Y-Offset"

    if [ $? -eq 0 ]; then
        case "$(get_result)" in
            1)
                change_width
                ;;
            2)
                change_height
                ;;
            3)
                change_x_offset
                ;;
            4)
                change_y_offset
                ;;
        esac
    fi

    advanced_menu
}
