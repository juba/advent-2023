import itertools
import math
import re

from advent_2023 import Day


def parse(input_data):
    directions, nodes = input_data.split("\n\n")
    nodes = [re.findall(r"\w{3}", line) for line in nodes.splitlines()]
    nodes = {k: {"L": left, "R": right} for k, left, right in nodes}
    return directions, nodes


def get_length(start, nodes, directions, condition):
    d = itertools.cycle(directions)
    current, i = start, 0
    while not condition(current):
        i += 1
        current = nodes.get(current).get(next(d))
    return i


def puzzle1(input_data):
    directions, nodes = parse(input_data)
    return get_length("AAA", nodes, directions, lambda x: x == "ZZZ")


def puzzle2(input_data):
    directions, nodes = parse(input_data)
    lengths = [
        get_length(key, nodes, directions, lambda x: x.endswith("Z"))
        for key in nodes.keys()
        if key.endswith("A")
    ]
    return math.lcm(*lengths)


if __name__ == "__main__":
    day = Day(8, test_results=[2, 6], input_results=[20777], test_data_indices=[0, 2])
    day.validate(puzzle1, puzzle2, test_only=False)
