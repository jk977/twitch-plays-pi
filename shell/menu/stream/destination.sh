#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_stream_uri() {
    prompt="Enter stream URI.\nAssumes local path if no protocol specified."

    show_submenu \
        --title "Stream URI" \
        --inputbox "$prompt" \
        $(dimensions) \
        "$streamuri"

    if [ $? -eq 0 ]; then
        set_data streamuri "$(get_result)"
    fi
}

change_stream_endpt() {
    prompt="Enter stream endpoint (e.g., filename, RTMP key).\n\nIf streaming to Twitch, enter the RTMP key found in your account's dashboard. It should begin with \"live\".\nIf streaming to a file, make sure the extension matches the output format in shell/core/stream.sh"

    show_submenu \
        --title "Stream Endpoint" \
        --inputbox "$prompt" \
        $(dimensions) \
        "$streamdest"

    if [ $? -eq 0 ]; then
        set_data streamdest "$(get_result)"
    fi
}

destination_menu() {
    status=0

    while [ $status -eq 0 ]; do
        show_submenu \
            --title "Stream Destination" --notags\
            --menu "Configure which option?" \
            $(dimensions) 2 \
            1 URI \
            2 Endpoint
        status=$?

        case "$(get_result)" in
            1)
                change_stream_uri
                ;;
            2)
                change_stream_endpt
                ;;
        esac
    done

    stream_menu
}
