from pathlib import Path
from typing import Generator, Iterable, List, Tuple
from math import ceil, floor


def read_input(path: Path):
    return tuple(
        tuple(int(n) for n in line.split()) for line in path.read_text().splitlines()
    )


def diff_and_last(values: Iterable[int]) -> Tuple[Tuple[int, ...], int]:
    return (
        tuple(next - current for current, next in zip(values[:-1], values[1:])),
        values[-1] - values[-2],
    )


def extrapolate(values: Iterable[int], reverse: bool = False) -> int:
    if reverse:
        values = tuple(reversed(values))
    current = values
    lasts = [values[-1]]
    while not all(c == 0 for c in current):
        current, last = diff_and_last(current)
        lasts.append(last)
    return sum(lasts)


def main():
    path = Path(__file__).parent / "input.txt"
    values = read_input(path)
    print(sum(extrapolate(v) for v in values))

    print(sum(extrapolate(v, reverse=True) for v in values))


if __name__ == "__main__":
    main()
