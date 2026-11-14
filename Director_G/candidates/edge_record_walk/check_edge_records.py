"""Run python -B check_edge_records.py OUTPUT_DIRECTORY. Standard library, exact.

Sharp source (0,R) on the unprogrammed signed Hadamard ring. Raw amplitudes
are integer signed path totals. Input group x comprises its two rails, and its
output group comprises (x+1,R),(x-1,L). Compare the full normalized mass of
these groups on fresh launches at depths t and t+1.
"""
import argparse
import json
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path


RINGS = (3, 4, 5, 6, 7, 8, 9, 10, 16, 17, 32)
CONTROLS = {
    "square": lambda v: v*v,
    "absolute": abs,
    "quartic": lambda v: v**4,
    "negative_weight_doubled": lambda v: v*v*(2 if v < 0 else 1),
}


def propagate(n, t_max):
    state = [[1, 0]]+[[0, 0] for _ in range(n-1)]
    snapshots = [state]
    for t in range(1, t_max+1):
        after = [[0, 0] for _ in range(n)]
        for x, (r, l) in enumerate(state):
            after[(x+1) % n][0] = r+l
            after[(x-1) % n][1] = r-l
        assert sum(r*r+l*l for r, l in after) == 2**t
        snapshots.append(after)
        state = after
    return snapshots


def brute_column(n, t):
    """Enumerate words; direction 0 is right, and each LL adjacency flips sign."""
    signed = [[0, 0] for _ in range(n)]
    counts = [[0, 0] for _ in range(n)]
    for word in product((0, 1), repeat=t):
        x = (t-2*sum(word)) % n
        rail = word[-1] if word else 0
        exponent = sum(a*b for a, b in zip(word, word[1:]))
        signed[x][rail] += (-1)**exponent
        counts[x][rail] += 1
    return signed, counts


def edge_tests(n, snapshots, limit):
    rows = []
    for t in range(1, limit+2):
        # These are line predictions even when the endpoints collide on the ring.
        expected = {"right_reference": (t, [1, 0]), "right_inner": (t-2, [t-1, 1]),
                    "left_reference": (-t, [0, (-1)**(t-1)])}
        if t >= 2:
            sign = (-1)**(t-2)
            expected["left_inner"] = (-t+2, [sign, -(t-3)*sign])
        tests = {}
        for name, (x, line) in expected.items():
            actual = snapshots[t][x % n]
            tests[name] = dict(site=x % n, actual=actual, line=line, agrees=(actual == line))
        rows.append(dict(t=t, within_no_alias_range=t < limit, probes=tests))
        if t < limit:
            assert all(item["agrees"] for item in tests.values())
    first = {name: next(row["t"] for row in rows if not row["probes"].get(name, {"agrees": True})["agrees"])
             for name in ("right_reference", "right_inner", "left_reference", "left_inner")}
    assert first == dict(right_reference=limit, right_inner=limit+1,
                         left_reference=limit, left_inner=limit+1)
    return rows, first


def score_panels(n, snapshots, limit):
    """Exact marginal changes. Store every failure location, plus its first value."""
    results = {}
    for mode, score in CONTROLS.items():
        rows = []
        for t in range(limit+2):
            before, after = snapshots[t:t+2]
            s0 = sum(score(v) for pair in before for v in pair)
            s1 = sum(score(v) for pair in after for v in pair)
            assert s0 > 0 and s1 > 0
            failures = []
            for x, (r, l) in enumerate(before):
                b = Fraction(score(r)+score(l), s0)
                a = Fraction(score(after[(x+1) % n][0])+score(after[(x-1) % n][1]), s1)
                if a != b:
                    failures.append(x)
            first = failures[0] if failures else None
            record = dict(t=t, totals=[s0, s1], failed_sites=failures)
            if first is not None:
                r, l = before[first]
                record["first_failure_before_after"] = [Fraction(score(r)+score(l), s0),
                                                        Fraction(score(r+l)+score(r-l), s1)]
            rows.append(record)
        results[mode] = rows
    assert not any(r["failed_sites"] for r in results["square"])
    if limit >= 3:
        for mode in CONTROLS.keys()-{"square"}:
            assert any(r["failed_sites"] for r in results[mode])
    return results


def infer_edge_scores(n, snapshots, limit):
    """Solve only measured-edge mass-preservation equations with the reference factor 2."""
    known = {0: Fraction(0), 1: Fraction(1)}
    rows = []
    def learn(t, cell, value):
        r, l = snapshots[t][cell % n]
        ref = snapshots[t][t % n]
        assert ref == [1, 0] and cell % n != t % n
        equation = {}
        for v, coefficient in ((r+l, 1), (r-l, 1), (r, -2), (l, -2)):
            equation[v] = equation.get(v, 0)+coefficient
        assert value not in known and equation[value] != 0
        remainder = sum(c*known[v] for v, c in equation.items() if v != value and c)
        known[value] = -remainder/equation[value]
        rows.append(dict(t=t, site=cell % n, input=[r, l], signed_argument=value, inferred=known[value]))

    learn(1, -1, -1)
    for t in range(2, limit):
        learn(t, t-2, t)
    for t in range(5, limit, 2):
        learn(t, -t+2, -(t-2))
    for t in range(6, limit, 2):
        learn(t, -t+2, -(t-4))
    # Only here use squares as an independent check of the inferred values.
    assert all(weight == v*v for v, weight in known.items())
    return rows


def one_ring(n):
    limit = n//gcd(2, n)
    snapshots = propagate(n, limit+2)
    rows, first = edge_tests(n, snapshots, limit)
    word_checks = []
    for t in range(min(10, limit+2)+1):
        signed, count = brute_column(n, t)
        assert signed == snapshots[t] and sum(map(sum, count)) == 2**t
        word_checks.append(2**t)
    # At n=2^r, divisibility by two becomes permanent once all raw entries are even.
    first_even = next((t for t, v in enumerate(snapshots) if all(z % 2 == 0 for pair in v for z in pair)), None)
    if n & (n-1) == 0:
        assert first_even == limit+1
    return dict(N=n, alias_period=limit, first_edge_formula_failure=first, edge_rows=rows,
                brute_words_by_depth=word_checks, first_all_even_through_panel=first_even,
                group_tests=score_panels(n, snapshots, limit),
                inferred_from_edge_equations=infer_edge_scores(n, snapshots, limit))


def main():
    return dict(source="(0,R), gain -1 exactly on L-to-L; sites modulo N; ordered cells R,L",
                assumptions=["One common function f of raw signed totals, with f(0)=0 and f(1)=1; f is unchanged across depths and, for an all-integers conclusion, across ring sizes or common local cones.",
                             "At each tested splitter, the total probability of its two input rails agrees with the total over its two successor ports at the next depth. The two snapshots use complete normalized terminal reads from fresh launches.",
                             "The reference input (1,0) and output (1,1) set the score normalization ratio to 2. No symmetry f(-v)=f(v), prior Born port law, or herald probability is used in the inference."],
                result_scope="Fixed rings give a finite edge calibration before aliasing. The no-wrap range grows along an unbounded family; the computations are finite examples. Failed alternative score marginals and all edge alias trials are retained.",
                rings=[one_ring(n) for n in RINGS])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    folder = parser.parse_args().output
    folder.mkdir(parents=True, exist_ok=True)
    target = folder/"edge_records.json"
    if target.exists():
        parser.exit(2, f"refusing to overwrite {target}\n")
    data = main()
    with target.open("xb") as stream:
        stream.write((json.dumps(data, default=str, separators=(",", ":"))+"\n").encode("utf-8"))
    print(f"Verified {len(RINGS)} signed rings, direct word counts, reference ratios and both signed edges.")
