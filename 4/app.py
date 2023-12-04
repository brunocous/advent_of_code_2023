from typing import Any, Dict, List
from pathlib import Path

from math import floor


def compute_win_tree(id_to_num_copies_won: Dict[int, int]) -> Dict[int, Any]:
    return {
        id: [id + 1 + i for i in range(num_copies_won)]
        for id, num_copies_won in id_to_num_copies_won.items()
    }


def compute_num_card_visits(win_tree: Dict[int, Any]) -> Dict[int, int]:
    visit_count = {key: 0 for key in win_tree.keys()}
    for card, next_cards in win_tree.items():
        visit_count[card] += 1
        next_card_to_visit: List[int] = next_cards
        while len(next_card_to_visit) > 0:
            next_card = next_card_to_visit.pop()
            visit_count[next_card] += 1
            next_card_to_visit.extend(win_tree[next_card])
    return visit_count


def compute_number_overlapping_numbers(
    winning_numbers: List[int], chosen_numbers: List[int]
) -> int:
    return len(set(winning_numbers).intersection(set(chosen_numbers)))


def compute_points(winning_numbers: List[int], chosen_numbers: List[int]) -> int:
    overlapping_numbers = set(winning_numbers).intersection(set(chosen_numbers))
    if len(overlapping_numbers) == 0:
        return 0
    return 2 ** (len(overlapping_numbers) - 1)


def read_rows(path: Path) -> Dict[int, Any]:
    rows = {}
    with open(path, "r") as f:
        for line in f:
            id, numbers = line.strip().split(":")
            winning_numbers, chosen_numbers = numbers.split("|")
            winning_numbers = [int(n) for n in winning_numbers.split(" ") if n != ""]
            chosen_numbers = [int(n) for n in chosen_numbers.split(" ") if n != ""]
            rows[int(id[-3:])] = {
                "winning_numbers": winning_numbers,
                "chosen_numbers": chosen_numbers,
            }
    return rows


def main():
    # read file
    path = Path(__file__).parent / "input.txt"
    rows = read_rows(path)
    total = sum(
        compute_points(row["winning_numbers"], row["chosen_numbers"])
        for row in rows.values()
    )
    print(total)

    number_overlapping_numbers = {
        key: compute_number_overlapping_numbers(
            row["winning_numbers"], row["chosen_numbers"]
        )
        for key, row in rows.items()
    }
    win_tree = compute_win_tree(number_overlapping_numbers)
    num_card_visits = compute_num_card_visits(win_tree)
    total_part2 = sum(num_card_visits.values())
    print(total_part2)


if __name__ == "__main__":
    main()
