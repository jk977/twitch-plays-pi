#!/bin/sh

mkdirs_if_absent() {
    for d in $@; do
        ! [ -d "$d" ] && mkdir "$d"
    done
}

mkdirs_if_absent shell/data bot/data

. shell/settings.sh
. shell/menu/main.sh

basedir="$( realpath $(dirname $0) )"
set_data basedir "$basedir"
main_menu
