from collections import namedtuple
from heapq import heappop, heappush

from advent_2023 import Day


def parse(lines):
    goal = len(lines[0]) - 1 + (len(lines) - 1) * 1j
    grid = {
        j + i * 1j: int(char)
        for i, line in enumerate(lines)
        for j, char in enumerate(line)
    }
    return grid, goal


Pos = namedtuple("Pos", ["pos", "dir", "straight"])


def new_dirs_puzzle1(pos):
    new_dirs = [-1j, 1j] if pos.dir in [-1 + 0j, 1 + 0j] else [-1 + 0j, 1 + 0j]
    return [*new_dirs, pos.dir] if pos.straight < 3 else new_dirs


def new_dirs_puzzle2(pos):
    new_dirs = (
        [-4j, 4j] if pos.dir / abs(pos.dir) in [-1 + 0j, 1 + 0j] else [-4 + 0j, 4 + 0j]
    )
    return [*new_dirs, pos.dir] if pos.straight < 10 else new_dirs


def next_positions(pos, grid, new_dirs):
    new_pos = []
    for new_dir in new_dirs:
        if pos.pos + new_dir in grid:
            n_moves = int(abs(new_dir))
            cost_to_add = sum(
                [grid[pos.pos + new_dir / n_moves * (i + 1)] for i in range(n_moves)]
            )
            new_pos.append(
                (
                    Pos(
                        pos=pos.pos + new_dir,
                        dir=new_dir / n_moves,
                        straight=pos.straight + n_moves
                        if pos.dir == new_dir / n_moves
                        else n_moves,
                    ),
                    cost_to_add,
                )
            )
    return new_pos


def find_cost(grid, goal, start, new_dirs_fn):
    frontier = []
    entry_count = 0
    heappush(frontier, (0, entry_count, start))
    cost = {start: 0}

    while frontier:
        _, _, current = heappop(frontier)
        new_dirs = new_dirs_fn(current)
        new_positions = next_positions(current, grid, new_dirs)
        if current.pos == goal:
            break
        for new_pos, cost_to_add in new_positions:
            new_cost = cost[current] + cost_to_add
            if new_pos not in cost or new_cost < cost[new_pos]:
                entry_count += 1
                cost[new_pos] = new_cost
                heappush(frontier, (new_cost, entry_count, new_pos))
    return min([v for (c, d, s), v in cost.items() if c == goal])


def puzzle1(input_data):
    grid, goal = parse(input_data.splitlines())
    start = Pos(pos=0j, dir=1 + 0j, straight=1)
    return find_cost(grid, goal, start, new_dirs_puzzle1)


def puzzle2(input_data):
    grid, goal = parse(input_data.splitlines())
    start = Pos(pos=0j, dir=4 + 0j, straight=4)
    return find_cost(grid, goal, start, new_dirs_puzzle2)


if __name__ == "__main__":
    day = Day(
        17,
        test_results=[102, 71],
        input_results=[1263, 1411],
        test_data_indices=[0, 3],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
