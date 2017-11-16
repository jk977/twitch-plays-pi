. shell/settings.sh
. "$shldir/utils/tests.sh"
. "$shldir/menu/common.sh"

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
    echo "$2" > "$( get_file "$1" )"
}

write_result() {
    # Writes result of input window to specified bot file if window was successful.
    # $1: Bot file name

    if test_zero "$?"; then
        write_file "$1" "$( get_result )"
    fi
}

change_nick() {
    current="$(read_file nick)"

    show_submenu \
        --title "Bot Username" \
        --inputbox "Enter username:" \
        $(dimensions) \
        "$current"

    write_result nick
}

change_pass() {
    current="$(read_file pass)"

    show_submenu \
        --title "Bot Password" \
        --inputbox "Enter password.\nPrefix the token with \"oauth:\" if using an OAuth token:" \
        $(dimensions) \
        "$current"

    write_result pass
}

change_host() {
    current="$(read_file host)"

    show_submenu \
        --title "Bot Host" \
        --inputbox "Enter host username. The bot will listen for inputs on the host's chat:" \
        $(dimensions) \
        "$current"

    write_result host
}

change_owner() {
    current="$(read_file owner)"

    show_submenu \
        --title "Bot Owner" \
        --inputbox "Enter owner username:" \
        $(dimensions) \
        "$current"

    write_result owner
}

bot_menu() {
    prompt="Select an option to configure.\nThese are used in the bot's interactions with the host site's API."
    status=0

    while test_zero "$status"; do
        show_submenu \
            --title "Bot" --notags \
            --menu "$prompt" \
            $(dimensions) 4 \
            1 "Username" \
            2 "Password" \
            3 "Host" \
            4 "Owner"
        status=$?

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
        esac
    done

    main_menu
}
