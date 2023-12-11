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


def blocked(tile, loop, grid):
    criterion_vertical = (
        lambda x: "-" in x or ("L" in x and "7" in x) or ("F" in x and "J" in x)
    )
    loop_up = [grid.get(l) for l in loop if l.real == tile.real and l.imag < tile.imag]
    if not criterion_vertical(loop_up):
        return False
    loop_down = [grid.get(l) for l in loop if l.real == tile.real and l.imag > tile.imag]
    if not criterion_vertical(loop_down):
        return False
    criterion_horizontal = (
        lambda x: "|" in x or ("L" in x and "7" in x) or ("F" in x and "J" in x)
    )
    loop_left = [grid.get(l) for l in loop if l.imag == tile.imag and l.real < tile.real]
    if not criterion_horizontal(loop_left):
        return False
    loop_right = [grid.get(l) for l in loop if l.imag == tile.imag and l.real > tile.real]
    if not criterion_horizontal(loop_right):
        return False
    return True


def propagate_outside(inside, outside):
    changed = True
    while changed:
        changed = False
        for tile in inside:
            neighbors = [
                tile - 1 - 1j,
                tile - 1j,
                tile + 1 - 1j,
                tile - 1,
                tile + 1,
                tile - 1 + 1j,
                tile + 1j,
                tile + 1 + 1j,
            ]
            if any(neigh in outside for neigh in neighbors):
                outside.append(tile)
                inside.remove(tile)
                changed = True
    return inside, outside


def plot(input_data, loop, inside, outside):
    lines = input_data.splitlines()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if j + i * 1j in outside:
                print("O", end="")
            elif j + i * 1j in inside:
                print(" ", end="")
            elif j + i * 1j in loop:
                print(char, end="")
            else:
                print("!", end="")
        print()


def puzzle2(input_data):
    grid, start = parse(input_data)
    loop = browse(grid, start)
    tiles = {k: blocked(k, loop, grid) for k, v in grid.items() if k not in loop}
    inside = [k for k, v in tiles.items() if v]
    outside = [k for k, v in tiles.items() if not v]
    inside, outside = propagate_outside(inside, outside)
    plot(input_data, loop, inside, outside)
    return len(inside)


if __name__ == "__main__":
    day = Day(
        10,
        test_results=[8, 8],
        input_results=[6831],
        test_data_indices=[8, 8],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
