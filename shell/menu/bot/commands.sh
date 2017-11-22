#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"


change_help() {
    current="$(read_file help)"

    show_window -sl inputbox \
        -t "Bot Help" \
        -p "Enter help link:" \
        -- "$current"

    if [ $? -eq 0 ]; then
        write_result help
    fi

    return 0
}

change_map() {
    current="$(read_file map)"

    show_window -sl inputbox \
        -t "Bot Map" \
        -p "Enter map link:" \
        -- "$current"

    if [ $? -eq 0 ]; then
        write_result owner
    fi

    return 0
}

command_menu() {
    while
        show_window -sl menu \
            -t "Bot Commands" \
            -p "Configure which command?" \
            -- 2 \
            1 "Help" \
            2 "Map"

        [ $? -eq 0 ] &&
            case "$(get_result)" in
                1)
                    change_help
                    ;;
                2)
                    change_map
                    ;;
            esac
    do :; done

    return 0
}
