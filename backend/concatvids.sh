#!/bin/sh

read varlist
ffmpeg -f concat -i $varlist -c copy output.mp4