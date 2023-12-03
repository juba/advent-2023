import re
from collections import defaultdict

from advent_2023 import Day


def get_symbols(lines, valid_fn):
    return [
        i + j * 1j
        for i, line in enumerate(lines)
        for j, char in enumerate(line)
        if valid_fn(char)
    ]


def valid(pos, i, smin, smax):
    return ((pos.real == i) and (pos.imag in (smin - 1, smax))) or (
        pos.real in (i - 1, i + 1) and (pos.imag >= smin - 1 and pos.imag <= smax)
    )


def puzzle1(input_data):
    lines = input_data.splitlines()
    symbols = get_symbols(lines, lambda x: x not in "0123456789.")
    total = 0
    for i, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            smin, smax = m.span()
            for s in symbols:
                if valid(s, i, smin, smax):
                    total += int(m[0])
                    break
    return total


def puzzle2(input_data):
    lines = input_data.splitlines()
    gears = get_symbols(lines, lambda x: x == "*")
    gears_numbers = defaultdict(list)
    for i, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            smin, smax = m.span()
            for g in gears:
                if valid(g, i, smin, smax):
                    gears_numbers[g].append(int(m[0]))
                    continue
    total = sum(
        [n[0] * n[1] for n in gears_numbers.values() if len(n) == 2]  # noqa: PLR2004
    )
    return total


if __name__ == "__main__":
    day = Day(3, test_results=[4361, 467835], input_results=[549908, 81166799])
    day.validate(puzzle1, puzzle2, test_only=False)
