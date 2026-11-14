"""Recompute the count-fraction comparisons from the archived Figure 3 counts.

Run python -B check_cesium_count_fraction.py NEW_DIRECTORY. Standard library only.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent / "results/cesium_negative_read.json"
PDF_SHA256 = "513fb6d398c0c6c51523e5154def4c154c8b35809f1348765d3ea3735b232c31"
FIGURE_COUNTS = {
    "blank": [0, 0, 0, 0, 0, 2, 15, 131, 33, 35, 14, 0, 0, 0, 0, 0, 0],
    "retain_negative": [0, 0, 0, 0, 0, 0, 31, 107, 32, 31, 0, 0, 22, 42, 111, 27, 1],
    "retain_positive": [2, 22, 113, 40, 31, 0, 0, 27, 29, 115, 25, 0, 0, 0, 0, 0, 0],
}
GRID = 1_000_000
FAMILIES = {
    "fixed_table_and_direction": 1,
    "one_specified_arm": 6,
    "either_arm_against_blank": 12,
    "five_wells_three_row_pairs_two_directions": 60,
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def walk(first):
    """Program R is the initially occupied spin moving towards negative plotted j."""
    signed = Counter()
    number = Counter()
    for word in product("RL", repeat=4):
        if first is not None and word[0] != first:
            continue
        sign, previous = 1, "R"
        for rail in word:
            if previous == rail == "L":
                sign = -sign
            previous = rail
        site = (word.count("L") - word.count("R")) // 2
        signed[site, previous] += sign
        number[site, previous] += 1
    counts = [sum(number[j, rail] for rail in "RL") for j in range(-2, 3)]
    squares = [sum(signed[j, rail] ** 2 for rail in "RL") for j in range(-2, 3)]
    require(sum(counts) == sum(squares) == (16 if first is None else 8), "walk normalization")
    return {"count": counts, "square": squares, "denominator": sum(counts)}


def selected_odds(model, alpha, neighbour_fraction=Fraction(0)):
    """Optional symmetric misidentification acts before well-dependent collection."""
    odds = []
    for name in ("blank", "retain_positive"):
        row = model[name]
        mixed = [(1 - alpha) * s + alpha * c for s, c in zip(row["square"], row["count"])]
        left, centre, right = mixed[1:4]
        error = neighbour_fraction
        left = (1 - error) * left + error * (mixed[0] + centre) / 2
        right = (1 - error) * right + error * (centre + mixed[4]) / 2
        odds.append(left / right)
    return odds[0] / odds[1]


class FixedMargins:
    """Fisher's noncentral hypergeometric law on the observed two-by-two margins."""
    def __init__(self, table):
        (self.observed, b), (c, d) = table
        n, m, k = self.observed + b, c + d, self.observed + c
        self.support = range(max(0, k - m), min(k, n) + 1)
        self.coefficients = [comb(n, x) * comb(m, k - x) for x in self.support]

    def upper_tail(self, theta):
        a, b = theta.as_integer_ratio()
        lo, hi = self.support[0], self.support[-1]
        weights = [c * a**(x - lo) * b**(hi - x)
                   for x, c in zip(self.support, self.coefficients)]
        return Fraction(sum(weights[self.observed - lo:]), sum(weights))


def alpha_bracket(predicate):
    """Monotone false-to-true transition, including a threshold on a grid point."""
    low, high = 0, GRID
    require(not predicate(Fraction(0)) and predicate(Fraction(1)), "threshold outside interval")
    while high - low > 1:
        middle = (low + high) // 2
        if predicate(Fraction(middle, GRID)):
            high = middle
        else:
            low = middle
    return [str(Fraction(low, GRID)), str(Fraction(high, GRID))]


def run():
    archive = json.loads(EVIDENCE.read_bytes())
    require(archive["source_sha256"] == PDF_SHA256 and archive["figure"] == 3, "original figure")
    for panel, expected in zip(archive["digitized"], FIGURE_COUNTS.values(), strict=True):
        require([panel["counts"][str(j)] for j in range(-8, 9)] == expected, "published counts")
    model = {name: walk(first) for name, first in zip(FIGURE_COUNTS, (None, "R", "L"), strict=True)}
    require(model["blank"]["square"] == [1, 10, 2, 2, 1]
            and model["retain_positive"]["square"] == [0, 1, 1, 5, 1], "orientation")
    table = [[FIGURE_COUNTS[name][j + 8] for j in (-1, 1)] for name in ("blank", "retain_positive")]
    (a, b), (c, d) = table
    observed_odds = Fraction(a * d, b * c)
    law = FixedMargins(table)
    limits = {}
    for family, comparisons in FAMILIES.items():
        size = Fraction(1, 20 * comparisons)
        limits[family] = {"comparisons": comparisons, "tail_size": str(size),
                          "alpha_bracket": alpha_bracket(
                              lambda x: law.upper_tail(selected_odds(model, x)) <= size)}
    require(selected_odds(model, Fraction(0)) == 25 and selected_odds(model, Fraction(1)) == 3,
            "pure laws")
    require([Fraction(row["alpha_bracket"][1]) * GRID for row in limits.values()]
            == [487884, 585974, 616924, 679303], "conditional upper endpoints")
    sensitivity = []
    for error in (Fraction(0), Fraction(1, 50), Fraction(1, 25)):
        # The analytic response in the article establishes monotonicity.
        bound = alpha_bracket(lambda x: law.upper_tail(selected_odds(model, x, error)) <= Fraction(1, 20))
        sensitivity.append({"adjacent_error": str(error), "odds_at_zero": str(selected_odds(model, Fraction(0), error)),
                            "odds_at_one": str(selected_odds(model, Fraction(1), error)), "alpha_bracket": bound})
    pure_tail = law.upper_tail(Fraction(3))
    return {"source": archive["source"], "original_pdf_sha256": PDF_SHA256, "figure": 3,
            "well_indices": list(range(-8, 9)), "counts_including_displaced": FIGURE_COUNTS,
            "total_launch_rows": [sum(row) for row in FIGURE_COUNTS.values()],
            "retained_counts": [sum(FIGURE_COUNTS["retain_negative"][:12]),
                                sum(FIGURE_COUNTS["retain_positive"][5:])],
            "blank_outside_ideal": {"site": -3, "atoms": 2},
            "model_wells": list(range(-2, 3)), "model_rows": model,
            "two_well_table_rows_blank_and_retain_positive": table, "table_columns": [-1, 1],
            "conditional_support": [law.support[0], law.support[-1]], "sample_odds": str(observed_odds),
            "alpha_matching_sample_odds": alpha_bracket(lambda x: selected_odds(model, x) <= observed_odds),
            "one_sided_exact_conditional_limits": limits, "pure_count_upper_tail": str(pure_tail),
            "symmetric_adjacent_misidentification_sensitivity": sensitivity}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "cesium_count_fraction.json").open("x", encoding="utf8", newline="\n") as output:
        json.dump(result, output, indent=2, allow_nan=False)
        output.write("\n")
