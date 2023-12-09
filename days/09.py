import functools
import itertools

from advent_2023 import Day


def reduce_line(line, index):
    line = [int(v) for v in line.split(" ")][::-1]
    res = []
    while any(line):
        res.append(line[index])
        line = [i - j for i, j in itertools.pairwise(line)]
    return res


def puzzle1(input_data):
    predict = [sum(reduce_line(line, 0)) for line in input_data.splitlines()]
    return sum(predict)


def puzzle2(input_data):
    lines = [reduce_line(line, -1)[::-1] for line in input_data.splitlines()]
    lines = [functools.reduce(lambda acc, cur: cur - acc, line) for line in lines]
    return sum(lines)


if __name__ == "__main__":
    day = Day(
        9,
        test_results=[114, 2],
        input_results=[1916822650, 966],
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
