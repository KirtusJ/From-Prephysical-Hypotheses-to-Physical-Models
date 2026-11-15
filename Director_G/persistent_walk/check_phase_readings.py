"""Exact minor certificate for eight terminal probabilities of the five-site walk.

Run with Python 3.9 or later, using only the standard library.
"""
from itertools import combinations
from math import isqrt
import json


PRIME = 1009
OFFSETS = (0, 1, 2, 3, 7, 8, 9, 10)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def determinant_mod(rows):
    """Gaussian elimination in the prime field, including the row-swap sign."""
    matrix = [list(row) for row in rows]
    size = len(matrix)
    determinant = 1
    for column in range(size):
        pivot = next((i for i in range(column, size) if matrix[i][column] % PRIME), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant = -determinant
        diagonal = matrix[column][column] % PRIME
        determinant = determinant * diagonal % PRIME
        inverse = pow(diagonal, -1, PRIME)
        for i in range(column + 1, size):
            multiplier = matrix[i][column] * inverse % PRIME
            for j in range(column + 1, size):
                matrix[i][j] = (matrix[i][j] - multiplier * matrix[column][j]) % PRIME
            matrix[i][column] = 0
    return determinant % PRIME


def minor_statistics(offsets):
    u, v = 667, 387
    nodes = (u, pow(u, -1, PRIME), v, pow(v, -1, PRIME))
    rows = [[pow(node, k, PRIME) for node in nodes] for k in offsets]
    results = []
    for width in (4, 5):
        frame = rows if width == 4 else [[1] + row for row in rows]
        minors = [determinant_mod(indices) for indices in combinations(frame, width)]
        results.append({"width": width, "checked": len(minors),
                        "nonzero": sum(x != 0 for x in minors),
                        "minimum_residue": min(minors)})
    return results


def main():
    require(all(PRIME % n for n in range(2, isqrt(PRIME) + 1)), "modulus is composite")
    require(244**2 % PRIME == 5, "wrong image of sqrt(5)")
    for node, sign in [(667, -1), (387, 1)]:
        require((4 * (node**2 + 1) - (3 + sign * 244) * node) % PRIME == 0,
                "phase misses its defining quadratic")
    selected = minor_statistics(OFFSETS)
    require([x["nonzero"] for x in selected] == [70, 56], "minor certificate failed")
    duplicate = minor_statistics((*OFFSETS[:-1], OFFSETS[-2]))
    require(all(x["minimum_residue"] == 0 for x in duplicate), "duplicate-row control failed")
    consecutive = minor_statistics(range(8))
    print(json.dumps({"prime": PRIME, "physical_tick_offsets": [2*k for k in OFFSETS],
                      "selected_schedule": selected,
                      "eight_consecutive_even_ticks_comparison": consecutive,
                      "duplicated_offset_control": duplicate}, indent=2))


if __name__ == "__main__":
    main()
