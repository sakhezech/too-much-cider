import argparse
import os
import time
from pathlib import Path

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
    for frame in frames:
        st = time.perf_counter()
        os.system('clear||cls')
        print(frame)
        et = time.perf_counter()
        try:
            time.sleep(freq - (et - st))
        except ValueError:
            pass
