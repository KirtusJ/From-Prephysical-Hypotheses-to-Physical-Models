"""Exact three-tick position read with static, sheet-blind H, I and X coins."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


COINS = "HHIIIX"


def sqrt_two(pair):
    a, b = pair
    return 2 * b, a


def add(first, second, sign=1):
    return first[0] + sign * second[0], first[1] + sign * second[1]


def square(pair):
    a, b = pair
    return a * a + 2 * b * b, 2 * a * b


def cover_steps(coins, launch=1, seam=True):
    """Each tick contributes sqrt(2) to the amplitude denominator."""
    size = 12 if seam else 6
    rails = [[(0, 0), (0, 0)] for _ in range(size)]
    rails[0][0 if launch == 1 else 1] = (1, 0)
    yield rails
    for _ in range(3):
        following = [[(0, 0), (0, 0)] for _ in range(size)]
        for j, (right, left) in enumerate(rails):
            gate = coins[j % 6]
            if gate == "H":
                right, left = add(right, left), add(right, left, -1)
            else:
                if gate == "X":
                    right, left = left, right
                right, left = sqrt_two(right), sqrt_two(left)
            following[(j + 1) % size][0] = right
            following[(j - 1) % size][1] = left
        rails = following
        yield rails


def site_masses(rails, tick):
    bins = [[] for _ in range(6)]
    for j, modes in enumerate(rails):
        bins[j % 6].extend(square(row) for row in modes if row != (0, 0))
    total = (0, 0)
    for group in bins:
        for mass in group:
            total = add(total, mass)
    if total != (2 ** tick, 0):
        raise ValueError("norm on cover")
    return bins


def physical_words(tick, launch=1, seam=True):
    """Walk each legal signed word in physical coordinates, counting local flips."""
    rows = []
    amplitudes = {}
    conditional = [Fraction(0) for _ in range(6)]
    counts = [0] * 6
    for word in product((1, -1), repeat=tick):
        x = sheet = splits = 0
        previous, sign = launch, 1
        for step in word:
            gate = COINS[x]
            if gate == "H":
                splits += 1
                if previous == step == -1:
                    sign = -sign
            elif step != (previous if gate == "I" else -previous):
                break
            dest = (x + step) % 6
            if seam and {x, dest} == {0, 5}:
                sheet ^= 1
            x, previous = dest, step
        else:
            key = (x, sheet, previous)
            amplitude = (sign, 0)
            for _ in range(tick - splits):
                amplitude = sqrt_two(amplitude)
            amplitudes[key] = add(amplitudes.get(key, (0, 0)), amplitude)
            conditional[x] += Fraction(1, 2 ** splits)
            counts[x] += 1
            rows.append(dict(word="".join("R" if d == 1 else "L" for d in word),
                             x=x, sheet=sheet, sign=sign, hadamards=splits))
    if sum(conditional) != 1:
        raise ValueError("local branching law")
    return rows, amplitudes, conditional, counts


def checked_output():
    controls = []
    for seam, launch in product((True, False), (1, -1)):
        for tick, rails in enumerate(cover_steps(COINS, launch, seam)):
            words, amplitudes, conditional, counts = physical_words(tick, launch, seam)
            for j, pair in enumerate(rails):
                for index, direction in enumerate((1, -1)):
                    if pair[index] != amplitudes.get((j % 6, j // 6, direction), (0, 0)):
                        raise ValueError("physical word and cover disagree")
            bins = site_masses(rails, tick)
            if tick == 3:
                expected = [[], [(3, 2*launch)], [], [(2, 0)], [], [(3, -2*launch)]]
                if bins != expected or counts[1::2] != [2, 1, 2]:
                    raise ValueError("three-well masses or legal word counts")
                if conditional[1::2] != [Fraction(3, 8), Fraction(1, 4), Fraction(3, 8)]:
                    raise ValueError("conditional fair branching")
            controls.append(dict(seam=seam, launch="R" if launch == 1 else "L", tick=tick,
                                 squared_mass_groups=bins, denominator=2**tick, words=words,
                                 legal_word_counts=counts,
                                 fair_branch_masses=list(map(str, conditional))))
    patterns = []
    for coins in map("".join, product("HIX", repeat=6)):
        pure_counts = []
        for tick, rails in enumerate(cover_steps(coins)):
            bins = site_masses(rails, tick)
            pure_counts.append(len({group[0] for group in bins if len(group) == 1}))
        patterns.append(dict(coins=coins, distinct_pure_masses=pure_counts))
    by_tick = [dict(sorted(Counter(row["distinct_pure_masses"][t] for row in patterns).items()))
               for t in range(4)]
    if any(3 in histogram for histogram in by_tick[:3]) or not by_tick[3].get(3):
        raise ValueError("earliest static three-mass record")
    return dict(coin_order="wells 0 through 5", witness=COINS,
                pair_encoding="(a,b) denotes a+b*sqrt(2) over the stated denominator",
                controls=controls, counts_by_tick=by_tick, all_static_assignments=patterns)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    path = parser.parse_args().output
    record = checked_output()
    # Keep each of the 729 complete experimental assignments on one line.
    patterns = record.pop("all_static_assignments")
    header = json.dumps(record, indent=2).removesuffix("\n}")
    rows = ",\n".join("    " + json.dumps(row) for row in patterns)
    text = header + ',\n  "all_static_assignments": [\n' + rows + "\n  ]\n}\n"
    path.write_bytes(text.encode())
