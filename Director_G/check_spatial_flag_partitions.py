"""Exact replay of walk records and within-site partitions. Standard library only."""

import argparse
import json
from fractions import Fraction
from itertools import accumulate, product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def replay(ticks, time, well, ring=None):
    sites = (
        list(range(ticks % 2, ring, 2)) if ring else list(range(-ticks, ticks + 1, 2))
    )
    rows = {}
    for word in product((0, 1), repeat=ticks):
        x, left_before, sign, tag = 0, 0, 1, 0
        for t, left in enumerate(word):
            if t == time and x == well:
                tag ^= 1
            if left_before and left:
                sign = -sign
            x += 1 - 2 * left
            if ring:
                x %= ring
            left_before = left
        key = x, tag, left_before
        rows[key] = rows.get(key, 0) + sign
    weights = [
        [sum(rows.get((x, b, l), 0) ** 2 for l in (0, 1)) for b in (0, 1)]
        for x in sites
    ]
    require(sum(map(sum, weights)) == 2**ticks, "conservation")
    return sites, weights


def cut_cells(rows, cuts):
    output = []
    choices = iter(cuts)
    for a, b in rows:
        if a and b and next(choices):
            output.extend([a, b])
        else:
            output.append(a + b)
    return output


def majors(first, second):
    n = max(len(first), len(second))

    def cumul(v):
        return list(accumulate(sorted(v + [0] * (n - len(v)), reverse=True)))

    a, b = cumul(first), cumul(second)
    return a != b and a[-1] == b[-1] and all(x >= y for x, y in zip(a, b))


def panel(ticks, time, well, ring=None):
    sites, bare_rows = replay(ticks, None, None, ring)
    _, tagged = replay(ticks, time, well, ring)
    bare = [a for a, b in bare_rows]
    variants = []
    for cuts in product((0, 1), repeat=sum(bool(a and b) for a, b in tagged)):
        cells = cut_cells(tagged, cuts)
        nb = sum(bool(x) for x in bare)
        nt = sum(bool(x) for x in cells)
        quadratic = Fraction(1, sum(w * w for w in cells)) - Fraction(
            1, sum(w * w for w in bare)
        )
        if ticks in (7, 9):
            require(majors(bare, cells), "majorization")
        if ticks == 7:
            require(
                max(bare) == 41 and max(cells) == 37 and cells.count(37) == 1,
                "remote maximum",
            )
            require(majors(bare, [a + b for a, b in tagged]), "coarse majorization")
        if ticks == 9:
            require(nb == 3 and 4 <= nt <= 7, "support change")
            require(
                Fraction(1, nb) - Fraction(1, nt) >= Fraction(1, 12), "order-zero gap"
            )
        variants.append(
            dict(
                split=cuts,
                cells=cells,
                support=nt,
                bare_majorizes=majors(bare, cells),
                remote_unit_quadratic_tag_minus_bare=str(quadratic),
            )
        )
    if ticks == 5:
        require(
            all(
                Fraction(v["remote_unit_quadratic_tag_minus_bare"]) < 0
                for v in variants[:1]
            )
            and Fraction(variants[-1]["remote_unit_quadratic_tag_minus_bare"]) > 0,
            "reversed ordering",
        )
    if ticks == 5:
        coarse = Fraction(variants[0]["remote_unit_quadratic_tag_minus_bare"])
        fine = Fraction(variants[-1]["remote_unit_quadratic_tag_minus_bare"])
        require(
            Fraction(89, 261) * coarse + Fraction(172, 261) * fine == 0,
            "hidden partition false pass",
        )
    return dict(sites=sites, bare=bare, flagged=tagged, variants=variants)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("output", type=Path)
    outfile = ap.parse_args().output
    data = {
        "five": panel(5, 2, -2),
        "seven": panel(7, 5, 1),
        "nine_on_ring": panel(9, 7, 1, 8),
    }
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open("x", encoding="utf8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
