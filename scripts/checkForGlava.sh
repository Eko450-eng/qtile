#!/usr/bin/env bash
#
# Pass in a program name as an argument
[[ -n "$@" ]] || exit

if pgrep $1
then
    echo Killing $1
    pkill $1
else
    echo Launching $1
    $1
fi
