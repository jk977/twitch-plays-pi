#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_log_path() {
    default="$(get_default_dir "$logdir")"

    show_submenu \
        --title "Log Path" \
        --inputbox "Enter path to save log files in:" \
        $(dimensions) \
        "$default"

    if [ $? -ne 0 ]; then
        log_menu
    fi

    set_directory logdir "$(get_result)"
    check_file_error
}

change_log_level() {
    if test_writable_dir "$logdir"; then :; else
        show_error "Log directory not found. Logging is disabled." 
        return 1
    fi

    log0=OFF
    log1=OFF

    case "$loglevel" in
        1)
            log1=ON
            ;;
        *)
            log0=ON
            ;;
    esac

    show_submenu \
        --title "Log Level" \
        --radiolist "Set logging level. Current log directory:\n$logdir" \
        $(dimensions) 2 \
        1 "Don't log output" $log0 \
        2 "Log output" $log1

    if [ $? -ne 0 ]; then
        log_menu
    fi

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
    show_submenu \
        --title "Logging" --notags \
        --menu "Configure which option?" \
        $(dimensions) 2 \
        0 "Change Log Path" \
        1 "Set Log Level"

    if [ $? -ne 0 ]; then
        main_menu
    fi

    case "$(get_result)" in
        0)
            change_log_path
            ;;
        1)
            change_log_level
            ;;
    esac
}
