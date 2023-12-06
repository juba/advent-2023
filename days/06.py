import math
import re
from functools import reduce
from operator import mul

from advent_2023 import Day


def compute_root(time, distance):
    delta = time**2 - 4 * distance
    if delta <= 0:
        return 0
    r1, r2 = (time - math.sqrt(delta)) / 2, (time + math.sqrt(delta)) / 2
    r1 = math.ceil(r1) if math.ceil(r1) != r1 else r1 + 1
    r2 = math.floor(r2) if math.floor(r2) != r2 else r2 - 1
    return r2 - r1 + 1


def puzzle1(input_data):
    times = [int(val) for val in re.findall(r"\d+", input_data.splitlines()[0])]
    dists = [int(val) for val in re.findall(r"\d+", input_data.splitlines()[1])]
    res = [compute_root(time, dist) for time, dist in zip(times, dists)]
    return reduce(mul, res)


def puzzle2(input_data):
    time = int(re.sub(r"[^\d]", "", input_data.splitlines()[0]))
    dist = int(re.sub(r"[^\d]", "", input_data.splitlines()[1]))
    return compute_root(time, dist)


if __name__ == "__main__":
    day = Day(6, test_results=[288, 71503], input_results=[449820, 42250895])
    day.validate(puzzle1, puzzle2, test_only=False)
