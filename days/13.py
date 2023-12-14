from advent_2023 import Day


def parse_block(block):
    lines = block.splitlines()
    row = [""] * len(lines)
    col = [""] * len(lines[0])
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            row[i] += "1" if char == "#" else "0"
            col[j] += "1" if char == "#" else "0"
    return row, col


def find_axis(values):
    n = len(values)
    axes = [i for i in range(n - 1) if values[i] == values[i + 1]]
    for axis in axes:
        left = values[max([0, 2 * axis - n + 2]) : axis + 1]
        right = values[min([n, 2 * (axis + 1) - 1]) : axis : -1]
        if left == right:
            return axis + 1
    return 0


def puzzle1(input_data):
    rows, cols = zip(*[parse_block(block) for block in input_data.split("\n\n")])
    rows = [find_axis(row) for row in rows]
    cols = [find_axis(col) for col in cols]
    return sum(rows) * 100 + sum(cols)


def find_diff(values):
    n = len(values)
    for i in range(n - 1):
        left = values[max([0, 2 * i - n + 2]) : i + 1]
        right = values[min([n, 2 * (i + 1) - 1]) : i : -1]
        diffs = [
            bin(int(i, 2) ^ int(j, 2)).count("1") for i, j in zip(left, right) if i != j
        ]
        if diffs == [1]:
            return i + 1
    return 0


def puzzle2(input_data):
    rows, cols = zip(*[parse_block(block) for block in input_data.split("\n\n")])
    rows = [find_diff(row) for row in rows]
    cols = [find_diff(col) for col in cols]
    return sum(rows) * 100 + sum(cols)


if __name__ == "__main__":
    day = Day(
        13,
        test_results=[405, 400],
        input_results=[34889, 34224],
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
