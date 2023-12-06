from pathlib import Path
from typing import List, Tuple
from math import ceil, floor


def read_input(path: Path) -> List[Tuple[int, int]]:
    times_str, distances_str = (line for line in path.read_text().splitlines())
    times, distances = (
        [int(t.strip()) for t in s.split()[1:]] for s in (times_str, distances_str)
    )
    return list(zip(times, distances))


def compute_roots_of_equation(a: int, b: int, c: int) -> Tuple[float, float]:
    delta = b**2 - 4 * a * c
    return ((-b + delta**0.5) / (2 * a), (-b - delta**0.5) / (2 * a))


def compute_number_of_ways_to_win(records: List[Tuple[int, int]]) -> int:
    all_ways_to_win = []
    for time, distance in records:
        a = -1
        b = time
        c = -distance
        roots = compute_roots_of_equation(a, b, c)
        print(roots)
        all_ways_to_win.append(abs(int(ceil(roots[1])) - int(floor(roots[0]))) - 1)
    # product af all ways to win
    return all_ways_to_win


def main():
    path = Path(__file__).parent / "input.txt"
    race_records = read_input(path)
    num_ways_to_win = compute_number_of_ways_to_win(race_records)
    p = 1
    for way in num_ways_to_win:
        p *= way
    print(f"part 1: {p}")

    path2 = Path(__file__).parent / "input2.txt"
    race_records2 = read_input(path2)
    print(compute_number_of_ways_to_win(race_records2))


if __name__ == "__main__":
    main()
