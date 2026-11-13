"""Finite forward returns, classical memory controls and exact port histories.

Run python -B check_ring_recurrence.py OUTPUT_DIRECTORY (standard library).
All probabilities use unobserved flight and one terminal position/rail read.
"""

import argparse
import json
import math
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path


def return_curves(order, horizon):
    sites = 4 * order
    count = Counter({(0, 1): 1})
    signed = Counter({(0, 1, 0): 1})
    snapshots = []
    for tick in range(horizon + 1):
        denominator = 1 << tick
        mass = Fraction(count[0, 1], denominator)
        sheet_return = [signed[0, 1, j] for j in range(order)]
        coarse = Fraction(sum(x*x for x in sheet_return), denominator)
        ordinary = Fraction(sheet_return[0]**2, denominator)
        assert sum(count.values()) == denominator
        assert sum(x*x for x in signed.values()) == denominator
        if tick:
            fourier = 0.5 / sites * sum(math.cos(2 * math.pi * j / sites)**tick
                                        for j in range(sites)) if tick % 2 == 0 else 0.
            assert abs(float(mass) - fourier) < 2e-14
            assert mass <= Fraction(1, 4)
        if tick in (0, 1, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128):
            snapshots.append(dict(t=tick, count=str(mass), squared_all_sheets=str(coarse),
                                  squared_origin_sheet=str(ordinary),
                                  c_one_third=str((mass + 2 * coarse) / 3)))
        if tick == horizon:
            break
        advanced = Counter()
        next_signed = Counter()
        for (x, old), ways in count.items():
            for new in (-1, 1):
                advanced[(x + new) % sites, new] += ways
        for (x, old, sheet), amplitude in signed.items():
            shifted = (sheet + x // 2) % order
            for new in (-1, 1):
                sign = -1 if new == old == -1 else 1
                next_signed[(x + new) % sites, new, shifted] += sign * amplitude
        count, signed = advanced, next_signed
    return dict(order=order, sites=sites, even_count_limit=str(Fraction(1, sites)),
                limsup_if_c_one_third=str(1 - Fraction(sites - 1, 3 * sites)),
                snapshots=snapshots)


def tape_step(state, order):
    x, rail, j, sign, tape, cursor = state
    new = tape[cursor]
    exchanged = tape[:cursor] + (rail,) + tape[cursor + 1:]
    return ((x + new) % (4 * order), new, (j + x // 2) % order,
            sign * (-1 if rail == new == -1 else 1), exchanged, (cursor + 1) % len(tape))


def undo_tape(state, order):
    x, new, j, sign, tape, cursor = state
    cursor = (cursor - 1) % len(tape)
    rail = tape[cursor]
    x = (x - new) % (4 * order)
    return (x, rail, (j - x // 2) % order,
            sign * (-1 if rail == new == -1 else 1),
            tape[:cursor] + (new,) + tape[cursor + 1:], cursor)


def finite_tape(order, length):
    sites = 4 * order
    tapes = list(product((-1, 1), repeat=length))
    # Check inverse on the full finite carrier, including signed sheet and pointer.
    states = product(range(sites), (-1, 1), range(order), (-1, 1), tapes, range(length))
    checked = 0
    for state in states:
        assert undo_tape(tape_step(state, order), order) == state
        checked += 1
    initials = [(0, 1, 0, 1, tape, 0) for tape in tapes]
    words = Counter()
    periods = []
    for initial in initials:
        state = initial
        word = []
        for _ in range(length):
            state = tape_step(state, order)
            word.append(state[1])
        words[tuple(word)] += 1
        state = tape_step(initial, order)
        period = 1
        while state != initial:
            state = tape_step(state, order)
            period += 1
            assert period <= checked
        periods.append(period)
    assert len(words) == 2**length and set(words.values()) == {1}
    simultaneous = math.lcm(*periods)
    return dict(order=order, tape_bits=length, inverse_states=checked,
                all_prefixes_equiprobable_through=length, initial_cycles=periods,
                complete_initial_distribution_return=simultaneous)


def exact_rank(order):
    # Positive even-time count sequence q_2n has M distinct nonzero spectral
    # values. Verify the moment Hankel rank with rational arithmetic.
    sites = 4 * order
    ch = Counter({0: 1})
    moments = []
    for tick in range(4 * order + 3):
        if tick and tick % 2 == 0:
            moments.append(Fraction(ch[0], 2 << tick))
        nxt = Counter()
        for x, n in ch.items():
            nxt[(x-1) % sites] += n
            nxt[(x+1) % sites] += n
        ch = nxt
    matrix = [[moments[i+j] for j in range(order + 1)] for i in range(order + 1)]
    rank = 0
    for col in range(order + 1):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for i in range(rank + 1, len(matrix)):
            factor = matrix[i][col] / matrix[rank][col]
            matrix[i] = [x - factor*y for x, y in zip(matrix[i], matrix[rank])]
        rank += 1
    assert rank == order
    return rank


def removed_history(order):
    """Removing one word in a dark port is a formal subevent, not a detector."""
    words = {}
    for word in product("LR", repeat=5):
        x, old, j, sign = 0, "R", 0, 1
        for new in word:
            j = (j + x // 2) % order
            sign *= -1 if new == old == "L" else 1
            x = (x + (1 if new == "R" else -1)) % (4 * order)
            old = new
        words["".join(word)] = ((x, old, j), sign)
    removed = "LRRLR"
    port, _ = words[removed]
    assert port == (1, "R", order-1)
    assert {w for w, (v, _) in words.items() if v == port} == {removed, "RLLRR"}
    all_paths, selected = Counter(), Counter()
    for word, (v, sign) in words.items():
        all_paths[v] += sign
        if word != removed:
            selected[v] += sign
    complete = sum(a*a for a in all_paths.values())
    formal = sum(a*a for a in selected.values())
    assert complete == 32 and formal == 33 and len(words) == 32
    return dict(order=order, removed=removed, resolved_port=port,
                total_square=[complete, 32], subset_square=[formal, 32],
                total_count=[32, 32], subset_count=[31, 32])


def rail_recovery():
    # Columns label two sharp preparation rails, rows label the decoded rail.
    # A balanced pulse followed by its exact decoder restores the signed
    # column. A memoryless fair output loses the input on the first pulse.
    h = ((1, 1), (1, -1))
    rows = []
    for c in (Fraction(0), Fraction(1, 8), Fraction(1, 3), Fraction(1)):
        matrix = []
        for out in range(2):
            row = []
            for source in range(2):
                amplitude = Fraction(sum(h[out][i] * h[i][source] for i in range(2)), 2)
                markov = sum(Fraction(1, 2) * Fraction(1, 2) for _ in range(2))
                row.append((1-c)*amplitude**2 + c*markov)
            matrix.append(row)
        contrast = sum(abs(row[0] - row[1]) for row in matrix) / 2
        assert contrast == 1-c
        rows.append(dict(count=str(c), read_by_launch=[[str(p) for p in row] for row in matrix],
                         total_variation=str(contrast)))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    directory = parser.parse_args().output
    directory.mkdir(parents=True, exist_ok=True)
    report = dict(curves=[return_curves(m, 128) for m in (3, 4, 5, 6, 9)],
                  count_moment_ranks={m: exact_rank(m) for m in (3, 4, 5, 6, 9)},
                  formal_subevent=[removed_history(m) for m in range(3, 17)],
                  balanced_rail_recovery=rail_recovery(),
                  tapes=[finite_tape(3, h) for h in (1, 2, 3, 4, 5)],
                  scope="Exact finite snapshots and finite reversible reservoirs. Late limsup and exclusion of a positive count for a closed finite-dimensional affine system follow from the analytic argument.")
    (directory / "ring_recurrence.json").write_bytes((json.dumps(report, indent=2) + "\n").encode())
