import re

from advent_2023 import Day


def puzzle1(input_data):
    lines = input_data.splitlines()
    digits = [re.findall(r"\d", line) for line in lines]
    return sum([int(d[0]) * 10 + int(d[-1]) for d in digits])


def puzzle2(input_data):
    lines = input_data.splitlines()
    alpha = dict(
        zip(  # noqa: B905
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
            range(1, 10),
        )
    )

    pattern = f"(\\d|{'|'.join(alpha.keys())})"
    tens = [re.findall(f"^.*?{pattern}", line)[0] for line in lines]
    units = [re.findall(f"^.*{pattern}.*?$", line)[0] for line in lines]
    digits = [int(alpha.get(ten, ten)) * 10 for ten in tens] + [
        int(alpha.get(unit, unit)) for unit in units
    ]
    return sum(digits)


if __name__ == "__main__":
    day = Day(1, test_results=[142, 281], input_results=[54338, 53389])
    day.validate(puzzle1, puzzle2)
