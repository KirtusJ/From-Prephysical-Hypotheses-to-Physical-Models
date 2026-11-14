"""Exact finite replays for four homogeneous arc gains and periodic position masks.

Run with Python 3: python -B check_four_gain_winding.py NEW_DIRECTORY
"""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import chain, combinations, product
from math import comb, gcd
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def census(size, masks, gains=None, orders=None):
    """Grow both physical daughters before applying each physical position mask."""
    group_zero = (0,) * len(orders) if orders else ()
    state = Counter({(0, "R", 0, 0, group_zero): 1})
    for layer in masks:
        later = Counter()
        for (x, old, left, ll, gain), count in state.items():
            for rail, step in (("R", 1), ("L", -1)):
                y = x + step
                if size is not None:
                    y %= size
                if layer is not None and y not in layer:
                    continue
                new = gain
                if gains:
                    new = tuple((a + b) % m for a, b, m in zip(gain, gains[old + rail], orders))
                later[y, rail, left + (rail == "L"), ll + (old == rail == "L"), new] += count
        state = later
    return state


def fork(size, laps=1):
    period = size // gcd(size, 2)
    masks = []
    for lap in range(laps):
        x = lap * (period + 1)
        for t in range(1, period + 2):
            sites = {(x + t) % size}
            if t < period:
                sites.add((x - t) % size)
            masks.append(sites)
    return masks


def ports(state):
    out = {}
    for (x, rail, left, _, _), count in state.items():
        out.setdefault((x, rail), Counter())[left] += count
    return out


def support_tests():
    panels = []
    for size in (3, 4, 5, 6, 7):
        period = size // gcd(size, 2)
        depth = 2 * period + 1
        universe = {t: {(t - 2 * d) % size for d in range(t + 1)} for t in range(1, depth + 1)}
        # Remove every possible set of zero, one or two individual (time, well) cells.
        gaps = [(t, x) for t in universe for x in sorted(universe[t])]
        cases = distinct_ports = long_spans = 0
        for cuts in chain.from_iterable(combinations(gaps, k) for k in range(3)):
            mask = [universe[t] - {x for s, x in cuts if s == t}
                    for t in range(1, depth + 1)]
            for cells in ports(census(size, mask)).values():
                values = sorted(cells)
                require(values == list(range(values[0], values[-1] + 1, period)), "winding gap")
                if values[-1] - values[0] >= 2 * period:
                    long_spans += 1
                    require(sum(cells.values()) >= 4, "fewer than four spliced words")
                distinct_ports += 1
            cases += 1
        panels.append(dict(ring=size, depth=depth, cases=cases,
                           occupied_ports=distinct_ports, two_winding_spans=long_spans))
    return panels


def splices(size, low, high):
    period = size // gcd(size, 2)
    height = period
    for cut, (a, b) in enumerate(zip(low, high), 1):
        height += (a == "L") - (b == "L")
        if height == 0:
            break
    require(height == 0 and 0 < cut < len(low), "no interior crossing")
    words = (low, high, high[:cut] + low[cut:], low[:cut] + high[cut:])
    require(len(set(words)) == 4, "four paths not distinct")
    return dict(ring=size, cut=cut, paths=words,
                left_counts=[word.count("L") for word in words])


def arc_identity():
    order = (10, 11)
    edge = {"RR": (3, 8), "RL": (7, 1), "LR": (4, 5), "LL": (9, 10)}
    a, b, c, d = (edge[k] for k in ("RR", "RL", "LR", "LL"))
    checked = 0
    for t in range(10):
        for word in product("RL", repeat=t):
            rail = "R"
            gain = [0, 0]
            left = ll = 0
            for child in word:
                left += child == "L"
                ll += child == rail == "L"
                gain = [(x + y) % m for x, y, m in zip(gain, edge[rail + child], order)]
                rail = child
            e = int(rail == "L")
            for i, modulus in enumerate(order):
                beta = b[i] + c[i] - 2 * a[i]
                h = a[i] + d[i] - b[i] - c[i]
                formula = t*a[i] + e*(a[i]-c[i]) + left*beta + ll*h
                require(gain[i] == formula % modulus, "arc identity")
            checked += 1
    return dict(words=checked, cyclic_orders=order, edge_gains=edge)


def scored_fork():
    # Group label (p,j) is z^p g^j in C2 x C3. z is the negative sign in both reads.
    gains = {"RR": (0, 0), "RL": (0, 1), "LR": (0, 0), "LL": (1, 1)}

    def scores(state, depth):
        z = [0, 0, 0]
        count = 0
        for (_, _, _, _, (negative, j)), n in state.items():
            z[j] += (-1)**negative * n
            count += n
        a, b, c = z
        coherent0 = sum(z)**2
        coherent1 = a*a + b*b + c*c - a*b - b*c - c*a
        return dict(signed_coefficients=z, unnormalized=[coherent0, coherent1, count],
                    probabilities=[str(Fraction(n, 2**depth)) for n in (coherent0, coherent1, count)])

    masks = fork(7)
    ring = census(7, masks, gains, (2, 3))
    control = census(7, [{t % 7} for t in range(1, 9)], gains, (2, 3))
    require(set(ports(ring)) == {(1, "R")} == set(ports(control)), "physical target")
    result = scores(ring, 8)
    require(result["probabilities"] == ["1/64", "1/256", "1/128"], "character/count rates")
    reference = scores(control, 8)
    require(reference["probabilities"] == ["1/256"] * 3, "matched reference")
    line_checked = 0
    for t in range(13):
        for port in ports(raw := census(None, [None] * t, gains, (2, 3))):
            selected = {cell: n for cell, n in raw.items() if cell[:2] == port}
            nums = scores(selected, t)["unnormalized"]
            require(nums[0] == nums[1], "line gauge")
            line_checked += 1
    return dict(gains=gains, ring=7, target=[1, "R"], masks=[sorted(x) for x in masks],
                fork=result, reference=reference, line_ports_checked=line_checked)


def checks():
    forks = []
    for size in (3, 4, 5, 6, 7, 8, 9, 12, 15):
        period = size // gcd(size, 2)
        for k in (1, 2, 3, 4):
            state = census(size, fork(size, k))
            expected = Counter({(k*(period+1) % size, "R", j*period, j*(period-1), ()): comb(k, j)
                                for j in range(k+1)})
            require(state == expected, (size, k, state))
        forks.append(dict(ring=size, deficit_period=period, repetitions=[1, 2, 3, 4]))
    # For N=2 even opposite directions have the same physical destination at every tick.
    small = census(2, fork(2))
    require(sum(small.values()) == 4, "tiny-ring control")
    return dict(arc_formula=arc_identity(), support=support_tests(), repeated_forks=forks,
                splice=splices(7, "R"*15, "L"*14+"R"), physical_probe=scored_fork(),
                tiny_ring=dict(ring=2, depth=2, admitted_paths=sum(small.values())))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    outdir = parser.parse_args().directory
    result = checks()
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "four_gain_winding.json").open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, indent=2)
        out.write("\n")
