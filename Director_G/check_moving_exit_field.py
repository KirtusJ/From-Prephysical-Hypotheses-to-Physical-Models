"""Enumerate left-exit writes in the co-moving coordinates of a binary field."""
from collections import Counter
from itertools import product
from math import comb


def panel(n, speed):
    counts = Counter()
    for word in product((1,-1), repeat=n):
        x, rail, sign = 0, 1, 1
        marks = set()
        for t, direction in enumerate(word):
            if direction == -1:
                marks.symmetric_difference_update((x-speed*t,))
                sign *= rail
            x, rail = x+direction, direction
        counts[x,rail,tuple(sorted(marks))] += sign
    out = Counter()
    for (x, _, _), a in counts.items():
        out[x] += a*a
    return out, len(counts)


for n in range(1, 12):
    fast, labels = panel(n, 2)
    assert labels == 2**n
    assert fast == {n-2*k:comb(n,k) for k in range(n+1)}
    same, _ = panel(n, 1)
    unmarked = Counter()
    for word in product((1,-1), repeat=n):
        sign = (-1)**sum(a == b == -1 for a, b in zip(word, word[1:]))
        unmarked[sum(word),word[-1]] += sign
    assert all(same[x] == sum(unmarked[x,d]**2 for d in (1,-1)) for x in fast)
print("Spatial panels agree at speeds one and two through 11 ticks.")
