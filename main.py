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

if __name__ == '__main__':
    d = {
        1: [partial(day1, 1), partial(day1, 3)], 2: [day2p1, day2p2], 3: day3, 4: day4, 5: day5, 6: day6, 7: day7,
        8: day8, 9: day9, 10: day10}

    for num, funs in d.items():
        try:
            funs = iter(funs)
        except TypeError:
            funs = [funs]

        for fun in funs:
            with open("input/day{}.txt".format(num)) as file:
                lines = (line.strip() for line in file.readlines())
                fun(lines)
