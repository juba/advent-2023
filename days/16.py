import itertools
import math
import re

from advent_2023 import Day

DIRECTIONS = {
    "/": {1: [-1j], -1: [1j], 1j: [-1], -1j: [1]},
    "\\": {1: [1j], -1: [-1j], 1j: [1], -1j: [-1]},
    "-": {1j: [-1, 1], -1j: [-1, 1], 1: [1], -1: [-1]},
    "|": {1: [-1j, 1j], -1: [-1j, 1j], 1j: [1j], -1j: [-1j]},
}


def parse(lines):
    width = len(lines[0])
    height = len(lines)
    grid = {
        j + i * 1j: char for i, line in enumerate(lines) for j, char in enumerate(line)
    }
    return grid, width, height


def get_energized(grid, start):
    beams = [start]
    energized, cache = set(), set()
    while len(beams) > 0:
        for b, _ in enumerate(beams):
            pos = beams[b][0] + beams[b][1]
            tile = grid.get(pos, None)
            if tuple(beams[b]) in cache or tile is None:
                del beams[b]
                continue
            cache.add(tuple(beams[b]))
            energized.add(pos)
            beams[b][0] = pos
            if tile != ".":
                directions = DIRECTIONS.get(tile).get(beams[b][1])
                beams[b][1] = directions[0]
                if len(directions) > 1:
                    beams.append([pos, directions[1]])
    return len(energized)


def puzzle1(input_data):
    grid, _, _ = parse(input_data.splitlines())
    return get_energized(grid, [-1 + 0j, 1])


def puzzle2(input_data):
    grid, width, height = parse(input_data.splitlines())
    starts = (
        [[-1 + i * 1j, 1] for i in range(height)]
        + [[width + i * 1j, -1] for i in range(height)]
        + [[i + -1j, 1j] for i in range(width)]
        + [[i + height * 1j, -1j] for i in range(width)]
    )
    res = [get_energized(grid, start) for start in starts]
    return max(res)


if __name__ == "__main__":
    day = Day(
        16,
        test_results=[46, 51],
        input_results=[7939],
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
