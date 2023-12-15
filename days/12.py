import re

from advent_2023 import Day


def parse(input_data):
    lines = [line.split() for line in input_data.splitlines()]
    return [(k, [int(val) for val in v.split(",")]) for k, v in lines]


def clean_left(d, v):
    d = re.sub(r"^\.+", "", d)
    while (
        d.startswith("#") and len(v) > 0 and re.match(r"^[#?]{" + str(v[0]) + "}[.?]", d)
    ):
        d = d[v[0] + 1 :]
        v = v[1:]
        d = re.sub(r"^\.+", "", d)
    return d, v


def possible(d, v):
    d = re.sub(r"^\.+", "", d)
    if len(d) < sum(v) + len(v) - 1:
        return False
    if len(v) > 0 and (m := re.match(r"^([#?]+)\.", d)):
        if "#" in m.group(1) and len(m.group(1)) < v[0]:
            return False
    if len(v) > 0 and (m := re.match(r"^(#+)", d)):
        if len(m.group(1)) > v[0]:
            return False
    if len(v) == 1:
        if m := re.search(r"(#.*#)", d):
            if len(m.group(1)) > v[0]:
                return False
    if d.count("#") > sum(v):
        return False
    if d.count("#") + d.count("?") < sum(v):
        return False
    return True


def count(d, v):
    if not possible(d, v):
        return 0
    d, v = clean_left(d, v)
    if not possible(d, v):
        return 0
    if "?" not in d:
        return 1
    if len(v) == 0 and "#" not in d:
        return 1
    if len(v) == 0 and "#" in d:
        return 0
    d_sharp = d.replace("?", "#", 1)
    d_dot = d.replace("?", ".", 1)
    return count(d_sharp, v) + count(d_dot, v)


def puzzle1(input_data):
    lines = parse(input_data)
    res = [count(d, v) for d, v in lines]
    return sum(res)


def puzzle2(input_data):
    return


if __name__ == "__main__":
    day = Day(
        12,
        test_results=[21],
        input_results=[7379],  # < 8071, > 6627, != 8068, != 7892, != 7890, != 8010
        test_data_indices=[1, 1],
    )
    day.validate(puzzle1, test_only=False)
