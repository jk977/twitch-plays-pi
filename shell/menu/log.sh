#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_log_path() {
    default="$(get_default_dir "$logdir")"

    show_window -sl inputbox \
        -t "Log Path" \
        -p "Enter path to save log files in:" \
        -- "$default"

    if [ $? -eq 0 ]; then
        set_directory logdir "$(get_result)"
        check_file_error
    fi

    return 0
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

    show_window -sl radiolist \
        -t "Log Level" \
        -p "Set logging level. Current log directory:\n$logdir" \
        -- 2 \
        1 "Don't log output" $log0 \
        2 "Log output" $log1

    if [ $? -eq 0 ]; then
        case "$(get_result)" in
            1)
                set_data loglevel 1
                ;;
            2)
                set_data loglevel 2
                ;;
        esac
    fi

    return 0
}

log_menu() {
    status=0

    while [ $status -eq 0 ]; do
        show_window -sl menu \
            -t "Logging" \
            -p "Configure which option?" \
            -- 2 \
            0 "Change Log Path" \
            1 "Set Log Level"
        status=$?

        if [ $status -eq 0 ]; then
            case "$(get_result)" in
                0)
                    change_log_path
                    ;;
                1)
                    change_log_level
                    ;;
            esac

            status=$?
        fi
    done

    return 0
}
