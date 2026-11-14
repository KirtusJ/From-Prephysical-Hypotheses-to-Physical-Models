"""Check the five-tick event in complete-record, local readout and counting models."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_position_record_blocks import record_histories
from check_two_column_transport import check, walk


def raw_counts(ticks, writes, incoming):
    rows = record_histories(ticks, writes, incoming)
    converted = {}
    for (word, last_site, rail), amplitude in rows.items():
        check(last_site == word[-1] and rail == int(word[-1] < word[-2]),
              "the last two writes must identify the rail")
        converted[word] = amplitude
    check(len(converted) == len(rows), "one terminal rail per transcript")
    return converted


def event(word, origin):
    return word[1] - word[0] == word[0] - origin


def signs_at_ten(word):
    return (event(word[:3], 0), event(word[3:], word[2]))


def powered(cells, q):
    # Exclude a zero kinematic cell even at q=0.
    scores = {k: mass ** q for k, mass in cells.items() if mass}
    total = sum(scores.values())
    return {k: Fraction(value, total) for k, value in scores.items()}


def local_block(mode, q):
    complete = Counter()
    for initial, first in enumerate((1, -1)):
        columns = {x: (row[0][initial], row[1][initial]) for x, row in walk(3).items()}
        if mode == "local_sites":
            at_four = powered({x: a*a+b*b for x, (a, b) in columns.items()}, q)
            for x, mass in at_four.items():
                a, b = columns[x]
                last_read = powered({1: (a+b)**2, -1: (a-b)**2}, q)
                for final_step, conditional in last_read.items():
                    complete[first, first+x, first+x+final_step] += mass * conditional / 2
        else:
            at_four = powered({(x, rail): a*a for x, ab in columns.items()
                               for rail, a in enumerate(ab)}, q)
            for (x, _), mass in at_four.items():
                # The clock-four rail read is physical in this implementation.
                for final_step in (1, -1):
                    complete[first, first+x, first+x+final_step] += mass / 4
    check(sum(complete.values()) == 1, "local block normalization")
    return complete


def counted(ticks, writes):
    counts = Counter()
    for steps in product((1, -1), repeat=ticks):
        x = 0
        word = []
        for i, step in enumerate(steps, 1):
            x += step
            if i in writes:
                word.append(x)
        counts[tuple(word)] += 1
    return {w: Fraction(k, 2 ** ticks) for w, k in counts.items()}


def join(w1, w2):
    return w1 + tuple(w1[-1] + x for x in w2)


def marginal(law, predicate):
    return sum(v for k, v in law.items() if predicate(k))


def two_table(law, r):
    tab = Counter()
    for word, p in law.items():
        tab[signs_at_ten(word)] += p
    check(sum(tab.values()) == 1, "joint normalization")
    for (i, j), observed in tab.items():
        check(observed == (r if i else 1-r) * (r if j else 1-r), "joint hit table")
    return {"".join("1" if bit else "0" for bit in pair): str(mass)
            for pair, mass in sorted(tab.items())}


def old_record_panel():
    old = record_histories(4, {2, 4}, 0)
    new = record_histories(5, {2, 4, 5}, 0)
    words = sorted({w for w, _, _ in old})
    rows = {}
    for w in words:
        left, right = (old.get((w, w[-1], rail), 0) for rail in (1, 0))
        new_amplitudes = []
        for move, rail in [(-1, 1), (1, 0)]:
            site = w[-1] + move
            new_amplitudes.append(new.get((w + (site,), site, rail), 0))
        check(new_amplitudes == [right - left, right + left], "one real tick after old word")
        rows[w] = {"old_amplitudes_RL": [right, left], "old_mass": left**2+right**2,
                   "new_amplitudes_left_right": new_amplitudes}
    hist = Counter((row["old_mass"], tuple(sorted(v*v for v in row["new_amplitudes_left_right"])))
                   for row in rows.values())
    check(hist == {(1,(1,1)):4, (2,(0,4)):2, (4,(4,4)):2, (0,(0,0)):1}, "complete word classes")
    controls = {}
    for q in (0, 1, 2, 3, 10):
        before = powered({w: r["old_mass"] for w, r in rows.items()}, q)
        after = powered({(w, i): amp**2 for w, r in rows.items()
                         for i, amp in enumerate(r["new_amplitudes_left_right"])}, q)
        delta = {}
        for tag, w in [("S", (2, 4)), ("L", (0, 2))]:
            delta[tag] = sum(p for (v, _), p in after.items() if v == w) - before[w]
        u = 2**q
        witness = 4*delta["S"]-delta["L"]
        analytic = Fraction(2*u*(2-u)**2*(2+u), (8+6*u*u)*(4+2*u+2*u*u))
        check(witness == analytic and delta["L"] == u*u*delta["S"], "two-old-word contrast")
        controls[str(q)] = {"delta_S": str(delta["S"]), "delta_L": str(delta["L"]),
                            "contrast": str(witness)}
    return {"rows": {f"{x},{y}": val for (x, y), val in rows.items()}, "powers": controls}


def run():
    writes = {1, 4, 5}
    both = writes | {t + 5 for t in writes}
    raw_one = [raw_counts(5, writes, rail) for rail in (0, 1)]
    raw_two = [raw_counts(10, both, rail) for rail in (0, 1)]
    prepared = counted(5, writes)
    counted_ten = counted(10, both)
    check(counted_ten == {join(u, v): a*b for u, a in prepared.items()
                          for v, b in prepared.items()}, "raw path counting versus independent blocks")
    computed = {"count": {"r": "3/8", "joint": two_table(counted_ten, Fraction(3, 8))}}
    for incoming, all_rows in enumerate(raw_two):
        composed = {}
        for u, a in raw_one[incoming].items():
            next_rail = int(u[-1] < u[-2])
            for v, b in raw_one[next_rail].items():
                composed[join(u, v)] = a * b
        check(composed == all_rows, "raw signed concatenation including the actual boundary rail")
        for q in (0, 1, 2, 3):
            global_one = powered({w: a*a for w, a in raw_one[incoming].items()}, q)
            global_law = powered({w: a*a for w, a in all_rows.items()}, q)
            kernels = {"global": global_one, "local_sites": local_block("local_sites", q),
                       "local_rail_cells": local_block("local_rail_cells", q)}
            formulas = {"global": Fraction(1 + 9**q, 7 + 9**q),
                        "local_sites": Fraction(5**q, 3 + 5**q),
                        "local_rail_cells": Fraction(1 + 4**q, 4 + 4**q)}
            for name, one in kernels.items():
                law = {join(u, v): a*b for u, a in one.items() for v, b in one.items()}
                if name == "global":
                    check(law == global_law, "every normalized ten-tick global record")
                r = marginal(one, lambda w: event(w, 0))
                check(r == formulas[name], "one-block event formula")
                entry = {"r": str(r), "joint": two_table(law, r)}
                own = computed.setdefault(name, {}).setdefault(str(q), entry)
                check(own == entry, "incoming-rail independence")
                if q == 1:
                    right = marginal(one, lambda w: w[0] == 1 and event(w, 0) and w[2] > w[1])
                    check(2*right == (Fraction(5, 16) if name == "local_rail_cells"
                                      else Fraction(9, 16)), "instrument at the same exponent")
    ref = counted(3, {1, 2, 3})
    for incoming in (0, 1):
        raw_ref = record_histories(3, {1, 2, 3}, incoming)
        check(len(raw_ref) == 8 and all(abs(a) == 1 for a in raw_ref.values()),
              "equal signed-reference words")
    check(len(ref) == 8 and all(p == Fraction(1, 8) for p in ref.values()), "count-reference words")
    r_star = Fraction(5, 8)
    weight = Fraction(11, 20)
    low, high = Fraction(1, 4), Fraction(41, 44)
    mean = weight * high + (1 - weight) * low
    persistent = weight * high**2 + (1 - weight) * low**2
    check(mean == r_star and persistent - mean**2 == Fraction(81, 704), "fresh/persistent control")
    return {
        "old_position_words_at_ticks_two_and_four": old_record_panel(),
        "numerator_scale_squared_ten_ticks": 1024,
        "ten_tick_signed_records": [
            {",".join(map(str, w)): a for w, a in sorted(rows.items())} for rows in raw_two
        ],
        "probabilities": computed,
        "mixture_q2_weight_11_over_20_otherwise_q0": {
            "single": str(mean), "fresh_double": str(mean**2), "persistent_double": str(persistent),
            "persistent_M": str(persistent - mean**2)
        },
    }


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    panel = run()
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(panel, output, indent=2)
        output.write("\n")
