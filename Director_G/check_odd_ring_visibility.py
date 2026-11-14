"""Odd-cycle parity, physical seam amplitudes and coherent controls."""
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path


def physical_words(length, ticks, source, connected, records=(), prepare_route=False):
    """Enumerate words from (site, sheet, rail, signed source coefficient)."""
    end = Counter()
    for origin, sheet, rail, coefficient in source:
        for steps in product((-1, 1), repeat=ticks):
            x, s, c, value, labels = origin, sheet, rail, coefficient, ()
            for t, step in enumerate(steps, 1):
                if c == step == -1:
                    value = -value
                y = (x + step) % length
                if connected and {x, y} == {0, length - 1}:
                    s ^= 1
                x, c = y, step
                for time, kind in records:
                    if t == time:
                        labels += (x if kind == "site" else c,)
                if prepare_route and t == 1 and c == -1 and x in (0, 1):
                    x = 1-x
            end[labels, x, s, c] += value
    return end


def propagated(length, ticks, source, connected):
    state = Counter({(x, s, c): v for x, s, c, v in source})
    for _ in range(ticks):
        after = Counter()
        for x, s, c in product(range(length), range(2), (-1, 1)):
            parent = (x - c) % length
            other = s ^ int(connected and {x, parent} == {0, length - 1})
            after[x, s, c] = state[parent, other, 1] + c*state[parent, other, -1]
        state = after
    return {x: state[x] for x in state if state[x]}


def base_masses(length, terminal):
    return [sum(v*v for (y, _, _), v in terminal.items() if x == y)
            for x in range(length)]


def table(length, t, source, connected):
    state = propagated(length, t, source, connected)
    words = physical_words(length, t, source, connected)
    assert state == {(x, s, c): v for (_, x, s, c), v in words.items() if v}
    return state


def ordinary_record_law(ends):
    law = Counter()
    for (labels, x, _, c), value in ends.items():
        law[labels, x, c] += value*value
    return {k: v for k, v in law.items() if v}


def check_charts():
    trials = 0
    for length in (3, 5, 7, 9):
        for parity, x, c in product(range(2), range(length), (-1, 1)):
            j = x + length*(parity ^ (x % 2))
            assert j % length == x and j % 2 == parity
            arrived = (j+c) % (2*length)
            new = (x+c) % length
            assert arrived == new + length*((1-parity) ^ (new % 2))
        for start in range(length):
            for initial_sheet in (0, 1):
                # The input includes coherent rail components on a sharp site.
                source = ((start, initial_sheet, 1, 2), (start, initial_sheet, -1, -1))
                for t in range(1, 8):
                    for records in ((), ((1, "rail"), (3, "site")), ((2, "site"),)):
                        u, v = [physical_words(length, t, source, c, records)
                                for c in (False, True)]
                        assert ordinary_record_law(u) == ordinary_record_law(v)
                        trials += 1
    return trials


def coherent_sources():
    out = []
    for relative in (1, -1):
        for source_sheet in (0, 1):
            source = ((0, 0, 1, 1), (1, source_sheet, 1, relative))
            rows = [base_masses(3, table(3, 2, source, c)) for c in (False, True)]
            expected = ([3 + 2*relative, 3 - 2*relative, 2], [3, 3, 2])
            assert rows == list(expected[::1 if source_sheet == 0 else -1])
            assert [sum(row) for row in rows] == [8, 8]
            out.append(dict(relative_sign=relative, sheet_at_1=source_sheet,
                            ordinary=rows[0], reciprocal=rows[1], denominator=8))
    return out


def unequal_flights():
    source = ((0, 0, 1, 1),)
    out = []
    for connected in (False, True):
        long, short = [table(3, t, source, connected) for t in (3, 2)]
        plus, minus = [], []
        for x in range(3):
            direct = cross = 0
            for s, c in product(range(2), (-1, 1)):
                key = x, s, c
                a, b = long.get(key, 0), short.get(key, 0)
                direct += a*a + 2*b*b
                cross += 2*a*b
            plus.append([direct, cross])
            minus.append([direct, -cross])
        expected = [[6, 0], [7, 0], [3, 0]] if connected else [[6, 4], [7, -2], [3, -2]]
        assert plus == expected
        out.append(dict(connected=connected, denominator=32, plus=plus, minus=minus))
    return out


def routed_source():
    rows = []
    for connected in (False, True):
        for initial in (1, -1):
            sharp = ((1, 0, initial, 1),)
            first = propagated(3, 1, sharp, connected)
            assert first == {(0, 0, -1): initial, (2, 0, 1): 1}
            after = []
            for (x, s, c), value in first.items():
                target = 1 - x if c == -1 and x in (0, 1) else x
                after.append((target, s, c, value))
            state = propagated(3, 2, after, connected)
            words = physical_words(3, 3, sharp, connected, prepare_route=True)
            assert state == {(x, s, c): v for (_, x, s, c), v in words.items() if v}
            coherent = base_masses(3, state)
            recorded = physical_words(3, 3, sharp, connected, ((1, "rail"),), True)
            law = ordinary_record_law(recorded)
            incoherent = [sum(v for (_, y, _), v in law.items() if x == y) for x in range(3)]
            assert incoherent == [2, 3, 3]
            expected = [2, 3, 3] if connected else [2, 3-2*initial, 3+2*initial]
            assert coherent == expected
            rows.append(dict(reciprocal=connected, launch_rail=initial, denominator=8,
                             coherent=coherent, direction_recorded=incoherent))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = ((0, 0, 1, 1),)
    even = [base_masses(4, table(4, 3, source, c)) for c in (False, True)]
    assert even == [[0, 8, 0, 0], [0, 6, 0, 2]]
    data = dict(sharp_source_record_checks=check_charts(), two_site_inputs=coherent_sources(),
                sharp_launch_router=routed_source(),
                controlled_hold=dict(coefficient_basis=["1", "sqrt(2)"], runs=unequal_flights()),
                even_four_cycle=dict(identity=even[0], reciprocal=even[1], denominator=8))
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(data, output, indent=2)
        output.write("\n")


if __name__ == "__main__":
    main()
