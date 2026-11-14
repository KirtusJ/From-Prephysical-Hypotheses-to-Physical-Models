"""Whole-position preparation for a gain on L following L. Stdlib, no install.

Run: python -B check_one_gain_preparation.py NEW_OUTPUT_DIRECTORY
"""
import argparse
import json
from collections import Counter
from itertools import combinations_with_replacement, product
from math import gcd
from pathlib import Path

from check_compact_residue_preparation import S, V, schedule


def require(ok, message):
    if not ok:
        raise ValueError(message)


def program_for(q, right, left, matched):
    """Keep the source exponent across BOTH rail groups. Every deposit gains two."""
    require(q >= 1 and all(0 <= j < q for j in (*right, *left)), "gain outside group")
    actions, words, receipts = [], [], []
    exponent = advances = 0

    def macro(side, word):
        actions.append(("macro", side, len(words), 0))
        words.append([word])

    for side, group in (("R", right), ("L", left)):
        start = exponent
        for residue in sorted(group, key=lambda j: (j - 2 - start) % q):
            steps = (residue - 2 - exponent) % q
            for _ in range(steps):
                macro(side, V)
            exponent = (exponent + steps) % q
            advances += steps
            receipts.append([side, residue, steps, exponent])
            actions.append(("deposit", side, -1, 0))
        if side == "R":
            actions.append(("transfer", side, -1, 0))
    require(advances <= 2 * (q - 1), "cyclic sweep bound")
    total_macros = 2 * (q - 1) if matched else advances
    for _ in range(total_macros - advances):
        macro("L", S)
    return actions, words, receipts, total_macros


def prepare(q, right, left, target, size=None, matched=False, allow_alias_test=False):
    if size is not None:
        require(size > 0 and (size // gcd(size, 2) >= 6 or allow_alias_test),
                "ring below proved width")
    actions, words, receipts, macros = program_for(q, right, left, matched)
    items = len(right) + len(left)
    core_time = 3 * items + 5 * macros + 6
    displacement = 3 * items + macros - 2
    prefix, padding = "", 0
    if size is None:
        shift = target - displacement
        prefix = "R" * shift if shift >= 0 else "L" * (1 - shift) + "R"
        # Prefix returns to rail R. LLRR is a zero-displacement R-to-R gain-one loop.
        initial_gain = max(0, -shift)
        prefix += "LLRR" * (-initial_gain % q)
    else:
        padding = (target - displacement) % size
    actions.extend((("hold", "L", -1, padding), ("finish", "L", -1, 0)))
    rows = schedule(actions, words)
    require(len(rows) == core_time + padding, "core clock")
    sites, location = [], 0
    for step in prefix:
        location += 1 if step == "R" else -1
        sites.append({location})
    for tick, row in enumerate(rows, 1):
        physical = {location + tick - 2 * d for d in row}
        sites.append(physical if size is None else {x % size for x in physical})
    require(max(map(len, sites)) <= 4, "mask width")
    return sites, dict(macros=macros, core_ticks=core_time, prefix=prefix,
                       padding=padding, deposits=receipts, ticks=len(sites))


def census(q, sites, size):
    """Evolve ordinary path multiplicity in physical coordinates, one native arc at a time."""
    state = Counter({(0, "R", 0): 1})
    for allowed in sites:
        following = Counter()
        for (x, incoming, exponent), amount in state.items():
            for outgoing, step in (("R", 1), ("L", -1)):
                y = x + step
                if size is not None:
                    y %= size
                if y in allowed:
                    gain = (exponent + (incoming == outgoing == "L")) % q
                    following[y, outgoing, gain] += amount
        state = following
    return state


def bins(state):
    return [[x, rail, j, n] for (x, rail, j), n in sorted(state.items())]


def trial(q, right, left, target, size, matched):
    sites, receipt = prepare(q, right, left, target, size, matched)
    actual = census(q, sites, size)
    expected = Counter((target, side, gain)
                       for side, group in (("R", right), ("L", left)) for gain in group)
    require(actual == expected, (q, size, target, right, left, matched, actual))
    return receipt, actual


def geometry():
    """For each wire and occupied boundary rail, enumerate every complete masked micro-word."""
    panels = []
    for name, actions, selected, expected in (
        ("advance", [("macro", "L", 0, 0)], [[V]], [[V], [S], [S]]),
        ("idle", [("macro", "L", 0, 0)], [[S]], [[S], [S], [S]]),
        ("deposit", [("deposit", "L", -1, 0)], [], [["LLR", "RRR"], ["RRR"], ["RRR"]]),
        ("transfer", [("transfer", "R", -1, 0)], [], [["RRR"], ["LLR"]]),
        ("coast", [("hold", "L", -1, 1)], [], [["R"], ["R"], ["R"]]),
        ("finish", [("finish", "L", -1, 0)], [], [[], ["RLL"], ["RRR"]]),
    ):
        rows = schedule(actions, selected)
        for period in (None, 6, 7, 8):
            actual = []
            for wire in range(len(expected)):
                accepted = []
                for letters in product("LR", repeat=len(rows)):
                    d = 2 * wire
                    for step, row in zip(letters, rows):
                        d += step == "L"
                        if not any(d == z if period is None else (d - z) % period == 0 for z in row):
                            break
                    else:
                        accepted.append("".join(letters))
                actual.append(accepted)
            require(actual == expected, (period, name, actual))
        panels.append(dict(stage=name, accepted_words_from_wires=expected))
    return panels


def controls():
    # One changed physical well in an otherwise exact named-port preparation.
    sites, _ = prepare(3, [0], [1], 0, 12)
    clean = census(3, sites, 12)
    mutation = None
    for k, layer in enumerate(sites):
        for y in sorted({(k + 1 - 2 * j) % 12 for j in range(6)} - layer):
            altered = sites[:k] + [layer | {y}] + sites[k + 1:]
            broken = census(3, altered, 12)
            if broken != clean:
                mutation = dict(tick=k + 1, extra_site=y, clean=bins(clean), actual=bins(broken))
                break
        if mutation:
            break
    require(mutation is not None, "extra-site control failed to break the preparation")

    # The hit on period five is a failure of the wiring, not a no-go for all masks.
    failed = []
    for size in (3, 5, 6, 8, 10):
        sites, _ = prepare(3, [0], [1], 0, size, allow_alias_test=True)
        actual = census(3, sites, size)
        expected = Counter({(0, "R", 0): 1, (0, "L", 1): 1})
        failed.append(dict(ring=size, expected=bins(expected), actual=bins(actual),
                           matches=actual == expected))
    return dict(extra_well=mutation, subthreshold_rings=failed)


def checks():
    small = []
    for q in (1, 2, 3, 4):
        choices = [values for k in range(3)
                   for values in combinations_with_replacement(range(q), k)]
        counts = Counter()
        maximum = 0
        for size, targets in ((None, (-7, 0, 5)), (12, range(12)), (7, range(7))):
            for target, right, left, matched in product(targets, choices, choices, (False, True)):
                receipt, _ = trial(q, right, left, target, size, matched)
                counts["line" if size is None else str(size)] += 1
                maximum = max(maximum, receipt["ticks"])
        small.append(dict(q=q, cases=dict(counts), max_ticks=maximum))
    larger = []
    for q in (5, 8, 17, 32, 97):
        for size, target in ((None, -37), (None, 41), (12, 11), (7, 6), (15, 14), (22, 0)):
            right, left = [q - 1, 0, 0, 1], [2, q // 2, 1, q - 1, 0]
            receipt, _ = trial(q, right, left, target, size, True)
            larger.append(dict(q=q, ring=size, target=target, ticks=receipt["ticks"]))
    receipt, actual = trial(7, [1, 1, 5], [0, 3, 6], -13, None, False)
    return dict(primitive_words=geometry(), exhaustive=small, larger=larger,
                line_example=dict(q=7, receipt=receipt, actual=bins(actual)), controls=controls())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = checks()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "one_gain_preparation.json").open("x", encoding="utf8", newline="\n") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
