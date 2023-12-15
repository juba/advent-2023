import functools
import re
from collections import OrderedDict

from advent_2023 import Day


def hashmap(values):
    red = lambda acc, cur: ((acc + ord(cur)) * 17) % 256
    return {val: functools.reduce(red, val, 0) for val in values}


def puzzle1(input_data):
    d = input_data.split(",")
    hm = hashmap(set(d))
    return sum([hm.get(v) for v in d])  # type: ignore


def puzzle2(input_data):
    steps = input_data.split(",")
    steps = [re.split(r"([=-])", step) for step in steps]
    hm = hashmap({step[0] for step in steps})
    boxes = {}
    for box_id in range(256):
        boxes[box_id] = OrderedDict()
    for label, op, focal in steps:
        box = boxes[hm.get(label)]
        if op == "-":
            if label in box:
                del box[label]
        if op == "=":
            box[label] = int(focal)
    return sum(
        [
            (box_id + 1) * slot_id * focal
            for box_id, box in boxes.items()
            for slot_id, focal in enumerate(box.values(), 1)
        ]
    )


if __name__ == "__main__":
    day = Day(
        15,
        test_results=[1320, 145],
        input_results=[508498, 279116],
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
