"""Replay independent site-only clocks of the reciprocal balanced walk."""
import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

from check_pure_mass_criterion import advance, by_words


def snapshot(length, tick):
    state = [(int(j == 0), 0) for j in range(2 * length)]
    for _ in range(tick):
        state = advance(state)
    signed, counts = by_words(length, tick)
    assert state == signed
    amplitudes = [state[x] + state[x + length] for x in range(length)]
    modes = [[v * v for v in row if v] for row in amplitudes]
    ordinary = list(map(sum, modes))
    paths = [counts[x] + counts[x + length] for x in range(length)]
    assert sum(ordinary) == sum(paths) == 2 ** tick
    return {"amplitudes_0R_0L_1R_1L": amplitudes, "modes": modes,
            "ordinary_numerators": ordinary, "word_counts": paths}


def assignments(modes):
    # Each occupied well has either one or two occupied modes.
    choices = []
    for row in modes:
        assert 1 <= len(row) <= 2
        choices.append([row] if len(row) == 1 else [row, [sum(row)]])
    return list(itertools.product(*choices))


def prefix_differences(a_rows, b_rows):
    # Normalize both clocks in units of 1/4096. Split each A cell in half.
    a = sorted((2 * v for row in a_rows for v in row for _ in range(2)), reverse=True)
    b = sorted((v for row in b_rows for v in row), reverse=True)
    increments = [y - x for x, y in itertools.zip_longest(a, b, fillvalue=0)]
    return list(itertools.accumulate(increments))


def six_well_scan():
    length = 6
    state = [(int(j == 0), 0) for j in range(2 * length)]
    counts = []
    for tick in range(1, 121):
        state = advance(state)
        modes = [[v * v for v in state[x] + state[x + length] if v] for x in range(length)]
        assert sum(map(sum, modes)) == 2 ** tick
        counts.append(len({row[0] for row in modes if len(row) == 1}))
    assert counts.count(0) == 117 and counts.count(1) == 3
    return counts


def run():
    a, b = (snapshot(7, tick) for tick in (10, 12))
    aw, bw = a["modes"], b["modes"]
    assert {i: row for i, row in enumerate(aw) if len(row) == 1} == {4: [49], 6: [441]}
    assert {i: row for i, row in enumerate(bw) if len(row) == 1} == {3: [49], 6: [784]}
    assert max(sum(row) for i, row in enumerate(aw) if i != 6) < 441
    assert max(map(max, bw)) > 784
    ratios = [Fraction(4 * aw[i][0], bw[j][0]) for i, j in ((4, 3), (6, 6))]
    assert min(ratios) > 2

    extremes = prefix_differences([[sum(row)] for row in aw], bw)
    assert min(extremes) == extremes[-1] == 0
    partitions_a, partitions_b = assignments(aw), assignments(bw)
    for pa, pb in itertools.product(partitions_a, partitions_b):
        differences = prefix_differences(pa, pb)
        assert min(differences) == differences[-1] == 0

    ac, bc = a["word_counts"], b["word_counts"]
    count_a = Fraction(ac[6], 441) - Fraction(ac[4], 49)
    count_b = Fraction(bc[6], 784) - Fraction(bc[3], 49)
    assert 9 ** 2 > 16 and count_b < 0
    lower_bound = count_a - count_b / 2
    assert lower_bound == Fraction(18673, 7056) > 0
    return {"A_tick_10": a, "B_tick_12": b,
            "corresponding_mass_ratios": list(map(str, ratios)),
            "B_minus_halved_A_prefixes_in_4096ths": extremes,
            "partition_pairs_checked": len(partitions_a) * len(partitions_b),
            "count_score_times_log9_lower_bound": str(lower_bound),
            "six_well_distinct_pure_masses_ticks_1_to_120": six_well_scan()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as artifact:
        artifact.write(json.dumps(run(), indent=2) + "\n")
