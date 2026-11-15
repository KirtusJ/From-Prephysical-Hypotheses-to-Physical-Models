"""Replay the two-party controlled reflection with exact sheet amplitudes."""

import argparse
from collections import Counter
from fractions import Fraction
from math import isqrt


def contact(state, dr, dl, p):
    r, l, z = state
    half = (p + 1) // 2
    return (r + dr) % p, (l + dl) % p, (z + half * (r * dl - l * dr)) % p


def run(state, word, p):
    for dr, dl in word:
        state = contact(state, dr, dl, p)
    return state


def check_prime(p):
    if p < 3 or p % 2 == 0 or any(p % d == 0 for d in range(3, isqrt(p) + 1, 2)):
        raise ValueError("choose an odd prime")

    # The preparation amplitude 1/sqrt(p) is a common factor. Start with
    # nonzero ordinary coordinates to check their restoration as well.
    r, l = 1, 2
    sector_counts = Counter()
    for a in (0, 1):
        words = [[(a, 0), (0, j), (-a, 0), (0, -j)] for j in range(p)]
        inverse_words = [[(-dr, -dl) for dr, dl in reversed(w)] for w in words]
        for start in range(p):
            initial = (r, l, start)
            states = [run(initial, word, p) for word in words]
            assert states == [(r, l, (start + a*j) % p) for j in range(p)]
            counts = Counter(states)
            for b in (0, 1):
                for j, word in enumerate(inverse_words):
                    output = [0] * p
                    for z in range(p):
                        sheet = (r, l, z)
                        incident = int(states[j] == sheet)
                        # Scale by p to keep the matrix 2|s><s| - I integral.
                        amplitude = 2*counts[sheet] - p*incident if b else p*incident
                        rr, ll, zz = run(sheet, word, p)
                        assert (rr, ll) == (r, l)
                        output[zz] += amplitude
                    # Equality for EACH j certifies full work uncomputation.
                    target = [p*int(z == start) for z in range(p)]
                    if a and b:
                        target = [2 - x for x in target]
                    assert output == target, (p, a, b, start, j)
                    if start == 0 and j == 0:
                        check_spectrum(p, a, b, output, sector_counts)
    expected = {1: 3*p + 1, -1: p - 1}
    assert sector_counts == expected
    return Fraction(p - 1, p)


def check_spectrum(p, a, b, output, sector_counts):
    for k in range(p):
        coefficients = [0] * p
        for z, weight in enumerate(output):
            coefficients[k*z % p] += weight
        sign = -1 if a and b and k else 1
        coefficients[0] -= p*sign
        # At a primitive p-th root, 1 + x + ... + x^(p-1) vanishes.
        assert len(set(coefficients)) == 1
        sector_counts[sign] += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("primes", nargs="*", type=int, default=[3, 5, 7, 11])
    for prime in parser.parse_args().primes:
        capacity = check_prime(prime)
        print(f"p={prime}: all central sheets, work labels and 4 route inputs passed; concurrence {capacity}")
