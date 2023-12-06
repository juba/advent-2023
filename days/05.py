import functools
import re

from advent_2023 import Day


def parse(input_data):
    def treat_block(block):
        m = [list(map(int, line.split(" "))) for line in block]
        m = [(source, source + span - 1, dest - source) for dest, source, span in m]
        return m

    blocks = [
        re.sub(r"^.*:\s", "", block).splitlines() for block in input_data.split("\n\n")
    ]
    seeds = [int(v) for v in re.findall(r"\d+", blocks[0][0])]
    maps = [treat_block(block) for block in blocks[1:]]

    return seeds, maps


def get_location(seed, maps):
    for m in maps:
        for start, end, change in m:
            if seed in range(start, end + 1):
                seed = seed + change
                break
    return seed


def puzzle1(input_data):
    seeds, maps = parse(input_data)
    return min([get_location(seed, maps) for seed in seeds])


def cross_mapping(intervals, mapping):
    res = []
    for start, stop in intervals:
        current = start
        for mstart, mstop, moff in mapping:
            if mstart > stop or mstop < current:
                continue
            if current < mstart:
                res.append((current, mstart - 1))
                current = mstart
            res.append((current + moff, min(mstop, stop) + moff))
            current = min(mstop, stop) + 1
        if current <= stop:
            res.append((current, stop))
    return res


def puzzle2(input_data):
    values, maps = parse(input_data)
    maps = [sorted(m, key=lambda x: x[0]) for m in maps]
    intervals = [
        (values[i * 2], values[i * 2] + values[i * 2 + 1] - 1)
        for i in range(len(values) // 2)
    ]
    res = functools.reduce(cross_mapping, maps, intervals)
    return min([r[0] for r in res])


if __name__ == "__main__":
    day = Day(5, test_results=[35, 46], input_results=[600279879, 20191102])
    day.validate(puzzle1, puzzle2, test_only=False)
