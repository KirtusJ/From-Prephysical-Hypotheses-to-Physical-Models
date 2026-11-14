"""Reproduce the finite checks for microscopic arrival-weight stability."""

import argparse
from itertools import product
import json
from math import fsum, hypot, sqrt
from pathlib import Path

from check_reflecting_path import launch, physical_step
from check_velocity_readout import fold_port, line_step


CLOCKS = (1, 2, 3, 6, 12, 24, 48, 96, 192, 384, 512)
RESULT = Path(__file__).with_name("results") / "spatial_weight_envelope.json"


def explicit_columns(tick):
    """Add every signed path for each of the two initial rails."""
    columns = []
    for origin_rail in range(2):
        sites = [[0, 0] for _ in range(tick + 1)]
        for word in product(range(2), repeat=tick):
            rail, sign = origin_rail, 1
            for direction in word:
                if rail == direction == 1:
                    sign = -sign
                rail = direction
            sites[word.count(0)][rail] += sign
        columns.append(sites)
    return columns


def initial_columns():
    return (([1], [0]), ([0], [1]))


def advance(columns):
    return tuple(line_step(right, left) for right, left in columns)


def kernel_rows(columns):
    (rr, lr), (rl, ll) = columns
    return list(zip(rr, rl, lr, ll))


def exact_controls():
    columns = initial_columns()
    for tick in range(11):
        expected = explicit_columns(tick)
        for basis, column in enumerate(columns):
            assert list(zip(*column)) == [tuple(site) for site in expected[basis]]
        columns = advance(columns)

    # Compare effects rail by rail as forms on the complete input coin.
    # The cross term detects relative-sign errors between the basis columns.
    folded_cases = 0
    for wells in range(2, 13):
        for source in range(wells):
            physical = [launch(wells, source, rail) for rail in range(2)]
            columns = initial_columns()
            for tick in range(wells):
                visited = set()
                for j, (rr, rl, lr, ll) in enumerate(kernel_rows(columns)):
                    site, swap = fold_port(source + 2 * j - tick, wells)
                    assert site not in visited
                    visited.add(site)
                    rails = ((lr, ll), (rr, rl)) if swap else ((rr, rl), (lr, ll))
                    for rail, (a, b) in enumerate(rails):
                        u, v = physical[0][site][rail], physical[1][site][rail]
                        assert (a*a, a*b, b*b) == (u*u, u*v, v*v)
                for site in set(range(wells)) - visited:
                    assert physical[0][site] == physical[1][site] == [0, 0]
                folded_cases += 1
                columns = advance(columns)
                physical = [physical_step(column) for column in physical]
    return {"path_enumeration_clocks_both_launch_rails": list(range(11)),
            "reflected_effects_well_counts": [2, 12],
            "reflected_source_clock_cases": folded_cases}


def coin_weights(kernel, coin, split):
    """Integer common-denominator weights. All input states have trace one."""
    cells = []
    for j, (a, b, c, d) in enumerate(kernel):
        if coin == "R":
            pair = (a*a, c*c)
        elif coin == "complex":
            # Initial vector (1, 1+i)/sqrt(3).
            pair = ((a+b)**2 + b*b, (c+d)**2 + d*d)
        else:
            # Maximally mixed initial coin.
            pair = (a*a + b*b, c*c + d*d)
        if split == "all" or (split == "alternating" and j % 2):
            cells.extend(pair)
        else:
            cells.append(sum(pair))
    return cells


def display(number):
    return float(format(number, ".11g"))


def stability_example(kernel, tick, coin, split):
    numerators = coin_weights(kernel, coin, split)
    total = sum(numerators)
    trace_denominator = {"R": 1, "complex": 3, "mixed": 2}[coin]
    assert total == trace_denominator * 2**tick
    ordinary = [n / total for n in numerators]
    moment = fsum(w * sqrt(tick*w) for w in ordinary)
    tv_values = []
    for power in (0.75, 1.25):
        powered = [w**power for w in ordinary]
        normalizer = fsum(powered)
        tv_values.append(display(0.5 * fsum(abs(b/normalizer-w)
                                             for b, w in zip(powered, ordinary))))
    return {"cells": len(numerators), "dark": numerators.count(0),
            "scaled_moment_3_over_2": display(moment), "tv_3_over_4_and_5_over_4": tv_values}


def envelope_row(kernel, tick):
    # At each site lambda_max(K* K) is the maximum over every density matrix.
    # Trace-one follows from the two norms and orthogonality of the columns.
    denominator = 2**tick
    assert sum(a*a + c*c for a, b, c, d in kernel) == denominator
    assert sum(b*b + d*d for a, b, c, d in kernel) == denominator
    assert sum(a*b + c*d for a, b, c, d in kernel) == 0
    scores = []
    cutoff = tick**(-2/3)
    for j, (a, b, c, d) in enumerate(kernel):
        g00, g11 = (a*a + c*c) / denominator, (b*b + d*d) / denominator
        g01 = (a*b + c*d) / denominator
        largest = (g00 + g11 + hypot(g00 - g11, 2*g01))/2
        x = 2*j - tick
        distance = abs(abs(x)/tick - 1/sqrt(2))
        scores.append((tick * largest * sqrt(distance + cutoff), x))
    best = max(score for score, x in scores)
    return {"clock": tick, "largest_scaled_site_weight": display(best),
            "maximizing_displacements_binary64": [x for score, x in scores if score == best],
            "examples": {coin + "_" + split: stability_example(kernel, tick, coin, split)
                         for coin, split in (("R", "none"), ("complex", "all"),
                                             ("mixed", "alternating"))}}


def report():
    controls = exact_controls()
    rows = []
    columns = initial_columns()
    for tick in range(1, max(CLOCKS) + 1):
        columns = advance(columns)
        if tick in CLOCKS:
            rows.append(envelope_row(kernel_rows(columns), tick))
    return {"controls": controls, "clock_tables": rows,
            "precision": "Exact integer kernels and darkness; envelope, moments and TV "
                         "use binary64, displayed to eleven significant digits."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="replace the checked JSON table")
    args = parser.parse_args()
    output = json.dumps(report(), indent=2) + "\n"
    if args.write:
        RESULT.write_bytes(output.encode("utf-8"))
    else:
        assert output == RESULT.read_text(encoding="utf-8"), "finite table differs"
        print("Checked both launch columns, reflected effects, and all stored clock tables.")


if __name__ == "__main__":
    main()
