from pathlib import Path
from typing import List, Tuple
from math import ceil, floor


def read_input(path: Path):
    for line in path.read_text().splitlines():
        print(line)


def main():
    path = Path(__file__).parent / "input.txt"
    race_records = read_input(path)


if __name__ == "__main__":
    main()
