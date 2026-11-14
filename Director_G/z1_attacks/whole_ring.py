"""Run python -B whole_ring.py OUTPUT_DIRECTORY. Prespecified predicates:

1. On N=4 the lifted signed graph is strongly connected, the signed arc matrix
   has A^t A=2I, and all full terminal bin counts match the proved distribution
   through t=24. Model and alternative agree on all full bins, normalized totals,
   empty events and both singleton signs, and reach a sharp return at t=8.
2. At t=3 the complete (-1,L) bin has count two and signed sum zero.
3. At t=4 take the first three walks into (0,R) and the first into (0,L) in
   lexicographic L-before-R word order. The alternative exceeds unit normalized
   weight, the ordinary continuation is consistent and the alternative fails.
4. For every pair of the 256 subsets at t=3, the alternative on the full
   product rectangle agrees with the product of the separate weights.

Predicates and witnesses are written before failing the run. Refuse overwrite.
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


ORIGIN = (0, "R")
VERTICES = list(product(range(4), "LR"))


def step(port, direction):
    x, previous = port
    return ((x + (1 if direction == "R" else -1)) % 4, direction), (
        -1 if previous == direction == "L" else 1)


def counts_and_signs(paths):
    bins = defaultdict(lambda: (0, 0))
    for _, port, sign in paths:
        n, d = bins[port]
        bins[port] = n+1, d+sign
    return bins


def extend(paths):
    return [(word+letter, target, sign*gain)
            for word, port, sign in paths for letter in "LR"
            for target, gain in [step(port, letter)]]


def term(n, d, prime=3):
    if n == 0:
        return 0
    factor = 1
    while n % prime == 0:
        n //= prime
        factor *= 32
    return factor*d*d


def weights(bins):
    return sum(d*d for n, d in bins.values()), sum(term(n, d) for n, d in bins.values())


def verify():
    states = {(ORIGIN, 1)}
    for _ in range(16):
        states |= {(y, s*g) for x, s in states for b in "LR" for y, g in [step(x,b)]}
    # Check both reachability directions in the 16-state gain lift.
    backward = {(ORIGIN, 1)}
    for _ in range(16):
        backward |= {(x, s) for x in VERTICES for s in (-1, 1) for b in "LR"
                     for y, g in [step(x,b)] if (y,s*g) in backward}
    cols = [{y:g for b in "LR" for y,g in [step(x,b)]} for x in VERTICES]
    gram = [[sum(a.get(y,0)*b.get(y,0) for y in VERTICES) for b in cols] for a in cols]
    identity = all(v == 2*(i == j) for i,r in enumerate(gram) for j,v in enumerate(r))
    counts, signed = Counter({ORIGIN: 1}), Counter({ORIGIN: 1})
    rows = []
    for t in range(25):
        bins = {v:(counts[v],signed[v]) for v in VERTICES}
        agree = all(term(n,d) == d*d for n,d in bins.values())
        expected = ([1] if t == 0 else [1,1] if t == 1 else [2**(t-2)]*4)
        rows.append(dict(t=t, count_by_port=[n for n,d in bins.values()],
                         signed_by_port=[d for n,d in bins.values()], equal=agree,
                         size_ok=sorted(n for n,d in bins.values() if n) == expected,
                         total_ok=sum(d*d for n,d in bins.values()) == 2**t))
        next_n, next_d = Counter(), Counter()
        for port,(n,d) in bins.items():
            for letter in "LR":
                y,g = step(port,letter)
                next_n[y] += n
                next_d[y] += g*d
        counts,signed = next_n,next_d

    t3 = [("", ORIGIN, 1)]
    for _ in range(3):
        t3 = extend(t3)
    dark = counts_and_signs(t3)[(3,"L")]
    t4 = extend(t3)
    selected = [p for p in t4 if p[1] == ORIGIN][:3] + [p for p in t4 if p[1] == (0,"L")][:1]
    ordinary, altered = weights(counts_and_signs(selected))
    ordinary_next, altered_next = weights(counts_and_signs(extend(selected)))

    events = [counts_and_signs([p for j,p in enumerate(t3) if mask >> j & 1]) for mask in range(256)]
    # On a rectangle, the signed product gain multiplies the two path signs.
    # Construct all product bins and evaluate the same term individually.
    failed_rectangles = []
    for i,a in enumerate(events):
        for j,b in enumerate(events):
            rectangle = sum(term(n*m,d*e) for n,d in a.values() for m,e in b.values())
            if rectangle != weights(a)[1]*weights(b)[1]:
                failed_rectangles.append([i,j])
    predicates = {
        "full_bins_and_return": len(states) == len(backward) == 16 and identity and
            term(0,0) == 0 and term(1,-1) == term(1,1) == 1 and
            all(r["equal"] and r["size_ok"] and r["total_ok"] for r in rows) and
            rows[8]["signed_by_port"][VERTICES.index(ORIGIN)]**2 == 2**8,
        "dark_split": dark == (2,0),
        "unselected_continuation": len(selected) == 4 and altered > 2**4 and
            ordinary_next == 2*ordinary and altered_next != 2*altered,
        "rectangles": not failed_rectangles,
    }
    return dict(predicates=predicates, vertices=VERTICES, forward_states=len(states),
                backward_states=len(backward), gram=gram, terminal_rows=rows,
                dark_bin_count_signed=dark,
                counterexample=dict(selected=selected, ordinary=ordinary, altered=altered,
                                   ordinary_next=ordinary_next, altered_next=altered_next,
                                   normalized_altered=str(Fraction(altered,16))),
                rectangles_tested=len(events)**2, failed_rectangles=failed_rectangles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory/"whole_ring.json"
    if output.exists():
        raise SystemExit(f"refusing to overwrite {output}")
    result = verify()
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(result["predicates"])
    raise SystemExit(int(not all(result["predicates"].values())))
