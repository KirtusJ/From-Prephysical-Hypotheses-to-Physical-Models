"""Replay explicit masks and evaluate their probability determinant modulo 101.

Input on stdin is the JSON emitted by check_continuation_span.py. This
verifier uses explicit direction words and knows nothing about how the
preparations or readouts were chosen. Requires only the standard library.
"""
import json
import sys
from itertools import product

SITES = 5
PRIME = 101


def unrestricted_paths(length):
    entries = []
    for steps in product((1, -1), repeat=length):
        site, last, sign = 0, 1, 1
        sites = []
        for direction in steps:
            site = (site + direction) % SITES
            sites.append(site)
            if direction == last == -1:
                sign = -sign
            last = direction
        entries.append((sites, (site, int(last == -1)), sign))
    return entries


def determinant(rows):
    value = 1
    rows = [[v % PRIME for v in row] for row in rows]
    for i in range(len(rows)):
        k = next((j for j in range(i, len(rows)) if rows[j][i]), None)
        if k is None:
            return 0
        if k != i:
            rows[k], rows[i] = rows[i], rows[k]
            value = -value
        pivot = rows[i][i]
        value = value * pivot % PRIME
        inv = pow(pivot, -1, PRIME)
        for j in range(i + 1, len(rows)):
            multiple = rows[j][i] * inv % PRIME
            if multiple:
                rows[j] = [(a - multiple * b) % PRIME
                           for a, b in zip(rows[j], rows[i])]
    return value % PRIME


def main():
    receipt = json.load(sys.stdin)
    prefixes = receipt["joint_probability_rank"]["preparation_masks"]
    readers = receipt["reader_certificate"]
    if len(prefixes) != 55 or len(readers) != 55:
        raise ValueError("Expected 55 preparations and 55 readers")
    if any(len(prefix) != 5 for prefix in prefixes):
        raise ValueError("Preparations must have five masks")
    paths = {n: unrestricted_paths(n) for n in range(5, 11)}
    keep = []
    for reader in readers:
        tail = reader["masks"]
        port = tuple(reader["port"])
        denominator = 2 ** (5 + len(tail))
        eligible = [(sites[:5], sign) for sites, target, sign in paths[5 + len(tail)]
                    if target == port and all(x in m for x, m in zip(sites[5:], tail))]
        keep.append((eligible, pow(denominator, -1, PRIME)))
    table = []
    for prefix in prefixes:
        row = []
        for eligible, denominator_inverse in keep:
            amplitude = sum(sign for visits, sign in eligible
                            if all(x in m for x, m in zip(visits, prefix)))
            row.append(amplitude * amplitude * denominator_inverse % PRIME)
        table.append(row)
    value = determinant(table)
    if not value:
        raise ValueError("Singular physical probability table")
    print(json.dumps({"rows": len(table), "columns": len(table[0]), "prime": PRIME,
                      "normalized_probability_determinant_mod_prime": value}))


if __name__ == "__main__":
    main()
