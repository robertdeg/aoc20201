import operator
import re
from functools import partial
from aoc.week1 import *
from itertools import groupby, chain
from collections import Counter
from functools import reduce

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

def cumsum(iterable, function = operator.add):
    sum = next(iterable)
    yield sum
    for value in iterable:
        sum = function(sum, value)
        yield sum

def day7(lines):
    positions = sorted([int(nr) for nr in next(lines).split(",")])
    n = len(positions)
    s = sum(positions)
    ss = sum(p * p for p in positions)
    average_lo, average_hi = s // n, (s - 1) // n + 1
    grouped = [(p, len(list(group))) for p, group in groupby(positions)]
    values = list(value for value, _ in grouped)
    counts = list(cumsum(count for _, count in grouped))
    sums = list(cumsum(value * count for value, count in grouped))

    objective = lambda value, count, sum: value * (2 * count - n) + s - 2 * sum
    min_costs = min(objective(value, count, sum) for value, count, sum in zip(values, counts, sums))

    print("Day 7 part 1: {}".format(min_costs))

    objective = lambda value, count, sum: value * (value * n - 2 * s) + value * (2 * count - n) + s - 2 * sum
    min_costs = min(objective(value, count, sum) for value, count, sum in zip(values, counts, sums))
    sum_at_avg =  sum(p for p in positions if p <= s / n)
    count__at_avg = sum(1 for p in positions if p <= s / n)
    min_costs = min(min_costs,
                 objective(average_lo, count__at_avg, sum_at_avg),
                 objective(average_hi, count__at_avg, sum_at_avg))

    print("Day 7 part 2: {}".format((ss + min_costs) // 2))

def day8(lines):
    count = 0
    total = 0
    for line in lines:
        parts = [part.strip() for part in line.split("|")]
        patterns = [set(p) for p in parts[0].split()]
        output = [p for p in parts[1].split()]
        count += sum(1 for digit in output if len(digit) in [2, 3, 4, 7])

        lookup = {0x24: '1', 0x5d: '2', 0x6d: '3', 0x2e: '4', 0x6b: '5', 0x7b: '6', 0x25: '7', 0x7f: '8', 0x6f: '9', 0x77: '0'}
        grouped = {length: list(g) for length, g in groupby(sorted(patterns, key=len), len)}
        seven = grouped[3][0]
        eight = grouped[7][0]
        four = grouped[4][0]
        one = grouped[2][0]

        #   -- 0 --                  --- 01 ---
        #   1     2                  02      04
        #   |- 3 -|  ==> (hex) ==>   --- 08 ---
        #   4     5                  10      20
        #   |- 6 -|                  --- 40 ---

        segments = dict()
        segments[0] = seven - four
        segments[1] = segments[3] = four - one
        segments[6] = reduce(set.intersection, grouped[5]) - four - seven - one
        segments[4] = eight - four - seven - one - segments[6]

        two = next(nr for nr in grouped[5] if nr.intersection(segments[4]))

        segments[3] = (four - one).intersection(two)
        segments[1] = four - one - segments[3]
        segments[2] = one.intersection(two)
        segments[5] = one - two

        segments = {next(iter(char)): 1 << index for index, char in segments.items()}

        number = int(''.join(lookup[reduce(operator.or_, (segments[char] for char in digit))] for digit in output))
        total = total + number

    print("Day 8 part 1: {}".format(count))
    print("Day 8 part 8: {}".format(total))


if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)], 2: [day2p1, day2p2], 3: day3, 4: day4, 5: day5, 6: day6,
        7: day7,
        8: day8}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)

