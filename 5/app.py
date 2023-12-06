from typing import Any, Callable, Dict, Generator, Iterable, List, NamedTuple
from pathlib import Path
from functools import partial
from tqdm import tqdm


class AlemenacMapping(NamedTuple):
    destination_categ: int
    source_categ: int
    range: int

    def is_in_source_range(self, id: int) -> bool:
        return self.source_categ <= id < self.source_categ + self.range

    def map(self, id: int) -> int:
        if self.is_in_source_range(id):
            return self.destination_categ + (id - self.source_categ)
        return id


def compute_min_location_of_seeds(
    seeds: Iterable[int], chain_of_mappings: List[List[AlemenacMapping]]
) -> int:
    mapping_functions = construct_mapping_functions(chain_of_mappings)
    min_location = 9999999999999
    for seed in tqdm(seeds):
        for f in mapping_functions:
            seed = f(seed)
        min_location = min(min_location, seed)
    return min_location


def read_seeds(section_data):
    return [int(s) for s in section_data.split()]


def read_mapping_section(section_data: str) -> List[AlemenacMapping]:
    mappings = []
    for l in section_data.split("\n"):
        destination_categ, source_categ, range = l.split()
        mappings.append(
            AlemenacMapping(int(destination_categ), int(source_categ), int(range))
        )
    return mappings


def construct_mapping_functions(
    chain_of_mappings: List[List[AlemenacMapping]],
) -> List[Callable]:
    def mapping_f(id: int, mapping_ranges: List[AlemenacMapping]):
        for single_range in mapping_ranges:
            if single_range.is_in_source_range(id):
                return single_range.map(id)
        return id

    return [
        partial(mapping_f, mapping_ranges=mapping_ranges)
        for mapping_ranges in chain_of_mappings
    ]


def compute_seed_ids(raw_seed_pairs: List[int]) -> Generator[None, None, int]:
    for start, seed_range in zip(raw_seed_pairs[::2], raw_seed_pairs[1::2]):
        for s in range(start, start + seed_range):
            yield s


def read_rows(path: Path):
    with open(path, "r") as file:
        content = file.read()

    sections = content.split("\n\n")  # Splitting by double newline

    section_to_read_function = {
        "seeds": read_seeds,
        "seed-to-soil map": read_mapping_section,
        "soil-to-fertilizer map": read_mapping_section,
        "fertilizer-to-water map": read_mapping_section,
        "water-to-light map": read_mapping_section,
        "light-to-temperature map": read_mapping_section,
        "temperature-to-humidity map": read_mapping_section,
        "humidity-to-location map": read_mapping_section,
    }
    chain_of_mappings = []
    for section in sections:
        title, *data = section.split("\n")
        title = title.split(":")[0]
        section_data = "\n".join(data)
        chain_of_mappings.append(section_to_read_function[title](section_data))
    return chain_of_mappings[0], chain_of_mappings[1:]


def main():
    # read file
    path = Path(__file__).parent / "input.txt"
    seeds, mappings = read_rows(path)
    print(seeds)
    min_location = compute_min_location_of_seeds(seeds, mappings)
    print(f"min of locations: {min_location}")

    print(
        f"min of seed ranges: {compute_min_location_of_seeds(compute_seed_ids(seeds), mappings)}"
    )


if __name__ == "__main__":
    main()
