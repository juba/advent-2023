import re

from advent_2023 import Day

NEXT = {
    "|": {(1j, "L"), (1j, "J"), (-1j, "7"), (-1j, "F"), (1j, "|"), (-1j, "|")},
    "-": {(-1, "L"), (-1, "F"), (1, "J"), (1, "7"), (1, "-"), (-1, "-")},
    "L": {(-1j, "|"), (-1j, "7"), (-1j, "F"), (1, "-"), (1, "J"), (1, "7")},
    "J": {(-1j, "|"), (-1j, "7"), (-1j, "F"), (-1, "-"), (-1, "F"), (-1, "L")},
    "7": {(1j, "|"), (1j, "L"), (1j, "J"), (-1, "-"), (-1, "F"), (-1, "L")},
    "F": {(1j, "|"), (1j, "L"), (1j, "J"), (1, "-"), (1, "7"), (1, "J")},
    "S": {
        (1j, "|"),
        (-1j, "|"),
        (1, "-"),
        (-1, "-"),
        (1j, "L"),
        (-1, "L"),
        (1j, "J"),
        (1, "J"),
        (-1j, "7"),
        (1, "7"),
        (-1j, "F"),
        (-1, "F"),
    },
}


def parse(input_data):
    lines = input_data.splitlines()
    grid = {
        i + j * 1j: lines[j][i]
        for j, _ in enumerate(lines)
        for i, _ in enumerate(lines[j])
    }
    start = list(grid.values()).index("S")
    start = list(grid.keys())[start]
    return grid, start


def browse(grid, start):
    prev, current = (None, start)
    loop = []
    looped = False
    while not looped:
        for move, pipe in NEXT.get(grid[current]):
            if current + move == prev:
                continue
            next_pipe = grid.get(current + move, None)
            if next_pipe == "S":
                loop.append(current)
                looped = True
                break
            if next_pipe == pipe:
                loop.append(current)
                prev = current
                current += move
                break
    return loop


def puzzle1(input_data):
    loop = browse(*parse(input_data))
    dist = len(loop) / 2
    return dist


# def plot(input_data, loop, inside):
#     lines = input_data.splitlines()
#     for i, line in enumerate(lines):
#         for j, char in enumerate(line):
#             if j + i * 1j in inside:
#                 print(".", end="")
#             elif j + i * 1j in loop:
#                 print(char, end="")
#             else:
#                 print("O", end="")
#         print()


# FIXME: this is really slow, and for it to be a real solution "S" must be
# replaced by its real value (it worked with our input but wouldn't on another)


def is_inside(tile, grid, vert):
    left = ("").join(
        [
            grid.get(i + tile.imag * 1j)
            for i in range(int(tile.real))
            if i + tile.imag * 1j in vert
        ]
    )
    left_edges = len(re.findall(r"(\||L7|FJ)", left))
    return left_edges % 2 == 1


def puzzle2(input_data):
    grid, start = parse(input_data)
    loop = browse(grid, start)
    vert = [l for l in loop if grid.get(l) != "-"]
    inside = [k for k in grid.keys() if k not in loop and is_inside(k, grid, vert)]
    return len(inside)


if __name__ == "__main__":
    day = Day(
        10,
        test_results=[8, 8],
        input_results=[6831, 305],
        test_data_indices=[8, 8],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
