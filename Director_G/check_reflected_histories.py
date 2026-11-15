"""Compare coherent half-interval histories with the folded group-velocity law."""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from math import acos, asin, fsum, pi, prod, sin, sqrt
from pathlib import Path


TIMES = (Fraction(1, 2), Fraction(1), Fraction(2))
LENGTHS = (32, 64, 128, 256, 512, 1024)
START = Fraction(1, 4)
WORDS = tuple("".join(p) for p in product("01", repeat=len(TIMES)))


def tick(state):
    right, left = state
    plus = [r + l for r, l in zip(right, left)]
    minus = [r - l for r, l in zip(right, left)]
    return [minus[0], *plus[:-1]], [*minus[1:], plus[-1]]


def norm(state):
    return sum(a*a for rail in state for a in rail)


def cut(state, bit):
    half = len(state[0]) // 2
    if bit == "0":
        return tuple(row[:half] + [0]*half for row in state)
    return tuple([0]*half + row[half:] for row in state)


def histories(length):
    # The stored amplitudes at clock t all have the same divisor sqrt(2**t).
    initial = ([0]*length, [0]*length)
    initial[0][length//4] = 1
    states = {"": initial}
    free = initial
    clocks = [int(time*length) for time in TIMES]
    for t in range(1, clocks[-1]+1):
        states = {word: tick(state) for word, state in states.items()}
        free = tick(free)
        if t in clocks:
            states = {word+bit: cut(state, bit)
                      for word, state in states.items() for bit in "01"}
            assert sum(norm(state) for state in states.values()) == 2**t
    return {w: norm(state) for w, state in states.items()}, norm(cut(free, "1"))


def by_words(length):
    """Independent microscopic paths. Amplitudes interfere only within an identical record."""
    clocks = tuple(int(time*length) for time in TIMES)
    cells = defaultdict(int)
    for proposals in product((0, 1), repeat=clocks[-1]):
        word = ""
        well, rail, sign = length//4, 0, 1
        for t, proposal in enumerate(proposals, 1):
            if proposal == rail == 1:
                sign *= -1
            destination = well + (1 if proposal == 0 else -1)
            if 0 <= destination < length:
                well, rail = destination, proposal
            else:
                rail = 1-proposal
            if t in clocks:
                word += str(int(2*well+1 >= length))
        cells[word, well, rail] += sign
    return {word: sum(value*value for (w, _, _), value in cells.items() if w == word)
            for word in WORDS}


def velocity_cdf(v):
    # On either band v(k)= +/- cos(k)/sqrt(1+cos(k)**2).
    # For sharp R, averaging both bands is the push-forward of (1+v(k))dk/(2*pi)
    # on the plus band. Restrict to [0,pi], on which v decreases.
    if v <= -1/sqrt(2):
        return 0.0
    if v >= 1/sqrt(2):
        return 1.0
    a = acos(v/sqrt(1-v*v))
    return 1 - (a + asin(sin(a)/sqrt(2))) / pi


def label(s):
    return str(int(1 - abs(1 - s % 2) >= Fraction(1, 2)))


def classical():
    # Over v in (-1,1), crossings of the half-interval threshold occur at
    # y+tau*v=n+1/2. Rational test points avoid rounding a boundary crossing.
    cuts = {Fraction(-1), Fraction(1)}
    for tau in TIMES:
        for n in range(int(START-tau)-2, int(START+tau)+3):
            v = (n + Fraction(1, 2) - START) / tau
            if -1 < v < 1:
                cuts.add(v)
    cuts = sorted(cuts)
    rows = []
    for lo, hi in zip(cuts, cuts[1:]):
        word = "".join(label(START + time*(lo+hi)/2) for time in TIMES)
        weight = velocity_cdf(float(hi)) - velocity_cdf(float(lo))
        assert weight >= 0
        rows.append({"v_from": str(lo), "v_to": str(hi), "word": word, "mass": weight})
    joint = {w: fsum(r["mass"] for r in rows if r["word"] == w) for w in WORDS}
    marginals = [fsum(p for w, p in joint.items() if w[j] == "1") for j in range(len(TIMES))]
    independent = {w: prod(p if bit == "1" else 1-p for p, bit in zip(marginals, w))
                   for w in WORDS}
    return rows, joint, independent


def tv(p, q):
    return fsum(abs(p[w]-q[w]) for w in WORDS)/2


def run():
    small, _ = histories(4)
    assert small == by_words(4)
    slices, joint, independent = classical()
    studies = []
    for length in LENGTHS:
        numerators, last_only = histories(length)
        denominator = 2**int(TIMES[-1]*length)
        p = {word: n/denominator for word, n in numerators.items()}
        studies.append({"wells": length, "ticks": [int(tau*length) for tau in TIMES],
                        "denominator_power_of_two": int(TIMES[-1]*length),
                        "word_numerators": {w: str(n) for w, n in numerators.items()},
                        "word_probabilities": p,
                        "total_variation_to_shared_velocity": tv(p, joint),
                        "total_variation_to_independent_marginals": tv(p, independent),
                        "total_mass_on_zero_limit_words": fsum(p[w] for w in WORDS if joint[w] == 0),
                        "uninterrupted_final_right_probability": last_only/denominator,
                        "right_probability_after_three_reads": fsum(p[w] for w in WORDS if w[-1] == "1")})
    return {"source": "well L/4, sharp R; scaled limit y=1/4; both wall reflections +1",
            "read": "coherent projection of the complete left/right half; retain both rails; 1 denotes right",
            "times_divided_by_length": list(map(str, TIMES)),
            "calibration_four_wells_word_numerators": small,
            "velocity_intervals": slices, "shared_velocity": joint,
            "independent_velocity_per_observation_from_same_origin": independent,
            "total_variation_between_classical_models": tv(joint, independent),
            "finite_studies": studies}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(run(), indent=2) + "\n")
