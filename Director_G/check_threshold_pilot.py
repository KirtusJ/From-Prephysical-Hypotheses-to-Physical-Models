"""Exact checks for science actions chosen from pilot hits on a persistent threshold."""

from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import json
from math import comb
from pathlib import Path


def threshold_response(mass, u, a, b):
    if a < mass < b:
        return b if u < (mass - a) / (b - a) else a
    if 1 - b < mass < 1 - a:
        return 1 - threshold_response(1 - mass, u, a, b)
    return mass


def target_menu(a, b):
    split = [Q(x, 8) for x in range(9)]
    low = [a + (b - a) * x for x in split]
    actions = sorted(set(low + [1 - s for s in low] + [Q(0), Q(1, 2), Q(1)]))
    # Midpoints integrate each constant region exactly for this grid of actions.
    types = [(x + y) / 2 for x, y in zip(split, split[1:])]
    return low, actions, types


def test_conditional_selection(a, b):
    low, actions, types = target_menu(a, b)
    gap = b - a
    errors = [[threshold_response(s, u, a, b) - s for u in types] for s in actions]
    assert all(sum(row) == 0 for row in errors)
    best_bit = max(sum(map(max, zip(first, second))) for first, second
                   in combinations_with_replacement(errors, 2)) / len(types)
    assert best_bit == gap / 2

    for pilot in low + [1 - s for s in low]:
        p = (min(pilot, 1 - pilot) - a) / gap
        hit = [threshold_response(pilot, u, a, b) for u in types]
        for m in range(1, 5):
            # Enumerate ordered pilot records and all final actions. Each score
            # uses the same type for all draws and the unconditional block weight.
            direct = Q(0)
            for record in product((0, 1), repeat=m):
                hits = sum(record)
                likelihood = [r**hits * (1 - r)**(m - hits) for r in hit]
                values = [sum(e * w for e, w in zip(row, likelihood)) / len(types)
                          for row in errors]
                direct += max(values)
                if hits == 0 and m == 1 and pilot == (a + b) / 2:
                    assert values[actions.index(1 - pilot)] == max(values)
                if hits == 1 and m == 1 and pilot == (a + b) / 2:
                    assert values[actions.index(pilot)] == max(values)
            tv = sum(comb(m, k) * abs(b**k * (1-b)**(m-k) - a**k * (1-a)**(m-k))
                     for k in range(m+1)) / 2
            assert direct == 2 * gap * p * (1-p) * tv
            if pilot in (a, b, 1 - a, 1 - b):
                assert direct == 0
            if m == 1 and p == Q(1, 2):
                assert direct == gap**2 / 2

    # If science types are independently redrawn, each target's conditional error is zero.
    c = (a + b) / 2
    for target in (c, 1 - c):
        assert sum(threshold_response(target, u, a, b) - target for u in types) == 0
    assert all((threshold_response(a, u, a, b) + threshold_response(b, u, a, b)) / 2
               == c for u in types)


def main():
    for endpoints in [(Q(0), Q(1, 4)), (Q(3, 16), Q(5, 16)), (Q(1, 4), Q(1, 2))]:
        test_conditional_selection(*endpoints)
    menu = json.loads((Path(__file__).parent / "results/echo_probability_map.json").read_bytes())["finite_menu"]
    denominator = int(menu["mass_denominator"])
    nodes = sorted({Q(int(row["numerator"]), denominator) for row in menu["routed_left_half_masks"]}
                   | {Q(1, 2)})
    a, b = max(zip(nodes, nodes[1:]), key=lambda pair: pair[1] - pair[0])
    h = b - a
    print(f"largest gap endpoints {float(a):.12f} and {float(b):.12f}")
    print(f"one pilot {float(h**2/2):.12f}, informative bit {float(h/2):.12f}")


if __name__ == "__main__":
    main()
