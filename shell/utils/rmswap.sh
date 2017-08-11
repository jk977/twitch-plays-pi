#!/bin/bash
# Removes all vim swap files in twitch-plays folder and subfolders.
# To be used after multiple crashes (usually caused by stream.sh changes).

dir="$( dirname $0 )"
source "$dir/../config.sh"

eval cd "$basedir"
printf "Current directory: $(pwd)\n"

files=()

# stores files to be deleted in $files
for path in $(find)
do
    filename=$( basename "$path" )
    if [[ "$filename" =~ \.sw[a-z] ]]
    then
        files+=("$path")
    fi
done

if [[ ${#files[@]} -eq 0 ]]
then
    printf "No swap files found.\n"
    exit 0
fi

printf "The following files will be removed:\n"

for file in "${files[@]}"
do
    printf "$file\n"
done

printf "\nContinue? [y/N]\n"
read input
input="${input// }" # trim all whitespace
printf "\n"

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

        printf "Files successfully removed!\n"
    else
        printf "Cancelling.\n"
    fi

    shopt -u nocasematch
fi
