import re
from collections import Counter
from aoc.utils import *
from itertools import groupby, chain


def day1(n: int, lines):
    values = [int(line) for line in lines]
    windows = windowed(values, n)

    incs = 0
    window = next(windows)
    prev = sum(window)
    for window in windows:
        s = sum(window)
        if s > prev:
            incs += 1
        prev = s

    print("Day 1 part {}: {}".format(1 if n == 1 else 2, incs))

def day2p1(lines):
    entries = (line.split(" ") for line in lines)
    depth = 0
    distance = 0
    for str, value in entries:
        if str == "forward":
            distance += int(value)
        elif str == "up":
            depth -= int(value)
        elif str == "down":
            depth += int(value)
        else:
            raise AssertionError(str)
    print("Day 2 part 1: {}".format(depth * distance))

def day2p2(lines):
    entries = (line.split(" ") for line in lines)
    aim = 0
    depth = 0
    distance = 0
    for str, value in entries:
        if str == "forward":
            distance += int(value)
            depth = depth + aim * int(value)
        elif str == "up":
            aim -= int(value)
        elif str == "down":
            aim += int(value)
        else:
            raise AssertionError(str)
    print("Day 2 part 2: {}".format(depth * distance))

def day3(lines):
    lines = list(lines)
    lines_t = transpose(lines)
    gamma, epsilon = list(), list()
    for bits in lines_t:
        bit = next(iter(most_common(bits)))
        gamma.append(bit)
        epsilon.append('1' if bit == '0' else '0')

    gamma = "".join(gamma)
    epsilon = "".join(epsilon)
    print("Day 3 part 1: {}".format(int(gamma, 2) * int(epsilon, 2)))

    sublines = list(lines)
    index = 0
    while len(sublines) > 1:
        tp = transpose(sublines)
        mc = most_common(tp[index])
        bit = '1' if len(mc) > 1 else next(iter(mc))
        # keep all lines that are the same at current index
        sublines = list(filter(lambda line: line[index] == bit, sublines))
        index += 1

    oxygen = int(sublines[0], 2)

    sublines = list(lines)
    index = 0
    while len(sublines) > 1:
        tp = transpose(sublines)
        mc = most_common(tp[index])
        bit = '1' if len(mc) > 1 else next(iter(mc))
        # keep all lines that differ at current index
        sublines = list(filter(lambda line: line[index] != bit, sublines))
        index += 1

    co2 = int(sublines[0], 2)

    print("Day 3 part 2: {}".format(co2 * oxygen))

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

    overlaps_straight_lines = Counter(chain.from_iterable(points(*xs) for xs in straight_lines)).values()
    overlap_all_lines = Counter(chain.from_iterable(points(*xs) for xs in all_lines)).values()

    at_least_two = lambda x : x > 1

    print("Day 5 part 1: {}".format(sum(1 for x in filter(at_least_two, overlaps_straight_lines))))
    print("Day 5 part 2: {}".format(sum(1 for x in filter(at_least_two, overlap_all_lines))))

