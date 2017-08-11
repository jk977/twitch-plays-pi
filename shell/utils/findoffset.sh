#!/bin/bash
# Reads stream log file and prints offset between corrected and original timestamps (debugging purposes)
# TODO implement background processes to speed up calculations

dir="$( dirname $0 )"
source "$dir/../config.sh"

echo "Parsing log file..."

old_times=( $( cat "$logdir/stream.log" | grep -Po '(?<=previous: )\d+' ) )
new_times=( $( cat "$logdir/stream.log" | grep -Po '(?<=current: )\d+' ) )
length="${#old_times[@]}"
total=0

echo "Parsing complete! Beginning calculations (this may take a while)..."

if (( ${#old_times[@]} != ${#new_times[@]} ))
then
    echo "An error occurred in parsing file."
    exit 1
fi

for (( i=0; i<${#old_times[@]}; i++ ))
do
    warning="Warning: null value found in array. Assigning to 0."
    before="${old_times[$i]}"
    after="${new_times[$i]}"

    if [[ -z "$before" ]]
    then
        echo "$warning"
        before=0
    fi

    if [[ -z "$after" ]]
    then
        echo "$warning"
        after=0
    fi

    difference=$((( before - after )))
    (( total += difference ))
done

echo "Average difference: $((( total / length ))) ms"
