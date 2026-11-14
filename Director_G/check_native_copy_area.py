"""Check localized-sheet forcing contrasts with literal signed paths and area walks.

Run: python -B check_native_copy_area.py NEW_OUTPUT_DIRECTORY
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
from math import gcd, isqrt
from pathlib import Path


def check(ok, message):
    if not ok:
        raise ArithmeticError(message)


def physical_paths(m, order, origin, incoming):
    """Store physical ring coordinates, final sheet address and signed amplitude."""
    ring = 4 * order
    histories = []
    for middles in product((-1, 1), repeat=m):
        x, rail, sheet, sign = origin % ring, incoming, 0, 1
        sites = []
        for middle in middles:
            final = -rail
            for out in (middle, final):
                sheet = (sheet + x // 2) % order
                if rail == out == -1:
                    sign = -sign
                x = (x + out) % ring
                rail = out
            sites.append(x)
        histories.append((tuple(sites), sheet, sign))
    return histories


def record_tables(histories, m):
    """Force each subset by appending the read sites to the orthogonal record."""
    tables = []
    for mask in range(1 << (m - 1)):
        times = [j for j in range(m - 1) if mask & (1 << j)]
        states = Counter()
        for sites, sheet, sign in histories:
            states[(sites[-1], sheet, tuple(sites[j] for j in times))] += sign
        tables.append(sum(v * v for v in states.values()))
    return tables


def force_contrast(table):
    return sum((-1) ** f.bit_count() * v for f, v in enumerate(table))


def excursion_areas(m):
    """Positive pair excursions. A flat increment has two midpoint-rail choices."""
    if m == 1:
        return Counter()
    counts = {(1, 1): 1}
    for step in range(2, m):
        updated = defaultdict(int)
        for (height, area), n in counts.items():
            for jump, ways in ((-1, 1), (0, 2), (1, 1)):
                h = height + jump
                if 1 <= h <= m - step:
                    updated[h, area + h] += ways * n
        counts = updated
    return Counter({area: n for (h, area), n in counts.items() if h == 1})


def numerator(m, order, areas):
    if m == 1:
        return 2
    return 2 * sum(n for a, n in areas.items() if (2 * a) % order == 0)


def group_sum_kernel(m, order, cuts):
    """Unrestricted signed differences; copy marks impose zero height only there."""
    states = {(0, 0): 1}
    for step in range(1, m + 1):
        updated = defaultdict(int)
        for (height, residue), n in states.items():
            for jump, ways in ((-1, 1), (0, 2), (1, 1)):
                h = height + jump
                if abs(h) > m - step or (step in cuts and h):
                    continue
                updated[h, (residue + 2*h) % order] += n * ways
        states = updated
    return states.get((0, 0), 0)


def threshold(order):
    k = order // gcd(order, 2)
    return 1 + isqrt(4 * k - 1)


def physical_census(areas):
    rows = []
    for order in (3, 4, 5, 6, 8, 9, 10, 18):
        for m in range(1, min(2 * order, 9)):
            table = record_tables(physical_paths(m, order, 0, 1), m)
            for origin, incoming in ((4*order - 1, -1), (3, 1)):
                shifted = record_tables(physical_paths(m, order, origin, incoming), m)
                check(shifted == table, "launch-rail, site-parity or seam discrepancy")
            full = len(table) - 1
            n = force_contrast(table)
            check(n == numerator(m, order, areas[m]), "physical contrast vs excursion count")
            for mask, value in enumerate(table):
                cuts = {j+1 for j in range(m-1) if mask & (1 << j)}
                check(value == group_sum_kernel(m, order, cuts), "forced mask vs pair DP")
                for j in range(m-1):
                    check(value >= table[mask | (1 << j)], "cut increases traced survival")
            check(all(table[full ^ (1 << j)] == table[full] for j in range(m-1)),
                  "isolated optional copy was visible")
            rows.append(dict(order=order, blocks=m, denominator=4**m, all_clear_numerator=n,
                             unforced_numerator=table[0], all_forced_numerator=table[-1],
                             masks=len(table)))
    return rows


def ambiguous_priors():
    order, m = 8, 4
    table = record_tables(physical_paths(m, order, 0, 1), m)
    a, b = 7, 5
    panel_a = [table[f | a] for f in range(8)]
    panel_b = [table[f | b] for f in range(8)]
    check(panel_a == panel_b and force_contrast(table) > 0, "sparse law ambiguity")
    # All-clear trial and fair randomized forcing, exact all-launch variance.
    c = Fraction(force_contrast(table), 4**m)
    variance = len(table) * Fraction(sum(table), 4**m) / c**2 - 1
    return dict(order=order, blocks=m, denominator=4**m, clean_table=table,
                contrast=str(c), distinct_deterministic_hidden_words=[a,b],
                forced_panels=[panel_a, panel_b], all_clear_for_both=0,
                fair_mask_all_clear_estimator_variance_on_clean_law=str(variance))


def zero_area_cut_witness(m, cut):
    # A four-block signed difference bridge 0,+1,0,-1,0, or its opposite.
    for start in range(m-3):
        if cut in (start+1, start+3):
            d = [0]*(m+1)
            d[start+1], d[start+3] = 1, -1
            check(sum(d) == 0 and d[cut] != 0, "zero-area local bridge")
            increments = [b-a for a,b in zip(d,d[1:])]
            check(all(abs(i) <= 1 for i in increments), "invalid bridge increment")
            return 2 * 2**increments.count(0)
    return 0


def long_cut_examples():
    rows = []
    for order, m in ((8, 3), (8, 4), (101, 4), (101, 5), (16, 8), (32, 10), (64, 16), (128, 26)):
        k0 = group_sum_kernel(m, order, set())
        ratios = [Fraction(group_sum_kernel(m, order, {j}), k0) for j in range(1, m)]
        check(ratios == ratios[::-1], "one-cut time symmetry")
        for j, ratio in enumerate(ratios, 1):
            lower = zero_area_cut_witness(m, j)
            check((1-ratio)*k0 >= lower, "constructive cut loss exceeds actual gap")
            if m >= 5:
                check(lower == 2**(m-3), "zero-area certificate misses an internal cut")
        rows.append(dict(order=order, blocks=m, unforced=str(Fraction(k0, 4**m)),
                         one_cut_ratios=list(map(str,ratios)), highest=str(max(ratios)),
                         least_relative_deficit=str(1-max(ratios))))
    return rows


def run():
    areas = {m: excursion_areas(m) for m in range(1, 33)}
    for m in range(2, 33):
        check(sorted(areas[m]) == list(range(m-1, m*m//4+1)), "hole in area support")
    thresholds = []
    for order in range(3, 251):
        m_first = next(m for m in range(2, 33) if numerator(m, order, areas[m]) > 0)
        check(m_first == threshold(order), "incorrect first active contrast depth")
        for m in range(m_first, min(2*order, 33)):
            check(numerator(m, order, areas[m]) > 0, "blind depth after first positive row")
        thresholds.append(dict(order=order, first_blocks=m_first,
                               signed_contrast_numerator=numerator(m_first,order,areas[m_first])))
    square_thresholds = []
    for q in (2, 3, 4, 8, 16):
        order, m = 2*q*q, 2*q
        c = Fraction(numerator(m, order, areas[m]), 4**m)
        check(c == Fraction(2,4**m), "maximal-area contrast")
        square_thresholds.append(dict(order=order, blocks=m, forced_settings=2**(m-1),
                           denominator=str(c)))
    return dict(
        scope="Exact model probabilities per original sharp site/rail/localized-sheet launch. "
              "All internal boundaries interrogated; final site and sheet traced. 2m<4M.",
        bit_order="Low bit means a persistent complete site copy at the first passing block.",
        predicates=["literal signed pointer records equal the independent unrestricted-area DP for every mask",
                    "both initial rails, two site parities and a ring seam give the same kernel",
                    "all-boundary signed contrast counts both orientations of nonzero excursions with 2*area=0 mod M",
                    "positive area support is every integer from m-1 through floor(m*m/4) for m>=2",
                    "first nonempty-boundary positive depth is ceil(2*sqrt(M/gcd(M,2)))",
                    "forcing cuts is monotone; one optional bit among mandatory neighboring cuts is blind",
                    "distinct fixed hidden words yield the same entire forced survival table",
                    "every internal cut from m=5 onward loses a zero-area bridge in the displayed longer panels"],
        physical_masks=physical_census(areas), sparse_ambiguity=ambiguous_priors(),
        first_visible_nontrivial=thresholds, square_area_examples=square_thresholds,
        native_single_cut_ratios=long_cut_examples(),
        costs="The full Boolean panel uses 2^(m-1) settings; the square-order threshold family "
              "has clean signed contrast 2/4^m. Fair-mask variance is specific to the given estimator.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = run()
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "native_copy_area.json").open("x", encoding="utf-8", newline="\n") as out:
        json.dump(result, out, indent=2)
        out.write("\n")


if __name__ == "__main__":
    main()
