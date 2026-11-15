"""Exact terminal path sums, controls, and sitewise partitions for unsigned swaps."""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path


PANELS = {
    5: (((3, 3),), {-5: (0, 1), -1: (0, -2), 1: (0, 4)}),
    6: (((3, 1), (4, 4)), {-2: (1, 0), 0: (0, -4), 2: (0, 5)}),
    9: (((2, 2), (3, -3)), {-9: (0, -1), -5: (0, 2),
                              -3: (0, -16), 3: (0, 2)}),
}
FIVE_SCORES = {-5: 16, -1: -8, 1: 1}
NINE_SCORES = {-9: 768, -5: -512, -3: 1, 3: 256}


def path_sums(ticks, swaps):
    amps, counts = Counter(), Counter()
    for steps in product((-1, 1), repeat=ticks):
        x, rail, sign = 0, 1, 1
        for tick, step in enumerate(steps, 1):
            if rail == step == -1:
                sign = -sign
            x += step
            rail = -step if (tick, x) in swaps else step
        amps[x, rail] += sign
        counts[x] += 1
    return {x: (amps[x, 1], amps[x, -1]) for x in counts}, counts


def propagate(ticks, swaps=(), sign_sites=()):
    state = {0: (1, 0)}
    for tick in range(1, ticks + 1):
        after = {}
        for x in range(-tick, tick + 1, 2):
            right = sum(state.get(x - 1, (0, 0)))
            r, l = state.get(x + 1, (0, 0))
            left = r - l
            if (tick, x) in swaps:
                right, left = left, right
            if (tick, x) in sign_sites:
                right, left = -right, -left
            after[x] = (right, left)
        state = after
    return state


def score(weights, coefficients):
    return Fraction(sum(weights[x] * c for x, c in coefficients.items()),
                    sum(weights.values()))


def check_panel(ticks, swaps, targets):
    rails, counts = path_sums(ticks, swaps)
    assert rails == propagate(ticks, swaps)
    assert all(rails[x] == pair for x, pair in targets.items())
    assert all(counts[x] == comb(ticks, (x + ticks) // 2) for x in rails)
    mass = {x: r*r + l*l for x, (r, l) in rails.items()}
    assert sum(mass.values()) == sum(counts.values()) == 2**ticks
    peak = max(targets, key=mass.get)
    assert all(mass[peak] > m for x, m in mass.items() if x != peak)
    mixed = sorted(x for x, (r, l) in rails.items() if r and l)
    largest_cells = 0
    for split in product((False, True), repeat=len(mixed)):
        split_sites = {x for x, s in zip(mixed, split) if s}
        cells = {x: (r*r, l*l) if x in split_sites else (mass[x],)
                 for x, (r, l) in rails.items()}
        assert all(cells[x] == (mass[x],) for x in targets)
        assert all(value < mass[peak] for x in rails if x != peak for value in cells[x])
        largest_cells = max(largest_cells, sum(len(v) for v in cells.values()))
        for q in (0, 1, 2, 7):
            weights = {x: sum(m**q for m in values if m) for x, values in cells.items()}
            if ticks == 5:
                assert score(weights, FIVE_SCORES) * sum(weights.values()) == (4**q - 4)**2
            if ticks == 9:
                value = 4**q
                factored = (value - 4)**2 * (value**2 + 8*value + 48)
                assert score(weights, NINE_SCORES) * sum(weights.values()) == factored
    report = dict(ticks=ticks, post_shift_swaps=swaps, normalizing_mass=2**ticks,
                  rows=[dict(site=x, right=r, left=l, mass=mass[x], words=counts[x])
                        for x, (r, l) in sorted(rails.items())],
                  partitions=2**len(mixed), maximum_positive_cells=largest_cells)
    if ticks == 5:
        uniform = score({x: 1 for x in rails}, FIVE_SCORES)
        fair = score(counts, FIVE_SCORES)
        assert uniform == Fraction(3, 2) and fair == Fraction(-27, 16)
        assert 9*uniform + 8*fair == 0
        report.update(fair_word_score=str(fair), whole_site_q0_score=str(uniform),
                      zero_score_mixture=dict(whole_site_q0="9/17", fair_words="8/17"))
    if ticks == 6:
        signed = propagate(6, sign_sites=((2, -2), (4, 2)))
        assert all(tuple(v*v for v in signed[x]) == tuple(v*v for v in rails[x]) for x in rails)
        assert (counts[-2], counts[0], counts[2]) == (15, 20, 15)
        assert 4**8 < 5**7
        lower = (Fraction(55, 4) - Fraction(72, 5)*Fraction(7, 8))/64
        assert lower == Fraction(23, 1280)
        report.update(signed_control_rows=sorted(signed.items()),
                      strict_fair_word_score_lower_bound=str(lower))
    if ticks == 9:
        assert largest_cells == 15
        assert score(counts, NINE_SCORES) == Fraction(981, 128)
        report.update(fair_word_score=str(score(counts, NINE_SCORES)),
                      equal_mass_pair_fair_difference=str(Fraction(counts[3]-counts[-5], 2**ticks)))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    panels = [check_panel(t, swaps, targets) for t, (swaps, targets) in PANELS.items()]
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(dict(panels=panels), output, indent=2)
        output.write("\n")


if __name__ == "__main__":
    main()
