"""Finite tests for the coefficient-sign implication in candidate Z1, target D2.

Predicates fixed before the first run, using the complete graph on F5 with
edge i -> j of gain (1,i*j) in F5 x F5 and launch 0.
1. Check degree, simple arcs, lift connectivity and the fixed-length subgroup.
2. Check the column inner products of the weighted step for every character.
3. Realize three prescribed multisets at one endpoint and one length.
4. A negative count coefficient and each negative inverse-class coefficient
   must give a negative exact weight on its prescribed event despite unit
   singleton weight. A nonnegative half-count/half-square control must pass.
The inverse classes here are 1 and 2 modulo 5. Their first coordinate is
invisible in squared amplitudes at fixed length. All arithmetic is integral
in Z[zeta_5]. Run with one unused JSON output path.
"""
import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


P = 5
CLASSES = (1, 2)
WITNESSES = (
    ("negative_count", (-1, 1, 1), (1, 1, 1, 1, 1)),
    ("negative_class_1", (1, -1, 1), (2, 2, 0, 0, 2)),
    ("negative_class_2", (1, 1, -1), (2, 0, 2, 2, 0)),
)


def check(condition, message):
    if not condition:
        raise ValueError(message)


def step(state, target):
    vertex, clock, phase = state
    return target, (clock + 1) % P, (phase + vertex * target) % P


def reachable(start, reverse=False):
    seen = {start}
    frontier = [start]
    while frontier:
        vertex, clock, phase = frontier.pop()
        for other in range(P):
            if reverse:
                neighbor = (other, (clock - 1) % P, (phase - other * vertex) % P)
            else:
                neighbor = step((vertex, clock, phase), other)
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return seen


def carrier():
    start = (0, 0, 0)
    vertices = {(v, c, g) for v in range(P) for c in range(P) for g in range(P)}
    check(reachable(start) == reachable(start, reverse=True) == vertices, "lift is disconnected")
    check(all(len({step((v, 0, 0), j)[0] for j in range(P)}) == P for v in range(P)),
          "wrong degree or parallel arcs")
    qualifying = []
    for a in range(P):
        for b in range(P):
            orthogonal = True
            for u in range(P):
                for v in range(u + 1, P):
                    exponents = Counter((b * (u - v) * j) % P for j in range(P))
                    # A polynomial of degree <=4 at zeta_5 vanishes precisely
                    # when its five coefficients are equal. Diagonal norm is 5.
                    if len({exponents[j] for j in range(P)}) != 1:
                        orthogonal = False
            if orthogonal:
                qualifying.append((a, b))
    check(qualifying == [(a, b) for a in range(P) for b in range(1, P)], "wrong characters")
    # All lifted closed walks have length divisible by 5, since clock advances.
    # Five loops at base vertex 0 close, so 5 is the lift period.
    state = start
    for _ in range(P):
        state = step(state, 0)
    check(state == start, "five-step period witness failed")
    check(step(start, 0)[0] == 0, "base loop missing")
    return dict(vertices=P, degree=P, lift_vertices=len(vertices),
                base_period=1, lift_period=P, qualifying_characters=len(qualifying))


def available_multisets(maximum):
    counts = Counter({(0, 0, 0): 1})
    for length in range(1, 20):
        after = Counter()
        for state, n in counts.items():
            for target in range(P):
                after[step(state, target)] += n
        counts = after
        counts_at_one = tuple(counts[1, length % P, b] for b in range(P))
        if min(counts_at_one) >= maximum:
            return length, counts_at_one
    raise ValueError("prescribed walks did not occur")


def weight(m, coefficients):
    a, c1, c2 = coefficients
    # Group the powers of zeta_5 and zeta_5^{-1} in conjugate pairs.
    # 2cos(2pi/5)=(-1+sqrt(5))/2; 2cos(4pi/5)=(-1-sqrt(5))/2.
    rational, radical = Fraction(a * sum(m)), Fraction(0)
    for k, coefficient in zip(CLASSES, (c1, c2)):
        exponents = Counter()
        for x, nx in enumerate(m):
            for y, ny in enumerate(m):
                exponents[(k * (x - y)) % P] += nx * ny
        check(exponents[1] == exponents[4] and exponents[2] == exponents[3], "nonreal square")
        rational += coefficient * (exponents[0] - Fraction(exponents[1] + exponents[2], 2))
        radical += coefficient * Fraction(exponents[1] - exponents[2], 2)
    return rational, radical


def sign(a, b):
    if b == 0 or a*b >= 0:
        x = a if b == 0 else b
        return (x > 0) - (x < 0)
    difference = a*a - 5*b*b
    return ((difference > 0) - (difference < 0)) * ((a > 0) - (a < 0))


def run():
    statistics = carrier()
    length, availability = available_multisets(2)
    tested = []
    for name, coeffs, multiset in WITNESSES:
        check(all(n <= bound for n, bound in zip(multiset, availability)), "unrealizable event")
        check(weight((1, 0, 0, 0, 0), coeffs) == (1, 0), "singleton calibration fails")
        parts = weight(multiset, coeffs)
        check(sign(*parts) == -1, "expected negative weight")
        positive = weight(multiset, (Fraction(1, 2), Fraction(1, 2), 0))
        check(sign(*positive) >= 0, "positive control failed")
        tested.append(dict(name=name, coefficients=coeffs, multiplicities=multiset,
                           exact_weight=[str(v) for v in parts], control_weight=[str(v) for v in positive]))
    return dict(carrier=statistics, end_vertex=1, length=length, available_walks_by_gain=availability,
                weight_format="A + B sqrt(5), stored as [A,B]", cases=tested)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    results = run()
    with args.output.open("x") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
