. shell/settings.sh
. "$shldir/tests.sh"

. "$shldir/menu/bot.sh"
. "$shldir/menu/emulator.sh"
. "$shldir/menu/log.sh"
. "$shldir/menu/stream/stream.sh"
. "$shldir/menu/common.sh"

clear_cache() {
    show_window -sl yesno \
        -t "Clear Cache?" \
        -p "This will remove all of the program's stored information. Continue?" \
        -- --defaultno

    if [ $? -eq 0 ]; then
        test_writable_dir "$logdir" && rm "$logdir/"*
        rm -r "$datadir" && show_window -sl msgbox -p "Clear successful!"
    fi

    return 0
}

main_menu() {
    status=0

    while [ $status -eq 0 ]; do
        show_window -l menu \
            -t "Main Menu" \
            -p "What do you want to change?" \
            -- 5 \
            1 "Bot" \
            2 "Emulator" \
            3 "Stream" \
            4 "Logging" \
            5 "Clear Cached Information"
        status=$?

        if [ $status -eq 0 ]; then
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

            status=$?
        fi
    done

    return 0
}
