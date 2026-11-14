"""Exact forward words, whole preparation matrices and projective orbit of the eight-well walk."""

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path

RING = 8
START = (1,) + (0,) * 15
SITES = (1, 3, 5, 7)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def step(state, switched):
    out = [0] * len(state)
    for x, (right, left) in enumerate(zip(state[::2], state[1::2])):
        phase = -1 if switched and (x // 2) % 2 else 1
        out[2 * ((x + 1) % RING)] = phase * (right + left)
        out[2 * ((x - 1) % RING) + 1] = phase * (right - left)
    return tuple(out)


def ray(state):
    divisor = gcd(*state)
    reduced = tuple(v // divisor for v in state)
    return min(reduced, tuple(-v for v in reduced))


def enumerate_histories(word):
    out = [0] * len(START)
    for directions in product((0, 1), repeat=len(word)):
        x, previous, sign = 0, 0, 1
        for bit, left in zip(word, directions):
            if bit == "1" and x in (2, 3, 6, 7):
                sign = -sign
            if previous and left:
                sign = -sign
            x = (x + (1 if not left else -1)) % RING
            previous = left
        out[2 * x + previous] += sign
    return tuple(out)


def site_numerators(state):
    return tuple(r * r + l * l for r, l in zip(state[::2], state[1::2]))


def profile(state):
    positive = sorted(v for v in site_numerators(state) if v)
    divisor = gcd(*positive)
    return tuple(v // divisor for v in positive)


def orbit():
    current = frozenset([ray(START)])
    seen = {}
    census = []
    all_profiles = set()
    while current not in seen:
        require(len(seen) <= 19, "projective orbit did not close")
        seen[current] = len(census)
        counts = Counter(profile(s) for s in current)
        all_profiles.update(counts)
        if len(census) <= 2:
            distributions = set()
            for state in current:
                weights = site_numerators(state)
                distributions.add(tuple(Fraction(x, sum(weights)) for x in weights))
            require(len(distributions) == 1, "common early site distribution")
        if (1, 1, 1, 5) in counts:
            require(len(counts) == 1, "single profile at this clock")
        census.append(
            dict(
                clock=len(census),
                rays=len(current),
                profiles={str(k): v for k, v in sorted(counts.items())},
            )
        )
        current = frozenset(ray(step(s, b)) for s in current for b in (False, True))
    require(
        all_profiles == {(1,), (1, 1), (1, 1, 1, 1), (1, 1, 2), (1, 1, 1, 5)},
        "complete orbit profiles",
    )
    t0 = seen[current]
    require((t0, len(census)) == (7, 19), "orbit endpoints")
    require(
        all(row["profiles"].keys() == {str((1, 1, 1, 5))} for row in census[3:9]),
        "firstness",
    )
    return dict(repeated_clocks=[t0, len(census)], census=census)


def panel():
    rows = []
    matrices = {side: [[0] * 8 for _ in range(8)] for side in (0, 1)}
    for a, b, c in product((0, 1), repeat=3):
        word = f"0000{a}1{b}{c}{c}"
        state = START
        for digit in word:
            state = step(state, digit == "1")
        require(state == enumerate_histories(word), "independent signed histories")
        active = [state[2 * x + r] for x in SITES for r in (0, 1)]
        require(all(t % 8 == 0 for t in active), "compressed coordinates")
        column = [t // 8 for t in active]
        require(
            sum(t * t for t in column) == 8, "unit norm on the original denominator"
        )
        weights = [(column[k] ** 2 + column[k + 1] ** 2) for k in range(0, 8, 2)]
        side = (a + b + c) % 2
        for i, v in enumerate(column):
            for j, w in enumerate(column):
                matrices[side][i][j] += v * w
        require(sorted(weights) == [0, 2, 2, 4], "expected site profile")
        rows.append(
            dict(
                word=word,
                parity=side,
                column=column,
                weights_over_eight=weights,
                ordinary=str(Fraction(weights[0], 8)),
                quadratic=str(Fraction(weights[0] ** 2, sum(v * v for v in weights))),
            )
        )
    require(matrices[0] == matrices[1], "equality of full matrices")
    result = {}
    for side in (0, 1):
        group = [r for r in rows if r["parity"] == side]
        vals = [
            sum(Fraction(r[law]) for r in group) / 4
            for law in ("ordinary", "quadratic")
        ]
        require(
            vals == [Fraction(1, 4), Fraction(1, 3 if side == 0 else 6)],
            "named site rates",
        )
        result[str(side)] = [str(v) for v in vals]
    for r in rows:
        p = r["weights_over_eight"]
        hidden = [
            Fraction(7, 10)
            * ((Fraction(2, 7) if n == 2 else Fraction(3, 7)) if n else 0)
            + Fraction(3, 10) * Fraction(n * n, sum(k * k for k in p))
            for n in p
        ]
        require(
            hidden == [Fraction(n, 8) for n in p],
            "hidden powers at every nine-tick site",
        )
    return dict(
        odd_sites=SITES,
        rows=rows,
        common_matrix_over_32=matrices[0],
        site_one_ordinary_and_quadratic=result,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    path = parser.parse_args().output
    result = dict(nine_ticks=panel(), orbit=orbit())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8", newline="\n") as f:
        json.dump(result, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
