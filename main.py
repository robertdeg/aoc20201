import re
from functools import partial
from aoc.week1 import *
from itertools import groupby, chain
from collections import Counter

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

def fish(counts: Counter, days: int) -> int:
    for _ in range(days):
        next_day = Counter()
        for remaining, count in counts.items():
            if remaining == 0:
                next_day[8] += count
                next_day[6] += count
            else:
                next_day[remaining - 1] += count
        counts = next_day
    return sum(counts.values())

def day6(lines):
    counts = Counter(int(nr) for nr in next(lines).split(","))
    print("Day 6 part 1: {}".format(fish(counts, 80)))
    print("Day 6 part 2: {}".format(fish(counts, 256)))


if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)],
        2: [day2p1, day2p2],
        3: day3,
        4: day4,
        5: day5,
        6: day6}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)

