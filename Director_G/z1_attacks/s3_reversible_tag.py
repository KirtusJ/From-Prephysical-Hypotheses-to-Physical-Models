"""Attack predicates fixed before the first evaluation, target Z1 v0.1 S3.

Run python -B s3_reversible_tag.py [OUTPUT_DIRECTORY]. Refuses to overwrite.
On the four-site signed ring started at (0,R), toggle a bit on each arrival
at site 1, for either output rail. No bit is read until the terminal read.

P1: original base sign lift strongly connected, original arcs and gains unchanged;
    16-column tagged raw step has Gram matrix 2I.
P2: all events through t=3 satisfy S2, and every singleton has weight one.
P3: find an original-endpoint/signed-multiset collision between two equally
    long events of size two with different tagged weights by t=6.
P4: locate the first differing full terminal port by t=6; keep all zeros.
P5: search 256 exact steps for a coarse and a joint launch return of weight
    one, retaining nulls. S5 at arbitrary precision also has a compact
    unitary recurrence proof independent of this bounded exact-return search.
P6: independent private bits on the product carrier give raw step Gram=4I
    and multiplicativity for every pair of equal-depth subsets through t=3.
    Test an illicit shared-XOR-bit alternative as a negative control.
All finite test failures are retained in the output.
"""
import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


N = 4
START = (0, 0, 0)
STATES = list(product(range(N), range(2), range(2)))


def successors(state):
    x, incoming, tag = state
    for rail, shift in ((0, 1), (1, -1)):
        y = (x + shift) % N
        yield (y, rail, tag ^ int(y == 1)), -1 if incoming == rail == 1 else 1


def paths(t):
    rows = [(START, 1, "")]
    for _ in range(t):
        rows = [(b, gain*h, word + "RL"[b[1]]) for a, gain, word in rows for b, h in successors(a)]
    return rows


def continued(rows):
    return [(b, gain*h, word + "RL"[b[1]]) for a, gain, word in rows for b, h in successors(a)]


def bins(rows, tagged=True):
    values = defaultdict(int)
    for a, g, unused_word in rows:
        values[a if tagged else a[:2]] += g
    return values


def square(values):
    return sum(v*v for v in values.values())


def product_weight(left, right, shared=False):
    values = defaultdict(int)
    for a, g, _ in left:
        for b, h, _ in right:
            key = (a[:2], b[:2], a[2] ^ b[2]) if shared else (a, b)
            values[key] += g*h
    return square(values)


def gram(columns, expected):
    return all(sum(v*b.get(s, 0) for s, v in a.items()) == (expected if i == j else 0)
               for i, a in enumerate(columns) for j, b in enumerate(columns))


def base_and_operator():
    base = list(product(range(N), range(2), (-1, 1)))
    strong = True
    for origin in base:
        occupied = {origin}
        fringe = [origin]
        while fringe:
            x, rail, accumulated = fringe.pop()
            for (y, out, _), sgn in successors((x, rail, 0)):
                nxt = y, out, accumulated*sgn
                if nxt not in occupied:
                    occupied.add(nxt)
                    fringe.append(nxt)
        strong &= len(occupied) == len(base)
    columns = [dict(successors(s)) for s in STATES]
    product_columns = [{(s, t):g*h for s, g in a.items() for t, h in b.items()}
                       for a in columns for b in columns]
    base_arcs = []
    for x, rail in product(range(N), range(2)):
        a = [(b[:2], g) for b, g in successors((x, rail, 0))]
        assert a == [(b[:2], g) for b, g in successors((x, rail, 1))]
        base_arcs.append((x, rail, a))
    return dict(base_gain_lift_strong=strong, raw_columns=len(columns), norm2=gram(columns, 2),
                product_raw_columns=len(product_columns), product_norm4=gram(product_columns, 4),
                base_arcs=base_arcs)


def exhaust():
    counts, failures, product_failures, shared_first = [], [], [], None
    for t in range(4):
        candidates = paths(t)
        subsets = [[row for j, row in enumerate(candidates) if mask >> j & 1]
                   for mask in range(1 << len(candidates))]
        weights = [square(bins(a)) for a in subsets]
        for k, (a, w) in enumerate(zip(subsets, weights)):
            if (len(a) == 1 and w != 1) or square(bins(continued(a))) != 2*w:
                failures.append([t, k])
        for i, a in enumerate(subsets):
            for j, b in enumerate(subsets):
                predicted = weights[i]*weights[j]
                weight = product_weight(a, b)
                if weight != predicted:
                    product_failures.append([t, i, j, weight, predicted])
                if shared_first is None and product_weight(a, b, shared=True) != predicted:
                    shared_first = dict(depth=t, left=a, right=b, private=weight,
                                        shared_xor=product_weight(a, b, shared=True))
        counts.append(dict(t=t, subsets=len(subsets), product_pairs=len(subsets)**2))
    return dict(counts=counts, continuation_or_singleton_failures=failures,
                product_failures=product_failures, shared_xor_first_mismatch=shared_first)


def collisions():
    first = None
    results = []
    for t in range(7):
        candidates = paths(t)
        by_type = {}
        differences = 0
        for a, b in combinations(candidates, 2):
            if a[0][:2] != b[0][:2]:
                continue
            key = (a[0][:2], tuple(sorted([a[1], b[1]])))
            pair = [a, b]
            weight = square(bins(pair))
            if key not in by_type:
                by_type[key] = (weight, pair)
            elif by_type[key][0] != weight:
                differences += 1
                if first is None:
                    old, previous = by_type[key]
                    first = dict(depth=t, endpoint_signed_multiset=key, event1=previous,
                                 event2=pair, tagged_weights=[old, weight], original=square(bins(pair, False)))
        results.append(dict(depth=t, disagreeing_with_first_in_same_key=differences))
    return dict(first_same_multiset_different_tagged_weight=first, census=results)


def flight():
    amp, original = {START:1}, {START[:2]:1}
    rows, first, coarse_return, joint_return = [], None, None, None
    peaks = []
    maximum = Fraction(0)
    for t in range(257):
        den = 2**t
        probs = [Fraction(sum(amp.get((x, r, b), 0)**2 for b in range(2)), den)
                 for x, r in product(range(N), range(2))]
        reference = [Fraction(original.get((x, r), 0)**2, den) for x, r in product(range(N), range(2))]
        assert sum(probs) == sum(reference) == 1
        if t <= 6:
            rows.append(dict(t=t, tagged=probs, original=reference))
            if first is None and probs != reference:
                first = dict(depth=t, differing_ports=[j for j in range(2*N) if probs[j] != reference[j]])
        if t and probs[0] > maximum:
            maximum = probs[0]
            peaks.append(dict(depth=t, coarse=maximum, joint_tag_blank=Fraction(amp.get(START, 0)**2, den)))
        if t and probs[0] == 1 and coarse_return is None:
            coarse_return = t
        if t and amp.get(START, 0)**2 == den and joint_return is None:
            joint_return = t
        raw, base = defaultdict(int), defaultdict(int)
        for s, value in amp.items():
            for b, sign in successors(s):
                raw[b] += sign*value
        for (x, r), value in original.items():
            for b, sign in successors((x, r, 0)):
                base[b[:2]] += sign*value
        amp, original = raw, base
    return dict(rows=rows, first_different_ports=first, first_exact_coarse_return=coarse_return,
                first_exact_joint_blank_return=joint_return, increasing_coarse_return_peaks=peaks,
                exact_return_search_horizon=256)


def main():
    operator, events, pairs, orbit = base_and_operator(), exhaust(), collisions(), flight()
    predicates = dict(P1=operator["base_gain_lift_strong"] and operator["norm2"],
                      P2=not events["continuation_or_singleton_failures"],
                      P3=pairs["first_same_multiset_different_tagged_weight"] is not None,
                      P4=orbit["first_different_ports"] is not None,
                      P5_bounded_exact_joint=orbit["first_exact_joint_blank_return"] is not None,
                      P6=operator["product_norm4"] and not events["product_failures"])
    return dict(source="Z1-R, N=4, start (0,R); positive edges except L->L. Flip bit on ARRIVAL at site 1, "
                       "after both outgoing rows of the Hadamard coin. Endpoint array index 2*x+rail, R=0, L=1. "
                       "Path rows give (x,rail,bit), gain, rail word. Event weights are unnormalized.",
                predicates=predicates, operator=operator, events=events, witnesses=pairs, flight=orbit,
                product_scope="Product signs multiply and each factor retains its bit. Both singleton weight "
                              "and subset-product multiplicativity hold before division by 2^t per factor. "
                              "The sole XOR of the two bits is a different event weight.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    folder = parser.parse_args().output_directory
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "s3_reversible_tag.json"
    if target.exists():
        parser.exit(1, "Refusing to overwrite " + str(target) + "\n")
    record = main()
    with target.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, default=str, separators=(",", ":"))
        handle.write("\n")
    print(json.dumps(record["predicates"], sort_keys=True))
