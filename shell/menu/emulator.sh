#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_rom_dir() {
    update_data emurom
    default=$(get_default_dir "$emurom")

    show_submenu \
        --title "ROM Location" \
        --inputbox "Enter location of the ROM (must be compatible with the emulator):" \
        $(dimensions) \
        "$default"

    if [ $? -ne 0 ]; then
        emulator_menu
    fi

    set_file emurom "$(get_result)"
    check_file_error
}

emulator_menu() {
    prompt="Configure which option?"

    show_submenu \
        --title "Emulator" --notags \
        --menu "$prompt" \
        $(dimensions) 2 \
        1 "ROM Location"

    if [ $? -ne 0 ]; then
        main_menu
    fi

    case "$(get_result)" in
        1)
            change_rom_dir
            ;;
    esac
}
