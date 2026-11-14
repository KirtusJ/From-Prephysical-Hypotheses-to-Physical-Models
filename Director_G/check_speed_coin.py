"""Check speed effects and the finite pooled-versus-microscopic test."""

import argparse
from fractions import Fraction
from math import comb, log
import json
from pathlib import Path

from check_spatial_weight_envelope import advance, explicit_columns, initial_columns, kernel_rows


RESULT = Path(__file__).with_name("results") / "speed_coin.json"
RADII = [0, 2, 4, 6, 8]
ORDINARY = [18, 44, 116, 76, 2]
A, B, C = 44, 76, 116


def radial_grams(kernel, tick):
    grams = {}
    for j, (a, b, c, d) in enumerate(kernel):
        radius = abs(2*j - tick)
        effect = grams.setdefault(radius, [0, 0, 0])
        effect[0] += a*a + c*c
        effect[1] += a*b + c*d
        effect[2] += b*b + d*d
    return grams


def square_sites(kernel, source):
    bins = [0] * len(RADII)
    for j, (a, b, c, d) in enumerate(kernel):
        weight = a*a + c*c if source == "right" else (a+b)**2 + (c+d)**2
        bins[abs(2*j - 8)//2] += weight**2
    return bins


def score(counts, theta):
    return (theta * Fraction(counts[1], A) + (1-theta) * Fraction(counts[2], C)
            - Fraction(counts[3], B)) / sum(counts)


def report():
    columns = initial_columns()
    radial_cases = 0
    for tick in range(81):
        kernel = kernel_rows(columns)
        grams = radial_grams(kernel, tick)
        assert all(a == c and b == 0 for a, b, c in grams.values())
        assert sum(v[0] for v in grams.values()) == 2**tick
        radial_cases += len(grams)
        if tick == 8:
            tick_eight = kernel
            shell_eight = [grams[r] for r in RADII]
        columns = advance(columns)
    assert shell_eight == [[n, 0, n] for n in ORDINARY]
    rr, ll = explicit_columns(8)
    assert tick_eight == [(a, b, c, d) for (a, c), (b, d) in zip(rr, ll)]
    fair = [sum(comb(8, k) for k in range(9) if abs(2*k-8) == r) for r in RADII]
    assert fair == [70, 112, 56, 16, 2]

    low, high = Fraction(2, 5), Fraction(1, 2)
    assert A**2 * C**3 > B**5 and A*C < B**2
    right = square_sites(tick_eight, "right")
    balanced = square_sites(tick_eight, "balanced")
    brackets = {name: [score(rows, low), score(rows, high)] for name, rows in
                (("fair", fair), ("microscopic_right", right), ("microscopic_balanced", balanced))}
    assert min(brackets["fair"]) > 0 and min(brackets["microscopic_right"]) > 0
    assert max(brackets["microscopic_balanced"]) < 0
    assert score(ORDINARY, low) == score(ORDINARY, high) == 0
    assert [r for r, n in zip(RADII, ORDINARY) if n == max(ORDINARY)] == [4]

    theta = log(C / B) / log(C / A)
    plus, minus = score(right, theta), score(balanced, theta)
    right_fraction = -minus/(plus-minus)
    mixed = [right_fraction * u/sum(right) + (1-right_fraction) * v/sum(balanced)
             for u, v in zip(right, balanced)]
    # Both populations already violate the ordinary origin probability on the same side.
    assert max(Fraction(right[0], sum(right)), Fraction(balanced[0], sum(balanced))) < Fraction(18, 256)
    return {"exact_radial_grams": {"ticks_inclusive": [0, 80], "radius_clock_cases": radial_cases},
            "eight_tick": {"radii": RADII, "signed_effects_RR_RL_LL": shell_eight,
                           "fair_counts": fair, "site_square_right_numerators": right,
                           "site_square_balanced_numerators": balanced},
            "interval_certificate": {"theta_bracket": [str(low), str(high)],
                                     "endpoint_scores": {k: [str(x) for x in v] for k, v in brackets.items()}},
            "one_score_cancelled_binary64": {
                "theta": theta, "right_fraction": right_fraction,
                "radius_probabilities": mixed,
                "tv_from_ordinary": 0.5 * sum(abs(x - n/256) for x, n in zip(mixed, ORDINARY))}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="replace the checked JSON")
    args = parser.parse_args()
    data = json.dumps(report(), indent=2) + "\n"
    if args.write:
        RESULT.write_bytes(data.encode("utf-8"))
    else:
        assert data == RESULT.read_text(encoding="utf-8"), "finite table differs"
        print("Checked all radial effects, the eight-tick tables and the two score signs.")


if __name__ == "__main__":
    main()
