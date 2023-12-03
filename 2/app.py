from pathlib import Path
from typing import Generator, NamedTuple


class gameSet(NamedTuple):
    max_red: int
    max_blue: int
    max_green: int


class singleSet(NamedTuple):
    red: int = 0
    blue: int = 0 
    green: int = 0

    def is_valid(self, game_set: gameSet) -> bool:
        return (
            self.red <= game_set.max_red
            and self.blue <= game_set.max_blue
            and self.green <= game_set.max_green
        )


# splits a line like Game 85: 14 green, 3 red, 16 blue; 3 blue, 6 green; 12 green, 6 blue, 2 red
# into the id (85) and a collection of single sets.
# It returns the id if each single set is valid, otherwise it returns 0.
def read_line(line: str) -> int:
    parts = line.split(":")
    if len(parts) != 2:
        return 0
    id = int(parts[0].split()[1])
    game_set = gameSet(12, 14, 13)
    for single_set in parts[1].split(";"):
        game_set_dict = {x.split()[1]: int(x.split()[0]) for x in single_set.split(",")}
        single_set = singleSet(**game_set_dict)
        if not single_set.is_valid(game_set):
            return 0
    return id


def read_file(path: Path) -> Generator[None, str, None]:
    with open(path, "r") as f:
        for line in f:
            yield line


def main():
    # read file
    path = Path(__file__).parent / "input.txt"
    total = sum(read_line(line) for line in read_file(path))
    print(total)


if __name__ == "__main__":
    main()
