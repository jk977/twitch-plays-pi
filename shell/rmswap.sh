#!/bin/bash
# Removes all vim swap files in twitch-plays folder and subfolders.
# To be used after multiple crashes (usually caused by stream.sh changes).

dir="$( dirname $0 )"
source "$dir/config.sh"

eval cd "$basedir"
echo "Current directory: $(pwd)"
echo

files=()

# stores files to be deleted in $files
for path in $(find)
do
    filename=$( basename "$path" )
    if [[ "$filename" =~ \.sw[a-z] ]]
    then
        files+=($path)
    fi
done

if [[ ${#files[@]} -eq 0 ]]
then
    echo "No swap files found."
    exit 0
fi

echo "The following files will be removed:"

for file in "${files[@]}"
do
    echo "$file"
done

echo
echo "Continue? [y/N]"

read input
input="${input// }" # trim all whitespace
echo

if [[ -n "$input" ]]
then
    shopt -s nocasematch

    # if input is y (ignoring case), delete files
    if [[ "$input" = 'y' ]]
    then
        for file in "${files[@]}"
        do
            rm "$file"
        done

        echo "Files successfully removed!"
    else
        echo "Cancelling."
    fi

    shopt -u nocasematch
fi
