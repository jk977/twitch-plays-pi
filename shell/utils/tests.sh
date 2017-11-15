#!/bin/sh

[ -n "$tests_included" ] && return
tests_included=true

test_empty() {
    [ -z "$1" ]
}

test_zero() {
    [ "$1" -eq 0 ] 2>/dev/null
}

test_readable_file() {
    ! [ -d "$1" ] && [ -r "$1" ]
}

test_writable_dir() {
    [ -d "$1" ] && [ -w "$1" ]
}
