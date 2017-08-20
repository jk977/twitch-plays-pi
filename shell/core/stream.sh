#!/bin/bash
# Starts streaming to Twitch.
# TODO fix audio to fully work instead of alternating on and off every ~0.5 seconds 

dir="$( dirname $0 )"
source "$dir/../config.sh"

audio_opts="-f mp3 -i $audiodir/all.mp3"
song_len=3191
video_opts="-f x11grab -r 30 -s 256x240 -i :0.0+0,36 -c:v libx264 -preset slow -pix_fmt yuv420p -s 256x240 -threads 4 -b 30k -f flv"

#uncomment for better video quality
#video_opts="-f x11grab -r 30 -s 256x240 -i :0.0+0,36 -c:v libx264 -preset slow -pix_fmt yuv420p -s 256x240 -threads 4 -b 30k -f flv"

#uncomment to save stream to file
#stream="/home/pi/Desktop/stream.flv"

while :
do
    avconv $audio_opts $video_opts -aq 5 -t $song_len "$stream" 2>&1 | tee "$logdir/stream.log"
done
