import re
from functools import partial
from aoc.utils import *
from aoc.week1 import *

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

    oxygen = int(str(sublines[0]), 2)

    sublines = list(lines)
    index = 0
    while len(sublines) > 1:
        tp = transpose(sublines)
        mc = most_common(tp[index])
        bit = '1' if len(mc) > 1 else next(iter(mc))
        # keep all lines that differ at current index
        sublines = list(filter(lambda line: line[index] != bit, sublines))
        index += 1

    co2 = int(str(sublines[0]), 2)

    print("Day 3 part 2 : {}".format(co2 * oxygen))

def day4(lines):
    lines = list(lines)

    print("Day 4 part 1 : {}".format(42))
    print("Day 4 part 2 : {}".format(24))

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
                lines = filter(None, (line.strip() for line in file.readlines()))
                fun(lines)

