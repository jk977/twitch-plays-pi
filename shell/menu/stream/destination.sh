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
    update_data s_uri

    show_window -sl inputbox \
        -t "Stream URI" \
        -p "Enter stream URI.\nAssumes local path if no protocol specified." \
        -- "$s_uri"

    if [ $? -eq 0 ]; then
        set_data s_uri "$( get_result | format_uri )"
    fi

    destination_menu
}

change_stream_endpt() {
    update_data s_dest

    show_window -sl inputbox \
        -t "Stream Endpoint" \
        -p "Enter stream endpoint (e.g., filename, RTMP key).\n\nIf streaming to Twitch, enter the RTMP key found in your account's dashboard. It should begin with \"live\".\nIf streaming to a file, make sure the extension matches the output format in shell/core/stream" \
        -- "$s_dest"

    if [ $? -eq 0 ]; then
        set_data s_dest "$(get_result)"
    fi

    destination_menu
}

destination_menu() {
    show_window -sl menu \
        -t "Stream Destination" \
        -p "Configure which option?" \
        -- 2 \
        1 URI \
        2 Endpoint

    if [ $? -eq 0 ]; then
        case "$(get_result)" in
            1)
                change_stream_uri
                ;;
            2)
                change_stream_endpt
                ;;
        esac
    fi

    stream_menu
}
