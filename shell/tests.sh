#!/bin/sh

[ -n "$tests_included" ] && return
tests_included=true

test_readable_file() {
    [ ! -d "$1" ] && [ -r "$1" ]
}

test_writable_dir() {
    [ -d "$1" ] && [ -w "$1" ]
}

test_installed() {
    which "$1" >/dev/null
}

test_number() {
    # checks if value is a number. prints number to stdout if
    # test succeeds, otherwise does nothing

    # $1: value to check

    echo $1 | awk '(int($1) == $1) { print $1; }'
}
