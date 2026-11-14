"""Exact word-permutation echoes on five binary slots and the eight-label pass map."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import permutations, product
import json
from math import comb
from pathlib import Path

from check_equal_label_source import source


def require(value, message):
    if not value:
        raise ValueError(message)


def permute(word, order):
    return tuple(word[j] for j in order)


def stats(values, orders, accepted):
    """Real integer amplitudes plus rational normalization, grouped by type class."""
    norm = sum(value**2 for value in values.values())
    layers = Counter()
    groups = defaultdict(Counter)
    for word, value in values.items():
        layers[sum(word)] += value
        if word in accepted:
            k, g, label = accepted[word]
            groups[k, g][label] += value
    symmetric = sum(Fraction(v*v, comb(5, k)*norm) for k, v in layers.items())
    selected = sum(Fraction(v*v, norm) for group in groups.values() for v in group.values())
    uniform = sum(Fraction(sum(group.values())**2, 8*norm) for group in groups.values())
    overlaps = []
    parity_sums = [0, 0]
    adj_sums = []
    for order in orders:
        dot = sum(v*values.get(permute(word, order), 0) for word, v in values.items())
        leak = 1-Fraction(dot*dot, norm*norm)
        overlaps.append(leak)
        inv = sum(i > j for p, i in enumerate(order) for j in order[p+1:])
        parity_sums[inv % 2] += leak
        if inv == 1:
            adj_sums.append(leak)
    average = sum(overlaps)/120
    x = 1-symmetric
    bound = 2*x-Fraction(5, 4)*x*x
    require(average >= bound and bound >= Fraction(3, 4)*x, "incident bound")
    require(parity_sums[0]/60 == parity_sums[1]/60 == average, "parity invariance")
    require(selected-uniform <= x, "postselection contraction")
    # Check adj >= ((3-sqrt(5))/8) * average without rounding.
    adjacent = sum(adj_sums)/4
    lhs = 3*average-8*adjacent
    require(lhs <= 0 or lhs*lhs <= 5*average*average, "path gap")
    return {"outside_symmetric": x, "uniform_permutation_leakage": average,
            "four_adjacent_mean": adjacent, "pass_norm": selected,
            "accepted_wrong_mass_per_start": selected-uniform,
            "leakage_histogram_permutations": dict(sorted(Counter(map(str, overlaps)).items()))}


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    output = parser.parse_args().output
    orders = list(permutations(range(5)))
    words = list(product((0,1), repeat=5))
    accepted = source(5,3)
    w0, w1 = [w for w in accepted if sum(w) == 2][:2]
    require(accepted[w0][:2] == accepted[w1][:2], "same junk")
    first, second = [w for w in words if sum(w) == 1][:2]
    states = {"unit_symmetric": {w: 1 for w in words},
              "irrep_four": {first: 1, second: -1},
              "all_layers": {w: 3*i % 13 - 5 for i,w in enumerate(words)}}
    for k in (2,8,32,128):
        states[f"weak_wrong_pass_{k}"] = {words[0]: k, w0: 1, w1: -1}
    results = {name: stats(value, orders, accepted) for name,value in states.items()}
    # The symmetric blank and the standard ray occupy different weight layers.
    # For coefficients sqrt(7/8), sqrt(1/8), every return overlap is rational.
    weak_phases = Counter()
    for order in orders:
        unit = states["irrep_four"]
        dot = sum(v*unit.get(permute(word, order), 0) for word, v in unit.items())
        overlap = Fraction(7,8) + Fraction(dot,16)
        require(overlap >= Fraction(3,4), "nonlinear full-bank escape")
        weak_phases[str(overlap**2)] += 1
    results["fixed_asymmetry_observed_echo_escape"] = {
        "outside_symmetric": "1/8", "blank_mass_histogram": dict(sorted(weak_phases.items()))
    }
    require(results["irrep_four"]["uniform_permutation_leakage"] == Fraction(3,4),
            "sharpness of unconditional bound")
    for k in (2,8,32,128):
        entry = results[f"weak_wrong_pass_{k}"]
        require(entry["pass_norm"] == entry["outside_symmetric"]
                == entry["accepted_wrong_mass_per_start"] == Fraction(2,k*k+2),
                "all selected mass misses the logical ray")
    with output.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(results, stream, default=str, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
