from advent_2023 import Day

DIRECTIONS1 = {"R": 1, "L": -1, "D": 1j, "U": -1j}


def compute_area(input_data, get_direction_fn, get_length_fn):
    digs = [line.split() for line in input_data.splitlines()]
    current = 0j
    points = [current]
    border = 0
    for dig in digs:
        current = current + get_direction_fn(dig) * get_length_fn(dig)
        border += get_length_fn(dig)
        points.append(current)
    area = 0
    for i, point in enumerate(points[:-1]):
        npoint = points[i + 1]
        area += point.real * npoint.imag - point.imag * npoint.real
    return area / 2 + border / 2 + 1


def puzzle1(input_data):
    get_direction = lambda dig: DIRECTIONS1[dig[0]]
    get_length = lambda dig: int(dig[1])
    return compute_area(input_data, get_direction, get_length)


DIRECTIONS2 = {"0": 1, "2": -1, "1": 1j, "3": -1j}


def puzzle2(input_data):
    get_direction = lambda dig: DIRECTIONS2[dig[2][7]]
    get_length = lambda dig: int(dig[2][2:7], 16)
    return compute_area(input_data, get_direction, get_length)


if __name__ == "__main__":
    day = Day(
        18,
        test_results=[62, 952408144115],
        input_results=[40745, 90111113594927],  # > 17661
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
