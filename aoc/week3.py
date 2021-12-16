import re
from collections import Counter
from aoc.utils import *
from itertools import groupby, chain, dropwhile
import heapq as hq
import operator
from functools import reduce

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

def split_at(xs, n : int):
    return xs[:n], xs[n:]

def day16(lines):
    line = next(lines)
    number = bin(int(line, 16))[2:]
    number = "0" * (len(line) * 4 - len(number)) + number

    def parse(bits: str):
        # first three bits
        version = int(bits[0:3], 2)
        type_id = int(bits[3:6], 2)
        bits = bits[6:]
        packet = dict(version = version, type = type_id)

        if type_id == 4:    # literal value
            literal = str()
            while int(bits[0], 2) == 1:
                literal = literal + bits[1:5]
                bits = bits[5:]
            literal = literal + bits[1:5]
            bits = bits[5:]

            packet.update(literal = int(literal, 2))

        else:   # operator
            length_type = int(bits[0], 2)
            if length_type == 0:
                total_length = int(bits[1:16], 2)
                bits = bits[16:]
                sub = list()
                start = remaining = len(bits)
                while start - remaining < total_length:
                    nested, bits = parse(bits)
                    sub.append(nested)
                    remaining = len(bits)
                packet.update(packets = sub)
            else:
                num_packets = int(bits[1:12], 2)
                bits = bits[12:]
                sub = list()
                for _ in range(num_packets):
                    nested, bits = parse(bits)
                    sub.append(nested)
                packet.update(packets = sub)

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

