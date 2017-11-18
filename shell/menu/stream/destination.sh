#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

format_uri() {
    awk '(substr($1, length($1), 1) != "/") {
            print $1"/";
            exit;
        }
        { print $1; }' |\
    tr -s / |\
    sed 's_:/_://_'
}

change_stream_uri() {
    prompt="Enter stream URI.\nAssumes local path if no protocol specified."

    show_submenu \
        --title "Stream URI" \
        --inputbox "$prompt" \
        $(dimensions) \
        "$s_uri"

    if [ $? -eq 0 ]; then
        result=$( get_result | format_uri )
        set_data s_uri "$result"
    fi
}

change_stream_endpt() {
    prompt="Enter stream endpoint (e.g., filename, RTMP key).\n\nIf streaming to Twitch, enter the RTMP key found in your account's dashboard. It should begin with \"live\".\nIf streaming to a file, make sure the extension matches the output format in shell/core/stream"

    show_submenu \
        --title "Stream Endpoint" \
        --inputbox "$prompt" \
        $(dimensions) \
        "$s_dest"

    if [ $? -eq 0 ]; then
        set_data s_dest "$(get_result)"
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
