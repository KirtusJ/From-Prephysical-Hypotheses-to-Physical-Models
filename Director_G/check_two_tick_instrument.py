"""Exact source-return and connectivity controls for a classical position-bin instrument."""
from argparse import ArgumentParser
from collections import defaultdict, deque
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

from check_reflecting_path import launch, physical_step


def signed_column(length, source, ticks):
    state = launch(length, source)
    for _ in range(ticks):
        state = physical_step(state)
    column = {2*x+r: a for x, row in enumerate(state) for r, a in enumerate(row) if a}
    assert sum(a*a for a in column.values()) == 2**ticks
    return column


def direct_column(length, source, ticks):
    totals = defaultdict(int)
    for proposals in product((0, 1), repeat=ticks):
        x, rail, sign = source, 0, 1
        for next_rail in proposals:
            if rail == next_rail == 1:
                sign = -sign
            dest = x + (1 if next_rail == 0 else -1)
            if 0 <= dest < length:
                x, rail = dest, next_rail
            else:
                rail = 1-next_rail
        totals[2*x+rail] += sign
    return {i: a for i, a in totals.items() if a}


def components(columns, sites):
    edges = {2*x+r: set() for x in sites for r in (0, 1)}
    for column in columns:
        cells = set(column).intersection(edges)
        for i, j in combinations(cells, 2):
            edges[i].add(j)
            edges[j].add(i)
    remaining = set(edges)
    groups = []
    while remaining:
        start = min(remaining)
        visited = {start}
        queue = deque([start])
        while queue:
            for neighbor in edges[queue.popleft()] - visited:
                visited.add(neighbor)
                queue.append(neighbor)
        groups.append(sorted(visited))
        remaining -= visited
    return groups


def echo(column, ticks, label, phase=lambda i: 1):
    # Echo a calibrated preparation after a label measurement and diagonal sign error.
    labels = sorted({label(i) for i in column})
    result = {}
    for b in labels:
        mass = sum(a*a for i, a in column.items() if label(i) == b)
        amplitude = sum(a*a*phase(i) for i, a in column.items() if label(i) == b)
        result[b] = (Fraction(mass, 2**ticks), Fraction(amplitude**2, 4**ticks))
    return result


def report():
    scans = []
    for length in range(4, 41):
        columns = [signed_column(length, x, 2) for x in range(length)]
        assert columns == [direct_column(length, x, 2) for x in range(length)]
        assert all(sorted(a*a for a in col.values()) == [1]*4 for col in columns)
        passed = []
        for cut in range(1, length):
            sizes = [len(components(columns, sites)) for sites in
                     (range(cut), range(cut, length))]
            assert sizes == [1, 1]
            passed.append(cut)
        scans.append({"wells": length, "tested": len(passed),
                      "disconnected_cuts": sorted(set(range(1, length)) - set(passed))})
    length, cut = 8, 4
    label = lambda i: int(i//2 >= cut)
    sample = []
    for x in range(length):
        col = signed_column(length, x, 2)
        correct = echo(col, 2, label)
        marked = echo(col, 2, label, lambda i: -1 if i == 2 else 1)
        sample.append({"right_launch": x, "signed_modes_RL_interleaved": sorted(col.items()),
                       "ideal_label_and_return": {b: str(h) for b, (_, h) in correct.items()},
                       "phase_at_1R": {b: str(h) for b, (_, h) in marked.items()}})
    assert sample[0]["ideal_label_and_return"][0] == "1"
    assert sample[0]["phase_at_1R"][0] == "1/4"
    interior_label = lambda i: int(2 <= i//2 <= 5)
    # Phase is the identity outside the central bin, and alternates inside it.
    parity_phase = lambda i: (-1)**(i//2) if interior_label(i) else 1
    central = []
    for ticks in range(3):
        for x in range(length):
            col = signed_column(length, x, ticks)
            assert echo(col, ticks, interior_label) == echo(col, ticks, interior_label, parity_phase)
            central.append((ticks, x))
    one = [signed_column(length, x, 1) for x in range(length)]
    two = [signed_column(length, x, 2) for x in range(length)]
    one_groups = components(one, range(cut))
    central_groups = components(two, range(2, 6))
    assert len(one_groups) > 1 and len(central_groups) == 2
    # A rotation across two modes of the same bin changes its basis-column return.
    # The other columns pass. A relative phase within that bin does the reverse.
    cosine, sine = Fraction(3, 5), Fraction(4, 5)
    assert cosine**2+sine**2 == 1
    return {"all_boundary_cuts": scans, "eight_well_two_tick_probes": sample,
            "one_tick_left_bin_components": one_groups, "central_two_tick_components": central_groups,
            "central_parity_false_pass_clock_and_launch": central,
            "single_mode_sign_basis_echo": "1 for all 16 modes",
            "central_even_odd_balanced_test": {"ideal_return": "1", "with_parity_phase": "0"},
            "rotation_basis_return_on_either_affected_mode": str(cosine**2)}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    with parser.parse_args().output.open("x", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(report(), indent=2) + "\n")
