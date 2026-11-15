"""Enumerate attainable blank orbits and optimal late binary responses over F5."""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


P = 5
V = tuple(product(range(P), repeat=3))
ZERO = (0, 0, 0)
E1, E2, E3 = BASIS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
Q = tuple(x for x in V if next((v for v in x if v), 0) == 1)


def cross(a, b):
    return (
        (a[1] * b[2] - a[2] * b[1]) % P,
        (a[2] * b[0] - a[0] * b[2]) % P,
        (a[0] * b[1] - a[1] * b[0]) % P,
    )


def dot(a, b):
    return sum(x * y for x, y in zip(a, b)) % P


def multiply(left, right):
    x, u = left
    y, v = right
    return (tuple((a + b) % P for a, b in zip(x, y)),
            tuple((a + b + 3 * w) % P for a, b, w in zip(u, v, cross(x, y))))


def spaces():
    """List all subspaces as their complete point sets."""
    lines = [frozenset(tuple(t * xi % P for xi in x) for t in range(P)) for x in Q]
    planes = [frozenset(v for v in V if dot(q, v) == 0) for q in Q]
    return [frozenset([ZERO]), *lines, *planes, frozenset(V)]


def best_orbits():
    # An ordinary subspace A can project from a stabilizer with central part K
    # exactly when all pairwise commutators from A lie in K.
    subs = spaces()
    maximal_sizes = {}
    for a in subs:
        commutators = {cross(x, y) for x, y in product(a, repeat=2)}
        for k in subs:
            if commutators <= k:
                order = len(a) * len(k)
                maximal_sizes[len(k)] = max(maximal_sizes.get(len(k), 0), order)
    return [len(V) ** 2 // maximal_sizes[5**c] for c in range(4)]


def canonical(point, ordinary_axes, central_axes):
    # The stabilizer contains the indicated coordinate subspaces A, K.
    # A left stabilizer factor gives a canonical representative of H g.
    x, _ = point
    cancel = tuple(-x[i] % P if i in ordinary_axes else 0 for i in range(3))
    xr, ur = multiply((cancel, ZERO), point)
    return xr, tuple(0 if i in central_axes else ur[i] for i in range(3))


def attain(ordinary_axes, central_axes, planned_size):
    def cell(point):
        return canonical(point, ordinary_axes, central_axes)

    states = {}
    for g in product(V, repeat=2):
        representative = cell(g)
        targets = tuple(cell(multiply(g, (e, ZERO))) for e in BASIS)
        if representative in states:
            assert states[representative] == targets
        else:
            states[representative] = targets
    assert len(states) == planned_size
    for i in range(3):
        assert len({targets[i] for targets in states.values()}) == len(states)

    # Identify the best decoder for *each* pair of stored state and late q.
    targets = defaultdict(Counter)
    for u, q in product(V, Q):
        targets[cell((ZERO, u)), q][bool(dot(u, q))] += 1
    mistakes_by_q = Counter()
    for (_, q), counts in targets.items():
        mistakes_by_q[q] += min(counts[False], counts[True])
    errors = sum(mistakes_by_q.values())
    total = len(V) * len(Q)
    return {
        "ordinary_stabilizer_axes": [i + 1 for i in ordinary_axes],
        "central_stabilizer_axes": [i + 1 for i in central_axes],
        "blank_orbit_size": planned_size,
        "perfectly_readable_probe_directions": sum(n == 0 for n in mistakes_by_q.values()),
        "misses": errors, "assignments": total, "mean_error": str(Fraction(errors, total)),
    }


def report():
    sizes = best_orbits()
    assert sizes == [3125, 125, 25, 1]
    stabilizers = [((0,), ()), ((0, 1), (2,)), ((0, 1), (1, 2)), ((0, 1, 2), (0, 1, 2))]
    outcomes = [attain(a, k, n) for (a, k), n in zip(stabilizers, sizes)]
    assert [row["mean_error"] for row in outcomes] == ["0", "5/31", "6/31", "1/5"]
    # The perfect central reader's 3125-state quotient identifies these
    # physical prefixes. Their raw centers evaluated at e3 disagree.
    a, b = (E1, ZERO), (E2, ZERO)
    ab = multiply(a, b)
    assert canonical(ab, (0,), ()) == canonical(b, (0,), ())
    assert dot(ab[1], E3) == 3 and dot(b[1], E3) == 0
    return {"field": P, "projective_directions": len(Q), "subspaces_per_factor": len(spaces()),
            "optimal_orbits": outcomes, "unclosed_prefix_raw_readings": [0, 3]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    output = parser.parse_args().output
    text = json.dumps(report(), indent=2) + "\n"
    if output:
        output.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
