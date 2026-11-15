"""Enumerate translated record queries and path overlaps over F5, with exact counts."""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


V = tuple(product(range(5), repeat=3))
ZERO = (0, 0, 0)
Q = tuple(q for q in V if next((x for x in q if x), 0) == 1)


def add(x, y):
    return tuple((a + b) % 5 for a, b in zip(x, y))


def dot(u, q):
    return sum(a * b for a, b in zip(u, q)) % 5


def writer(a, b):
    return (
        (a[1] * b[2] - a[2] * b[1]) % 5,
        (a[2] * b[0] - a[0] * b[2]) % 5,
        (a[0] * b[1] - a[1] * b[0]) % 5,
    )


def require(match, where):
    if not match:
        raise ValueError(where)


def measure(amplitudes, writes, *, dephase=False):
    mass = sum(a * a for a in amplitudes.values())
    query_errors = []
    for q in Q:
        # Add the classical output noise from the coordinate measurement of the blank.
        noise = Counter()
        for z, a in amplitudes.items():
            noise[dot(z, q)] += a * a
        for u in V:
            ideal = dot(u, q)
            binary = sum(n for offset, n in noise.items() if bool((ideal + offset) % 5) != bool(ideal))
            raw = mass - noise[0]
            query_errors.append((writes[u], binary, raw))
    binary_sum = sum(count * error for count, error, _ in query_errors)
    raw_sum = sum(count * error for count, _, error in query_errors)
    trials = mass * len(Q) * sum(writes.values())
    worst = max(error for _, error, _ in query_errors)
    overlaps = []
    for d in V[1:]:
        # Dephasing kills all off-diagonal terms needed by a nonzero translation.
        overlaps.append(0 if dephase else sum(a * amplitudes[add(z, d)] for z, a in amplitudes.items()))
    visibilities = Counter(Fraction(abs(x), mass) for x in overlaps)
    return {
        "w": Fraction(mass - amplitudes[ZERO] ** 2, mass),
        "mean_binary_error": Fraction(binary_sum, trials),
        "mean_raw_error": Fraction(raw_sum, trials),
        "worst_binary_error": Fraction(worst, mass),
        "mean_absolute_visibility": Fraction(sum(map(abs, overlaps)), len(overlaps) * mass),
        "visibility_counts": {str(v): count for v, count in sorted(visibilities.items())},
    }


def run():
    uniform = {u: 1 for u in V}
    pair_writes = Counter(writer(a, b) for a, b in product(V, repeat=2))
    require(pair_writes[ZERO] == 745 and set(pair_writes[u] for u in V[1:]) == {120}, "write prior")
    require(len(Q) == 31, "number of projective probes")
    cases = {}
    for a, b in [(1, 0), (31, 1), (6, 1), (1, 1), (0, 1)]:
        amplitudes = {z: (a if z == ZERO else b) for z in V}
        row = measure(amplitudes, uniform)
        w = row["w"]
        mass = a * a + 124 * b * b
        predicted = Fraction(2 * a * b + 123 * b * b, mass)
        require(row["mean_binary_error"] == 10 * w / 31, "balanced-write binary error")
        require(row["mean_raw_error"] == row["worst_binary_error"] == 25 * w / 31, "raw and worst errors")
        require(row["visibility_counts"] == {str(predicted): 124}, "isotropic fringe")
        cases[f"origin_{a}_others_{b}"] = row

    amplitudes = {z: (6 if z == ZERO else 1) for z in V}
    natural = measure(amplitudes, pair_writes)
    require(natural["mean_binary_error"] == 53 * natural["w"] / 155, "ordered-pair prior")
    classical = measure(amplitudes, uniform, dephase=True)
    require(classical["mean_absolute_visibility"] == 0, "dephased blank")
    require(classical["mean_binary_error"] == cases["origin_6_others_1"]["mean_binary_error"], "dephased flags")
    line = measure({z: int(z[1:] == (0, 0)) for z in V}, uniform)
    require(line["visibility_counts"] == {"0": 120, "1": 4}, "translations on and off a single line")
    require(line["mean_binary_error"] == Fraction(8, 31), "line-state error")
    return {
        "number_of_writes": len(V),
        "number_of_projective_probes": len(Q),
        "number_of_nonzero_route_differences": len(V) - 1,
        "isotropic_pure_blanks_uniform_writes": cases,
        "origin_6_others_1_uniform_ordered_source_pairs": natural,
        "origin_6_others_1_dephased_uniform_writes": classical,
        "uniform_amplitude_on_first_coordinate_line": line,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    output = parser.parse_args().output
    report = json.dumps(run(), default=str, indent=2) + "\n"
    if output:
        output.write_text(report, encoding="utf-8", newline="\n")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
