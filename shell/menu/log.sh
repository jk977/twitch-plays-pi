#!/bin/sh
. shell/settings.sh
. shell/menu/common.sh

change_log_path() {
    default="$(get_default_dir "$logdir")"

    show_submenu \
        --title "Log Path" \
        --inputbox "Enter path to save log files in:" \
        $(dimensions) \
        "$default"

    if [ "$?" -eq 0 ]; then
        set_directory logdir "$(get_result)"
        check_file_error
    fi
}

change_log_level() {
    if ! [ -e "$logdir" ]; then
        show_error "Log directory not found. Logging is disabled." 
        return 1
    fi

    log0=OFF
    log1=OFF

    case "$loglevel" in
        0)
            log0=ON
            ;;
        1)
            log1=ON
            ;;
        *)
            ;;
    esac

    show_submenu \
        --title "Log Level" \
        --radiolist "Set logging level. Current log directory:\n$logdir" \
        $(dimensions) 2 \
        1 "Don't log output" $log0 \
        2 "Log output" $log1

    case "$(get_result)" in
        1)
            set_data loglevel 1
            ;;
        2)
            set_data loglevel 2
            ;;
    esac
}

log_menu() {
    status=0

    while [ "$status" -eq 0 ]; do
        show_submenu \
            --title "Logging" --notags \
            --menu "Configure which option?" \
            $(dimensions) 2 \
            0 "Change Log Path" \
            1 "Set Log Level"
        status=$?

        case "$(get_result)" in
            0)
                change_log_path
                ;;
            1)
                change_log_level
                ;;
        esac
    done

    main_menu
}
