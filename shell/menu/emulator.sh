#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_rom_dir() {
    update_data emurom
    default=$(get_default_dir "$emurom")

    show_window -sl inputbox \
        -t "ROM Location" \
        -p "Enter location of the ROM (must be compatible with the emulator):" \
        -- "$default"

    status=$?
    result=$(get_result)

    if [ $status -eq 0 ] && check_file_error "$result"; then
        set_file emurom "$result"
    fi

    return 0
}

emulator_menu() {
    while
        show_window -sl menu \
            -t "Emulator" \
            -p "Configure which option?" \
            -- 1 \
            1 "ROM Location"

        [ $? -eq 0 ] &&
            case "$(get_result)" in
                1)
                    change_rom_dir
                    ;;
            esac
    do :; done

    return 0
}
