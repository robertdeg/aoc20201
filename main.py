import operator
import re
from functools import partial
from aoc.week1 import *
from aoc.week2 import *
from itertools import groupby, chain, dropwhile, tee
from collections import Counter
from functools import reduce

def day13(lines):
    grouped = map(operator.itemgetter(1), groupby(lines, lambda line : len(line) > 0))
    coordinates = {(int(x), int(y)) for x, y in map(lambda line: line.split(","), next(grouped))}
    next(grouped)
    instructions = map(lambda line: re.match(r"fold along ([x|y])=(\d+)", line).groups(), next(grouped))

    def fold(axis, index, cs):
        if axis == "x":
            return {(2 * int(index) - x if x > int(index) else x, y) for x, y in cs}
        else:
            return {(x, 2 * int(index) - y if y > int(index) else y) for x, y in cs}

    coordinates = fold(*next(instructions), coordinates)
    print("Day 13 part 1: {}".format(len(coordinates)))

    coordinates = reduce(lambda cs, instr: fold(*instr, cs), instructions, coordinates)

    max_x = max(map(operator.itemgetter(0), coordinates))
    max_y = max(map(operator.itemgetter(1), coordinates))

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print("{}".format("#" if (x, y) in coordinates else " "), end="")
        print()

def day14(lines):
    template = next(lines)
    next(lines)
    instructions = (re.match(r"([A-Z][A-Z]) -> ([A-Z])", line).groups() for line in lines)
    rules = {pair : insert for pair, insert in instructions}
    pairs = Counter(a + b for a, b in zip(template, template[1:]))

    def step(counts: Counter) -> Counter:
        result = Counter()
        for pair, count in counts.items():
            insert = rules.get(pair, None)
            if insert:
                result[pair[0] + insert] += count
                result[insert + pair[1]] += count
            else:
                result[pair] += count

        return result

    def score(pairs: Counter) -> Counter:
        charcounts = Counter({template[0]: -1, template[-1]: -1})
        for (a, b), count in pairs.items():
            charcounts[a] += count
            charcounts[b] += count

        charcounts = Counter({c: n // 2 for c, n in charcounts.items()}) + Counter({template[0]: 1, template[-1]: 1})
        min_count = min(charcounts.values())
        max_count = max(charcounts.values())
        return max_count - min_count

    for _ in range(10):
        pairs = step(pairs)

    print("Day 14 part 1: {}".format(score(pairs)))

    for _ in range(30):
        pairs = step(pairs)

    print("Day 14 part 2: {}".format(score(pairs)))

if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)], 2: [day2p1, day2p2], 3: day3, 4: day4, 5: day5, 6: day6, 7: day7,
        8: day8, 9: day9, 10: day10, 11: day11, 12: day12, 13: day13,
        14: day14}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)
