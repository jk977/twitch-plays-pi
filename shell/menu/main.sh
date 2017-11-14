. shell/menu/common.sh
. shell/menu/bot.sh
. shell/menu/emulator.sh
. shell/menu/log.sh
. shell/menu/stream/stream.sh

clear_cache() {
    whiptail \
        $submenu_buttons \
        --title "Clear Cache?" --defaultno \
        --yesno "This will remove all of the program's stored information. Continue?" \
        $(dimensions)
    status=$?

    if [ "$status" -eq 0 ]; then
        rm "$basedir/bot/data/"*
        rm "$shldir/data/"*
        whiptail --msgbox "Clear successful!" $(height) $(width)
    fi

    main_menu
}

main_menu() {
    show_window \
        $main_menu_buttons \
        --title "Main Menu" --notags \
        --menu "What do you want to change?" \
        $(dimensions) 5 \
        1 "Bot" \
        2 "Emulator" \
        3 "Stream" \
        4 "Logging" \
        5 "Clear Cached Information"
    status=$?

    case "$(get_result)" in
        1)
            bot_menu
            ;;
        2)
            emulator_menu
            ;;
        3)
            stream_menu
            ;;
        4)
            log_menu
            ;;
        5)
            clear_cache
            ;;
    esac

    if [ "$status" -ne 0 ]; then
        exit 0
    fi
}
