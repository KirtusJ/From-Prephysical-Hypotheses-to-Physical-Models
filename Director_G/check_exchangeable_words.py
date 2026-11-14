"""Exact word laws for the reflected walk and a finitely extendible rival."""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from math import comb, prod
from pathlib import Path

from check_protected_word_echo import DIRECTIONS, START, outbound


def require(condition, message):
    if not condition:
        raise ValueError(message)


def walk_profiles():
    signed = Counter()
    counted = Counter()
    for directions in DIRECTIONS:
        mode, sign = outbound((START, 0, 0), directions)
        signed[mode] += sign
        counted[mode[2]] += 1

    masses = Counter()
    for (_, _, word), amplitude in signed.items():
        masses[word] += amplitude**2
    return tuple(Fraction(masses[j], 64) for j in range(4)), tuple(
        Fraction(counted[j], 64) for j in range(4)
    )


def marginal(table, places):
    result = Counter()
    for row, probability in table.items():
        result[tuple(row[j] for j in places)] += probability
    return result


def score(table, target):
    first = marginal(table, (0,))
    collision = sum(prob for row, prob in table.items() if row[0] == row[1])
    return collision - 2 * sum(first[j,] * p for j, p in enumerate(target)) + sum(
        p * p for p in target
    )


def nine_bank_marginal(target):
    # Keep the whole finite source in factored form and project onto banks 0,1,2.
    masks = [((), Fraction(7, 16))]
    masks.extend((pair, Fraction(9, 16 * comb(9, 2))) for pair in combinations(range(9), 2))
    common = (target[0] / (1 - target[2]), target[1] / (1 - target[2]))
    result = Counter()
    for rare, weight in masks:
        labels = [(2,) if site in rare else (0, 1) for site in range(3)]
        for row in product(*labels):
            result[row] += weight * prod(common[label] for label in row if label != 2)
    return result


def audit():
    target, fair = walk_profiles()
    require(target == tuple(Fraction(i, 64) for i in (29, 27, 8, 0)), "target words")
    require(fair == tuple(Fraction(i, 64) for i in (49, 7, 8, 0)), "fair words")
    ordinary = {row: prod(target[j] for j in row) for row in product(range(4), repeat=3)}
    fair_pairs = {row: prod(fair[j] for j in row) for row in product(range(4), repeat=2)}
    rival = nine_bank_marginal(target)
    require(sum(rival.values()) == 1, "nine-bank normalization")
    for pair in combinations(range(3), 2):
        require(marginal(rival, pair) == marginal(ordinary, pair), "pair mismatch")
    for row in ordinary:
        require(rival[row] == rival[row[::-1]] == rival[row[1:] + row[:1]], "exchangeability")
    require(rival[2, 2, 2] == 0 and ordinary[2, 2, 2] == Fraction(1, 512), "rare triple")
    require(score(rival, target) == 0, "finite rival score")
    require(score(fair_pairs, target) == Fraction(25, 128), "fair-history score")

    collision = sum(p*p for p in target)
    # Fixed counts attain the negative finite-N boundary of the two-word score.
    fixed = {}
    for i, j in product(range(4), repeat=2):
        fixed[i,j] = target[i] * (64*target[j] - int(i == j)) / 63
    fixed_collision = sum(fixed[j,j] for j in range(4))
    require(score(fixed, target) + (1 - fixed_collision)/64 == 0, "negative finite score")
    extension = []
    for n in range(3, 11):
        mean = n * target[2]
        second = n * (n - 1) * target[2]**2
        extension.append({"banks": n, "E_K": mean, "E_K_times_K_minus_one": second,
                          "excess_over_mean": second - mean})
    require(extension[-2]["excess_over_mean"] == 0, "nine-bank boundary")
    require(extension[-1]["excess_over_mean"] == Fraction(5, 32), "ten-bank violation")

    return {
        "word_order": ["00", "01", "10", "11"],
        "ordinary_signed_word_masses": target,
        "unsigned_fair_path_word_law": fair,
        "ordinary_equal_word_rate": collision,
        "score_on_independent_fair_histories": score(fair_pairs, target),
        "fixed_64_bank_equal_word_rate": fixed_collision,
        "fixed_64_bank_score": score(fixed, target),
        "rare_pair_bank": {"two_rare_weight": Fraction(9, 16), "size": 9,
                           "score": score(rival, target)},
        "extension_obstruction": extension,
        "triple_table": [
            {"words": [format(j, "02b") for j in row], "ordinary": weight,
             "nine_bank_rival": rival[row]} for row, weight in ordinary.items()
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_bytes((json.dumps(audit(), indent=2, default=str) + "\n").encode())

