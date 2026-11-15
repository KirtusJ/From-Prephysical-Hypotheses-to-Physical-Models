"""Check sampled total-nonnegative winding minors by two exact constructions.

The matrix entries come from complete physical direction words. The comparison
number uses partial tuples on the deficit cover, enforcing disjointness.
Every effective mask sequence is tested in the four short fixtures, along
with deterministic random and unmasked fixtures at longer horizons.
No third-party dependencies; tests remain active with python -O.
"""
from collections import Counter
from itertools import combinations, permutations, product
from math import gcd
from random import Random
import json


def source_records(n, tmax, masks):
    records = {}
    for word in product((0, 1), repeat=tmax):
        x = left = 0
        for t, bit in enumerate(word):
            left += bit
            x = (x + 1 - 2 * bit) % n
            if x not in masks[t]:
                break
        else:
            counts = records.setdefault(x, Counter())
            counts[left, word[-1]] += 1
    return records


def minor(values):
    total = 0
    for choice in permutations(range(len(values))):
        sign = -1 if sum(k > j for i, k in enumerate(choice)
                         for j in choice[i+1:]) % 2 else 1
        term = sign
        for row, col in enumerate(choice):
            term *= values[row][col]
        total += term
    return total


def disjoint_counts(n, masks, sources):
    states = {tuple(sources): 1}
    jumps = tuple(product((0, 1), repeat=len(sources)))
    for tick, permitted in enumerate(masks[:-1], start=1):
        new = Counter()
        for before, mult in states.items():
            for jump in jumps:
                after = tuple(e + j for e, j in zip(before, jump))
                if any(low >= high for low, high in zip(after, after[1:])):
                    continue
                if all((tick - 2 * e) % n in permitted for e in after):
                    new[after] += mult
        states = new
    return states


def compare(n, tmax, masks, orders):
    records = source_records(n, tmax, masks)
    period = n // gcd(2, n)
    for k in range(1, 4):
        rows = ([-1], [-1, 0], [-1, 0, 1])[k - 1]
        sources = [i * period for i in rows]
        disjoint = disjoint_counts(n, masks, sources)
        for x, slots in records.items():
            lo = min(level for level, rail in slots)
            def entry(index):
                level, parity = divmod(index, 2)
                return slots.get((lo + level * period, 1-parity), 0)
            def sink(index):
                level, parity = divmod(index, 2)
                return lo + level * period + parity-1
            # All columns that can be reached, plus one zero column on each side.
            lower, upper = min(sources), max(sources) + tmax - 1
            columns = [c for c in range(2*((lower-lo)//period-2),
                                         2*((upper-lo)//period+3)+1)
                       if lower <= sink(c) <= upper]
            if not columns:
                raise ValueError(("No effective columns", n, tmax, x, lo))
            columns = [min(columns)-1, *columns, max(columns)+1]
            for cs in combinations(columns, k):
                sinks = tuple(sink(c) for c in cs)
                d = minor([[entry(c-2*i) for c in cs] for i in rows])
                families = disjoint.get(sinks, 0)
                if d != families or d < 0:
                    raise ValueError((n, tmax, masks, x, rows, cs, d, families))
                orders[k, int(d > 0)] += 1


def available(n, tick):
    return sorted({(tick - 2*l) % n for l in range(tick+1)})


def exhaustive(n, tmax):
    options = []
    for t in range(1, tmax+1):
        sites = available(n,t)
        options.append([frozenset(site for i, site in enumerate(sites)
                                  if bits & (1 << i)) for bits in range(1 << len(sites))])
    yield from product(*options)


def rail_order_control():
    # The ring has three sites and every mask is open.
    # Both endpoints have x=0: the only words are RRR and LLL.
    slots = source_records(3, 3, [set(range(3))]*3)[0]
    results = []
    for reverse in (False, True):
        matrix = []
        for row in (0, 1):
            values = []
            for col in (2, 3):
                level, parity = divmod(col-2*row, 2)
                rail = parity if reverse else 1-parity
                values.append(slots.get((3*level, rail), 0))
            matrix.append(values)
        results.append(minor(matrix))
    if results != [1, -1]:
        raise ValueError(("Rail-order mutation escaped", results))
    return {"issued_order": results[0], "exchanged_rails": results[1]}


def main():
    rng = Random(20261115)
    orders = Counter()
    by_group = Counter()
    for n, t in [(3, 1), (3, 2), (3, 3), (4, 4)]:
        for masks in exhaustive(n, t):
            compare(n, t, masks, orders)
            by_group["exhaustive"] += 1
    for n in (3, 4, 5, 6, 7, 8):
        for t in (1, 3, 6, 8):
            sites = [available(n, j+1) for j in range(t)]
            for sample in range(6):
                masks = [frozenset(x for x in allowed if sample == 0 or rng.random() < .8)
                         for allowed in sites]
                compare(n, t, masks, orders)
                by_group["full" if sample == 0 else "random"] += 1
    print(json.dumps({"rail_order_control": rail_order_control(),
                      "mask_sequences": dict(by_group),
                      "minors": {str(k): {"zero":orders[k,0], "positive":orders[k,1]}
                                 for k in range(1,4)}}, indent=2))


if __name__ == '__main__':
    main()
