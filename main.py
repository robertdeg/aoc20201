from functools import partial
from aoc.week1 import *
from itertools import groupby

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
    print("Day 5 part 1: {}".format(scores[0][1]))
    print("Day 5 part 2: {}".format(scores[-1][1]))

if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)],
        2: [day2p1, day2p2],
        3: day3,
        4: day4}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)

