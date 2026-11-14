"""Enumerate ideal response tables and test one fewer classical memory state.

Each preparation row has equal weight. The later query column is uniform and
independent of the row. The decoder sees only the classical message and the
query. A scalar read is scored by exact equality over F5.
"""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


P = 5
ZERO = (0, 0, 0)
E1, E2 = (1, 0, 0), (0, 1, 0)
VECTORS = tuple(product(range(P), repeat=3))


def is_line_representative(vector):
    """Choose one vector on each line by setting its first nonzero entry to 1."""
    return next((value for value in vector if value), 0) == 1


DIRECTIONS = tuple(vector for vector in VECTORS if is_line_representative(vector))


def scalar(covector, direction):
    return sum(u * x for u, x in zip(covector, direction)) % P


def pack(bits):
    return sum(int(bit) << index for index, bit in enumerate(bits))


def bit_distance(a, b):
    return (a ^ b).bit_count()


def scalar_distance(a, b):
    return sum(x != y for x, y in zip(a, b))


def check(observed, expected, label):
    if observed != expected:
        raise ValueError(f"{label}: expected {expected}, found {observed}")


def summarize(rows, query_count, distance, expected_distances, expected_error):
    """A collision costs at least the smallest distance, by the triangle inequality."""
    distances = Counter(distance(a, b) for a, b in combinations(rows.values(), 2))
    check(dict(distances), expected_distances, "row pair distances")
    check(len(set(rows.values())), len(rows), "distinct target response rows")

    # Merge e2 into e1. Each message decodes to the target row named by that message.
    encoder = {u: E1 if u == E2 else u for u in rows}
    retained = len(set(encoder.values()))
    check(retained, len(rows) - 1, "message count")
    disagreements = [distance(row, rows[encoder[u]]) for u, row in rows.items()]
    errors = sum(disagreements)
    check(errors, min(distances), "constructed encoder attains the collision bound")
    assignments = len(rows) * query_count
    error_rate = Fraction(errors, assignments)
    check(error_rate, expected_error, "uniform mean error")
    return {
        "target_rows": len(rows),
        "uniform_queries_per_row": query_count,
        "row_pair_distance_counts": {str(d): distances[d] for d in sorted(distances)},
        "retained_states": retained,
        "merged_input": E2,
        "decoded_as": E1,
        "miscoded_assignments": errors,
        "total_assignments": assignments,
        "sharp_mean_error": str(error_rate),
    }


def tables():
    check(len(DIRECTIONS), 31, "projective directions")
    raw_rows = {u: tuple(scalar(u, x) for x in DIRECTIONS) for u in VECTORS}
    classes = (ZERO, *DIRECTIONS)
    binary_rows = {u: pack(value != 0 for value in raw_rows[u]) for u in classes}

    planes = [set(i for i, value in enumerate(raw_rows[u]) if value == 0) for u in DIRECTIONS]
    plane_sizes = Counter(map(len, planes))
    intersections = Counter(len(a & b) for a, b in combinations(planes, 2))
    check(dict(plane_sizes), {6: 31}, "projective kernel sizes")
    check(dict(intersections), {1: 465}, "distinct plane intersections")

    # Column (a, x) adds the later shift a before testing (u + a)(x) != 0.
    continued_rows = {}
    for u in VECTORS:
        blocks = []
        for shift in VECTORS:
            shifted = tuple((x + y) % P for x, y in zip(u, shift))
            blocks.append(pack(value != 0 for value in raw_rows[shifted]))
        continued_rows[u] = sum(block << (i * len(DIRECTIONS)) for i, block in enumerate(blocks))

    return {
        "field": P,
        "fixed_direction_representative": "first nonzero coordinate equals 1",
        "directions_per_kernel_counts": dict(plane_sizes),
        "pairwise_kernel_intersection_size_counts": dict(intersections),
        "binary_one_write": summarize(
            binary_rows, len(DIRECTIONS), bit_distance, {10: 465, 25: 31}, Fraction(5, 496)
        ),
        "scalar_one_write": summarize(
            raw_rows, len(DIRECTIONS), scalar_distance, {25: 7750}, Fraction(1, 155)
        ),
        "binary_after_independent_additive_write": summarize(
            continued_rows, len(VECTORS) * len(DIRECTIONS), bit_distance,
            {1250: 7750}, Fraction(2, 775)
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    output = parser.parse_args().output
    report = json.dumps(tables(), indent=2) + "\n"
    if output:
        output.write_text(report, encoding="utf-8", newline="\n")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
