"""Verify the gain-neutral return period for every indicated finite ring.

Input is a ring N and four homogeneous gain labels a,b,c,d for transitions
RR, RL, LR, LL. Group operations use additive notation in this executable.
One computation uses the integer label relation modulo the subgroup generated
by b+c-a-d. The independent graph calculation uses actual outgoing arcs only.
Run with Python 3.9+; no third-party packages. Prints one JSON summary.
"""
from collections import Counter, deque
from itertools import product
from math import gcd, lcm
import json


class ProductGroup:
    def __init__(self, moduli):
        self.moduli = moduli
        self.zero = tuple(0 for _ in moduli)
        self.elements = list(product(*(range(m) for m in moduli)))

    def scale(self, times, x):
        return tuple(times * value % m for value, m in zip(x, self.moduli))

    def add(self, x, y):
        return tuple((a + b) % m for a, b, m in zip(x, y, self.moduli))

    def order(self, x):
        return lcm(*(m // gcd(v, m) for v, m in zip(x, self.moduli)))


def predicted_period(ring_size, group, labels):
    a, b, c, d = labels
    bc = group.add(b, c)
    ad = group.add(a, d)
    h = group.add(bc, group.scale(-1, ad))
    irrelevant = {group.scale(i, h) for i in range(group.order(h))}

    def quotient_order(x):
        return next(i for i in range(1, group.order(x) + 1)
                    if group.scale(i, x) in irrelevant)

    right_lap = group.scale(ring_size, a)
    p = quotient_order(right_lap)
    q = quotient_order(bc)
    period = gcd(ring_size * p, 2 * q)
    for k in range(p):
        for j in range(q):
            image = group.add(group.scale(k, right_lap), group.scale(j, bc))
            if image in irrelevant:
                period = gcd(period, ring_size * k + 2 * j)
    return period


def graph_period(ring_size, group, labels, predicted):
    """Explore actual labelled arcs. Period from integral BFS depth defects."""
    start = (0, 0, group.zero)
    depth = {start: 0}
    todo = deque([start])
    period = 0
    incoming = {}
    edges = 0
    while todo:
        parent = todo.popleft()
        site, old_rail, gain = parent
        step = depth[parent] + 1
        for rail, move in ((0, 1), (1, -1)):
            new_gain = group.add(gain, labels[2 * old_rail + rail])
            child = ((site + move) % ring_size, rail, new_gain)
            incoming.setdefault(child, []).append(parent)
            edges += 1
            if child not in depth:
                depth[child] = step
                todo.append(child)
            # Inductively every path from the root to child has this clock class.
            if (step - depth[child]) % predicted:
                raise ValueError(("Endpoint clock class disagrees", parent, child))
            period = gcd(period, step - depth[child])
    backward = {start}
    todo.append(start)
    while todo:
        for parent in incoming[todo.popleft()]:
            if parent not in backward:
                backward.add(parent)
                todo.append(parent)
    if backward != set(depth):
        raise ValueError("Reachable component not strongly connected")
    return period, len(depth), edges


def masked_word_record(word, ring_size, labels):
    """Check each singleton physical-position mask permits one outgoing arc."""
    site = lift = 0
    rail = 0
    gain = 1
    for letter in word:
        move = {"R": 1, "L": -1}[letter]
        next_site = (site + move) % ring_size
        admitted = [(next_rail, delta) for next_rail, delta in [(0, 1), (1, -1)]
                    if (site + delta) % ring_size == next_site]
        if len(admitted) != 1:
            raise ValueError(("Mask admits unexpected successor count", admitted))
        next_rail, delta = admitted[0]
        gain *= labels[2 * rail + next_rail]
        site, rail, lift = next_site, next_rail, lift + delta
    return {"time": len(word), "site": site, "rail": "RL"[rail],
            "gain": gain, "lift": lift}


def example_checks():
    # In this five-cycle every arc flips sign. Time parity fully determines sign.
    all_minus = (-1,) * 4
    p = masked_word_record("R", 5, all_minus)
    q = masked_word_record("R" * 6, 5, all_minus)
    if (p["site"], p["rail"], p["gain"], q["site"], q["rail"], q["gain"]) != (
            1, "R", -1, 1, "R", 1):
        raise ValueError("Opposite-sign five-cycle control failed")

    # In this three-cycle only right steps flip sign. R and RRRR synchronize
    # at time 8 with preserved gains, but equality of time AND lift would
    # determine the right-step count and hence force equal signs.
    by_right = (-1, 1, -1, 1)
    returns = [masked_word_record(w, 3, by_right) for w in ("LLLLRLR", "LRLR")]
    if any((a["site"], a["rail"], a["gain"]) != (0, "R", 1) for a in returns):
        raise ValueError("Three-cycle padding was not a neutral return")
    pair = [masked_word_record(w, 3, by_right)
            for w in ("LLLLRLR" + "R", "LRLR" + "RRRR")]
    observed = [(a["time"], a["site"], a["rail"], a["gain"], a["lift"])
                for a in pair]
    if observed != [(8, 1, "R", -1, -2), (8, 1, "R", 1, 4)]:
        raise ValueError(("Clock versus lift example failed", observed))
    return {"time_parity": [p, q], "common_clock_different_lifts": pair}


def main():
    examples = example_checks()
    counts = Counter()
    settings = vertices = arcs = 0
    groups = [(1,), (2,), (3,), (4,), (5,), (2, 2), (2, 3)]
    for moduli in groups:
        group = ProductGroup(moduli)
        for n in range(3, 9):
            for labels in product(group.elements, repeat=4):
                predicted = predicted_period(n, group, labels)
                observed, size, edges = graph_period(n, group, labels, predicted)
                if observed != predicted:
                    raise ValueError((moduli, n, labels, observed, predicted))
                settings += 1
                vertices += size
                arcs += edges
                counts[observed] += 1
    print(json.dumps(dict(rings=list(range(3, 9)), groups=groups, settings=settings,
                          lifted_vertices=vertices, checked_endpoint_transitions=arcs,
                          periods=dict(sorted(counts.items())), examples=examples),
                     indent=2))


if __name__ == '__main__':
    main()
