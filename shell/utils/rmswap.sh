#!/bin/bash
# Removes all vim swap files in twitch-plays folder and subfolders.
# Useful in case of crashes or unexpected powering off while using vim.

dir="$( dirname $0 )"
source "$dir/../config.sh"
printf "Searching directory $basedir\n\n"

files=()

# stores files to be deleted in $files
for file in $(find "$basedir" -name "*.sw[a-z]"); do
    files+=("$file")
done

if [[ ${#files[@]} -eq 0 ]]; then
    printf "No swap files found.\n"
    exit 0
fi

printf "The following files will be removed:\n"

for file in "${files[@]}"; do
    printf "$file\n"
done

printf "\nContinue? [y/N]\n"
read input
input="${input// }" # trim all whitespace
printf "\n"

if [[ -n "$input" ]]; then
    shopt -s nocasematch

    # if input is y (ignoring case), delete files
    if [[ "$input" = 'y' ]]; then
        for file in "${files[@]}"; do
            rm "$file"
        done

        printf "Files successfully removed!\n"
    else
        printf "Canceling.\n"
    fi

    shopt -u nocasematch
fi
