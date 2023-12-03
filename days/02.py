import re
from functools import reduce
from itertools import starmap
from operator import ge, mul

from advent_2023 import Day

COLORS = ["red", "green", "blue"]


def puzzle1(input_data):
    lines = input_data.splitlines()
    counts = [
        [
            reduce(lambda x, y: max(int(x), int(y)), re.findall(f"(\\d+) {col}", line), 0)
            for col in COLORS
        ]
        for line in lines
    ]
    max_values = [12, 13, 14]
    res = [all(starmap(ge, zip(max_values, count))) for count in counts]  # noqa: B905
    total = sum([i + 1 for i, v in enumerate(res) if v])
    return total


def puzzle2(input_data):
    lines = input_data.splitlines()
    counts = [
        [
            reduce(lambda x, y: max(int(x), int(y)), re.findall(f"(\\d+) {col}", line), 0)
            for col in COLORS
        ]
        for line in lines
    ]
    res = [reduce(mul, count) for count in counts]
    return sum(res)


if __name__ == "__main__":
    day = Day(2, test_results=[8, 2286], input_results=[2406, 78375])
    day.validate(puzzle1, puzzle2)
