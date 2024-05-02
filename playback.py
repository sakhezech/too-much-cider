import os
import time
from pathlib import Path

if __name__ == '__main__':
    files = Path('./output/').glob('*.txt')
    files = list(files)
    files.sort()

    frames = [f.read_text() for f in files]
    for frame in frames:
        st = time.perf_counter()
        os.system('clear||cls')
        print(frame)
        et = time.perf_counter()
        time.sleep(0.033333 - (et - st))
