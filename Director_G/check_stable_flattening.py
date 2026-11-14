"""Construct and replay finite signed-Walsh words in one protected record bin."""
from argparse import ArgumentParser
from fractions import Fraction
from functools import reduce
from itertools import product
import json
from math import gcd
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def odd_content(row):
    value = reduce(gcd, row, 0)
    return value // (value & -value) if value else 0


def apply(row, gate):
    kind, slots = gate
    if kind == "minus":
        row[slots[0]] *= -1
    elif kind == "swap":
        i, j = slots
        row[i], row[j] = row[j], row[i]
    elif kind == "walsh":
        a, b, c, d = (row[i] for i in slots)
        sums = (a+b+c+d, a-b+c-d, a+b-c-d, a-b-c+d)
        require(all(v % 2 == 0 for v in sums), "nonintegral Walsh step")
        for i, value in zip(slots, sums):
            row[i] = value // 2
    else:
        raise ValueError(kind)


def reduction(source):
    """Retain exact slot indices. Each gate is its own inverse."""
    row = list(source)
    content = odd_content(row)
    norm = sum(a*a for a in row)
    size = len(row)
    word = []

    def emit(kind, slots):
        gate = (kind, slots)
        apply(row, gate)
        word.append(gate)

    for i, a in enumerate(row):
        if a < 0:
            emit("minus", [i])
    while True:
        occupied = [i for i, a in enumerate(row) if a]
        even = next((i for i in occupied if row[i] % 2 == 0), None)
        if even is not None:
            selected = [even]
        elif occupied and min(row[i] for i in occupied) < max(row[i] for i in occupied):
            selected = [max(occupied, key=row.__getitem__), min(occupied, key=row.__getitem__)]
        else:
            break
        empty = [i for i, a in enumerate(row) if a == 0]
        needed = 4 - len(selected)
        if len(empty) < needed:
            shortage = needed - len(empty)
            empty.extend(range(len(row), len(row) + shortage))
            row.extend([0]*shortage)
        slots = selected + empty[:needed]
        before = sum(row[i]**4 for i in slots)
        old_norm = sum(row[i]**2 for i in slots)
        emit("walsh", slots)
        require(sum(row[i]**4 for i in slots) < before, "strict descent")
        require(sum(row[i]**2 for i in slots) == old_norm, "norm preservation")
    for i in range(sum(a != 0 for a in row)):
        if not row[i]:
            j = next(j for j in range(i+1, len(row)) if row[j])
            emit("swap", [i, j])
    count = norm // (content*content) if content else 0
    require(row == [content]*count + [0]*(len(row)-count), "terminal content and count")
    require(len(row) <= max(size, count), "padded slot bound")
    replayed = list(row)
    for gate in reversed(word):
        apply(replayed, gate)
    require(replayed == list(source) + [0]*(len(row)-size), "reverse replay")
    return dict(source=list(source), squared_norm=norm, odd_content=content,
                cells=count, padded_width=len(row), word=word)


def four_tick_walk():
    rows = {}
    for word in product((0, 1), repeat=4):
        site = 4 - 2*sum(word)
        pairs = zip((0,)+word, word)
        amplitude = (-1)**sum(a*b for a, b in pairs)
        cell = (site, word[-1])
        rows[cell] = rows.get(cell, 0) + amplitude
    require(rows[2, 0] == 3 and rows[2, 1] == 1, "four-tick source and site conventions")
    site = [value for (x, r), value in sorted(rows.items()) if x == 2]
    rest = [value for (x, r), value in sorted(rows.items()) if x != 2]
    return dict(ordered_ports=[[*p, v] for p, v in sorted(rows.items())],
                site_two=reduction(site), other_sites=reduction(rest),
                sole_right_rail=reduction([rows[2, 0]]), denominator=16)


def transport_pair(x, y):
    """Explicitly concatenate the two words on one padded register."""
    a, b = reduction(x), reduction(y)
    width = max(a["padded_width"], b["padded_width"])
    transported = list(x) + [0]*(width-len(x))
    possible = (a["squared_norm"], a["odd_content"]) == (b["squared_norm"], b["odd_content"])
    if possible:
        for gate in a["word"] + list(reversed(b["word"])):
            apply(transported, gate)
        require(transported == list(y) + [0]*(width-len(y)), "two-word conversion")
    return dict(left=a, right=b, conversion=possible)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    counts = [0]*5
    for length in range(1, 5):
        for row in product(range(-3, 4), repeat=length):
            reduction(row)
            counts[length] += 1
    pairs = [transport_pair([3, 5], [1]*34), transport_pair([9, 15], [3]*34),
             transport_pair([6, 10], [1]*136), transport_pair([3], [1]*9),
             transport_pair([0, 0], [0]), transport_pair([-2], [1, 1, 1])]
    # A common denominator converts a genuinely dyadic pair to the integers.
    den = 8
    dx = [Fraction(3, den), Fraction(5, den)]
    dy = [Fraction(1, den)]*34
    scaled = [[int(a*den) for a in row] for row in (dx, dy)]
    require(transport_pair(*scaled)["conversion"], "common denominator")
    result = dict(signed_box_by_length=counts[1:], examples=pairs,
                  dyadic_example_common_denominator=den, walk=four_tick_walk())
    with args.output.open("x", encoding="utf8", newline="\n") as out:
        json.dump(result, out, separators=(",", ":"))
        out.write("\n")


if __name__ == "__main__":
    main()
