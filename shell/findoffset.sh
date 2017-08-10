#!/bin/bash
# Reads stream log file and prints offset between corrected and original timestamps (debugging purposes)
# TODO implement threading to speed up calculations

dir="$( dirname $0 )"
source "$dir/config.sh"

echo "Parsing log file..."

befores=( $( cat "$logdir/stream.log" | grep -Po '(?<=previous: )\d+' ) )
afters=( $( cat "$logdir/stream.log" | grep -Po '(?<=current: )\d+' ) )
total=0

echo "Parsing complete! Beginning calculations (this may take a while)..."

if (( ${#befores[@]} != ${#afters[@]} ))
then
    echo "An error occurred in parsing file."
    exit 1
fi

for (( i=0; i<${#befores[@]}; i++ ))
do
    warning="Warning: null value found in array. Assigning to 0."
    before="${befores[$i]}"
    after="${afters[$i]}"

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

echo "Average difference: $((( $total / ${#befores[@]} ))) ms"
