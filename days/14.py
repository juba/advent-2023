import re

from advent_2023 import Day


def parse(lines, direction):
    if direction == "W":
        return lines
    if direction == "E":
        return [line[::-1] for line in lines]
    cols = [""] * len(lines[0])
    for line in lines:
        for j, char in enumerate(line):
            cols[j] += char
    if direction == "S":
        cols = [col[::-1] for col in cols]
    return cols


def reverse_parse(lines, direction):
    if direction == "S":
        lines = [line[::-1] for line in lines]
        return parse(lines, "N")
    else:
        return parse(lines, direction)


def puzzle1(input_data):
    lines = input_data.splitlines()
    cols = parse(lines, "N")
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


def move(line):
    while True:
        oldline = line
        line = re.sub(r"(\.+)O", r"O\1", oldline, count=1)
        if oldline == line:
            break
    return line


def cycle(lines):
    for direction in ("N", "W", "S", "E"):
        lines = parse(lines, direction)
        lines = [move(line) for line in lines]
        lines = reverse_parse(lines, direction)
    return lines


def weight(lines):
    res = 0
    n = len(lines)
    for i, line in enumerate(lines):
        res += (n - i) * line.count("O")
    return res


def puzzle2(input_data):
    lines = input_data.splitlines()
    i = 0
    results = [lines]
    while True:
        i += 1
        lines = cycle(lines)
        if lines in results:
            cycle_length = i - results.index(lines)
            offset = results.index(lines)
            break
        results.append(lines)
    lines = input_data.splitlines()
    n_cycles = offset + (1000000000 - offset) % cycle_length
    for _ in range(n_cycles):
        lines = cycle(lines)
    return weight(lines)


if __name__ == "__main__":
    day = Day(
        14,
        test_results=[136, 64],
        input_results=[103333, 97241],  # > 96962
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
