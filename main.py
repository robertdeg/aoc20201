import operator
import re
from functools import partial, reduce
from aoc.week1 import *
from aoc.week2 import *
from aoc.week3 import *
from itertools import groupby, chain, dropwhile, tee
from collections import Counter
import heapq as hq

if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)], 2: [day2p1, day2p2], 3: day3, 4: day4, 5: day5, 6: day6, 7: day7,
        8: day8, 9: day9, 10: day10, 11: day11, 12: day12, 13: day13, 14: day14, 15: day15,
        16: day16}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)
