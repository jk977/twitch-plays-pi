#!/bin/sh
. shell/settings.sh
. "$shldir/utils/tests.sh"
. "$shldir/menu/common.sh"

change_rom_dir() {
    default=$(get_default_dir "$emurom")

    show_submenu \
        --title "ROM Location" \
        --inputbox "Enter location of the ROM (must be compatible with the emulator):" \
        $(dimensions) \
        "$default"

    if [ $? -eq 0 ]; then
        set_file emurom "$(get_result)"
        check_file_error
    fi
}

emulator_menu() {
    prompt="Configure which option?"
    status=0

    while [ $status -eq 0 ]; do
        show_submenu \
            --title "Emulator" --notags \
            --menu "$prompt" \
            $(dimensions) 2 \
            1 "ROM Location"
        status=$?

        case "$(get_result)" in
            1)
                change_rom_dir
                ;;
        esac
    done

    main_menu
}
