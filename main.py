import operator
import re
from functools import partial
from aoc.week1 import *
from aoc.week2 import *
from itertools import groupby, chain
from collections import Counter
from functools import reduce

def day10(lines):
    scoresx = {'(': 1, '[': 2, '{': 3, '<': 4, ')': 3, ']': 57, '}': 1197, '>': 25137}
    opening = lambda c : 1 if c in "<{[(" else -1

    def score(line):
        stack = list(" ")
        for c in line:
            stack.append(c)
            if stack[-1] in ">}])" and stack[-2] in "<{[(":
                if stack[-2:] == list("<>")or stack[-2:] == list("()") or stack[-2:] == list("[]") or stack[-2:] == list("{}"):
                    stack = stack[:-2]
                else:
                    return scoresx[stack[-1]], None
        return 0, stack[1:]

    compl = lambda line: reduce(lambda s, c: s * 5 + c, (scoresx[c] for c in reversed(line)), 0)

    scores = [score(line) for line in lines]

    ss = list(sorted(compl(line) for s, line in scores if s == 0))
    print("Day 10 part 1: {}".format(sum(s for s, stack in scores)))
    print("Day 10 part 2: {}".format(ss[len(ss) // 2]))

def day11(lines):
    map = {(int(row), int(col)): int(value) for row, values in enumerate(lines) for col, value in enumerate(values)}
    dims_x = min(x for x, y in map), max(x for x, y in map) + 1
    dims_y = min(y for x, y in map), max(y for x, y in map) + 1
    def adjacent(x, y):
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x-1,y-1), (x+1,y+1), (x-1,y+1), (x+1,y-1)

    def step(values: dict, flashes: int) -> (dict, int):
        result = dict()
        for pos in values:
            result[pos] = values[pos] + 1

        n = 1
        while n > 0:
            n = 0
            for pos, value in result.items():
                if value > 9:
                    n += 1
                    result[pos] = -1
                    for nbor in adjacent(*pos):
                        if result.get(nbor, -1) > -1:
                            result[nbor] += 1

            flashes += n

        for pos, value in result.items(): result[pos] = 0 if value < 0 else value

        return result, flashes

    def print_map(values: dict):
        for y in range(*dims_y):
            for x in range(*dims_x):
                value = values[(y, x)]
                if value > 0:
                    print(value, end='')
                else:
                    print(' ', end='')
            print()
        print()

    flashes = 0
    steps = 0
    print_map(map)
    for _ in range(1000):
        map, flashes = step(map, flashes)
        if len({v for v in map.values()}) == 1:
            break

        steps += 1
        # print_map(map)

    print("Day 11 part 1: {}".format(flashes))
    print("Day 11 part 2: {}".format(steps + 1))

def day12(lines):
    edges = list(line.split("-") for line in lines)
    outgoing = {src : list(map(operator.itemgetter(1), g)) for src, g in groupby(sorted(edges, key = operator.itemgetter(0)), key = operator.itemgetter(0))}
    incoming = {src : list(map(operator.itemgetter(0), g)) for src, g in groupby(sorted(edges, key = operator.itemgetter(1)), key = operator.itemgetter(1))}

    def num_paths(v: str, visited: dict) -> int:
        if v == "end": return 1
        n = 0
        visited = dict(visited)
        if v.islower(): visited[v] = visited.get(v, 0) + 1
        for w in chain(iter(incoming.get(v, [])), iter(outgoing.get(v, []))):
            if w.isupper():
                n += num_paths(w, visited)
            elif w not in visited or w not in ("start", "end") and sum(1 for _, k in visited.items() if k > 1) == 0:
                n += num_paths(w, visited)
        return n

    print("Day 12 part 1: {}".format(num_paths("start", dict())))

if __name__ == '__main__':
    d = {
        #1: [partial(day1, 1), partial(day1, 3)], 2: [day2p1, day2p2], 3: day3, 4: day4, 5: day5, 6: day6, 7: day7,
        #8: day8, 9: day9, 10: day10, 11: day11,
        12: day12}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = [line.strip() for line in file.readlines()]
                fun(lines)
