from collections import Counter

from advent_2023 import Day

HANDS = {
    (5,): "G",
    (1, 4): "F",
    (2, 3): "E",
    (1, 1, 3): "D",
    (1, 2, 2): "C",
    (1, 1, 1, 2): "B",
    (1, 1, 1, 1, 1): "A",
}


def get_sum(pairs):
    res = enumerate([pair.split("-")[1] for pair in sorted(pairs)])
    return sum([(i + 1) * int(v) for i, v in res])


def convert_to_string(c, v, counts):
    return f"{HANDS.get(tuple(sorted(counts.values())))}{c}-{v}"  # type: ignore


def convert1(c, v):
    c = c.translate(str.maketrans("AKQJT98765432", "MLKJIHGFEDCBA"))
    return convert_to_string(c, v, Counter(c))


def puzzle1(input_data):
    return get_sum([convert1(*line.split(" ")) for line in input_data.splitlines()])


def convert2(c, v):
    c = c.translate(str.maketrans("AKQT98765432J", "MLKJIHGFEDCBA"))
    counts = Counter(c)
    if "A" in c and c != "AAAAA":
        nj = counts.pop("A")
        counts[counts.most_common(1)[0][0]] += nj  # type: ignore
    return convert_to_string(c, v, counts)


def puzzle2(input_data):
    return get_sum([convert2(*line.split(" ")) for line in input_data.splitlines()])


if __name__ == "__main__":
    day = Day(7, test_results=[6440, 5905], input_results=[246424613, 248256639])
    day.validate(puzzle1, puzzle2, test_only=False)
