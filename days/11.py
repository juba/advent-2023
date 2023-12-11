import itertools

from advent_2023 import Day


def parse(input_data, expansion):
    lines = input_data.splitlines()
    galaxies = [
        i + j * 1j
        for j, _ in enumerate(lines)
        for i, _ in enumerate(lines[j])
        if lines[j][i] == "#"
    ]
    cols = {int(g.real) for g in galaxies}
    empty_cols = [i for i in range(max(cols)) if i not in cols]
    rows = {int(g.imag) for g in galaxies}
    empty_rows = [i for i in range(max(rows)) if i not in rows]
    offset = {g: 0 + 0 * 1j for g in galaxies}
    for g in galaxies:
        offset[g] += expansion * len([row for row in empty_rows if g.imag > row]) * 1j
        offset[g] += expansion * len([col for col in empty_cols if g.real > col])
    galaxies = [g + offset[g] for g in galaxies]
    return galaxies


def sum_distances(galaxies):
    pairs = itertools.combinations(galaxies, 2)
    dist = [abs(g1.real - g2.real) + abs(g1.imag - g2.imag) for g1, g2 in pairs]
    return sum(dist)


def puzzle1(input_data):
    galaxies = parse(input_data, expansion=1)
    return sum_distances(galaxies)


def puzzle2(input_data):
    galaxies = parse(input_data, expansion=999999)
    return sum_distances(galaxies)


if __name__ == "__main__":
    day = Day(
        11,
        test_results=[374, 82000210],
        input_results=[10154062, 553083047914],
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
