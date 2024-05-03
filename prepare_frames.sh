#!/usr/bin/env sh
if [ ! -f "./input.webm" ]; then
    yt-dlp -o input ${1:-'https://www.youtube.com/watch?v=FtutLA63Cp8'}
fi
mkdir -p ./frames/
ffmpeg  -i input.webm  \
    -f lavfi -i color=gray:size=2x2,scale=${2:-17x9} \
    -f lavfi -i color=black:size=2x2,scale=${2:-17x9} \
    -f lavfi -i color=white:size=2x2,scale=${2:-17x9} \
    -filter_complex "[0:v]scale=${2:-17x9},threshold" \
    ./frames/frame%04d.png
