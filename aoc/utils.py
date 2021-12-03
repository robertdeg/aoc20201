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

def transpose(lines):
    res = list()
    it = iter(lines)
    line = next(it)
    for value in line:
        res.append([value])
    for line in it:
        for index, value in enumerate(line):
            res[index].append(value)
    return res

