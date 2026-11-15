"""Replay the calibration that links terminal probabilities to the coherent-cut test."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

WEAK = (-5, -1)
MEDIUM = (-3, -1)
STRONG = (3, 1)
CANCELED = ((-1, 1), (1, 1))


def enumerate_paths():
    signed, counts = Counter(), Counter()
    for directions in product((1,-1), repeat=5):
        mode = sum(directions), directions[-1]
        flips = sum(r == s == -1 for r, s in zip((1,)+directions, directions))
        signed[mode] += (-1)**flips
        counts[mode] += 1
    return signed, counts


def propagate():
    amplitudes = {(0,1):1}
    counts = {(0,1):1}
    for _ in range(5):
        following, multiplicity = Counter(), Counter()
        for (x, r), n in counts.items():
            for d in (-1,1):
                out = (x+d, d)
                following[out] += amplitudes[x,r] * (-1 if d == r == -1 else 1)
                multiplicity[out] += n
        amplitudes, counts = following, multiplicity
    return amplitudes, counts


def score(panel):
    return 16*panel[WEAK]-8*panel[MEDIUM]+panel[STRONG]


def run():
    signed, counts = enumerate_paths()
    assert (signed,counts) == propagate()
    assert set(signed) == set(counts)
    mass = {mode:v*v for mode,v in signed.items()}
    assert Counter(mass.values()) == {0:2, 1:4, 4:3, 16:1}
    assert (mass[WEAK],mass[MEDIUM],mass[STRONG]) == (1,4,16)
    assert {mode for mode,v in mass.items() if v == 0} == set(CANCELED)
    fair = {mode:F(n,32) for mode,n in counts.items()}
    dark = sum(fair[mode] for mode in CANCELED)
    assert (score(fair),dark) == (F(-3,8),F(5,16))
    assert score(fair)+F(6,5)*dark == 0
    controls = []
    for q in (F(0),F(1,2),F(1),F(3,2),F(2),F(4)):
        t = F(2)**int(2*q)
        weights = {mode: {0:0,1:1,4:t,16:t*t}[v] for mode,v in mass.items()}
        z = sum(weights.values())
        p = {mode:n/z for mode,n in weights.items()}
        s = (t-4)**2/(t*t+3*t+4)
        assert s == score(p) and (s == 0) == (q == 1)
        controls.append({"q":str(q), "score":str(s), "normalizer":str(z)})
    # Retain the exact cancellation of the uncorrected score in a nonordinary mixture.
    s = F(4,23)
    fraction_fair = s/(s-score(fair))
    assert (1-fraction_fair)*s + fraction_fair*score(fair) == 0
    assert fraction_fair*dark > 0
    return {"source":"right rail at displacement zero",
            "modes":[{"x":x,"rail":"R" if r==1 else "L","signed":n,
                      "squared_numerator":n*n,"unsigned":counts[x,r]}
                     for (x,r),n in sorted(signed.items())],
            "power_controls":controls, "fair_score":str(score(fair)),
            "fair_canceled_mass":str(dark),
            "zero_uncorrected_score_mixture":{"other_power":"3/2",
                "fair_fraction":str(fraction_fair),"canceled_rate":str(fraction_fair*dark)},
            "outside_window_score_at_half":str(F(2,7)),
            "outside_window_score_at_three_halves":str(F(4,23))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    with args.output.open("x",encoding="utf-8",newline="\n") as result:
        result.write(json.dumps(run(),indent=2)+"\n")
