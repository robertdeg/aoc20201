import itertools

import networkx as nx
import numpy as np
import math
import re
from collections import Counter, defaultdict
from aoc.utils import *
from itertools import groupby, chain, dropwhile, takewhile, product, permutations, combinations
import heapq as hq
import operator
from functools import reduce, partial


def day22(lines):
    cubes = (
    re.match(r"(on|off) x=([-]?\d+)\.\.([-]?\d+),y=([-]?\d+)\.\.([-]?\d+),z=([-]?\d+)\.\.([-]?\d+)", line).groups() for
    line in lines)
    cubes = (((int(x1), int(x2), int(y1), int(y2), int(z1), int(z2)), s) for s, x1, x2, y1, y2, z1, z2 in cubes)

    def volume(cube: (int, int, int, int, int, int)) -> int:
        x1, x2, y1, y2, z1, z2 = cube
        return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

    def ranges(cube: (int, int, int, int, int, int)) -> iter:
        x1, x2, y1, y2, z1, z2 = cube
        yield x1, x2
        yield y1, y2
        yield z1, z2

    def overlap(cube1: (int, int, int, int, int, int), cube2: (int, int, int, int, int, int)) -> (
    int, int, int, int, int, int):
        for (a1, a2), (b1, b2) in zip(ranges(cube1), ranges(cube2)):
            if min(a1, a2) > max(b1, b2) or max(a1, a2) < min(b1, b2):
                return None

        return tuple(
            chain.from_iterable((max(a1, b1), min(a2, b2)) for (a1, a2), (b1, b2) in zip(ranges(cube1), ranges(cube2))))

    weighted_cubes = Counter()

    remainder = list()
    for cube, state in cubes:
        if max(map(abs, cube)) > 50:
            remainder.append((cube, state))
            continue

        overlapping = list((overlap(cube, other), count) for other, count in weighted_cubes.items() if other is not None)

        for overlap_cube, count in overlapping:
            weighted_cubes[overlap_cube] -= count

        if state == "on":
            weighted_cubes[cube] += 1

    print("Day 22 part 1: {}".format(sum(count * volume(cube) for cube, count in weighted_cubes.items() if cube is not None)))

    for cube, state in remainder:
        overlapping = list((overlap(cube, other), count) for other, count in weighted_cubes.items() if other is not None)

        for overlap_cube, count in overlapping:
            weighted_cubes[overlap_cube] -= count

        if state == "on":
            weighted_cubes[cube] += 1

    print("Day 22 part 1: {}".format(sum(count * volume(cube) for cube, count in weighted_cubes.items() if cube is not None)))
