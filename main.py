import operator
import re
from functools import partial
from aoc.week1 import *
from aoc.week2 import *
from itertools import groupby, chain, dropwhile, tee
from collections import Counter
from functools import reduce
import heapq as hq

def day15(lines):
    def adjacent(height: int, width: int, row: int, col: int):
        if row < height - 1: yield row + 1, col
        if col < width - 1: yield row, col + 1
        if row > 0: yield row - 1, col
        if col > 0: yield row, col - 1

    risks = {(int(row), int(col)): int(risk) for row, cols in enumerate(lines) for col, risk in enumerate(cols)}
    height, width = map(operator.add, reduce(lambda tup1, tup2 : map(max, tup1, tup2), risks), (1, 1))

    def risk(row: int, col: int) -> int:
        return (risks[(row % height, col % width)] + row // height + col // width - 1) % 9 + 1;

    def distances(height: int, width: int, row: int, col: int):
        visited = set()
        shortest = {(0, 0): 0}
        queue = [(0, (0, 0))]
        while queue:
            dist, pos = hq.heappop(queue)
            if pos in visited:
                continue

            if pos == (row, col):
                return dist

            visited.add(pos)
            for adj in adjacent(height, width, *pos):
                if adj not in shortest or dist + risk(*adj) < shortest[adj]:
                    shortest[adj] = dist + risk(*adj)
                    hq.heappush(queue, (shortest[adj], adj))

        return None

    print("Day 15 part 1: {}".format(distances(height, width, height - 1, width - 1)))
    print("Day 15 part 2: {}".format(distances(height * 5, width * 5, height * 5 - 1, width * 5 - 1)))


if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)], 2: [day2p1, day2p2], 3: day3, 4: day4, 5: day5, 6: day6, 7: day7,
        8: day8, 9: day9, 10: day10, 11: day11, 12: day12, 13: day13, 14: day14,
        15: day15}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)
