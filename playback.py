import argparse
import os
import sys
import time
from pathlib import Path

if sys.platform != 'win32':
    import curses


def playback(stdscr: 'curses._CursesWindow', frames: list[str], nap: float):
    nap = int(1000 * nap)
    curses.use_default_colors()
    for frame in frames:
        stdscr.clear()
        stdscr.addstr(frame)
        stdscr.refresh()
        curses.napms(nap)


def playback_windows(frames: list[str], nap: float):
    for frame in frames:
        st = time.perf_counter()
        os.system('cls')
        print(frame)
        et = time.perf_counter()
        try:
            time.sleep(nap - (et - st))
        except ValueError:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir',
        type=Path,
        default=Path('./output/'),
        help='frame directory (defaults to ./output/)',
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='frames per second (defaults to 30)',
    )
    args = parser.parse_args()

    files = args.dir.glob('*.txt')
    files = list(files)
    files.sort()

    freq = 1 / args.fps
    frames = [f.read_text() for f in files]
    if sys.platform == 'win32':
        playback_windows(frames, freq)
    else:
        curses.wrapper(playback, frames, freq)
