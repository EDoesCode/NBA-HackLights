#!/bin/sh


read varname
rm file.mp4
ffmpeg -i $varname -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 file.mp4
