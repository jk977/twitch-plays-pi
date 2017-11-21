#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

format_uri() {
    sed 's_//*_/_; s_/*$_/_; s_:/*_://_' # squeeze, append /, add // after :
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

    return 0
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

    return 0
}

destination_menu() {
    while
        show_window -sl menu \
            -t "Stream Destination" \
            -p "Configure which option?" \
            -- 2 \
            1 "URI" \
            2 "Endpoint"

        [ $? -eq 0 ] &&
            case "$(get_result)" in
                1)
                    change_stream_uri
                    ;;
                2)
                    change_stream_endpt
                    ;;
            esac
    do :; done

    return 0
}
