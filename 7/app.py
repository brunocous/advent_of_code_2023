from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple, Callable
from enum import Enum
import functools
from math import ceil, floor


card_ordering = "23456789TJQKA"
card_ordering_joker = "J23456789TJQKA"


class Type(Enum):
    FiveOfAKind = 1
    FourOfAKind = 2
    FullHouse = 3
    ThreeOfAKind = 4
    TwoPair = 5
    OnePair = 6
    HighCard = 7


multiples_count_to_type = {
    5: Type.FiveOfAKind,
    41: Type.FourOfAKind,
    32: Type.FullHouse,
    311: Type.ThreeOfAKind,
    221: Type.TwoPair,
    2111: Type.OnePair,
    11111: Type.HighCard,
}


def jokerify_count(hand: str, counts: List[int]) -> List[int]:
    joker_count = hand.count("J")

    if joker_count == 0:
        return counts
    elif joker_count == 5:
        return [5]
    elif joker_count == 4:
        return [5]
    elif joker_count == 3:
        if counts == [3, 1, 1]:
            return [4, 1]
        else:
            return [5]
    elif joker_count == 2:
        if counts == [2, 1, 1, 1]:
            return [3, 1, 1]
        elif counts == [2, 2, 1]:
            return [4, 1]
        else:
            return [5]
    elif joker_count == 1:
        if counts == [1, 1, 1, 1, 1]:
            return [2, 1, 1, 1]
        elif counts == [2, 1, 1, 1]:
            return [3, 1, 1]
        elif counts == [2, 2, 1]:
            return [3, 2]
        elif counts == [3, 1, 1]:
            return [4, 1]
        else:
            return [5]
    else:
        raise ValueError("Invalid joker count")


def compute_hand_type(hand: List[str], jokerify=False) -> Type:
    card_to_count = {}
    for card in hand:
        card_to_count[card] = card_to_count.get(card, 0) + 1
    counts = [i for i in sorted(card_to_count.values(), reverse=True)]
    if jokerify:
        counts = jokerify_count(hand, counts)
    return multiples_count_to_type[int("".join([str(i) for i in counts]))]


def compare_hands(
    item1: Tuple[str, int], item2: Tuple[str, int], jokerify: bool = False
) -> int:
    same_hand_f = functools.partial(compare_same_type_hands, jokerify=jokerify)
    hand1_type, hand2_type = (
        compute_hand_type(i[0], jokerify=jokerify) for i in (item1, item2)
    )
    if hand1_type.value < hand2_type.value:
        return -1
    elif hand1_type.value > hand2_type.value:
        return 1
    else:
        return same_hand_f(item1[0], item2[0])


def compare_same_type_hands(
    hand1: List[str], hand2: List[str], jokerify: bool = False
) -> int:
    ordering = card_ordering_joker if jokerify else card_ordering
    for l, r in zip(hand1, hand2):
        if ordering.index(l) < ordering.index(r):
            return 1
        elif ordering.index(l) > ordering.index(r):
            return -1


def read_input(path: Path):
    hands_and_bids = path.read_text().split()
    return list(zip(hands_and_bids[::2], [int(i) for i in hands_and_bids[1::2]]))


def compute_ranking(
    hands_and_bids: List[Tuple[str, int]], jokerify: bool = False
) -> List[int]:
    cmp_f = (
        functools.partial(compare_hands, jokerify=True) if jokerify else compare_hands
    )
    hands_and_bids.sort(key=functools.cmp_to_key(cmp_f), reverse=True)
    return hands_and_bids


def compute_winnings(
    rankings: List[Tuple[str, int]],
) -> int:
    winnings = 0
    for i, (_, bid) in enumerate(rankings):
        winnings += (i + 1) * bid
    return winnings


def main():
    path = Path(__file__).parent / "input.txt"
    hands_and_bids = read_input(path)
    ranking = compute_ranking(hands_and_bids)
    print(ranking)
    print(f"Total winnings: {compute_winnings(ranking)}")

    ranking_jokerified = compute_ranking(hands_and_bids, jokerify=True)
    print(ranking_jokerified)
    print(f"Total winnings: {compute_winnings(ranking_jokerified)}")


if __name__ == "__main__":
    main()
