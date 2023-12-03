from pathlib import Path
from typing import Generator, NamedTuple, Optional, List, Tuple


class Position(NamedTuple):
    row: int
    column: int

    def equal(self, other: "Position") -> bool:
        return self.row == other.row and self.column == other.column


class MultiDigitNumber(NamedTuple):
    value: int
    positions_of_digits: List[Position]

    def number_of_digits(self) -> int:
        return len(self.positions_of_digits)

    def positions_around_the_number(
        self, max_row: int, schematic: List[str]
    ) -> Generator[Position, None, None]:
        for position in self.positions_of_digits:
            row, col = position.row, position.column

            # Directions: up, down, left, right, and diagonals
            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ]

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < max_row and 0 <= new_col < len(schematic[new_row]):
                    yield Position(row=new_row, column=new_col)


class Gear(NamedTuple):
    position: Position

    def positions_around_the_gear(
        self, schematic: List[str]
    ) -> Generator[Position, None, None]:
        row, col = self.position.row, self.position.column

        # Directions: up, down, left, right, and diagonals
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(schematic) and 0 <= new_col < len(schematic[new_row]):
                yield Position(row=new_row, column=new_col)


class GearRatio(NamedTuple):
    gear: Gear
    ratio_numbers: Tuple[MultiDigitNumber, MultiDigitNumber]

    def compute(self) -> int:
        return self.ratio_numbers[0].value * self.ratio_numbers[1].value


def is_symbol(char: str) -> bool:
    assert len(char) == 1
    return (char != ".") and not char.isdigit()


def keep_numbers_with_at_least_one_symbol_around(
    numbers: List[MultiDigitNumber], schematic: List[str]
) -> List[MultiDigitNumber]:
    max_row = len(schematic)
    numbers_to_keep = []

    for number in numbers:
        for position in number.positions_around_the_number(max_row, schematic):
            if is_symbol(schematic[position.row][position.column]):
                numbers_to_keep.append(number)
                break
    return numbers_to_keep


def find_numbers(schematic: List[str]) -> List[MultiDigitNumber]:
    numbers = []
    for row_index, row in enumerate(schematic):
        column_index = 0
        while column_index < len(row):
            char = row[column_index]
            if char.isdigit():
                positions_of_digits = [Position(row=row_index, column=column_index)]
                offset = 1
                while (
                    column_index + offset < len(row)
                    and row[column_index + offset].isdigit()
                ):
                    positions_of_digits.append(
                        Position(row=row_index, column=column_index + offset)
                    )
                    offset += 1
                # create the number
                number_value = "".join(row[pos.column] for pos in positions_of_digits)
                numbers.append(
                    MultiDigitNumber(
                        value=int(number_value),
                        positions_of_digits=positions_of_digits,
                    )
                )
                column_index += offset
            else:
                column_index += 1
    return numbers


def find_gears(schematic: List[str]) -> List[Gear]:
    # only single gears
    gears = []
    for row_index, row in enumerate(schematic):
        column_index = 0
        while column_index < len(row):
            char = row[column_index]
            if char == "*":
                gears.append(
                    Gear(position=Position(row=row_index, column=column_index))
                )
            column_index += 1
    return gears


def find_gear_ratios(
    gears: List[Gear], numbers: List[MultiDigitNumber], schematic: List[str]
) -> List[GearRatio]:
    gear_ratios = []
    for gear in gears:
        adjacent_numbers = []
        numbers_to_check = numbers.copy()
        for pos_to_check in gear.positions_around_the_gear(schematic):
            for number in numbers_to_check:
                if pos_to_check in number.positions_of_digits:
                    adjacent_numbers.append(number)
                    numbers_to_check.remove(number)
                if len(adjacent_numbers) == 2:
                    break
            if len(adjacent_numbers) == 2:
                break
        if len(adjacent_numbers) == 2:
            gear_ratios.append(
                GearRatio(gear=gear, ratio_numbers=tuple(adjacent_numbers))
            )
    return gear_ratios


def read_rows(path: Path) -> List[str]:
    rows = []
    with open(path, "r") as f:
        for line in f:
            rows.append(line.strip())
    return rows


def main():
    # read file
    path = Path(__file__).parent / "input.txt"
    schematic = read_rows(path)
    numbers = find_numbers(schematic)
    good_numbers = keep_numbers_with_at_least_one_symbol_around(numbers, schematic)
    print(f"part 1: {sum(number.value for number in good_numbers)}")

    gears = find_gears(schematic)
    gear_ratios = find_gear_ratios(gears, numbers, schematic)
    print(f"part 2: {sum(gear_ratio.compute() for gear_ratio in gear_ratios)}")


if __name__ == "__main__":
    main()
