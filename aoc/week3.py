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


def day15(lines):
    def adjacent(height: int, width: int, row: int, col: int):
        if row < height - 1: yield row + 1, col
        if col < width - 1: yield row, col + 1
        if row > 0: yield row - 1, col
        if col > 0: yield row, col - 1

    risks = {(int(row), int(col)): int(risk) for row, cols in enumerate(lines) for col, risk in enumerate(cols)}
    height, width = map(operator.add, reduce(lambda tup1, tup2: map(max, tup1, tup2), risks), (1, 1))

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


def split_at(xs, n: int):
    return xs[:n], xs[n:]


def day16(lines):
    line = next(lines)
    number = bin(int(line, 16))[2:]
    number = "0" * (len(line) * 4 - len(number)) + number

    def parse(bits: str):
        version = int(bits[0:3], 2)
        type_id = int(bits[3:6], 2)
        bits = bits[6:]
        packet = dict(version=version, type=type_id)

        if type_id == 4:  # literal value
            literal = str()
            while int(bits[0], 2) == 1:
                literal = literal + bits[1:5]
                bits = bits[5:]
            literal = literal + bits[1:5]
            bits = bits[5:]

            packet.update(literal=int(literal, 2))

        else:  # operator
            length_type = int(bits[0], 2)
            sub = list()
            if length_type == 0:
                total_length = int(bits[1:16], 2)
                bits = bits[16:]
                start = remaining = len(bits)
                while start - remaining < total_length:
                    nested, bits = parse(bits)
                    sub.append(nested)
                    remaining = len(bits)
            else:
                num_packets = int(bits[1:12], 2)
                bits = bits[12:]
                for _ in range(num_packets):
                    nested, bits = parse(bits)
                    sub.append(nested)

            packet.update(packets=sub)

        return packet, bits

    def versions(packet: dict):
        return reduce(operator.add, (versions(sub) for sub in packet.get("packets", list())), [packet["version"]])

    def evaluate(packet: dict) -> int:
        type_id = packet["type"]
        sub_packets = map(evaluate, packet.get("packets", list()))
        if type_id == 0:
            return sum(sub_packets)
        elif type_id == 1:
            return reduce(operator.mul, sub_packets)
        elif type_id == 2:
            return min(sub_packets)
        elif type_id == 3:
            return max(sub_packets)
        elif type_id == 4:
            return packet["literal"]
        elif type_id == 5:
            first, second = sub_packets
            return 1 if first > second else 0
        elif type_id == 6:
            first, second = sub_packets
            return 1 if first < second else 0
        elif type_id == 7:
            first, second = sub_packets
            return 1 if first == second else 0

    packet, bits = parse(number)
    print("Day 16 part 1: {}".format(sum(versions(packet))))
    print("Day 16 part 2: {}".format(evaluate(packet)))


def day17(lines):
    xmin, xmax, ymin, ymax = map(int, re.match(r"target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)",
                                               next(lines).strip()).groups())
    max_y_velocity = -1 - ymin
    min_x_velocity = math.ceil((-1 + math.sqrt(1 + 8 * xmin)) / 2)

    print("Day 17 part 1: {}".format(max_y_velocity * (max_y_velocity + 1) // 2))

    vdistance = lambda velocity, steps: (2 * velocity - steps + 1) * steps // 2
    hdistance = lambda velocity, steps: (2 * velocity - steps + 1) * steps // 2 if steps < velocity else velocity * (
            velocity + 1) // 2

    def valid_steps(yvel):
        distances = ((steps, vdistance(yvel, steps)) for steps in itertools.count(1))
        return takewhile(lambda x: x[1] >= ymin, dropwhile(lambda x: x[1] > ymax, distances))

    # min speed needed to reach more than min_distance in given nr. of steps
    def min_speed(steps: int, min_distance: int):
        return (2 * min_distance - steps * (steps - 1) - 1) // (2 * steps) + 1

    my_answers = set()
    for vy in range(ymin, -ymin):
        for steps, vdist in valid_steps(vy):
            max_x_velocity = (2 * xmax + steps * (steps - 1)) // (2 * steps) + 1
            for vx in range(min_x_velocity, max_x_velocity):
                if xmin <= hdistance(vx, steps) <= xmax:
                    my_answers.add((vx, vy))

    print("Day 17 part 2: {}".format(len(my_answers)))


def day18(lines):
    def split(value):
        if isinstance(value, int):
            return (False, value) if value < 10 else (True, [value // 2, (value - 1) // 2 + 1])
        else:
            left, right = value
            changed, left = split(left)
            if changed:
                return True, [left, right]

            changed, right = split(right)
            return changed, [left, right]

    def inc_rightmost(tree, value: int):
        return tree + value if isinstance(tree, int) else [tree[0], inc_rightmost(tree[1], value)]

    def inc_leftmost(tree, value: int):
        return tree + value if isinstance(tree, int) else [inc_leftmost(tree[0], value), tree[1]]

    def magnitude(tree):
        if isinstance(tree, int):
            return tree
        else:
            left, right = tree
            return 3 * magnitude(left) + 2 * magnitude(right)

    def explode(tree, depth: int = 0):
        if isinstance(tree, int): return False, tree, (0, 0)
        left, right = tree
        if depth >= 4 and isinstance(left, int) and isinstance(right, int):
            return True, 0, (left, right)
        else:
            exploded, left, lcarry = explode(left, depth + 1)
            if exploded:
                right = inc_leftmost(right, lcarry[1])
                return True, [left, right], (lcarry[0], 0)

            exploded, right, rcarry = explode(right, depth + 1)
            if exploded:
                left = inc_rightmost(left, rcarry[0])

            return exploded, [left, right], (lcarry[0], rcarry[1])

    def add(tree, number):
        tree = [tree, number]
        exploded, tree, carry = explode(tree)
        while exploded:
            exploded, tree, carry = explode(tree)

        changed, tree = split(tree)
        while changed:
            exploded, tree, carry = explode(tree)
            while exploded:
                exploded, tree, carry = explode(tree)
            changed, tree = split(tree)

        return tree

    numbers = list(eval(line) for line in lines)
    print("Day 18 part 1: {}".format(magnitude(reduce(add, numbers))))
    print("Day 18 part 2: {}".format(max(magnitude(add(x, y)) for x, y in combinations(numbers, 2))))


def day19(lines):
    mhdist = lambda xs, ys: (sum(abs(x - y) for x, y in zip(xs, ys)), sum((x - y) ** 2 for x, y in zip(xs, ys)))
    diff = lambda xs, ys: type(xs)(x - y for x, y in zip(xs, ys))
    permute = lambda values, permutation: type(values)(values[i] for i in permutation)
    rotations = lambda xs, ys: set(
        p for p in permutations([0, 1, 2]) if all(abs(x) - abs(y) == 0 for x, y in zip(permute(xs, p), ys)))
    elemdiv = lambda xs, ys: type(xs)(x // y for x, y in zip(xs, ys))
    project = lambda xs, rotation, muls, translation: type(xs)(
        map(operator.add, map(operator.mul, permute(xs, rotation), muls), translation))

    def match(target: set, source: set):
        """returns projection of yss space to xss space"""
        for tvec, svec in product(target, source):
            tdists = {mhdist(x, tvec): diff(x, tvec) for x in target if x != tvec}
            sdists = {mhdist(y, svec): diff(y, svec) for y in source if y != svec}
            shared = set(tdists).intersection(set(sdists))
            if len(shared) > 10:
                rotation = next(
                    iter(reduce(set.intersection, (rotations(sdists[dist], tdists[dist]) for dist in shared))))
                factors = next(elemdiv(permute(sdists[dist], rotation), tdists[dist]) for dist in shared)
                return rotation, factors, diff(tvec, project(svec, rotation, factors, (0, 0, 0)))
        return None

    scanners = dict()
    for valid, g in groupby(lines, lambda line: len(line) > 0):
        if valid:
            nr = int(re.match(r"--- scanner (\d+) ---", next(g)).group(1))
            vectors = [tuple(map(int, line.split(","))) for line in g]
            scanners[nr] = vectors

    # returns the projections of all scanners in the coordinate space of scanner scanner_id
    def transformations(scanner_id, visited=set()) -> dict:
        visited.add(scanner_id)
        result = dict()
        for i, projection in ((i, match(scanners[scanner_id], scanners[i])) for i in scanners if i not in visited):
            if projection is not None:
                sub = transformations(i, visited)
                result[i] = (projection, sub)
        return result

    def beacons(base, scanner_id, visited=set()):
        visited.add(scanner_id)
        result = set(scanners[scanner_id])
        for i, (projection, reachable) in base.items():
            result = result.union(set(map(lambda v: project(v, *projection), beacons(reachable, i, visited))))
        return result

    def positions(base, scanner_id, visited=set()):
        visited.add(scanner_id)
        result = set()
        for i, (projection, reachable) in base.items():
            result.add(projection[2])
            result = result.union(set(project(pos, *projection) for pos in positions(reachable, i, visited)))
        return result

    projections = transformations(0)
    all_beacons = beacons(projections, 0)
    all_scanners = positions(projections, 0)
    print("Day 19 part 1: {}".format(len(all_beacons)))
    print("Day 19 part 2: {}".format(
        max(sum(abs(x - y) for x, y in zip(xs, ys)) for xs, ys in ordered_pairs(iter(all_scanners)))))


def day20(lines):
    def nbors(row: int, col: int) -> iter:
        return ((row - 1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col - 1), (row, col), (row, col + 1),
                (row + 1, col - 1), (row + 1, col), (row + 1, col + 1))

    def output(algorithm: str, image: dict, coordinate: tuple, outside: int) -> int:
        bits = "".join(str(image.get(nbor, outside)) for nbor in nbors(*coordinate))
        dec = int(bits, 2)
        return algorithm[dec]

    def dimensions(image: dict) -> tuple:
        tmin = lambda t1, t2: (min(t1[0], t2[0]), min(t1[1], t2[1]))
        tmax = lambda t1, t2: (max(t1[0], t2[0]), max(t1[1], t2[1]))
        return tuple(reduce(tmin, image)), tuple(reduce(tmax, image))

    def enhance(algorithm: str, image: dict, outside: int):
        (top, left), (bottom, right) = dimensions(image)
        return algorithm[int(str(outside) * 9, 2)], \
               {(row, col) : output(algorithm, image, (row, col), outside)
                for row in range(top - 2, bottom + 3)
                for col in range(left - 2, right + 3)}

    pixels_lit = lambda image: sum(1 for _, val in image.items() if val == 1)

    algorithm = [1 if v == '#' else 0 for v in next(lines)]
    _, image = next(lines), {(row, col) : 1 if c == "#" else 0 for row, line in enumerate(lines) for col, c in enumerate(line)}

    outside = 0
    for _ in range(2):
        outside, image = enhance(algorithm, image, outside)

    print("Day 20 part 1: {}".format(pixels_lit(image)))

    for _ in range(48):
        outside, image = enhance(algorithm, image, outside)

    print("Day 20 part 2: {}".format(pixels_lit(image)))


def day21(lines):
    add = lambda xs, ys: tuple(x + y for x, y in zip(xs, ys))
    mul = lambda x, ys: tuple(x * y for y in ys)
    advance = lambda pos, delta: (pos + delta - 1) % 10 + 1

    start1, = re.match(r"Player 1 starting position: (\d+)", next(lines)).groups()
    start2, = re.match(r"Player 2 starting position: (\d+)", next(lines)).groups()

    scores = [0, 0]
    positions = [int(start1), int(start2)]
    rolls = 0

    delta = 1 + 2 + 3
    rolls = 0
    while max(scores) < 1000:
        positions[rolls % 2] = (positions[rolls % 2] + delta - 1) % 10 + 1
        scores[rolls % 2] += positions[rolls % 2]
        rolls += 1
        delta = (delta + 9) % 10

    print("Day 21 part 1: {}".format(min(scores) * rolls * 3))

    counts = Counter(sum(xs) for xs in product({1, 2, 3}, repeat=3))

    def wins(positions: (int, int), scores: (int, int)) -> (int, int):
        p1, p2 = positions
        s1, s2 = scores
        if s1 >= 21:
            return 1, 0
        elif s2 >= 21:
            return 0, 1

        win1, win2 = reduce(add, (mul(counts[delta], wins((p2, advance(p1, delta)), (s2, s1 + advance(p1, delta)))) for delta in range(3, 10)))
        return win2, win1

    print("Day 21 part 2: {}".format(wins((int(start1), int(start2)), (0, 0))))
