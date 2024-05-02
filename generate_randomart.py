import copy
import random
import time
from pathlib import Path

from hashime import DrunkenBishop
from PIL import Image

# bishop population size
POPULATION = 300
# number of copies we will make of the surviving bishops
CLONES = 6
# number of surviving bishops
SURVIVING = POPULATION // CLONES

# input and output dirs
FRAMES_DIR = Path('./frames/')
OUTPUT_DIR = Path('./output/')


def fitness(bishop: DrunkenBishop, frame: list[list[int]]) -> int:
    score = 0
    for bishop_row, frame_row in zip(bishop._matrix, frame):
        for bishop_val, frame_val in zip(bishop_row, frame_row):
            if bishop_val > 0 and frame_val > 0:
                score += +10
            elif bishop_val > 0 and frame_val == 0:
                score += -20
    return score


def generate_randomart(img_path: Path) -> None:
    st = time.perf_counter()
    with Image.open(img_path).convert('1') as img:
        raw_data = list(img.getdata())  # type: ignore
        width = img.width
        height = img.height
    frame = [raw_data[i * width : (i + 1) * width] for i in range(height)]

    def frame_fitness(bishop: DrunkenBishop) -> int:
        return fitness(bishop, frame)

    bishops = [
        DrunkenBishop(width=width, height=height) for _ in range(POPULATION)
    ]
    for _ in range(16):
        for bishop in bishops:
            bishop.update(random.randbytes(2))
        bishops.sort(key=frame_fitness, reverse=True)
        slice = bishops[:SURVIVING]
        bishops = slice
        for _ in range(CLONES - 1):
            bishops.extend(copy.deepcopy(slice))
    drunkest_bishop = bishops[0]

    # ./frames/frame0001.png -> ./output/frame0001.txt
    out_path = OUTPUT_DIR / img_path.with_suffix('.txt').name
    with out_path.open('w') as f:
        f.write(
            drunkest_bishop.to_art(
                top_text=img_path.name,
                bottom_text='SHA256',
            )
        )
    et = time.perf_counter()
    print(f'finished {img_path.name} in {et-st:.2f}s.')


if __name__ == '__main__':
    import multiprocessing
    import os

    OUTPUT_DIR.mkdir(exist_ok=True)

    with multiprocessing.Pool() as pool:
        print(f'started with {os.cpu_count()} processes.')
        img_path = list(FRAMES_DIR.glob('*.png'))
        st = time.perf_counter()
        pool.map(generate_randomart, img_path)
        et = time.perf_counter()
        print(f'done in {et - st:.2f}s.')
