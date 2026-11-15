"""Exact nine-tick position records with a heralded rational phase reference.

Run python -I -B check_rational_reference_walk.py. An optional --table PATH
writes all 64 three-write words at the declared Pell index to a new JSON file.
The table conditions on three success flags and also gives incident masses.
"""
import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


def pairs(index):
    a, b = 1, 0
    for _ in range(index):
        previous = (a, b)
        a, b = a + 2*b, a + b
    return previous, (a, b)


def signed_flight(site, rail, a, b):
    """Matrix columns from the eight physical direction paths in a flight."""
    columns = [[0, 0] for _ in range(4)]
    for word in product((0, 1), repeat=3):
        y, old, weight = site, rail, 1
        for tick, new in enumerate(word, 1):
            if tick == 2 and y % 2 == 0:
                if new == old:
                    weight = 0
                    break
                weight *= a
            else:
                if tick == 2:
                    weight *= b
                if new == old == 1:
                    weight = -weight
            y = (y+new) % 4
            old = new
        columns[y][old] += weight
    return columns


def density_table(branches):
    # Unnormalized real density at each recorded site. The common success
    # factor and the two outer Hadamard denominators are restored at the end.
    live = {(): (1, 0, 0)}
    for _ in range(3):
        out = {}
        for prefix, (rr, rl, ll) in live.items():
            y = prefix[-1] if prefix else 0
            blocks = [[0, 0, 0] for _ in range(4)]
            for a, b in branches:
                right, left = [signed_flight(y, rail, a, b) for rail in (0, 1)]
                for site, vals in enumerate(blocks):
                    x, z = right[site]
                    u, v = left[site]
                    vals[0] += rr*x*x + 2*rl*x*u + ll*u*u
                    vals[1] += rr*x*z + rl*(x*v+u*z) + ll*u*v
                    vals[2] += rr*z*z + 2*rl*z*v + ll*v*v
            out.update({prefix+(site,): block for site, block in enumerate(blocks)})
        live = out
    return {w: rr+ll for w, (rr, _, ll) in live.items()}


def coherent_table(branches):
    """Independent propagation. Keep each unresolved selector choice coherent
    until both rail amplitudes arrive, and sum distinct choices as alternatives.
    """
    table = defaultdict(int)
    for choices in product(branches, repeat=3):
        live = {((), 0): (1, 0)}
        for t in range(9):
            a, b = choices[t//3]
            nxt = defaultdict(lambda: [0, 0])
            for (prefix, y), (r, l) in live.items():
                if t % 3 == 1 and y % 2 == 0:
                    out = (a*l, a*r)
                else:
                    scale = b if t % 3 == 1 else 1
                    out = (scale*(r+l), scale*(r-l))
                for rail, value in enumerate(out):
                    site = (y+rail) % 4
                    history = prefix+(site,) if t % 3 == 2 else prefix
                    nxt[history, site][rail] += value
            live = nxt
        for (w, _), (r, l) in live.items():
            table[w] += r*r + l*l
    return table


def stopped_table(prob, herald):
    """Every full position word or the earlier address prefix followed by FAIL."""
    stops = []
    for depth in range(3):
        for prefix in product(range(4), repeat=depth):
            mass = sum(p for w, p in prob.items() if w[:depth] == prefix)
            stops.append((prefix+("fail",), mass*herald**depth*(1-herald)))
    words = [(w, p*herald**3) for w, p in prob.items()]
    leaves = stops + words
    if sum(p for _, p in leaves) != 1:
        raise ArithmeticError("lost incident launches")
    return leaves


def compare_at_nine(branches, P, C):
    """Signed paths for the two-call echo. Omit 1/sqrt(2) at ticks 1,2,9.
    A coefficient x+y*sqrt(2) needs a factor sqrt(2) on the even bypass
    at tick 2. At tick 6 the integer filters already carry their own scale.
    """
    for sign in (-1, 1):
        masses = defaultdict(lambda: [0, 0])
        for a, b in branches:
            paths = [(0, 0, 1, 0)]
            for tick in range(1, 10):
                nxt = []
                for site, old, x, y in paths:
                    if tick in (1, 9) or (tick in (2, 6) and site % 2):
                        coeff = sign if tick == 2 else b if tick == 6 else 1
                        for rail in (0, 1):
                            scale = -coeff if rail == old == 1 else coeff
                            nxt.append(((site+rail) % 4, rail, scale*x, scale*y))
                    elif tick in (2, 6):
                        rail = 1-old
                        xx, yy = (2*y, x) if tick == 2 else (a*x, a*y)
                        nxt.append(((site+rail) % 4, rail, xx, yy))
                    else:
                        nxt.append(((site+old) % 4, old, x, y))
                paths = nxt
            amplitudes = defaultdict(lambda: [0, 0])
            for site, rail, x, y in paths:
                amplitudes[site, rail][0] += x
                amplitudes[site, rail][1] += y
            for (site, _), (x, y) in amplitudes.items():
                masses[site][0] += x*x+2*y*y
                masses[site][1] += 2*x*y
        # Normalize by 8P. Code zero has (1+sign*sqrt(2)*C/P)/2.
        expected = [[4*P, 4*sign*C], [4*P, -4*sign*C], [0, 0], [0, 0]]
        if [masses[site] for site in range(4)] != expected:
            raise ArithmeticError("nine-tick echo does not recover the declared phase")


def calculate(index):
    branches = pairs(index)
    P = sum(a*a for a, _ in branches)
    C = sum(a*b for a, b in branches)
    largest = max(max(a, 2*b) for a, b in branches)
    K = 1 << (largest-1).bit_length()
    herald = Fraction(P, 2*K*K)
    if P != 2*sum(b*b for _, b in branches) or P*P-2*C*C != 2:
        raise ArithmeticError("Pell identities")
    weights = density_table(branches)
    compare_at_nine(branches, P, C)
    amplitudes = coherent_table(branches)
    if any(weights[w] != amplitudes.get(w, 0) for w in weights):
        raise ArithmeticError("physical path sum and density map disagree")
    denominator = (4*P)**3
    if len(weights) != 64 or sum(weights.values()) != denominator:
        raise ArithmeticError("incomplete word table")
    prob = {w: Fraction(m, denominator) for w, m in weights.items()}
    levels = []
    for depth in range(3):
        rows = []
        for prefix in product(range(4), repeat=depth):
            row = [sum(p for w, p in prob.items() if w[:depth+1] == prefix+(j,))
                   for j in range(4)]
            if any(row):
                rows.append(row)
        levels.append(rows)
    root = levels[0][0]
    stopped = stopped_table(prob, herald)
    if root != [0, Fraction(3, 8)+Fraction(C, 2*P),
                Fraction(1, 2)-Fraction(C, 2*P), Fraction(1, 8)]:
        raise ArithmeticError("named ports do not match the analytic one-flight read")
    if index == 2:
        for depth, rows in enumerate(levels):
            if len(rows) != 3**depth or any(len({p for p in row if p}) != 3 for row in rows):
                raise ArithmeticError("three distinct bright weights at each reached prefix")
        if sum(p > 0 for p in prob.values()) != 27:
            raise ArithmeticError("unexpected support")
        positive = [(w, p) for w, p in stopped if p]
        low = min(p for _, p in positive)
        high = max(p for _, p in positive)
        if (len(stopped) != 85 or len(positive) != 40 or
                [w for w, p in positive if p == high] != [("fail",)] or
                any(len(w) != 3 or w[-1] == "fail" for w, p in positive if p == low)):
            raise ArithmeticError("stopped-word maxima, minima or support")
        for rows in levels:
            for row in rows:
                total = sum(row)
                stop = total*(1-herald)
                positive_children = [p*herald for p in row if p]
                if len(set(positive_children+[stop])) != 4 or stop <= max(positive_children):
                    raise ArithmeticError("invalid coarse-write sibling weights")
        print(f"Stopped table: {len(positive)}/{len(stopped)} positive leaves, "
              f"minimum={low}, maximum={high}.")
    print(f"Pell index {index}, K={K}, P={P}, C={C}, herald={herald}, "
          f"all three heralds={herald**3}.")
    print("First address probabilities:", ", ".join(str(p) for p in root))
    print("Distinct positive child counts by depth:",
          [[len({p for p in row if p}) for row in rows] for rows in levels])
    return {"pell_index": index, "probability_of_three_heralds": str(herald**3),
            "stopped_records_per_launch": [{"record": list(w), "probability": str(p)}
                                           for w, p in stopped],
            "probability_of_first_failure_at_call":
                [str(herald**j*(1-herald)) for j in range(3)],
            "words": [{"addresses": list(w), "conditional": str(p),
                       "incident": str(p*herald**3)} for w, p in sorted(prob.items())]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=int, default=2)
    parser.add_argument("--table", type=Path, help="export to a new JSON file")
    args = parser.parse_args()
    if args.index < 1:
        parser.error("index must be positive")
    result = calculate(args.index)
    if args.table:
        with args.table.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
