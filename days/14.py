from advent_2023 import Day


def parse(input_data):
    lines = input_data.splitlines()
    cols = [""] * len(lines[0])
    for line in lines:
        for j, char in enumerate(line):
            cols[j] += char
    return cols


def puzzle1(input_data):
    cols = parse(input_data)
    n = len(cols[0])
    res = 0
    for col in cols:
        free = 0
        for i, char in enumerate(col):
            if char == "O":
                res += n - i + free
            if char == ".":
                free += 1
            if char == "#":
                free = 0
    return res


def puzzle2(input_data):
    return


if __name__ == "__main__":
    day = Day(
        14,
        test_results=[136],
        input_results=[],
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, test_only=False)
