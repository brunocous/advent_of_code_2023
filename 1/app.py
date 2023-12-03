
from pathlib import Path
from typing import Optional, Generator

def first_digit(s: str)->Optional[int]:
    for char in s:
        if char.isdigit():
            return int(char)
    return None

def last_digit(s: str)->Optional[int]:
    for char in reversed(s):
        if char.isdigit():
            return int(char)
    return None

def parse_line(s: str)->int:
    first = first_digit(s)
    last = last_digit(s)
    if first is None or last is None:
        return 0
    return first*10 + last

def read_file(path: Path)->Generator[None, str, None]:
    with open(path, "r") as f:
        for line in f:
            yield line


def main():
    # read file
    path = Path(__file__).parent / "input.txt"
    total = sum(parse_line(line) for line in read_file(path))
    print(total)

if __name__ == "__main__":
    main()