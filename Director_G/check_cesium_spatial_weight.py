"""Compare terminal site-weight powers on the two Fig. 3 arm continuations."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from check_cesium_count_fraction import EVIDENCE, FIGURE_COUNTS, PDF_SHA256, FixedMargins, require


def continuation(initial, visibility):
    # Each global spin dephasing multiplies off-diagonal spin blocks by
    # visibility. A path-pair interference term acquires one factor for
    # each post-tick spin disagreement. The terminal rail is distinguished.
    histories = defaultdict(list)
    for path in product("RL", repeat=3):
        word = (initial,) + path
        sign = (-1) ** sum(a == b == "L" for a, b in zip(word, word[1:]))
        site = (word.count("L") - word.count("R")) // 2
        histories[site, path[-1]].append((path, sign))
    weights = defaultdict(F)
    for mode, paths in histories.items():
        for (p, a), (q, b) in product(paths, repeat=2):
            disagreements = sum(i != j for i, j in zip(p, q))
            weights[mode] += a * b * visibility**disagreements / 8
    require(sum(weights.values()) == 1 and min(weights.values()) >= 0, "path-pair weights")
    return weights


def endpoint(weights, power, blur):
    sites = defaultdict(F)
    for (site, rail), mass in weights.items():
        sites[site] += mass
    normalizer = sum(total**power for total in sites.values())
    output = defaultdict(F)
    for (site, rail), mass in weights.items():
        weighted = mass * sites[site]**(power-1) / normalizer
        for shift, chance in ((-1, blur/2), (0, 1-blur), (1, blur/2)):
            output[site+shift,rail] += weighted * chance
    require(sum(output.values()) == 1, "reported mass")
    return output


def factor_bounds(numerator, denominator, site):
    # For positive counted denominators the ratio of fixed-gain sums
    # is at least the smallest finite mode ratio at this site.
    finite = [numerator[site, c] / denominator[site, c] for c in "RL" if denominator[site, c]]
    require(bool(finite), "no supported denominator")
    return min(finite)


def odds_at(visibility, power, blur):
    b, c = [endpoint(continuation(rail, visibility), power, blur) for rail in "RL"]
    left = sum(b[-1,r] for r in "RL") / sum(c[-1,r] for r in "RL")
    right = sum(c[1,r] for r in "RL") / sum(b[1,r] for r in "RL")
    return left*right, factor_bounds(b,c,-1) * factor_bounds(c,b,1)


def upper_limit(lower_tail, size):
    # Invert the exact lower tail on a 0.001 odds-ratio grid, rounding up.
    low, high = 1, 100_000
    require(lower_tail(F(low,1000)) > size > lower_tail(F(high,1000)), "unbracketed odds limit")
    while high-low > 1:
        mid = (low+high)//2
        if lower_tail(F(mid,1000)) >= size:
            low = mid
        else:
            high = mid
    return F(high,1000)


def run():
    archive = json.loads(EVIDENCE.read_bytes())
    require(archive["source_sha256"] == PDF_SHA256 and archive["figure"] == 3, "source provenance")
    counts = {}
    for (name, reference), panel in zip(FIGURE_COUNTS.items(), archive["digitized"], strict=True):
        counts[name] = [panel["counts"][str(j)] for j in range(-8,9)]
        require(counts[name] == reference, "digitized atom count changed")
    b, c = counts["retain_negative"], counts["retain_positive"]
    table = [[row[7],row[9]] for row in (b,c)]
    require(table == [[107,31],[27,115]], "named well pair or arm changed")
    # Reversing the columns sends theta to its reciprocal and lets us use
    # the original, exact inclusive upper-tail implementation in both directions.
    forward = FixedMargins(table)
    reverse = FixedMargins([row[::-1] for row in table])
    def lower(theta):
        return reverse.upper_tail(1/theta)
    readings = []
    for visibility, error in product((F(1), F(94,100), F(0)), (F(0),F(2,100),F(4,100))):
        for power in (1,2):
            same_spin_gain, spin_gain_lower = odds_at(visibility, power, error)
            if not error:
                a = 2 + 2*visibility**2
                require(same_spin_gain == (a+1)**(2*power), "spin-blind identity")
                require(spin_gain_lower == (a*(a+1)**(power-1))**2, "spin-resolved bound")
            readings.append(dict(visibility=str(visibility), symmetric_displacement_error=str(error),
                                 site_power=power, spin_blind_odds=str(same_spin_gain),
                                 spin_sensitive_odds_lower=str(spin_gain_lower),
                                 spin_blind_lower_tail=float(lower(same_spin_gain)),
                                 largest_lower_tail_with_spin_gains=float(lower(spin_gain_lower))))
    thresholds = {str(k): str(upper_limit(lower,F(1,20*k))) for k in (1,60)}
    require(odds_at(F(1),2,F(0)) == (625,400), "ideal nonlinear terminal law")
    for rail, peak in (("R",-1),("L",1)):
        w = continuation(rail,F(1))
        for power, expected in ((1,F(5,8)),(2,F(25,28))):
            o = endpoint(w,power,F(0))
            require(sum(o[peak,c] for c in "RL") == expected, "single three-tick test")
    return dict(pdf=archive["source"], pdf_sha256=PDF_SHA256, reference="Figure 3 (a), (b), (c)",
                sites=list(range(-8,9)), detected_counts=counts, detected_totals=list(map(sum,counts.values())),
                retained_and_displaced=[[sum(b[:12]),sum(b[12:])],[sum(c[5:]),sum(c[:5])]],
                comparisons=dict(wells=[-1,1], table=table, observed_odds=str(F(b[7]*c[9],b[9]*c[7])),
                    fair_path_count_odds=9, fair_path_count_upper_tail=float(forward.upper_tail(F(9))),
                    one_sided_95_upper_odds_by_family_rounded_up=thresholds, sensitivities=readings),
                scope="Detected atom endpoints reconstructed from the vector figure. Independent stable row sampling conditional on margins. No all-prepared-atoms denominator.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    with parser.parse_args().output.open("x",encoding="utf8",newline="\n") as out:
        json.dump(run(),out,indent=2,allow_nan=False)
        out.write("\n")
