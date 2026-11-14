"""Propagate sorted tags through the binary occupation walk. Requires only the standard library."""

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

from check_occupation_contact import (
    ONE,
    TILTS,
    ZERO,
    add,
    evolve,
    magnitude,
    scale,
    times_i,
)


def require(test, message):
    if not test:
        raise ValueError(message)


def tagged_gate(state, bond, tilt, swap):
    result = {}

    def add_to(key, value):
        result[key] = add(result.get(key, ZERO), value)

    for (record, mask, left_tag, right_tag), v in state.items():
        occupation = (mask >> bond) & 3
        if occupation in (0, 3):
            flipped = swap and occupation == 3
            u, w = (right_tag, left_tag) if flipped else (left_tag, right_tag)
            add_to((record, mask, u, w), scale(5, v))
        else:
            add_to((record, mask, left_tag, right_tag), scale(tilt[0], v))
            add_to(
                (record, mask ^ (3 << bond), left_tag, right_tag), times_i(tilt[1], v)
            )
    return {k: v for k, v in result.items() if v != ZERO}


def tagged_run(timesteps, amplitudes, swap, read_at):
    # alpha=|0>, beta=(p|0>+b|1>)/d. Internal coefficients are checked as integers.
    p, b, d = amplitudes
    require(p * p + b * b == d * d, "tag norm")
    state = {((), 5, 0, 0): (p, 0), ((), 5, 0, 1): (b, 0)}
    for t in range(timesteps):
        state = tagged_gate(state, t % 2, TILTS[t % 2], swap)
        if t + 1 in read_at:
            state = {
                (word + (mask,), mask, i, j): v
                for (word, mask, i, j), v in state.items()
            }
    norm = (5**timesteps * d) ** 2
    table = {}
    resolved = {}
    for (word, mask, i, j), v in state.items():
        key = word + (mask,)
        mass = Q(magnitude(v), norm)
        table[key] = table.get(key, 0) + mass
        resolved[key, i, j] = mass
    require(sum(table.values()) == 1, "all occupation words including failures")
    return table, resolved


def scalar_run(timesteps, contact, read_at):
    sectors = {(): {5: ONE}}
    for t in range(timesteps):
        sectors = {
            word: evolve(state, 3, t, contact) for word, state in sectors.items()
        }
        if t + 1 in read_at:
            sectors = {
                word + (mask,): {mask: v}
                for word, state in sectors.items()
                for mask, v in state.items()
            }
    return {
        word + (mask,): Q(magnitude(v), 25**timesteps)
        for word, state in sectors.items()
        for mask, v in state.items()
    }


def as_text(table):
    return {str(key): str(value) for key, value in sorted(table.items())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    out = parser.parse_args().output
    panels = {}
    for depth, reads in ((3, ()), (3, (1,)), (3, (2,)), (6, (2, 4))):
        plus = scalar_run(depth, 1, reads)
        minus = scalar_run(depth, -1, reads)
        archive = {"plus": as_text(plus), "minus": as_text(minus), "tags": {}}
        for p, b, d in ((1, 0, 1), (0, 1, 1), (3, 4, 5), (4, 3, 5)):
            gamma = Q(p * p, d * d)
            weight = (1 + gamma) / 2
            tagged, resolved = tagged_run(depth, (p, b, d), True, reads)
            frozen, _ = tagged_run(depth, (p, b, d), False, reads)
            for key in plus.keys() | minus.keys() | tagged.keys() | frozen.keys():
                want = weight * plus.get(key, 0) + (1 - weight) * minus.get(key, 0)
                require(tagged.get(key, 0) == want, "exchange sector decomposition")
                require(frozen.get(key, 0) == plus.get(key, 0), "identity contact")
            if depth == 3 and not reads:
                require(
                    tagged[(5,)] == (7696 - 5760 * gamma) / 15625, "three-gate return"
                )
                tv = (
                    sum(
                        abs(tagged.get(k, 0) - plus.get(k, 0))
                        for k in tagged.keys() | plus.keys()
                    )
                    / 2
                )
                require(tv == Q(1152, 3125) * (1 - gamma), "sharp occupation distance")
                if p == 0:
                    require(
                        resolved[(5,), 0, 1] == Q(1296, 15625)
                        and resolved[(5,), 1, 0] == Q(6400, 15625),
                        "orthogonal tag assignments",
                    )
            archive["tags"][str(gamma)] = {
                "occupation_words": as_text(tagged),
                "joint_tag_outcomes": as_text(resolved),
            }
        panels[str((depth, reads))] = archive
    isolated = {((), 3, 0, 1): ONE}
    keep = tagged_gate(isolated, 0, TILTS[0], False)
    exchange = tagged_gate(isolated, 0, TILTS[0], True)
    require(
        keep == {((), 3, 0, 1): (5, 0)} and exchange == {((), 3, 1, 0): (5, 0)},
        "terminal identity ambiguity",
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(panels, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
