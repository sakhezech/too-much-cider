import random
from pathlib import Path

from hashime import DrunkenBishop
from PIL import Image


def fitness(
    bishop: DrunkenBishop,
    frame: list[list[int]],
    hit_score: int,
    miss_score: int,
) -> int:
    score = 0
    for bishop_row, frame_row in zip(bishop._matrix, frame):
        for bishop_val, frame_val in zip(bishop_row, frame_row):
            if bishop_val > 0 and frame_val > 0:
                score += hit_score
            elif bishop_val > 0 and frame_val == 0:
                score += miss_score
    return score


def get_drunkest_bishop(
    img_path: Path,
    population: int,
    surviving: int,
    generations: int,
    bytes_fed: int,
    hit_score: int,
    miss_score: int,
) -> DrunkenBishop:
    with Image.open(img_path).convert('1') as img:
        raw_data = list(img.getdata())  # type: ignore
        width = img.width
        height = img.height
    frame = [raw_data[i * width : (i + 1) * width] for i in range(height)]

    def frame_fitness(bishop: DrunkenBishop) -> int:
        return fitness(bishop, frame, hit_score, miss_score)

    bishops = [
        DrunkenBishop(width=width, height=height) for _ in range(population)
    ]
    for _ in range(generations):
        for bishop in bishops:
            bishop.update(random.randbytes(bytes_fed))
        bishops.sort(key=frame_fitness, reverse=True)
        top_bishops = bishops[:surviving]
        bad_bishops = bishops[surviving:]

        for i, bad_bishop in enumerate(bad_bishops):
            good_bishop = top_bishops[i % surviving]
            bad_bishop._x = good_bishop._x
            bad_bishop._y = good_bishop._y
            bad_bishop._matrix = [
                [v for v in row] for row in good_bishop._matrix
            ]
    return bishops[0]


def write_randomart(
    bishop: DrunkenBishop,
    img_path: Path,
    output: Path,
    bottom_text: str,
) -> None:
    if output.is_dir():
        # ./frames/frame0001.png -> ./output/frame0001.txt
        out_path = output / img_path.with_suffix('.txt').name
    else:
        out_path = output

    with out_path.open('w') as f:
        f.write(
            bishop.to_art(
                top_text=img_path.name,
                bottom_text=bottom_text,
            )
        )


if __name__ == '__main__':
    import argparse
    import multiprocessing
    import os
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--population',
        metavar='POP',
        type=int,
        default=1000,
        help='number of nodes in population (defaults to 1000)',
    )
    parser.add_argument(
        '--surviving',
        type=int,
        default=10,
        help='number of surviving nodes (defaults to 10)',
    )
    parser.add_argument(
        '--hit-score',
        type=int,
        default=10,
        help='points added when randomart char falls in the frame stencil'
        ' (defaults to 10)',
    )
    parser.add_argument(
        '--miss-score',
        type=int,
        default=-20,
        help="points added when randomart char doesn't fall in the frame"
        ' stencil (defaults to -20)',
    )
    parser.add_argument(
        '--generations',
        metavar='GEN',
        type=int,
        default=16,
        help='number of generations (defaults to 16)',
    )
    parser.add_argument(
        '--bytes-fed',
        metavar='BYTES',
        type=int,
        default=2,
        help='number of bytes fed into the algorithm each generation'
        ' (defaults to 2)',
    )
    parser.add_argument(
        '--processes',
        metavar='PROCS',
        type=int,
        default=None,
        help='number of spawned python processes'
        ' (defaults to the number of cpu cores)',
    )
    parser.add_argument(
        '--bottom-text',
        metavar='TEXT',
        type=str,
        default=None,
        help='text on the bottom of the frame (defaults to None)',
    )
    parser.add_argument(
        '-i',
        '--input',
        type=Path,
        default=Path('./frames/'),
        help='input file or directory (defaults to ./frames/)',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=Path,
        default=Path('./output/'),
        help='output file or directory (defaults to ./output/)',
    )
    args = parser.parse_args()

    if args.input.is_dir():
        img_paths = list(args.input.glob('*'))
    else:
        img_paths = [args.input]

    if not args.output.exists() and args.input.is_dir():
        args.output.mkdir(exist_ok=True)

    def func(img_path: Path) -> None:
        st = time.perf_counter()
        drunkest_bishop = get_drunkest_bishop(
            img_path,
            population=args.population,
            surviving=args.surviving,
            generations=args.generations,
            bytes_fed=args.bytes_fed,
            hit_score=args.hit_score,
            miss_score=args.miss_score,
        )
        write_randomart(
            drunkest_bishop,
            img_path,
            args.output,
            args.bottom_text,
        )
        et = time.perf_counter()
        print(f'finished {img_path} in {et-st:.2f}s.')

    with multiprocessing.Pool(args.processes) as pool:
        img_paths.sort()
        print(f'started with {args.processes or os.cpu_count()} process(es).')
        st = time.perf_counter()
        pool.map(func, img_paths)
        et = time.perf_counter()
        print(f'done in {et - st:.2f}s.')
