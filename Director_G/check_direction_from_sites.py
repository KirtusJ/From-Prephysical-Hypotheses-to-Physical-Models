"""Compare a two-position-toggle direction record with a direct rail record."""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path


def require(value, problem):
    if not value:
        raise ValueError(problem)


def f(site):
    return site // 2 % 2


def written_tick(field, order, record, use_rail=False, premature=False):
    result = Counter()
    for (x, src, y, bit, tags), amplitude in field.items():
        pre = bit ^ f(x + 1) if record and not use_rail else bit
        kept_tags = tags + (pre,) if premature else tags
        for direction in (0, 1):
            dst = (x + (1 if direction == 0 else -1)) % (4 * order)
            sheet = (y + x // 2) % order
            out = pre
            if record:
                out ^= direction if use_rail else f(dst)
            sign = -1 if src == direction == 1 else 1
            result[dst, direction, sheet, out, kept_tags] += sign * amplitude
    return Counter({port: n for port, n in result.items() if n})


def compare_linear_map(order):
    # Every basis column is tested, including both incoming rails and
    # both initial bit values. Equality extends by linearity.
    words = 0
    for x, src, y, bit in product(range(4 * order), range(2), range(order), range(2)):
        initial = {(x, src, y, bit, ()): 1}
        actual = written_tick(initial, order, True)
        expect = written_tick(initial, order, True, use_rail=True)
        require(actual == expect, "two toggles changed a signed basis column")
        words += 1
    return dict(order=order, columns=words)


def control_count(size):
    solutions = 0
    for post in product((0, 1), repeat=size):
        # The right-moving edge fixes every pre bit once post is chosen.
        if all(post[(x+1) % size] != post[(x-1) % size] for x in range(size)):
            solutions += 1
    require(solutions == (4 if size % 4 == 0 else 0), "period-four obstruction")
    return [size, solutions]


def outgoing_witness(order, premature, fold_sheet):
    field = {(0, 0, 0, 0, ()): 1}
    for tick in range(1, 5):
        field = written_tick(field, order, tick == 2, premature=premature and tick == 2)
        if tick == 2:
            field = {k: n for k, n in field.items() if k[3] == 1}
    # At folded zero, evaluating a polynomial at 1 adds its coefficients.
    # On a localized physical sheet, distinct final addresses are orthogonal.
    groups = Counter()
    for (x, rail, y, bit, tags), value in field.items():
        if (x, rail, bit) == (0, 0, 1):
            groups[(tags, 0 if fold_sheet else y)] += value
    return Fraction(sum(n*n for n in groups.values()), 16)


def run():
    controls = []
    for order in (3, 4, 5, 7, 12):
        values = [outgoing_witness(order, premature, fold)
                  for fold in (True, False) for premature in (False, True)]
        require(values[:2] == [Fraction(1, 4), Fraction(1, 8)], "unwanted pointer read")
        controls.append(dict(order=order, zero_character=[str(v) for v in values[:2]],
                             localized_sheet=[str(v) for v in values[2:]]))
    return dict(basis_columns=[compare_linear_map(m) for m in (3, 4, 5, 9, 16)],
                toggle_pairs_by_circumference=[control_count(n) for n in range(3, 17)],
                control_order=["end read only", "also read before stream"],
                four_tick_witness=controls)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("directory", type=Path)
    dest = cli.parse_args().directory
    dest.mkdir(parents=True, exist_ok=True)
    with (dest / "direction_from_sites.json").open("x", encoding="utf8", newline="\n") as handle:
        json.dump(run(), handle, indent=2, allow_nan=False)
        handle.write("\n")
