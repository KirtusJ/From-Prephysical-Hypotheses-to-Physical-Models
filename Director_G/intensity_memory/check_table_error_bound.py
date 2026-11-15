"""Compute a sufficient uniform error limit for the particular 55-reader table.

Run in the same directory as check_continuation_span.py. Table probabilities
are per original launch, with masks and a terminal R/L port. No observations
are used as inputs. Pure Python rational elimination, not a sampling bound.
"""
from fractions import Fraction
import json

from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location


spec = spec_from_file_location("continuation", Path(__file__).with_name("check_continuation_span.py"))
continuation = module_from_spec(spec)
spec.loader.exec_module(continuation)


def inverse(matrix):
    n = len(matrix)
    reduced = [row[:] + [Fraction(i == j) for j in range(n)]
               for i, row in enumerate(matrix)]
    for k in range(n):
        pivot = next((i for i in range(k, n) if reduced[i][k]), None)
        if pivot is None:
            raise ValueError("Singular probability table")
        reduced[pivot], reduced[k] = reduced[k], reduced[pivot]
        diagonal = reduced[k][k]
        reduced[k] = [x / diagonal for x in reduced[k]]
        for i, row in enumerate(reduced):
            if i == k or not row[k]:
                continue
            factor = row[k]
            reduced[i] = [a - factor * b for a, b in zip(row, reduced[k])]
    return [row[n:] for row in reduced]


def main():
    _, readers = continuation.port_effect_ranks()
    prep_record = continuation.certify_joint_rank(readers)
    T = prep_record["common_preparation_clock"]
    start = (1,) + (0,) * (continuation.DIM-1)
    P = []
    for prefix in prep_record["preparation_masks"]:
        field = continuation.forward(start, prefix)
        P.append([Fraction(continuation.forward(field, suffix)[port]**2, 2**(T+len(suffix)))
                  for suffix, port in readers])
    Q = inverse(P)
    norm = max(sum(abs(entry) for entry in row) for row in Q)
    if norm != 1280:
        raise ValueError(("Inverse norm changed", norm))
    print(json.dumps({"size": len(P), "matrix_inverse_infinity_norm": str(norm),
                      "sufficient_uniform_error_strictly_below": str(1/(len(P)*norm))}))


if __name__ == "__main__":
    main()
