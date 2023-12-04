import re

from advent_2023 import Day


def get_wins(lines):
    lines = [line.split("|") for line in lines]
    get_numbers = lambda x: set(re.findall(r"(\d+)(?: |$)", x))
    return [
        len(get_numbers(line[0]).intersection(get_numbers(line[1]))) for line in lines
    ]


def puzzle1(input_data):
    wins = get_wins(input_data.splitlines())
    return sum([pow(2, win - 1) for win in wins if win > 0])


def puzzle2(input_data):
    wins = get_wins(input_data.splitlines())
    copies = [1] * len(wins)
    for i, win in enumerate(wins):
        s = slice(i + 1, i + win + 1)
        copies[s] = (x + copies[i] for x in copies[s])
    return sum(copies)


if __name__ == "__main__":
    day = Day(4, test_results=[13, 30], input_results=[17803, 5554894])
    day.validate(puzzle1, puzzle2, test_only=False)
