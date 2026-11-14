"""Reproduce the exact sharp-source reset panel with python -B check_renewal_launch.py OUTDIR."""

import argparse
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path


PREDICATES = [
    "At each two-tick split, count both surviving and rejected coordinate intensities.",
    "Test the binomial survival, even release amplitudes and physical position variance.",
    "Sum attempted blocks and return distances separately; enforce the 4m and 2m bounds.",
    "Include all timeout mass; compare the renewal CDF with direct enumeration at m=2.",
    "Compare a coordinate label on both rails against the intended coherent success branch.",
]


def tick(state):
    result = Counter()
    for (x, rail), signed in state.items():
        result[x + 1, "R"] += signed
        result[x - 1, "L"] += signed if rail == "R" else -signed
    return {key: value for key, value in result.items() if value}


def splits(m):
    state = {(0, "R"): 1}
    failures = []
    previous = Fraction(1)
    expected_blocks = 0
    for j in range(1, m + 1):
        expected_blocks += previous
        wanted = "L" if j % 2 else "R"
        both = tick(tick(state))
        state = {key: value for key, value in both.items() if key[1] == wanted}
        rejected = {x: Fraction(value**2, 4**j)
                    for (x, rail), value in both.items() if rail != wanted}
        surviving = Fraction(sum(value**2 for value in state.values()), 4**j)
        assert surviving == Fraction(comb(2*j, j), 4**j)
        assert previous == surviving + sum(rejected.values())
        failures.append(rejected)
        previous = surviving
    return state, failures, previous, expected_blocks


def renewal_cdf(m, p, costs, horizon):
    cdf = []
    for deadline in range(horizon + 1):
        success = p if deadline >= 3*m else Fraction(0)
        success += sum(weight * cdf[deadline - cost] for cost, weight in costs.items()
                       if cost <= deadline)
        cdf.append(success)
    return cdf


def enumerate_bad_prefixes(m, p, costs, deadline):
    def branch(remaining):
        if remaining < 3*m:
            return Fraction(0)
        return p + sum(weight * branch(remaining - cost)
                       for cost, weight in costs.items() if cost <= remaining)
    return branch(deadline)


def panel(m):
    state, failures, p, expected_blocks = splits(m)
    expected_counts = {(2*j-m, "R"): (-1)**(m-j)*comb(m, j) for j in range(m+1)}
    assert state == expected_counts
    assert expected_blocks == 2*m*p
    failure_blocks = sum(j*sum(row.values()) for j, row in enumerate(failures, 1))
    return_per_attempt = sum(abs(x)*weight for row in failures for x, weight in row.items())
    assert failure_blocks == m*p and return_per_attempt <= 2*m*p
    variance = sum(x*x*value**2 for (x, rail), value in state.items())
    assert Fraction(variance, 4**m)/p == Fraction(m*m, 2*m-1)

    # Two moving ticks and one read slot per block. On failure use two controller
    # slots and one neighbour-route slot per site between the clicked port and home.
    costs = Counter()
    for j, row in enumerate(failures, 1):
        for x, weight in row.items():
            costs[3*j + abs(x) + 2] += weight
    expected_slots = (3*m*p + sum(cost*weight for cost, weight in costs.items()))/p
    separate_costs = 6*m + return_per_attempt/p + 2*(1/p - 1)
    assert expected_slots == separate_costs
    cdf = renewal_cdf(m, p, costs, 12*m)
    deadlines = sorted({3*m-1, 3*m, 4*m, 6*m, 12*m})
    for t in deadlines:
        assert 0 <= cdf[t] <= 1 and (1-cdf[t])*t <= expected_slots
        if m == 2:
            assert cdf[t] == enumerate_bad_prefixes(m, p, costs, t)
    # Keeping the site on every block makes each next flip probability 1/2
    # from a sharp input (verified independently on the two possible rails).
    for rail, wanted in (("R", "L"), ("L", "R")):
        two = tick(tick({(0, rail): 1}))
        assert sum(v*v for (x, r), v in two.items() if r == wanted) == 2
    labelled_yield = Fraction(1, 2**m)
    assert labelled_yield < p
    return {
        "m": m, "single_attempt_success": str(p),
        "site_label_on_every_block_success": str(labelled_yield),
        "accepted_raw_sites": {str(x): v for (x, r), v in sorted(state.items())},
        "first_failure_site_mass_by_block": [
            {str(x): str(v) for x, v in sorted(row.items())} for row in failures],
        "release_site_variance": str(Fraction(m*m, 2*m-1)),
        "mean_active_Hadamard_ticks": 4*m,
        "mean_neighbour_return_slots": str(return_per_attempt/p),
        "mean_all_slots": str(expected_slots),
        "deadline_panel": [{"slots": t, "released": str(cdf[t]),
                            "timeout": str(1-cdf[t])} for t in deadlines],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", type=Path)
    outdir = parser.parse_args().outdir
    rows = [panel(m) for m in (2, 4, 6, 8, 12)]
    result = {"predicates": PREDICATES, "panel": rows}
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "renewal_launch.json").open("x", encoding="utf8", newline="\n") as output:
        output.write(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
