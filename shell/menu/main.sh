. shell/menu/common.sh
. shell/menu/bot.sh
. shell/menu/emulator.sh
. shell/menu/log.sh
. shell/menu/stream/stream.sh

main_menu() {
    show_window \
        --title "Main Menu" --notags \
        --menu "What do you want to change?" \
        $(height) $(width) 4 \
        1 "Bot" \
        2 "Emulator" \
        3 "Stream" \
        4 "Logging"
    status=$?

    case $(get_result) in
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
    esac

    if [ "$status" -ne 0 ]; then
        exit 0
    fi
}
