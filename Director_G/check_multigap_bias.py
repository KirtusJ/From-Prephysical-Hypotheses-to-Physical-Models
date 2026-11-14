"""Verify the cutoff, sharp value and a finite two-gap control using exact arithmetic."""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import json


def optimum(widths):
    widths = sorted(widths, reverse=True)
    for k in range(1, len(widths) + 1):
        active = widths[:k]
        cutoff = (2*k - 1) / (2 * sum(1/h for h in active))
        if cutoff <= active[-1] and (k == len(widths) or widths[k] <= cutoff):
            assert cutoff >= widths[0]/2
            p = [max(0, 2*(1-cutoff/h)) for h in widths]
            assert sum(p) == 1
            value = cutoff + sum(max(h-cutoff, 0)**2/h for h in widths)
            # Under the attaining law, the winning uniform tail has mean (cutoff+h)/2.
            assert value == sum(weight*(cutoff+h)/2 for h, weight in zip(widths, p))
            return cutoff, value, sum(weight > 0 for weight in p)
    raise AssertionError("no crossing")


def main():
    menu = json.loads((Path(__file__).parent / "results/echo_probability_map.json").read_text())["finite_menu"]
    den = int(menu["mass_denominator"])
    left = sorted({Q(int(item["numerator"]), den) for item in menu["routed_left_half_masks"]} | {Q(1, 2)})
    assert left[0] == 0 and left[-1] == Q(1, 2)
    widths = [b-a for a,b in zip(left,left[1:])]
    cutoff, value, active = optimum(widths)
    assert len(widths) == 33 and active == 11
    assert Q(19822640675,10**12) < value < Q(19822640676,10**12)
    assert optimum([Q(1)])[1] == Q(3, 4)
    # Equal gaps: every permutation couples two four-point midpoint marginals.
    d = [Q(9+2*j,16) for j in range(4)]
    brute = max(sum(max(x,y) for x,y in zip(d,order))/4 for order in permutations(d))
    assert brute == optimum([Q(1),Q(1)])[1] == Q(7,8)
    print(f"lower gaps={len(widths)}, active={active}, cutoff={float(cutoff):.12f}, optimum={float(value):.12f}")


if __name__ == "__main__":
    main()
