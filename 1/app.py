from pathlib import Path
from typing import Optional, Generator

phonetic_to_digit = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def first_phonetic_digit(s: str) -> Optional[int]:
    first_occurance_digit = {}
    for d in phonetic_to_digit.keys():
        # return index in string if found
        if d in s:
            first_occurance_digit[d] = s.find(d)

    if len(first_occurance_digit) == 0:
        return None
    # return the digit with the smallest index
    return phonetic_to_digit[min(first_occurance_digit, key=first_occurance_digit.get)]


def last_phonetic_digit(s: str) -> Optional[int]:
    last_occurance_digit = {}
    for d in phonetic_to_digit.keys():
        # return index in string if found
        if d in s:
            last_occurance_digit[d] = s.rfind(d)

    if len(last_occurance_digit) == 0:
        return None
    # return the digit with the biggest index
    return phonetic_to_digit[max(last_occurance_digit, key=last_occurance_digit.get)]


def first_digit(s: str) -> Optional[int]:
    for char in s:
        if char.isdigit():
            return int(char)
    return None


def last_digit(s: str) -> Optional[int]:
    for char in reversed(s):
        if char.isdigit():
            return int(char)
    return None


def parse_line(s: str) -> int:
    first = first_digit(s)
    last = last_digit(s)
    if first is None or last is None:
        return 0
    return first * 10 + last


def parse_line_part2(s: str) -> int:
    first = first_phonetic_digit(s)
    last = last_phonetic_digit(s)
    if first is None or last is None:
        return 0
    return first * 10 + last


def read_file(path: Path) -> Generator[None, str, None]:
    with open(path, "r") as f:
        for line in f:
            yield line


def main():
    # read file
    path = Path(__file__).parent / "input.txt"
    total = sum(parse_line(line) for line in read_file(path))
    print(total)

    total_part2 = sum(parse_line_part2(line) for line in read_file(path))
    print(total_part2)


if __name__ == "__main__":
    main()
