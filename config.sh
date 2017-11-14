#!/bin/sh
. shell/settings.sh
. shell/menu/main.sh

basedir="$( realpath $(dirname $0) )"
set_data basedir "$basedir"
main_menu
