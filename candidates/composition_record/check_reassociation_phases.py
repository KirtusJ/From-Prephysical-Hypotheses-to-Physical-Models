"""Replay the reassociation phase cycles, their kernel and real-fringe recovery."""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from math import cos, pi, sin
from pathlib import Path
from random import Random

from check_contacts import BASIS, SEEDS, ZERO, add, fifth_power, rank


def multiple(x, n):
    return tuple((n*a) % 5 for a in x)


def cycles():
    alternating = []
    for order in permutations(range(3)):
        inv = sum(i > j for i, j in combinations(order, 2))
        alternating.append(((-1)**inv, *(BASIS[i] for i in order)))
    points = (*BASIS, *(add(x, y) for x, y in combinations(BASIS, 2)))
    return [alternating] + [[(1, x, multiple(x, j), x) for j in range(5)]
                            for x in points]


def cycle_value(word, phase, modulus):
    return sum(sign*phase(a, b, c) for sign, a, b, c in word) % modulus


def boundary_pairs(word):
    # Integer coefficients exhaust arbitrary phase-valued pair gauges.
    result = Counter()
    for sign, a, b, c in word:
        for pair, direction in (((b, c), 1), ((add(a, b), c), -1),
                                ((a, add(b, c)), 1), ((a, b), -1)):
            result[pair] += sign*direction
    return {k: v for k, v in result.items() if v}


def primitive(a, b):
    ai, aj = a
    bi, bj = b
    return -ai*bj + 5*((ai+bi)//5)*((aj+bj) % 5)


def skew_check():
    residues = tuple(product(range(5), repeat=2))
    counts = Counter()
    for a, b, c in product(residues, repeat=3):
        ab = tuple((x+y) % 5 for x, y in zip(a, b))
        bc = tuple((x+y) % 5 for x, y in zip(b, c))
        lhs = primitive(b, c)-primitive(ab, c)+primitive(a, bc)-primitive(a, b)
        skew = a[0]*((b[1]+c[1])//5)-a[1]*((b[0]+c[0])//5)
        assert (lhs-5*skew) % 25 == 0
        counts[(lhs-5*skew)//25] += 1
    return dict(sorted(counts.items()))


def folded(r):
    r %= 5
    return min(r, 5-r)


def recover(folds, reference, sums):
    if reference is None:
        return tuple(0 for f in folds)
    a = folds[reference]  # choose one of the two global orientations
    result = []
    for j, value in enumerate(folds):
        if j == reference or value == 0:
            result.append(value)
            continue
        allowed = {b % 5 for b in (value, -value) if folded(a+b) == sums[j]}
        assert len(allowed) == 1
        result.append(allowed.pop())
    return tuple(result)


def real_fringe_replay():
    folded_alone = Counter()
    extra_reads = Counter()
    for row in product(range(5), repeat=7):
        folds = tuple(map(folded, row))
        active = [i for i, x in enumerate(folds) if x]
        ref = active[0] if active else None
        sums = {i: folded(row[ref]+row[i]) for i in active[1:]}
        out = recover(folds, ref, sums)
        conjugate = tuple(-a % 5 for a in row)
        assert out == row or out == conjugate
        folded_alone[folds] += 1
        extra_reads[len(sums)] += 1
    return {"value_vectors": sum(extra_reads.values()),
            "folded_patterns_with_multiplicity": dict(sorted(Counter(folded_alone.values()).items())),
            "number_of_extra_reads": dict(sorted(extra_reads.items()))}


def main():
    words = cycles()
    # The oriented boundary vanishes as a formal sum of ordered pairs,
    # including the endpoints with a zero input.
    boundary = [boundary_pairs(word) for word in words]
    assert all(not residual for residual in boundary)
    matrix = [[cycle_value(word, seed, 5) for seed in SEEDS] for word in words]
    assert rank(matrix) == 7
    basis = BASIS
    cross = [[fifth_power(seed, x, y) for seed in SEEDS]
             for x, y in combinations(basis, 2)]
    assert rank(matrix+cross) == 10
    skew_read = []
    for i, j in combinations(range(3), 2):
        ij, ji = 1+3*i+j, 1+3*j+i
        assert all((row[ij]-row[ji]) % 5 == 0 for row in matrix)
        skew_read.append([(row[ij]-row[ji]) % 5 for row in cross])
    assert skew_read == [[1,0,0],[0,1,0],[0,0,1]]
    rng = Random(817)
    vectors = tuple(product(range(5), repeat=3))
    gauges = {(a, b): rng.randrange(25) if a != ZERO and b != ZERO else 0
              for a, b in product(vectors, repeat=2)}

    def gauge(a, b, c):
        return gauges[b,c]-gauges[add(a,b),c]+gauges[a,add(b,c)]-gauges[a,b]

    assert all(cycle_value(word, gauge, 25) == 0 for word in words)
    phases = [cos(2*pi*j/5) for j in range(3)]
    result = {
        "columns": ["det"]+[f"a{i+1} C{j+1}" for i in range(3) for j in range(3)],
        "rows": ["alternator","e1","e2","e3","e1+e2","e1+e3","e2+e3"],
        "phase_matrix": matrix, "additional_calibrated_contact_rows": cross,
        "skew_on_calibrated_contact_rows": skew_read, "phase_rank": rank(matrix),
        "joint_rank": rank(matrix+cross),
        "skew_primitive_multiple_of_25_histogram": skew_check(),
        "ordinary_real_contrasts": phases,
        "nearest_real_margin": min(phases[j]-phases[j+1] for j in range(2))/2,
        "nearest_complex_margin": sin(pi/5), "real_fringe_replay": real_fringe_replay(),
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare every retained result to JSON")
    args = parser.parse_args()
    output = json.dumps(main(), indent=2, allow_nan=False)
    if args.check:
        stored = Path(__file__).with_name("reassociation_phases.json").read_text(encoding="utf-8")
        assert json.loads(stored) == json.loads(output)
        print("Seven phase coordinates, three calibrated lifts, 15,625 carry triples and 78,125 real-fringe cases verified.")
    else:
        print(output)
