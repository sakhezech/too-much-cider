import copy
import random
import time
from pathlib import Path

from hashime import DrunkenBishop
from PIL import Image


def fitness(bishop: DrunkenBishop, frame: list[list[int]]) -> int:
    score = 0
    for bishop_row, frame_row in zip(bishop._matrix, frame):
        for bishop_val, frame_val in zip(bishop_row, frame_row):
            if bishop_val > 0 and frame_val > 0:
                score += +10
            elif bishop_val > 0 and frame_val == 0:
                score += -20
    return score


def generate_randomart(
    img_path: Path,
    population: int,
    surviving: int,
    output: Path,
) -> None:
    st = time.perf_counter()
    clones = population // surviving
    with Image.open(img_path).convert('1') as img:
        raw_data = list(img.getdata())  # type: ignore
        width = img.width
        height = img.height
    frame = [raw_data[i * width : (i + 1) * width] for i in range(height)]

    def frame_fitness(bishop: DrunkenBishop) -> int:
        return fitness(bishop, frame)

    bishops = [
        DrunkenBishop(width=width, height=height) for _ in range(population)
    ]
    for _ in range(16):
        for bishop in bishops:
            bishop.update(random.randbytes(2))
        bishops.sort(key=frame_fitness, reverse=True)
        slice = bishops[:surviving]
        bishops = slice
        for _ in range(clones - 1):
            bishops.extend(copy.deepcopy(slice))
    drunkest_bishop = bishops[0]

    if output.is_dir():
        # ./frames/frame0001.png -> ./output/frame0001.txt
        out_path = output / img_path.with_suffix('.txt').name
    else:
        out_path = output

    with out_path.open('w') as f:
        f.write(
            drunkest_bishop.to_art(
                top_text=img_path.name,
                bottom_text='SHA256',
            )
        )
    et = time.perf_counter()
    print(f'finished {img_path} in {et-st:.2f}s.')


if __name__ == '__main__':
    import argparse
    import functools
    import multiprocessing
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--population',
        metavar='POP',
        type=int,
        default=300,
        help='number of nodes in population (defaults to 300)',
    )
    parser.add_argument(
        '--surviving',
        type=int,
        default=50,
        help='number of surviving nodes (defaults to 50)',
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('./frames/'),
        help='input file or directory (defaults to ./frames/)',
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('./output/'),
        help='output file or directory (defaults to ./output/)',
    )
    parser.add_argument(
        '--processes',
        metavar='PROCS',
        type=int,
        default=None,
        help='number of spawned python processes'
        ' (defaults to the number of cpu cores)',
    )
    args = parser.parse_args()

    if args.input.is_dir():
        img_paths = list(args.input.glob('*'))
    else:
        img_paths = [args.input]

    if not args.output.exists() and args.input.is_dir():
        args.output.mkdir(exist_ok=True)

    func = functools.partial(
        generate_randomart,
        population=args.population,
        surviving=args.surviving,
        output=args.output,
    )

    with multiprocessing.Pool(args.processes) as pool:
        img_paths.sort()
        print(f'started with {os.cpu_count()} processes.')
        st = time.perf_counter()
        pool.map(func, img_paths)
        et = time.perf_counter()
        print(f'done in {et - st:.2f}s.')
