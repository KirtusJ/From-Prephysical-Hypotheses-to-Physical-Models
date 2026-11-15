"""Exact replay of the eight-site distance and complete-address comparisons."""

import argparse
import json
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path


def check(condition, message):
    if not condition:
        raise ValueError(message)


def columns(start):
    """Integer amplitudes. Physical amplitudes are scaled by 2**(-t/2)."""
    field = [(0, 0)] * 8
    field[0] = start
    history = [field]
    for _ in range(24):
        field = [(sum(field[(x - 1) % 8]),
                  field[(x + 1) % 8][0] - field[(x + 1) % 8][1])
                 for x in range(8)]
        history.append(field)
    return history


def signed_words(ticks, input_rail):
    field = [[0, 0] for _ in range(8)]
    for word in product(range(2), repeat=ticks):
        # The only negative Hadamard entry is L->L, including the initial coin.
        flips = sum(a * b for a, b in zip((input_rail,) + word, word))
        displacement = ticks - 2 * sum(word)
        field[displacement % 8][word[-1]] += (-1) ** flips
    return [tuple(row) for row in field]


def raw_counts(ticks):
    counts = [0] * 8
    for left in range(ticks + 1):
        counts[(ticks - 2 * left) % 8] += comb(ticks, left)
    return counts


def probabilities(masses, q):
    weights = [F(m) ** q if m else F(0) for m in masses]
    return [w / sum(weights) for w in weights]


def average(weights, rows):
    return [sum(w * x for w, x in zip(weights, entries)) for entries in zip(*rows)]


def main():
    right, left = columns((1, 0)), columns((0, 1))
    for rail, history in enumerate((right, left)):
        for t in (2, 6, 18):
            check(signed_words(t, rail) == history[t], f"word sum at {t}, rail {rail}")
        check(history[24] == [(4096*a, 4096*b) for a, b in history[0]], "period")

    masses = {2: [2, 1, 1], 5: [5, 1, 1, 1]}
    mixture = [F(57, 204), F(7, 204), F(140, 204)]
    powers = [-2, 0, 2]
    clock_table = []
    for t in range(24):
        records = {}
        for label, history in (("R", right), ("L", left)):
            squares = [a*a + b*b for a, b in history[t]]
            check(sum(squares) == 2**t, "normalization")
            positive = sorted((m for m in squares if m), reverse=True)
            ratios = [F(m, positive[-1]) for m in positive]
            expected = (masses[2] if t in (2, 9, 14, 21) else
                        masses[5] if 3 <= t <= 8 or 15 <= t <= 20 else
                        [1] * len(positive))
            check(ratios == expected, f"clock classification at {t}")
            matched = average(mixture, [probabilities(squares, q) for q in powers])
            check(matched == probabilities(squares, 1), f"fresh mixture at {t}, {label}")
            records[label] = squares
        clock_table.append({"ticks": t, "denominator": 2**t, "site_numerators": records})

    flight_data = {}
    for t in (6, 18):
        rows = []
        for d in range(8):
            a, b = right[t][d]
            c, e = left[t][d]
            effect = F(0) if d % 2 else F(5 if d == 4 else 1, 8)
            check(a*a + b*b == c*c + e*e == effect * 2**t and a*c + b*e == 0,
                  f"scalar effect at {t}, {d}")
            rows.append({"displacement": d, "matrix_times_2_to_half_ticks": [[a, c], [b, e]],
                         "effect": str(effect), "fair_paths": raw_counts(t)[d]})
        flight_data[str(t)] = rows

    # Interfere the two first sites at tick ten, or preserve separate records.
    # Physical amplitudes in the two-flight product have denominator 2**5.
    controls = []
    for direction in (right, left):
        row = []
        for final in range(8):
            branches = []
            for first in (2, 6):
                a, b = direction[6][first]
                shift = (final - first) % 8
                branches.append(tuple(a*r + b*l for r, l in zip(right[4][shift], left[4][shift])))
            row.append(branches)
        controls.append(row)
    joint_rows = {}
    for coherent in (False, True):
        by_radius = []
        for sites in ((0,), (2, 6), (4,)):
            gram = []
            for i, j in ((0, 0), (0, 1), (1, 1)):
                numerator = 0
                for x in sites:
                    vi, vj = controls[i][x], controls[j][x]
                    if coherent:
                        vi, vj = [list(map(sum, zip(*vi)))], [list(map(sum, zip(*vj)))]
                    numerator += sum(a*b for u, v in zip(vi, vj) for a, b in zip(u, v))
                gram.append(F(numerator, 2**10))
            check(gram[0] == gram[2] and gram[1] == 0, "scalar two-write effect")
            by_radius.append(gram[0])
        expected = [F(1, 8), F(0), F(1, 8)] if coherent else [F(3, 32), F(1, 16), F(3, 32)]
        check(by_radius == expected, "two-write radial row")
        joint_rows["coherent" if coherent else "fine_rail_preserving"] = list(map(str, by_radius))

    radial = [1, 2, 5]
    direct = [probabilities(radial, q) for q in powers]
    coarse_mixture = average(mixture, direct)
    check(coarse_mixture == [F(n, 8772) for n in (2201, 1378, 5193)], "coarse mixture")
    counting = [F(5, 16), F(1, 2), F(3, 16)]
    for t, expected in [(6, counting), (18, [F(257, 1024), F(1, 2), F(255, 1024)])]:
        n = raw_counts(t)
        check([F(a, 2**t) for a in (n[0], n[2]+n[6], n[4])] == expected, "fair paths")
    check(average([F(1, 52), F(35, 52), F(16, 52)], [direct[1], direct[2], counting])
          == probabilities(radial, 1), "counting admixture at six")

    # First and second clock rivals with nonnegative powers.
    check(average([F(1, 2)] * 2, [probabilities(masses[2], q) for q in (0, 2)])
          == probabilities(masses[2], 1), "changed first law")
    check(average([F(5, 12), F(7, 12)], [probabilities(masses[5], q) for q in (0, 2)])
          == probabilities(masses[5], 1), "changed second law")
    for history in (right, left):
        distributions = []
        for q in (0, 2):
            for t in (2, 6):
                rail_cells = [a*a for row in history[t] for a in row]
                scored = probabilities(rail_cells, q)
                sites = [a+b for a, b in zip(scored[::2], scored[1::2])]
                if t == 2:
                    check(sites == probabilities([sum(a*a for a in row) for row in history[t]], 1),
                          "split first read")
                else:
                    distributions.append(sites)
        check(average([F(9, 20), F(11, 20)], distributions)
              == probabilities([sum(a*a for a in row) for row in history[6]], 1),
              "persistent rail-cell mixture")

    return {"flight_effects_and_path_counts": flight_data, "sharp_clock_table": clock_table,
            "joint_final_radius_given_first_radius_two_per_incident": joint_rows,
            "fresh_powers": powers, "fresh_weights": list(map(str, mixture)),
            "direct_distance_for_same_mixture": list(map(str, coarse_mixture)),
            "counting_false_pass_at_six": {"q0": "1/52", "q2": "35/52", "counting": "16/52"},
            "antipode_count_change": str(F(255, 1024) - F(3, 16)),
            "clock_dependent_q2_probabilities": ["1/2", "7/12"],
            "rail_split_persistent_q2_probability": "11/20"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="replace the checked-in result")
    options = parser.parse_args()
    result = (json.dumps(main(), indent=2) + "\n").encode("utf-8")
    result_path = Path(__file__).with_name("results") / "ring_distance.json"
    if options.write:
        result_path.write_bytes(result)
    elif result_path.read_bytes() != result:
        raise ValueError("stored distance table differs from replay")
    print("Verified the two launch columns, all 24 clocks, path sums and detector controls.")
