#!/bin/sh
. shell/settings.sh
. shell/menu/common.sh

change_rom_dir() {
    default=$(get_default_dir "$emurom")

    show_window \
        --title "ROM Path" \
        --inputbox "Enter path to the game (must be compatible with the emulator):" \
        $(height) $(width) \
        "$default"

    if [ "$?" -eq 0 ]; then
        set_file emurom "$(get_result)"
        check_file_error
    fi
}

emulator_menu() {
    prompt="Configure which option?"
    status=0

    while [ "$status" -eq 0 ]; do
        show_window \
            --title "Emulator" --notags \
            --menu "$prompt" \
            $(height) $(width) 2 \
            1 "ROM Path"
        status=$?

        case "$(get_result)" in
            1)
                change_rom_dir
                ;;
        esac
    done

    main_menu
}
