import re

from advent_2023 import Day

day = Day(1, test_results=[142, 281], input_results=[54338, 53389])


def puzzle1(input_data):
    lines = input_data.splitlines()
    digits = [re.findall(r"\d", line) for line in lines]
    return sum([int(d[0]) * 10 + int(d[-1]) for d in digits])


def puzzle2(input_data):
    lines = input_data.splitlines()
    alpha_digits = dict(
        zip(
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
            range(1, 10),
            strict=True,
        )
    )

    convert = (  # noqa: E731
        lambda d: int(alpha_digits[d]) if d in alpha_digits else int(d)
    )

    pattern = f"(\\d|{'|'.join(alpha_digits.keys())})"
    tens = [re.findall(f"^.*?{pattern}", line)[0] for line in lines]
    units = [re.findall(f"^.*{pattern}.*?$", line)[0] for line in lines]
    digits = [convert(ten) * 10 for ten in tens] + [convert(unit) for unit in units]
    return sum(digits)


if __name__ == "__main__":
    day.validate(puzzle1, puzzle2)
