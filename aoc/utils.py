import functools
import itertools
import operator


def most_common(items) -> set:
    counts = dict()
    for i in items:
        counts[i] = counts.get(i, 0) + 1
    mc = max(counts.values())
    return {key for key, count in counts.items() if count == mc}

def merge_dicts(d1: dict, d2: dict, merge) -> dict:
    res = dict(d1.items())
    for k, v in d2.items():
        if k in res:
            res[k] = merge(res[k], v)
        else:
            res[k] = v
    return res

def windowed(it, n):
    iti = iter(it)
    window = list()
    for _ in range(n):
        window.append(next(iti))
    yield window
    for value in iti:
        window = window[1:] + [value]
        yield window

def transpose(lines: iter):
    res = list()
    it = iter(lines)
    line = next(it)
    for value in line:
        res.append([value])
    for line in it:
        for index, value in enumerate(line):
            res[index].append(value)
    return res

def span(values: iter, min_fun = min, max_fun = max):
    min_val = max_val = next(values)
    for value in values:
        min_val = min_fun(min_val, value)
        max_val = max_fun(max_val, value)

    return min_val, max_val

def scan(fun, values: iter, init = None) -> iter:
    if init is None:
        init = next(iter)
    yield init
    for value in values:
        init = fun(init, value)
        yield init

def ordered_pairs(values: iter):
    first = next(values, None)
    while first is not None:
        values, successors = itertools.tee(values)
        for second in successors:
            yield first, second
        first = next(values, None)

def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries"
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = itertools.tee(iterable)
    return itertools.filterfalse(pred, t1), filter(pred, t2)

def vec_vec_mul(v1: tuple, v2: tuple):
    return functools.reduce(operator.add, map(operator.mul, v1, v2))

def mat_vec_mul(v1: tuple, v2: tuple):
    return tuple(vec_vec_mul(row, v2) for row in v1)

def mat_mul(m: tuple, v: tuple) -> tuple:
    vt = transpose(v)
    return tuple((tuple(vec_vec_mul(row, col) for col in vt) for row in m))

def mat_one(n: int) -> tuple:
    return tuple(tuple([0] * k + [1] + [0] * (n - k - 1)) for k in range(n))