"""Exact two-time position records with a cell projection or a site-resolving instrument."""
import argparse
from collections import defaultdict
from itertools import product
import json
from math import acos, asin, pi, sqrt
from pathlib import Path


def propagate(state, steps):
    """Integer path sums with the common amplitude divisor omitted."""
    for _ in range(steps):
        out = defaultdict(lambda: [0, 0])
        for x, (right, left) in state.items():
            out[x + 1][0] += right + left
            out[x - 1][1] += right - left
        state = out
    return state


def mass(state):
    return sum(r*r + l*l for r, l in state.values())


def enumerate_words(steps, initial_rail):
    contributions = defaultdict(lambda: [0, 0])
    for word in product((0, 1), repeat=steps):
        x, previous, sign = 0, initial_rail, 1
        for proposed in word:
            if previous == proposed == 1:
                sign *= -1
            x += 1 - 2*proposed
            previous = proposed
        contributions[x][previous] += sign
    return contributions


def small_history_control(steps):
    """Compute both instruments directly by complete two-flight histories."""
    by_site = defaultdict(int)
    by_cell = defaultdict(int)
    for word in product((0, 1), repeat=2*steps):
        x, sign, rail = 0, 1, 0
        for tick, proposal in enumerate(word, start=1):
            if rail == proposal == 1:
                sign *= -1
            x += 1 - 2*proposal
            rail = proposal
            if tick == steps:
                middle = x
        a = 6*abs(middle) <= steps
        b = 3*abs(x) > steps
        by_site[a, b, middle, x, rail] += sign
        by_cell[a, b, x, rail] += sign
    def table(rows):
        probs = [[0, 0], [0, 0]]
        for (a, b, *_), value in rows.items():
            probs[a][b] += value**2
        return probs
    return table(by_cell), table(by_site)


def trial(steps):
    right = propagate({0: (1, 0)}, steps)
    left = propagate({0: (0, 1)}, steps)
    assert mass(right) == mass(left) == 2**steps
    if steps <= 8:
        assert dict(right) == dict(enumerate_words(steps, 0))
        assert dict(left) == dict(enumerate_words(steps, 1))
    effects = defaultdict(lambda: [0, 0, 0])
    for d, (a, b) in right.items():
        c, e = left[d]
        pair = effects[abs(d)]
        pair[0] += a*a + b*b
        pair[1] += c*c + e*e
        pair[2] += a*c + b*e
    assert all(rr == ll and off == 0 for rr, ll, off in effects.values())
    tail = sum(e[0] for d, e in effects.items() if 2*d > steps)
    fine = [[0, 0], [0, 0]]
    split = [{}, {}]
    # Prefix range sums of the restart effects for a translated final interval.
    start_d = -steps
    prefix = [(0, 0, 0)]
    for d in range(start_d, steps + 1):
        a, b = right.get(d, (0, 0))
        c, e = left.get(d, (0, 0))
        rr, ll, off = prefix[-1]
        prefix.append((rr+a*a+b*b, ll+c*c+e*e, off+a*c+b*e))
    for x, (r, l) in right.items():
        group = int(6*abs(x) <= steps)
        split[group][x] = r, l
        low = max(-steps, -(steps//3)-x)
        high = min(steps, steps//3-x)
        base = 0
        if low <= high:
            rr, ll, off = (end-beg for end, beg in
                           zip(prefix[high+1-start_d], prefix[low-start_d]))
            base = rr*r*r + ll*l*l + 2*off*r*l
        fine[group][0] += base
        fine[group][1] += (r*r+l*l)*2**steps - base
    coarse = [[0, 0], [0, 0]]
    for group, branch in enumerate(split):
        last = propagate(branch, steps)
        for x, (r, l) in last.items():
            coarse[group][3*abs(x) > steps] += r*r+l*l
        assert sum(coarse[group]) == sum(fine[group]) == mass(branch)*2**steps
    assert sum(map(sum, fine)) == 2**(2*steps)
    bound = mass(split[1])*tail
    assert fine[1][1] >= bound
    if steps <= 8:
        assert (coarse, fine) == small_history_control(steps)
    return {"flight_ticks": steps, "wells": 8*steps, "common_denominator": 2**(2*steps),
            "joint_coarse": coarse, "joint_fine": fine, "joint_lower_numerator": bound,
            "tail_numerator_single_flight": tail, "first_A_numerator": mass(split[1]),
            "symmetric_displacement_effects_checked": len(effects)}


def run():
    rows = [trial(n) for n in (1, 2, 3, 4, 6, 8, 16, 32, 64, 128, 256, 384)]
    return {"indices": "Rows A false,true. Columns B false,true. All probabilities per incident launch.",
            "origin": "Launch 4n on 8n wells, distances relative to the actual launch.",
            "lower_limit": 4*asin(1/sqrt(35))*acos(1/sqrt(3))/(pi*pi), "trials": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    with parser.parse_args().output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(run(), indent=2) + "\n")
