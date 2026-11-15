"""Replay the three signed ticks, terminal readout partitions, and controls."""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path


SCHEDULE = {(2, -2), (7, 3), (8, 6)}
SITES = tuple(range(-10, 11, 2))
SCORES = {-2: 81, 0: -18, 4: 1}


def word_counts(schedule, ticks=10):
    amplitudes = Counter()
    unsigned = Counter()
    for word in product((1, -1), repeat=ticks):
        x, previous, sign = 0, 1, 1
        for tick, direction in enumerate(word, 1):
            if previous == direction == -1:
                sign = -sign
            x += direction
            if (tick, x) in schedule:
                sign = -sign
            previous = direction
        amplitudes[x, previous] += sign
        unsigned[x] += 1
    return {x: [amplitudes[x, 1], amplitudes[x, -1]]
            for x in range(-ticks, ticks+1, 2)}, unsigned


def propagated(schedule, ticks=10):
    state = {0: (1, 0)}
    for tick in range(1, ticks+1):
        after = {}
        for x in range(-tick, tick + 1, 2):
            r, l = state.get(x + 1, (0, 0))
            phase = -1 if (tick, x) in schedule else 1
            after[x] = [phase * sum(state.get(x - 1, (0, 0))), phase * (r - l)]
        state = after
    return state


def mean_score(weights):
    return Fraction(sum(value * weights[x] for x, value in SCORES.items()),
                    sum(weights.values()))


def localized_sheet_masses():
    """Start on sheet zero. Swap the two sheets at each addressed vertex."""
    state = Counter({(0, 1, 0): 1})
    for tick in range(1, 11):
        after = Counter()
        for (site, rail, sheet), amplitude in state.items():
            for direction in (1, -1):
                x = site + direction
                out_sheet = sheet ^ int((tick, x) in SCHEDULE)
                sign = -1 if rail == direction == -1 else 1
                after[x, direction, out_sheet] += sign * amplitude
        state = after
    return {x: sum(state[x, rail, sheet]**2
                   for rail in (1, -1) for sheet in (0, 1)) for x in SITES}


def flat_reference_control(masses):
    """Mean gains agree, but type-dependent response and gain covary."""
    e = Fraction(12417, 57602)
    gains1 = {-2: e, 0: 1-e, 4: e}
    gains2 = {x: 1-g for x, g in gains1.items()}
    total1 = sum(masses.values())
    total2 = sum(m*m for m in masses.values())
    corrected = {
        x: (gains1[x] * Fraction(masses[x], total1)
            + gains2[x] * Fraction(masses[x]**2, total2)) / (gains1[x]+gains2[x])
        for x in SCORES
    }
    score = sum(SCORES[x]*corrected[x] for x in SCORES)
    assert score == 0 and all(0 < g < 1 for g in gains1.values())
    ports = list(SCORES)
    cycle_scores = []
    for offset in range(3):
        routed = Fraction()
        for j, x in enumerate(ports):
            port = ports[(j+offset) % len(ports)]
            routed += SCORES[x] * (gains1[port]*Fraction(masses[x], total1)
                                   + gains2[port]*Fraction(masses[x]**2, total2)) / 2
        cycle_scores.append(routed)
    mean_routed = sum(cycle_scores)/3
    expected = sum(gains2.values())/6 * mean_score({x: m*m for x, m in masses.items()})
    assert mean_routed == expected and mean_routed > 0
    return {"q1_gains": {x: str(g) for x, g in gains1.items()},
            "q2_gains": {x: str(g) for x, g in gains2.items()},
            "corrected_target_rates": {x: str(p) for x, p in corrected.items()},
            "equal_mixture_corrected_score": str(score),
            "cyclic_routing_scores_per_incident": [str(d) for d in cycle_scores],
            "cyclic_routing_mean": str(mean_routed)}


def run():
    terminal, counts = word_counts(SCHEDULE)
    bare, _ = word_counts(set())
    assert terminal == propagated(SCHEDULE) and bare == propagated(set())
    assert [counts[x] for x in SITES] == [comb(10, j) for j in range(11)]
    masses = {x: sum(a*a for a in row) for x, row in terminal.items()}
    assert sum(masses.values()) == 1024
    assert [terminal[x] for x in SCORES] == [[2, 0], [0, -6], [-18, 0]]
    assert max(n for x, n in masses.items() if x != 4) == 225
    mixed = [x for x, row in terminal.items() if all(row)]
    partitions = []
    for choices in product((False, True), repeat=len(mixed)):
        split = {x for x, bit in zip(mixed, choices) if bit}
        cells = {x: ([a*a for a in terminal[x] if a] if x in split else [masses[x]])
                 for x in SITES}
        assert sum(map(len, cells.values())) <= 17
        record = {"split_sites": sorted(split), "scores": {}}
        for q in (0, 1, 2, 3):
            weights = {x: sum(v**q for v in row) for x, row in cells.items()}
            score = mean_score(weights)
            assert score * sum(weights.values()) == 4**q * (9**q - 9)**2
            assert (score == 0) == (q == 1)
            record["scores"][str(q)] = str(score)
        partitions.append(record)
    assert len(partitions) == 64
    ordinary_variance = Fraction(sum(k*k*masses[x] for x, k in SCORES.items()), 1024)
    count_score = mean_score(counts)
    bare_masses = {x: sum(a*a for a in row) for x, row in bare.items()}
    localized = localized_sheet_masses()
    assert all(2*localized[x] == masses[x] + bare_masses[x] for x in SITES)
    assert count_score == Fraction(6297, 512)
    assert mean_score(localized) == Fraction(745, 512)
    short_schedule = {(2, -2), (4, 2)}
    short, short_counts = word_counts(short_schedule, ticks=6)
    assert short == propagated(short_schedule, ticks=6)
    assert [short[x] for x in (-2, 0, 2)] == [[-1, 0], [0, 4], [0, -5]]
    assert [short_counts[x] for x in (-2, 0, 2)] == [15, 20, 15]
    assert max(sum(v*v for v in row) for x, row in short.items() if x != 2) == 16
    assert 25**7 > 16**8
    return {
        "signs_after_shift": sorted(SCHEDULE), "scores_by_site": SCORES,
        "all_sites": [{"x": x, "rails_R_L": terminal[x], "site_numerator": masses[x],
                       "unsigned_words": counts[x], "bare_rails_R_L": bare[x],
                       "localized_sheet_numerator": localized[x]} for x in SITES],
        "all_partitions": partitions, "fair_count_score": str(count_score),
        "ordinary_score_variance": str(ordinary_variance),
        "ordinary_fixed_sheet_unobserved_score": str(mean_score(localized)),
        "flat_reference_control": flat_reference_control(masses),
        "six_tick_alternative": {
            "signs_after_shift": sorted(short_schedule),
            "all_sites": [{"x": x, "rails_R_L": row, "unsigned_words": short_counts[x]}
                          for x, row in short.items()]}
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(run(), output, indent=2)
        output.write("\n")
