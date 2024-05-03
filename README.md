# Too Much Cider

Draw images with randomart.

## Dependencies

For this to work you will need:

- `python` - for running this whole thing.
- `pillow` - for working with images in python.
- `hashime` - for hash visualization.

If you want to work with videos, you will also need:

- `ffmpeg` - for resizing and breaking down videos into individual frames.
- `yt-dlp` - for downloading videos.

You can find `python` [here](https://www.python.org/downloads/)
and `ffmpeg` [here](https://ffmpeg.org/download.html).

`pillow`, `hashime`, and `yt-dlp` are provided in `requirements.txt`.

## Running

First make a virtual environment and install the dependencies.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Drawing an image.

```sh
# Options: `python generate_randomart.py --help`.

python generate_randomart.py -i img.png -o img.txt
# You also can pass in a directory as input and output.
python generate_randomart.py -i ./frames/ -o ./output/
```

Download, resize, turn black and white, and break down into frames a video.

```sh
# First argument - video URL, second argument - resizing dimensions.

./prepare_frames.sh 'https://www.youtube.com/watch?v=FtutLA63Cp8' 17x9
```

Playback a list of drawn images.

```sh
# Options: `python playback.py --help`.

python playback.py --dir ./output/ --fps 30
```
