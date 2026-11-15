"""Replay the signed reflecting shift in physical and unfolded coordinates."""
import argparse
from itertools import product
import json
from pathlib import Path


def physical_step(state, walls=(1, 1), signed=True):
    length = len(state)
    out = [[0, 0] for _ in state]
    for x, (right, left) in enumerate(state):
        plus = right + left
        minus = right - left if signed else right + left
        if x + 1 == length:
            out[x][1] = walls[1] * plus
        else:
            out[x + 1][0] = plus
        if x == 0:
            out[x][0] = walls[0] * minus
        else:
            out[x - 1][1] = minus
    return out


def path_words(length, ticks):
    """Follow proposed directions. The stored rail after a bounce is reversed."""
    sums = [[0, 0] for _ in range(length)]
    counts = [[0, 0] for _ in range(length)]
    for word in product((0, 1), repeat=ticks):
        site, rail, sign = 0, 0, 1
        for proposal in word:
            if rail == proposal == 1:
                sign = -sign
            neighbor = site + (1 if proposal == 0 else -1)
            if 0 <= neighbor < length:
                site, rail = neighbor, proposal
            else:
                rail = 1 - proposal
        sums[site][rail] += sign
        counts[site][rail] += 1
    return sums, counts


def cycle_step(state, wrap):
    size = len(state)
    return [[(wrap if j == 0 else 1) * sum(state[j - 1]),
             (wrap if j + 1 == size else 1) *
             (state[(j + 1) % size][0] - state[(j + 1) % size][1])]
            for j in range(size)]


def decode(state, parity):
    length = len(state) // 2
    out = []
    for x in range(length):
        if x % 2 == parity:
            out.append(state[x].copy())
        else:
            j = 2 * length - 1 - x
            # u_j=(-1)^(j-length) in this half. The lifted L rail gains -1.
            sign = (-1) ** (j - length)
            right, left = state[j]
            out.append([-sign * left, sign * right])
    return out


def launch(size, x=0, rail=0):
    state = [[0, 0] for _ in range(size)]
    state[x][rail] = 1
    return state


def site_masses(rows):
    return [a*a + b*b for a, b in rows]


def gauge_controls():
    controls = []
    for length in range(2, 15):
        clocks = 3 * length + 3
        for x, rail in product(range(length), range(2)):
            physical = launch(length, x, rail)
            lifted = launch(2 * length, x, rail)
            for tick in range(clocks + 1):
                assert physical == decode(lifted, (x + tick) % 2)
                assert sum(a*a + b*b for a, b in physical) == 2**tick
                physical = physical_step(physical)
                lifted = cycle_step(lifted, (-1)**length)
        controls.append({"wells": length, "basis_launches": 2*length, "last_clock": clocks})
    return controls


def report():
    state = launch(6)
    wrong_wall = launch(6)
    fair = launch(6)
    for _ in range(11):
        state = physical_step(state)
        wrong_wall = physical_step(wrong_wall, walls=(-1, 1))
        fair = physical_step(fair, signed=False)
    assert (state, fair) == path_words(6, 11)
    assert state == [[0, 9], [12, 3], [3, -18], [-15, 0], [0, -24], [2, 26]]
    assert [sum(v) for v in fair] == [463, 463, 341, 341, 220, 220]
    assert 576**2 * 81 > 225**3 and 463 * 225 > 3 * 81 * 341
    assert max(sum(z*z for z in row) for row in state[:-1]) == 576 < 676
    short = launch(3)
    bare = launch(6)
    for _ in range(4):
        short = physical_step(short)
        bare = cycle_step(bare, 1)
    wrong_odd = decode(bare, 0)
    assert site_masses(short) == [2, 1, 13] and site_masses(wrong_odd) == [2, 5, 9]
    return {"six_well_tick_11": {"signed_rails": state, "word_counts_by_rail": fair,
                                 "mass_with_negative_left_reflection": site_masses(wrong_wall)},
            "three_well_tick_4": {"ordinary_reflecting": site_masses(short),
                                  "untwisted_unfolding_control": site_masses(wrong_odd)},
            "signed_basis_checks": gauge_controls()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as dest:
        dest.write(json.dumps(report(), indent=2) + "\n")
