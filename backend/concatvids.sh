#!/bin/sh



ffmpeg -f concat -i $0 -c copy output.mp4
mv output.mp4 ../highlights/