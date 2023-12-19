import ast
import re
from advent_2023 import Day


def parse(input_data):
    conditions, data = (block.splitlines() for block in input_data.split("\n\n"))
    conditions = {
        key: [test.split(":") for test in tests.split(",")]
        for condition in conditions
        for key, tests in re.findall(r"^(.*){(.*)}", condition)
    }
    data = [ast.literal_eval(re.sub(r"([xmsa])=", r'"\1":', d)) for d in data]
    return conditions, data


def apply_rule(cond, a, m, s, x):
    for c in cond:
        if len(c) == 1:
            return c[0]
        if len(c) == 2 and eval(c[0]):
            return c[1]


def puzzle1(input_data):
    conditions, data = parse(input_data)
    accepted = []
    for d in data:
        a, m, s, x = d["a"], d["m"], d["s"], d["x"]
        next_rule = "in"
        while next_rule not in ["A", "R"]:
            cond = conditions[next_rule]
            next_rule = apply_rule(cond, a, m, s, x)
        if next_rule == "A":
            accepted.append(a + m + s + x)
    return sum(accepted)


def update_state(state, test, *, not_=False):
    letter = test[0]
    value = int(test[2:])
    if test[1] == ">":
        if not_ and value <= state[letter][1]:
            state[letter][1] = value
        if not not_ and state[letter][0] < value + 1:
            state[letter][0] = value + 1
    if test[1] == "<":
        if not_ and state[letter][0] <= value:
            state[letter][0] = value
        if not not_ and state[letter][1] > value - 1:
            state[letter][1] = value - 1
    return state


def browse_reverse(state, conditions):
    for k, tests in conditions.items():
        found = False
        for test in tests[::-1]:
            if found:
                state = update_state(state, test[0], not_=True)
            elif test[-1] == state["parent"]:
                found = True
                if len(test) == 2:
                    state = update_state(state, test[0], not_=False)
        if found:
            state["parent"] = k
            break
    return state


def puzzle2(input_data):
    conditions, _ = parse(input_data)
    start_states = []
    for k, tests in conditions.items():
        for i, test in enumerate(tests):
            if test[-1] == "A":
                state = {
                    "a": [1, 4000],
                    "m": [1, 4000],
                    "s": [1, 4000],
                    "x": [1, 4000],
                    "parent": k,
                }
                if len(test) == 2:
                    state = update_state(state, test[0], not_=False)
                for j in range(i - 1, -1, -1):
                    state = update_state(state, tests[j][0], not_=True)
                start_states.append(state)
    final_states = []
    for state in start_states:
        s = state
        while s["parent"] != "in":
            s = browse_reverse(s, conditions)
        final_states.append(s)
    result = [
        (s["a"][1] - s["a"][0] + 1)
        * (s["m"][1] - s["m"][0] + 1)
        * (s["s"][1] - s["s"][0] + 1)
        * (s["x"][1] - s["x"][0] + 1)
        for s in final_states
    ]
    return sum(result)


if __name__ == "__main__":
    day = Day(
        19,
        test_results=[19114, 167409079868000],
        input_results=[386787, 131029523269531],
        test_data_indices=[0, 0],
    )
    day.validate(puzzle1, puzzle2, test_only=False)
