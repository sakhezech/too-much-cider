import time
from pathlib import Path

files = Path('./output/').glob('*.txt')
files = list(files)
files.sort()

frames = [f.read_text() for f in files]
for frame in frames:
    print(frame)
    time.sleep(0.033333)
