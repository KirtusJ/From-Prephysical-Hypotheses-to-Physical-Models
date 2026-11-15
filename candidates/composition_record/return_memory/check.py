"""Test whether tick one predicts tick three after a recorded one at tick two."""

import argparse
import csv
from decimal import Decimal, ROUND_CEILING, localcontext
from math import comb
from pathlib import Path


SETTINGS = 99
TRIPLES = [format(i, "03b") for i in range(8)]  # Chronological, earliest on left.


def fisher_masses(first_no, first_yes, second_no, second_yes):
    """Return the Fisher two-sided tail and its denominator as exact integers."""
    first_size = first_yes + first_no
    total_yes = first_yes + second_yes
    total_no = first_no + second_no
    lo = max(0, first_size - total_no)
    hi = min(total_yes, first_size)
    observed = comb(total_yes, first_yes) * comb(total_no, first_size - first_yes)
    weight = comb(total_yes, lo) * comb(total_no, first_size - lo)
    tail = total = 0
    for yes in range(lo, hi + 1):
        total += weight
        if weight <= observed:
            tail += weight
        if yes < hi:
            numerator = weight * (total_yes - yes) * (first_size - yes)
            denominator = (yes + 1) * (total_no - first_size + yes + 1)
            weight, remainder = divmod(numerator, denominator)
            if remainder:
                raise ArithmeticError("nonintegral table weight")
    if total != comb(total_yes + total_no, first_size):
        raise ArithmeticError("incomplete fixed-margin support")
    return tail, total


def rounded_upper(numerator, denominator):
    with localcontext() as ctx:
        ctx.prec = 7
        ctx.rounding = ROUND_CEILING
        return format(Decimal(numerator) / Decimal(denominator), "E")


def output_row(fields, counts):
    if sum(counts) != 40_000:
        raise ValueError("unexpected shot total")
    # Chronological cells 010/011 and 110/111 differ only in the last bit.
    tail, total = fisher_masses(counts[2], counts[3], counts[6], counts[7])
    return [*fields, *counts, rounded_upper(tail, total),
            rounded_upper(min(SETTINGS * tail, total), total)]


def audit(source):
    rows = []
    current = None
    with source.open(encoding="ascii") as data:
        for line in data:
            fields = line.rstrip("\r\n").split("\t")
            if fields[0] == "job":
                if len(fields) != 4:
                    raise ValueError("invalid job header")
                if current is not None:
                    rows.append(output_row(current, counts))
                current = fields[1:]
                counts = [0] * 8
            else:
                word, multiplicity = fields
                if current is None or len(word) != 20 or set(word) - {"0", "1"}:
                    raise ValueError("expected one 20-bit word in a job")
                frequency = int(multiplicity)
                if frequency <= 0:
                    raise ValueError("nonpositive word frequency")
                triple = word[-3:][::-1]
                counts[int(triple, 2)] += frequency
    if current is not None:
        rows.append(output_row(current, counts))
    if len(rows) != SETTINGS or len({row[0] for row in rows}) != SETTINGS:
        raise ValueError("expected 99 distinct jobs")
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("word_counts", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = audit(args.word_counts)
    with args.output.open("x", newline="", encoding="ascii") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["job_id", "J_radians", "QASM_angle",
                         *(f"n_{s}" for s in TRIPLES),
                         "fisher_p_upper", "bonferroni_99_upper"])
        writer.writerows(rows)
