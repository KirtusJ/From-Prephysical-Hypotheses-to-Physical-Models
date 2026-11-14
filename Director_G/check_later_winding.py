"""Reproduce the later-clock winding probabilities and exact launch test in a fresh directory."""

import argparse
from fractions import Fraction as F
import json
from math import comb, gcd
from pathlib import Path

from check_first_winding_clock import port_contrast
from check_fixed_ring_moments import at_port, check, physical_ring
from check_tag_shot_budget import binomial_cdf, bounds


def tv_bound(t, d, order):
    """Sum the unsigned prefix-pair bounds at every surviving harmonic."""
    n, k = t - 1, order // 2
    total = 0
    for g in range(k, n // d + 1):
        moment = int(g % order == k) + int(g % order == (-k) % order)
        total += moment * comb(2*n, n - g*d)
    return min(F(1), F(total, 2**n))


def port_laws(size, q, clocks):
    """Return the two normalized laws from unsigned physical word counts."""
    d = size // gcd(size, 2)
    order = q // gcd(d, q)
    check(order >= 2, "the two witnesses require at least two reduced labels")
    for t, state in physical_ring(size, q, clocks):
        plus, minus = {}, {}
        for x in range(size):
            for rail in (0, 1):
                port = (x, rail)
                a, _ = at_port(state, q, x, rail)
                diagonal = sum(v*v for v in a)
                difference = port_contrast(a, q, d, order // 2)
                cross, rem = divmod(difference, 2)
                check(rem == 0, "paired oriented gain lags")
                plus[port] = F(diagonal + cross, 2**t)
                minus[port] = F(diagonal - cross, 2**t)
        for law in (plus, minus):
            check(min(law.values()) >= 0 and sum(law.values()) == 1, "normalized law")
        tv = sum(abs(plus[p] - minus[p]) for p in plus) / 2
        check(tv <= tv_bound(t, d, order), "all-harmonic prefix bound")
        yield t, plus, minus, tv


def binomial_mass(n, k, p):
    return comb(n, k) * p**k * (1-p)**(n-k)


def decision_test(p, q):
    """Classify as plus above k hits and at k with probability tie."""
    def chances(n, k, tie):
        plus_error = binomial_cdf(n, k, p) - tie * binomial_mass(n, k, p)
        minus_error = 1 - binomial_cdf(n, k, q) + tie * binomial_mass(n, k, q)
        return plus_error, minus_error

    limit = F(1, 20)
    tie162 = (limit - (1 - binomial_cdf(162, 59, q))) / binomial_mass(162, 59, q)
    lower = chances(162, 59, tie162)
    upper = chances(163, 60, F(9, 10))
    simple = chances(168, 61, F(0))
    check(p > q and 0 < tie162 < 1 and lower[1] == limit and lower[0] > limit,
          "most powerful 162-launch test at the allowed minus error")
    check(max(*upper, *simple) < limit, "both reported rules meet both error targets")
    return {str(n): {"tie_count": k, "probability_of_plus_at_tie": bounds(tie),
                     "plus_error": bounds(errors[0]), "minus_error": bounds(errors[1])}
            for n, k, tie, errors in [(162, 59, tie162, lower), (163, 60, F(9, 10), upper),
                                      (168, 61, F(0), simple)]}


def calculate():
    panels = []
    for size in (3, 4, 5, 6, 7, 8, 9, 16):
        d = size // gcd(size, 2)
        for q in (2, 3, 4, 5, 6, 7, 9):
            order = q // gcd(d, q)
            if order < 2:
                continue
            first = (order // 2)*d + 1
            clocks = {first-1, first, first+1, first+d, first+2*d}
            for t, _, _, tv in port_laws(size, q, clocks):
                if t == first:
                    check(tv == tv_bound(t, d, order), "equality at the first clock")
            panels.append([size, q])

    mask = {(x, 0) for x in (0, 4, 8, 12)}
    masks = {"four_right_ports": mask,
             "four_sites_both_rails": {(x, r) for x, _ in mask for r in (0, 1)},
             "whole_right_rail": {(x, 0) for x in range(16)},
             "shift_by_two_on_right": {(x+2, 0) for x, _ in mask}}
    clocks = range(81, 221)
    scans, controls = [], {}
    for t, plus, minus, tv in port_laws(16, 21, clocks):
        num = tv * 2**t
        check(num.denominator == 1, "dyadic TV numerator")
        scans.append(num.numerator)
        if t in (81, 82):
            check(tv == F(1 if t == 81 else 79, 2**80), "first two clock distances")
        if t not in (81, 82) and t not in range(142, 147):
            continue
        readings = {}
        for name, ports in masks.items():
            readings[name] = [sum(law[p] for p in ports) for law in (plus, minus)]
        if t in (81, 143, 145):
            check(readings["four_right_ports"] == [0, 0], "odd-clock parity control")
        if t == 144:
            p, q = readings["four_right_ports"]
            check({port for port in plus if plus[port] > minus[port]} == mask and p-q == tv,
                  "positive difference occurs exactly on the four named right ports")
            check(readings["shift_by_two_on_right"][0] < readings["shift_by_two_on_right"][1],
                  "moving the mask two sites reverses the contrast")
            design = decision_test(p, q)
        controls[str(t)] = {name: list(map(str, rates)) for name, rates in readings.items()}
    return {"prefix_bound_panels_wells_and_gain_orders": panels,
            "panel_clock_offsets_from_first": ["-1", "0", "1", "D", "2D"],
            "well_count": 16, "gain_order": 21, "first_clock_in_scan": clocks.start,
            "last_clock_in_scan": clocks.stop-1, "tv_numerators_in_units_of_2_to_minus_t": scans,
            "plus_then_minus_event_probabilities": controls,
            "tick_144_launch_tests_decimal_enclosures": design}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "later_winding.json"
    if target.exists():
        parser.exit(2, f"Refusing to overwrite {target}\n")
    result = calculate()
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
