#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"
. "$shldir/menu/bot/commands.sh"

get_file() {
    echo "$botdata/$1.dat"
}

read_file() {
    # $1: Name of file to read (path and extension not needed)
    cat "$( get_file "$1" )" 2>/dev/null
}

write_file() {
    # $1: Name of file to write (path and extension not needed)
    # $2: Content to write
    echo "$2" >"$( get_file "$1" )"
}

write_result() {
    # Writes result of input window to specified bot file if window was successful.
    # $1: Bot file name

    if [ $? -eq 0 ]; then
        write_file "$1" "$(get_result)"
    fi
}

change_nick() {
    current="$(read_file nick)"

    show_window -sl inputbox \
        -t "Bot Username" \
        -p "Enter username:" \
        -- "$current"

    if [ $? -eq 0 ]; then
        write_result nick
    fi

    return 0
}

change_pass() {
    current="$(read_file pass)"

    show_window -sl inputbox \
        -t "Bot Password" \
        -p "Enter password.\nPrefix the token with \"oauth:\" if using an OAuth token:" \
        -- "$current"

    if [ $? -eq 0 ]; then
        write_result pass
    fi

    return 0
}

change_host() {
    current="$(read_file host)"

    show_window -sl inputbox \
        -t "Bot Host" \
        -p "Enter host username. The bot will listen for inputs on the host's chat:" \
        -- "$current"

    if [ $? -eq 0 ]; then
        write_result host
    fi

    return 0
}

change_owner() {
    current="$(read_file owner)"

    show_window -sl inputbox \
        -t "Bot Owner" \
        -p "Enter owner username:" \
        -- "$current"

    if [ $? -eq 0 ]; then
        write_result owner
    fi

    return 0
}

bot_menu() {
    while
        show_window -sl menu \
            -t "Bot" \
            -p "Select an option to configure.\nThese are used in the bot's interactions with the host site's API." \
            -- 5 \
            1 "Username" \
            2 "Password" \
            3 "Host" \
            4 "Owner" \
            5 "Commands"

        [ $? -eq 0 ] &&
            case "$(get_result)" in
                1)
                    change_nick
                    ;;
                2)
                    change_pass
                    ;;
                3)
                    change_host
                    ;;
                4)
                    change_owner
                    ;;
                5)
                    command_menu
                    ;;
            esac
    do :; done

    return 0
}
