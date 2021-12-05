import re
from functools import partial
from aoc.week1 import *
from itertools import groupby, chain

def build_board(numbers: list) -> (int, dict):
    return len(numbers), {int(value) : (r, c) for r, row in enumerate(numbers) for c, value in enumerate(row)}

def marked_positions(values: dict, called: set) -> set:
    return {pos for value, pos in values.items() if value in called}

def unmarked_values(values: dict, called: set) -> set:
    return {value for value, pos in values.items() if value not in called}

def winning_values(values: dict, called: set, dim: int) -> set:
    positions = marked_positions(values, called)
    for row, group in groupby(sorted(r for r, c in positions)):
        if len(list(group)) == dim:
            return {value for value, (r, c) in values.items() if r == row}
    for col, group in groupby(sorted(c for r, c in positions)):
        if len(list(group)) == dim:
            return {value for value, (r, c) in values.items() if c == col}
    return set()

def score_board(values: dict, called: list, dim: int) -> tuple:
    cs = set()
    for nr in called:
        cs.add(nr)
        ws = winning_values(values, cs, dim)
        if ws:
            when = len(cs)
            score = sum(unmarked_values(values, cs)) * nr
            return when, score

    raise AssertionError("board is never complete")

def day4(lines):
    first = next(lines)
    drawn = [int(nr) for nr in first.split(",")]
    lines = (line.split() for line in lines)
    next(lines) # skip empty line
    scores = list()
    for k, group in groupby(lines, len):
        if k > 0:
            dim, board = build_board(list(group))
            scores.append(score_board(board, drawn, dim))

    scores = list(sorted(scores))
    print("Day 4 part 1: {}".format(scores[0][1]))
    print("Day 4 part 2: {}".format(scores[-1][1]))

def is_diagonal(x1, y1, x2, y2):
    return x1 != x2 and y1 != y2

def points(x1, y1, x2, y2):
    if x1 == x2:
        return ((x1, y) for y in range(min([y1, y2]), max([y1, y2]) + 1))
    elif y1 == y2:
        return ((x, y1) for x in range(min([x1, x2]), max([x1, x2]) + 1))
    else:
        mx = 1 if x2 > x1 else -1
        my = 1 if y2 > y1 else -1
        return ((x1 + mx * delta, y1 + my * delta) for delta in range(abs(x1 - x2) + 1))

def day5(lines):
    matches = (re.match("(\d+),(\d+) -> (\d+),(\d+)", line) for line in lines)
    all_lines = [(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))) for m in matches]
    straight_lines = list(filter(lambda tuple: not is_diagonal(*tuple), all_lines))

    points_on_straight_lines = sorted(list(chain.from_iterable(points(*xs) for xs in straight_lines)))
    overlaps_straight_lines = (len(list(g)) for point, g in groupby(points_on_straight_lines))

    points_on_all_lines = sorted(list(chain.from_iterable(points(*xs) for xs in all_lines)))
    overlap_all_lines = (len(list(g)) for point, g in groupby(points_on_all_lines))

    at_least_two = lambda x : x > 1

    print("Day 5 part 1: {}".format(sum(1 for x in filter(at_least_two, overlaps_straight_lines))))
    print("Day 5 part 2: {}".format(sum(1 for x in filter(at_least_two, overlap_all_lines))))

if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)],
        2: [day2p1, day2p2],
        3: day3,
        4: day4,
        5: day5}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)

