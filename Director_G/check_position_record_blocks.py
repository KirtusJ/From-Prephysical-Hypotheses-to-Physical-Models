"""Exact comparison of signed position-write histories and regenerated walk blocks."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import json

from check_two_column_transport import check, walk


def record_histories(ticks, writes, incoming):
    """Accumulate amplitude by complete position transcript, terminal site and rail."""
    branches = {((), 0, incoming): 1}
    for clock in range(1, ticks + 1):
        following = Counter()
        for (transcript, x, rail), amplitude in branches.items():
            for outgoing, move in enumerate((1, -1)):
                site = x + move
                word = transcript + (site,) if clock in writes else transcript
                following[word, site, outgoing] += (-1) ** (rail * outgoing) * amplitude
        branches = following
    check(sum(a * a for a in branches.values()) == 2 ** ticks, "history norm")
    return branches


def block_kernel(ticks):
    """Average the two translated one-rail kernels in common integer units."""
    answer = Counter()
    for z, matrix in walk(ticks - 1).items():
        for rail, first in enumerate((1, -1)):
            answer[z + first] += sum(row[rail] ** 2 for row in matrix)
    check(sum(answer.values()) == 2 ** ticks, "kernel normalization")
    check(all(answer[-x] == mass for x, mass in answer.items()), "kernel reflection")
    return answer


def fully_written(ticks):
    return Counter({2 * h - ticks: comb(ticks, h) for h in range(ticks + 1)})


def schedule(lengths, middle):
    writes, boundaries, clock = set(), [], 0
    for ticks, write in zip(lengths, middle):
        writes.update((clock + 1, clock + ticks - 1, clock + ticks))
        if write:
            check(ticks == 4, "optional middle control is defined at four ticks")
            writes.add(clock + 2)
        clock += ticks
        boundaries.append(clock)
    return sorted(writes), boundaries


def recorded_displacements(lengths, middle, incoming):
    writes, boundaries = schedule(lengths, middle)
    selected = [writes.index(t) for t in boundaries]
    answer = Counter()
    for (word, _, _), amplitude in record_histories(sum(lengths), writes, incoming).items():
        sites = [0] + [word[i] for i in selected]
        answer[tuple(b - a for a, b in zip(sites, sites[1:]))] += amplitude * amplitude
    return answer


def verify_product(lengths, middle):
    kernels = [fully_written(t) if write else block_kernel(t) for t, write in zip(lengths, middle)]
    reference = Counter()
    for ((x, mx), (z, mz)) in product(kernels[0].items(), kernels[1].items()):
        reference[x, z] = mx * mz
    for incoming in (0, 1):
        actual = recorded_displacements(lengths, middle, incoming)
        check(actual == reference, "conditional two-block displacements for each incoming rail")
    return {f"{x},{z}": mass for (x, z), mass in sorted(reference.items())}


def joint_return_table(full_hist):
    rates = Counter()
    for key, mass in full_hist.items():
        x, z = (int(k) for k in key.split(","))
        rates[x == 0, z == 0] += Fraction(mass, 256)
    return rates


def run():
    kernels = {}
    for t in (3, 4, 5, 6, 7, 8, 16, 32, 64, 128):
        hist = block_kernel(t)
        variance = Fraction(sum(x*x*m for x, m in hist.items()), 2 ** t)
        if t <= 8:
            for incoming in (0, 1):
                measured = recorded_displacements([t], [False], incoming)
                check(all(measured[x,] == m for x, m in hist.items()), "one-block signed histories")
        kernels[str(t)] = {
            "denominator": 2 ** t, "variance": str(variance),
            "displacement_numerators": dict(sorted(hist.items())),
        }
    check(kernels["4"]["variance"] == "5", "four-tick variance")
    two = {}
    returns = {}
    for mask in product((False, True), repeat=2):
        key = "".join("W" if on else "C" for on in mask)
        two[key] = verify_product((4, 4), mask)
        returns[key] = joint_return_table(two[key])
    two["unequal_4_5"] = verify_product((4, 5), (False, False))

    p = Fraction(1, 2)
    outcomes = tuple(product((False, True), repeat=2))
    fresh = {o: sum(panel[o] for panel in returns.values()) / 4 for o in outcomes}
    shared = {o: (returns["CC"][o] + returns["WW"][o]) / 2 for o in outcomes}
    check(fresh[True, True] == Fraction(1, 16), "fresh returns")
    check(shared[True, True] - fresh[True, True] == p * (1 - p) / 16, "return covariance")
    for code, law in returns.items():
        product_rate = sum((4*int(i)-Fraction(1, 2)) * (4*int(j)-Fraction(1, 2)) * mass
                           for (i, j), mass in law.items())
        check(product_rate == (code == "WW"), "return-product inversion")
    return {
        "kernels": kernels,
        "two_block_integer_joint_displacements": two,
        "two_block_denominators": {"four_plus_four": 256, "four_plus_five": 512},
        "two_return_transcripts_fair_optional_write": {
            name: {f"{int(i)},{int(j)}": str(law[i, j]) for i, j in outcomes}
            for name, law in [("fresh", fresh), ("shared", shared)]
        },
        "timing_write_numerators_over_period": {
            str(t): {
                "single": sum(i in {0, 1, t-1} for i in range(t)),
                "adjacent": sum(i in {0, 1, t-1} and (i+1) % t in {0, 1, t-1}
                                for i in range(t)),
                "shared_switch_adjacent": 3,
            } for t in range(4, 9)
        },
    }


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = run()
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
