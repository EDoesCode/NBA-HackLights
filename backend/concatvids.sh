#!/bin/sh

read varlist

ffmpeg -f concat -i $varlist -c copy output.mp4
mv output.mp4 ../highlights/