import operator
import re
from functools import partial
from aoc.week1 import *
from itertools import groupby, chain
from collections import Counter
from functools import reduce


def day8(lines):
    count = 0
    total = 0
    for line in lines:
        parts = [part.strip() for part in line.split("|")]
        patterns = [set(p) for p in parts[0].split()]
        output = [p for p in parts[1].split()]
        count += sum(1 for digit in output if len(digit) in [2, 3, 4, 7])

        lookup = {0x24: '1', 0x5d: '2', 0x6d: '3', 0x2e: '4', 0x6b: '5', 0x7b: '6', 0x25: '7', 0x7f: '8', 0x6f: '9',
                  0x77: '0'}
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


def day9(lines):
    def adjacent(x, y):
        yield x + 1, y
        yield x - 1, y
        yield x, y + 1
        yield x, y - 1

    map = {(int(row), int(col)): int(value) for row, values in enumerate(lines) for col, value in enumerate(values)}
    heights = (height for (x, y), height in map.items() if all(map.get((ax, ay), 10) > height for ax, ay in adjacent(x, y)))
    risk = sum(h + 1 for h in heights)

    basins = {(row, col) for (row, col), height in map.items() if height < 9}

    def flood_fill(basin, x, y):
        basin.add( (x, y) )
        basins.remove((x, y))
        for x2, y2 in adjacent(x, y):
            if (x2, y2) in basins:
                flood_fill(basin, x2, y2)

    sizes = list()
    while basins:
        sx, sy = next(iter(basins))
        basin = set()
        flood_fill(basin, sx, sy)
        sizes.append( len(basin) )

    print("Day 9 part 1: {}".format(risk))
    print("Day 9 part 8: {}".format(reduce(operator.mul, sorted(sizes)[-3:])))


if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)], 2: [day2p1, day2p2], 3: day3, 4: day4, 5: day5, 6: day6, 7: day7,
        8: day8, 9: day9}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)
