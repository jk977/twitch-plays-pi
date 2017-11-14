. shell/menu/common.sh
. shell/menu/emulator.sh
. shell/menu/log.sh
. shell/menu/stream/stream.sh

main_menu() {
    show_window \
        --title "Main Menu" --notags \
        --menu "What do you want to change?" \
        $(height) $(width) 3 \
        1 "Emulator" \
        2 "Stream" \
        3 "Logging"
    status=$?

    case $(get_result) in
        1)
            emulator_menu
            ;;
        2)
            stream_menu
            ;;
        3)
            log_menu
            ;;
    esac

    if [ "$status" -ne 0 ]; then
        exit 0
    fi
}
