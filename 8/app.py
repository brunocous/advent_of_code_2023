from pathlib import Path
from typing import Dict, List, Tuple
from math import gcd


def read_input(path: Path) -> List[str]:
    with open(path, "r") as file:
        data = file.readlines()
    lines = tuple(line.strip() for line in data)
    graph = {}
    for l in lines[2:]:
        p = l.split("=")
        graph[p[0].strip()] = p[1].split(",")

    graph = {
        k: {"L": v[0].replace("(", "").strip(), "R": v[1].replace(")", "").strip()}
        for k, v in graph.items()
    }

    return lines[0], graph


def num_steps_to_traverse(
    commands: str,
    graph: Dict[str, Dict[str, str]],
    start: str = "AAA",
    end: str = "ZZZ",
) -> int:
    steps = [start]
    current_node = start
    at_end = False
    while not at_end:
        for c in commands:
            next_step = graph[current_node][c]
            steps.append(next_step)
            current_node = next_step

            if next_step == end:
                at_end = True
                break
    return len(steps) - 1


def find_lcm(numbers: List[int]) -> int:
    lcm = 1
    for i in numbers:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def num_steps_to_parallel_traverse(
    commands: str, graph: Dict[str, Dict[str, str]]
) -> int:
    start_nodes = {k for k in graph.keys() if k.endswith("A")}
    num_steps = []
    for start_node in start_nodes:
        counter = 0
        current_node = start_node
        at_end = False
        while not at_end:
            for c in commands:
                next_step = graph[current_node][c]
                current_node = next_step
                counter += 1

                if next_step.endswith("Z"):
                    at_end = True
                    num_steps.append(counter)
                    break
    return find_lcm(num_steps)


def main():
    path = Path(__file__).parent / "input.txt"
    commands, graph = read_input(path)
    # print(num_steps_to_traverse(commands, graph))

    print(num_steps_to_parallel_traverse(commands, graph))


if __name__ == "__main__":
    main()
