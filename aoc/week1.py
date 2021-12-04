from aoc.utils import *

def day1(n: int, lines):
    values = [int(line) for line in lines]
    windows = windowed(values, n)

    incs = 0
    window = next(windows)
    prev = sum(window)
    for window in windows:
        s = sum(window)
        if s > prev:
            incs += 1
        prev = s

    print("Day 1 part {}: {}".format(1 if n == 1 else 2, incs))

def day2p1(lines):
    entries = (line.split(" ") for line in lines)
    depth = 0
    distance = 0
    for str, value in entries:
        if str == "forward":
            distance += int(value)
        elif str == "up":
            depth -= int(value)
        elif str == "down":
            depth += int(value)
        else:
            raise AssertionError(str)
    print("Day 2 part 1: {}".format(depth * distance))

def day2p2(lines):
    entries = (line.split(" ") for line in lines)
    aim = 0
    depth = 0
    distance = 0
    for str, value in entries:
        if str == "forward":
            distance += int(value)
            depth = depth + aim * int(value)
        elif str == "up":
            aim -= int(value)
        elif str == "down":
            aim += int(value)
        else:
            raise AssertionError(str)
    print("Day 2 part 2: {}".format(depth * distance))

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

    oxygen = int(sublines[0], 2)

    sublines = list(lines)
    index = 0
    while len(sublines) > 1:
        tp = transpose(sublines)
        mc = most_common(tp[index])
        bit = '1' if len(mc) > 1 else next(iter(mc))
        # keep all lines that differ at current index
        sublines = list(filter(lambda line: line[index] != bit, sublines))
        index += 1

    co2 = int(sublines[0], 2)

    print("Day 3 part 2: {}".format(co2 * oxygen))

