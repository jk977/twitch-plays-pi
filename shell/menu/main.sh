. shell/settings.sh
. "$shldir/utils/tests.sh"

. "$shldir/menu/bot.sh"
. "$shldir/menu/emulator.sh"
. "$shldir/menu/log.sh"
. "$shldir/menu/stream/stream.sh"
. "$shldir/menu/common.sh"

clear_cache() {
    show_submenu \
        --title "Clear Cache?" --defaultno \
        --yesno "This will remove all of the program's stored information. Continue?" \
        $(dimensions)
    status=$?

    if test_zero "$status"; then
        rm -r "$datadir"
        whiptail --msgbox "Clear successful!" $(dimensions)
    fi

    main_menu
}

main_menu() {
    show_menu \
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
