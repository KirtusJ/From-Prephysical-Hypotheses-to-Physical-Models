"""Finite-time bounds and all plotted observations in the Cheng optical walk."""

import argparse
import csv
from fractions import Fraction as F
import json
from math import comb, sqrt
from pathlib import Path


RESULTS = Path(__file__).resolve().parent / "results"


def tables(name, index):
    with (RESULTS / name).open(encoding="utf-8", newline="") as file:
        return {int(row.pop(index)): {key: float(value) if value else None
                                     for key, value in row.items()}
                for row in csv.DictReader(file)}


def next_step(h, t):
    output = {}
    for x in range(-t - 1, t + 2, 2):
        a, b = h.get(x - 1, (0, 0))
        c, d = h.get(x + 1, (0, 0))
        output[x] = (a + b, c - d)
    return output


def compositions(n, k):
    if k == 0:
        return int(n == 0)
    return comb(n - 1, k - 1) if n >= k else 0


def run_count(t, x):
    # With sharp initial H the sign is minus once per adjacent V,V.
    # k runs partition all V steps, separated by at least one H.
    v = (t - x) // 2
    h = t - v
    if v == 0:
        return (1, 0)
    right = left = 0
    for k in range(1, min(v, h + 1) + 1):
        factor = (-1) ** (v - k) * compositions(v, k)
        right += factor * (comb(h, k) if h >= k else 0)
        left += factor * comb(h, k - 1)
    return right, left


def concentration_floor(sites):
    """Common bound on the pooled position probabilities, before computing IPR."""
    n = len(sites)
    if n == 1:
        return F(1)
    peak = max(sites, key=lambda x: max(sites[x]))
    rail = max(sites[peak])
    outside = [sum(v) for x, v in sites.items() if x != peak]
    if max(outside) > rail:
        return F(1, n)
    mass = rail**2 / (rail**2 + sum(v**2 for v in outside))
    mass = max(mass, F(1, n))
    return mass**2 + (1 - mass)**2 / (n - 1)


def gain_needed(peak_floor, n, upper_ipr):
    peak_ceiling = (1 + sqrt((n - 1) * (n * upper_ipr - 1))) / n
    return (peak_floor / (1 - peak_floor)) / (peak_ceiling / (1 - peak_ceiling))


def analysis():
    positions = tables("cheng_positions.csv", "x")
    observed = tables("cheng_concentration.csv", "t")
    assert list(positions) == list(range(-20, 21, 2))
    assert list(observed) == list(range(21))
    h = {0: (1, 0)}
    series = []
    for t, row in observed.items():
        assert all(rails == run_count(t, x) for x, rails in h.items())
        sites = {x: tuple(F(a * a, 2**t) for a in rails) for x, rails in h.items()}
        assert sum(sum(rails) for rails in sites.values()) == 1
        ordinary = sum(sum(rails)**2 for rails in sites.values())
        floor = concentration_floor(sites)
        hi = row["cap_high"]
        series.append({"t": t, "ordinary": float(ordinary), "q_ge_2_floor": float(floor),
                       "observed": row["blue"], "cap_low": row["cap_low"], "cap_high": hi})
        if t < 20:
            h = next_step(h, t)

    # Transfer uniformity through the bound for q >= 2, allowing either
    # rail partition independently at each well and on each launch.
    interior = {x for x in sites if abs(x) <= 10}
    M = max(sum(sites[x]) for x in interior)
    A = sum(sum(sites[x])**2 for x in interior)
    B = sum(r**2 for x, pair in sites.items() if x not in interior for r in pair if r >= M)
    ceiling = A / (A + B)
    assert ceiling == F(21691630560, 109192894721)
    bars = max(max(abs(row["theory_blue_top"] - float(sites[x][1])),
                   abs(row["theory_stack_top"] - float(sum(sites[x]))))
               for x, row in positions.items())
    numerical_ipr = max(abs(observed[row["t"]]["numerical_blue_line"] - row["ordinary"])
                        for row in series)
    assert bars < 0.0001 and numerical_ipr < 0.0002
    fractions = {}
    for name, columns in [("caption_black_total", ["black"]),
                          ("legend_black_plus_gray", ["black", "gray"])]:
        values = {x: sum(row[c] for c in columns) for x, row in positions.items()}
        total = sum(values.values())
        center = sum(values[x] for x in interior)
        fractions[name] = {"all": total, "interior": center, "share": center / total,
                           "concentration_after_scaling": sum((v / total)**2 for v in values.values())}
    twenty_peak = max(sites[12])
    outside_squares = sum(sum(r)**2 for x, r in sites.items() if x != 12)
    twenty_floor = twenty_peak**2 / (twenty_peak**2 + outside_squares)
    return {"all_clocks": series, "q_ge_2_floor_above_plotted_cap_ticks": [
                r["t"] for r in series if r["cap_high"] is not None and r["q_ge_2_floor"] > r["cap_high"]],
            "tick4_q_ge_1_concentration_floor": float(F(109, 256)),
            "terminal_gain_ratio_needed_at_plotted_upper_cap": {
                "tick4_q_ge_1": gain_needed(5 / 8, 5, observed[4]["cap_high"]),
                "tick4_q_ge_2": gain_needed(81 / 91, 5, observed[4]["cap_high"]),
                "tick20_q_ge_2": gain_needed(float(twenty_floor), 21, observed[20]["cap_high"])},
            "tick20": {"interior_ordinary": float(sum(sum(sites[x]) for x in interior)),
                       "interior_q_ge_2_ceiling": float(ceiling), "graph": fractions},
            "largest_position_theory_read_error": bars,
            "largest_concentration_theory_read_error": numerical_ipr}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = analysis()
    path = RESULTS / "cheng_walk.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    else:
        assert json.loads(path.read_text(encoding="utf-8")) == result
        print("Verified 21 clocks, 21 sites, two figure readings, exact paths and finite-time bounds.")
