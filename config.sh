#!/bin/sh

cd "$( dirname $0 )" # in case script is ran from a different directory
. shell/utils/tests.sh

mkdirs_if_absent() {
    for d in $@; do
        ! [ -d "$d" ] && mkdir "$d"
    done
}

if test_empty "$(which whiptail)"; then
    echo "Error: Whiptail must be installed to run config.sh" >&2
    exit 1
fi

mkdirs_if_absent shell/data bot/data

. shell/settings.sh
. shell/menu/main.sh

basedir="$(pwd)"
set_data basedir "$basedir"
main_menu
