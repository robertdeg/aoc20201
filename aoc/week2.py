import re
from collections import Counter
from aoc.utils import *
from itertools import groupby, chain, dropwhile
import operator
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
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

    map = {(int(row), int(col)): int(value) for row, values in enumerate(lines) for col, value in enumerate(values)}
    risk = sum(height + 1 for (x, y), height in map.items() if all(map.get((ax, ay), 10) > height for ax, ay in adjacent(x, y)))
    print("Day 9 part 1: {}".format(risk))

    basins = {(row, col) for (row, col), height in map.items() if height < 9}

    def basin_size(x, y):
        basins.remove((x, y))
        return sum(basin_size(x2, y2) for x2, y2 in adjacent(x, y) if (x2, y2) in basins) + 1

    sizes = list()
    while basins:
        sx, sy = next(iter(basins))
        sizes.append(basin_size(sx, sy))

    print("Day 9 part 2: {}".format(reduce(operator.mul, sorted(sizes)[-3:])))

def day10(lines):
    map = {'(': 1, '[': 2, '{': 3, '<': 4, ')': -1, ']': -2, '}': -3, '>': -4}
    score = {'(': 1, '[': 2, '{': 3, '<': 4, ')': 3, ']': 57, '}': 1197, '>': 25137}

    canceller = lambda seq, e: seq[:-1] if map[e] < 0 and map[seq[-1]] + map[e] == 0 else seq + [e]

    part1, part2 = 0, list()

    for line in lines:
        reduced = list(reduce(canceller, line[1:], list(line[:1])))
        bad_closing = next(dropwhile(lambda x: map[x] > 0, reduced), None)
        if bad_closing is not None:
            part1 += score[bad_closing]
        else:
            part2.append(reduce(lambda s, c: s * 5 + c, (map[c] for c in reversed(reduced)), 0))

    part2 = sorted(part2)
    print("Day 10 part 1: {}".format(part1))
    print("Day 10 part 2: {}".format(part2[len(part2) // 2]))

def day11(lines):
    map = {(int(row), int(col)): int(value) for row, values in enumerate(lines) for col, value in enumerate(values)}
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

    flashes = 0
    steps = 0
    for _ in range(1000):
        map, flashes = step(map, flashes)
        if len({v for v in map.values()}) == 1:
            break

        steps += 1

    print("Day 11 part 1: {}".format(flashes))
    print("Day 11 part 2: {}".format(steps + 1))

def day12(lines):
    edges = list(line.split("-") for line in lines)
    outgoing = {src : list(map(operator.itemgetter(1), g)) for src, g in groupby(sorted(edges, key = operator.itemgetter(0)), key = operator.itemgetter(0))}
    incoming = {src : list(map(operator.itemgetter(0), g)) for src, g in groupby(sorted(edges, key = operator.itemgetter(1)), key = operator.itemgetter(1))}

    def num_paths(v: str, visited: dict, lim: int = 0) -> int:
        if v == "end": return 1
        n = 0
        visited = dict(visited)
        if v.islower(): visited[v] = visited.get(v, 0) + 1
        for w in chain(iter(incoming.get(v, [])), iter(outgoing.get(v, []))):
            if w.isupper():
                n += num_paths(w, visited, lim)
            elif w not in visited or w not in ("start", "end") and sum(1 for _, k in visited.items() if k > 1) < lim:
                n += num_paths(w, visited, lim)
        return n

    print("Day 12 part 1: {}".format(num_paths("start", dict())))
    print("Day 12 part 2: {}".format(num_paths("start", dict(), 1)))

