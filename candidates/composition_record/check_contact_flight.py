"""Compare actual determinant contacts with a position-dependent field, using integer amplitudes."""

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from math import atan, comb, pi, sqrt
from pathlib import Path


def actual_contacts(initial, ticks, modulus, coupled=True):
    """Basis keys are (site, incoming direction, two label coordinates, central residue)."""
    half = pow(2, -1, modulus)
    state = initial.copy()
    for _ in range(ticks):
        following = defaultdict(int)
        for (x, incoming, r, l, z), amplitude in state.items():
            for move in (1, -1):
                dr, dl = int(move == 1), int(move == -1)
                increment = half * (r * dl - l * dr) if coupled else 0
                target = (x + move, move, (r + dr) % modulus, (l + dl) % modulus,
                          (z + increment) % modulus)
                following[target] += -amplitude if incoming == move == -1 else amplitude
        state = {key: value for key, value in following.items() if value}
    return state


def decoded(state, tick, modulus):
    """Undo the terminal base labels and endpoint central phase in real coordinates."""
    half, quarter = pow(2, -1, modulus), pow(4, -1, modulus)
    out = {}
    for (x, direction, r, l, z), value in state.items():
        assert (r, l) == ((tick + x) * half % modulus, (tick - x) * half % modulus)
        key = (x, direction, (z + (tick - 1) * x * quarter) % modulus)
        assert key not in out
        out[key] = value
    return out


def field_steps(initial, ticks, modulus):
    state = initial.copy()
    half = pow(2, -1, modulus)
    for _ in range(ticks):
        following = defaultdict(int)
        for (x, incoming, sheet), value in state.items():
            following[x + 1, 1, (sheet + half * x) % modulus] += value
            following[x - 1, -1, (sheet + half * x) % modulus] += value * incoming
        state = {key: value for key, value in following.items() if value}
    return state


def sharp_words(ticks, modulus):
    """Sum independent signed direction words, using their ordered-pair count."""
    out = defaultdict(int)
    half = pow(2, -1, modulus)
    for word in product((1, -1), repeat=ticks):
        right = word.count(1)
        left = ticks - right
        inversions = sum(word[:j].count(-1) for j, move in enumerate(word) if move == 1)
        z = (right * left - 2 * inversions) * half % modulus
        amplitude = (-1) ** sum(a == b == -1 for a, b in zip((1,) + word, word))
        out[sum(word), word[-1] if word else 1, right % modulus, left % modulus, z] += amplitude
    return {key: value for key, value in out.items() if value}


def positions(state):
    weights = defaultdict(int)
    for (x, *_), value in state.items():
        weights[x] += value * value
    return weights


def launch(sites, modulus, encode):
    half, quarter = pow(2, -1, modulus), pow(4, -1, modulus)
    return {(x, 1, half*x % modulus, -half*x % modulus, quarter*x % modulus)
            if encode else (x, 1, 0, 0, 0): 1 for x in sites}


def five_step_trace():
    """Trace Laurent coefficients, computed without using complex arithmetic."""
    all_tables = []
    for sector in (1, 2, 3, 4):
        table = {m: [0] * 5 for m in (-5, -3, -1, 1, 3, 5)}
        for word in product((1, -1), repeat=5):
            # Close the rail to form the trace. Use every one of the five momentum shifts.
            sign = (-1) ** sum(a == b == -1 for a, b in zip((word[-1],) + word, word))
            phase = sector * sum(j * direction for j, direction in enumerate(word)) % 5
            table[sum(word)][phase] += sign
        assert table[5] == [1, 0, 0, 0, 0] and table[-5] == [-1, 0, 0, 0, 0]
        assert all(len(set(table[m])) == 1 for m in (-3, -1, 1, 3))
        all_tables.append(table)
    return all_tables


def trial():
    flights = []
    packet_cases = []
    for modulus in (5, 7, 11):
        for ticks in range(13):
            for sites in ((0,), (-1, 1), (-4, 0, 2)):
                state = actual_contacts(launch(sites, modulus, True), ticks, modulus)
                field = field_steps({(x, 1, 0): 1 for x in sites}, ticks, modulus)
                assert decoded(state, ticks, modulus) == field
                assert sum(positions(state).values()) == len(sites) * 2 ** ticks
                packet_cases.append([modulus, ticks, list(sites)])
            if ticks <= 10:
                sharp = actual_contacts(launch((0,), modulus, False), ticks, modulus)
                assert sharp == sharp_words(ticks, modulus)
    modulus = 5
    for ticks in range(21):
        initial = launch((0,), modulus, False)
        active = actual_contacts(initial, ticks, modulus)
        quiet = actual_contacts(initial, ticks, modulus, coupled=False)
        p, ordinary = positions(active), positions(quiet)
        sites = list(range(-ticks, ticks + 1, 2))
        assert sum(p.values()) == sum(ordinary.values()) == 2 ** ticks
        flights.append({"ticks": ticks, "sites": sites, "denominator": 2 ** ticks,
                        "contacts": [p[x] for x in sites], "commuting": [ordinary[x] for x in sites],
                        "total_variation": str(Fraction(sum(abs(p[x] - ordinary[x]) for x in sites),
                                                        2 ** (ticks + 1)))})
        if ticks == 10:
            at_origin = {str(direction): [active.get((0, direction, 0, 0, z), 0) for z in range(5)]
                         for direction in (1, -1)}
            assert at_origin == {"1": [26, -5, -5, -5, -5], "-1": [2, 1, 1, 1, 1]}
    assert flights[10]["contacts"][5] == 784 and flights[10]["commuting"][5] == 72
    sharp_packet = actual_contacts(launch((-1, 1), 5, False), 2, 5, coupled=False)
    synchronized = actual_contacts(launch((-1, 1), 5, True), 2, 5)
    # k=0 (uniform central character): sum signed amplitudes over z with amplitudes normalized in that sector.
    uniform = defaultdict(int)
    for (x, direction, r, l, _), value in synchronized.items():
        uniform[x, direction, r, l] += value
    assert positions(sharp_packet)[1] == 3 and positions(uniform)[1] == 5
    v = sqrt(0.5)
    # The odd tilt of the sharp-right density integrates to zero on a symmetric speed window.
    k = 1 / sqrt(1 - 2 * 0.25**2)
    bare_tail = 1 - 2 * atan(0.25 * k) / pi
    assert all(len(set(row[1:])) == 1 for row in at_origin.values())
    trivial = sum(sum(row)**2 for row in at_origin.values())
    nontrivial = sum((row[0] - row[1])**2 for row in at_origin.values())
    at_10 = [str(Fraction(n, 1024)) for n in (trivial, nontrivial)]
    assert at_10 == ["9/128", "481/512"]
    return {"field_equivalence_cases": packet_cases, "raw_path_depths_each_modulus": list(range(11)),
            "sharp_F5": flights, "tick_10_center_amplitudes_over_32": at_origin,
            "tick_10_center_trivial_and_nontrivial_sectors": at_10,
            "tick_10_fresh_direction_writer_center": str(Fraction(comb(10, 5), 2**10)),
            "five_step_trace_by_central_frequency": five_step_trace(),
            "outer_speed_panel": {"cut": 0.25, "free_edge": v, "nonzero_sector_edge": v**5,
                                  "ordinary_tail": bare_tail, "clean_memory_tail": bare_tail/5},
            "two_sources_at_tick_2_plus1": {"denominator": 8, "unprepared_ordinary_label": 3,
                                             "synchronized_and_uniform_central": 5}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    with parser.parse_args().output.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(trial(), indent=2) + "\n")
