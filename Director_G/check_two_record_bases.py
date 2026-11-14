"""Read the same three-tick eight-well records in two flag bases. Standard library."""

import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


SITES = (1, 3, 5, 7)


def propagate():
    state = {(0, 0, 0): 1}
    for tick in range(1, 4):
        nxt = defaultdict(int)
        for (site, rail, flag), v in state.items():
            for left in (0, 1):
                target = (site + 1 - 2 * left) % 8
                bit = flag ^ int(tick == 1 and target == 1)
                nxt[target, left, bit] += -v if rail and left else v
        state = nxt
    return state


def word_rows(erased):
    s = defaultdict(int)
    for word in product((0, 1), repeat=3):
        site = (3 - 2 * sum(word)) % 8
        flag = int(word[0] == 0)
        sign = (-1) ** sum(a * b for a, b in zip(word, word[1:]))
        for y in (0, 1):
            if erased:
                s[site, word[-1], y] += -sign if y and flag else sign
            elif y == flag:
                s[site, word[-1], y] += sign
    return s


def powered(row, q):
    numerators = [w**q if w else 0 for w in row]
    return [Fraction(w, sum(numerators)) for w in numerators]


def run():
    base = propagate()
    arc = word_rows(False)
    keys = tuple(product(SITES, (0, 1), (0, 1)))
    require(all(arc[k] == base[k] for k in keys), "position/rail/flag transfer")
    panels = {}
    for erased, name in ((False, "recorded"), (True, "hadamard")):
        alternate = word_rows(erased)
        if erased:
            candidate = {
                (x, r, f): base[x, r, 0] + (-1 if f else 1) * base[x, r, 1]
                for x, r, f in keys
            }
            require(
                all(alternate[k] == candidate[k] for k in keys),
                "analyzer word amplitudes",
            )
        amp = [[[alternate[x, r, f] for r in (0, 1)] for x in SITES] for f in (0, 1)]
        rows = [[sum(v * v for v in pair) for pair in row] for row in amp]
        den = 16 if erased else 8
        require(
            sum(map(sum, rows)) == den and all(sum(row) * 2 == den for row in rows),
            "branch norms",
        )
        pooled = [Fraction(a + b, den) for a, b in zip(*rows)]
        require(
            pooled == list(map(Fraction, ("3/8", "1/8", "1/8", "3/8"))),
            "unchanged site totals",
        )
        controls = {}
        for q in (0, 1, 2, 3, 6):
            chosen = [sum(powered(row, q)[1:3]) for row in rows]
            want = Fraction(2, 3 + 5**q) if erased else Fraction(1, 2 + 2**q)
            require(chosen == [want, want], "event independent of flag weighting")
            divided = [powered(row, q) for row in rows]
            combined = powered([v for row in rows for v in row], q)
            require(
                combined == [v / 2 for row in divided for v in row],
                "global and row-normalized",
            )
            for w in map(Fraction, ("0", "1/9", "1/2", "8/9", "1")):
                require(
                    w * chosen[0] + (1 - w) * chosen[1] == want,
                    "unequal branch-weight control",
                )
            controls[str(q)] = str(want)
        panels[name] = dict(
            rail_columns=amp,
            site_cells=rows,
            kinematic_denominator=den,
            middle_bin_by_power=controls,
        )
    return panels


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("output", type=Path)
    dest = ap.parse_args().output
    data = dict(odd_sites=SITES, bases=run())
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("x", encoding="utf8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
