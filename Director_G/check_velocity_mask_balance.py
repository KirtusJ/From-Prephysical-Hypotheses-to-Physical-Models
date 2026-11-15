"""Identify seven-tick site frequencies from equal-mass position masks."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path

from check_reflecting_path import physical_step


MASKS = [
    ((0,), (7,)),
    ((1,), (4,)),
    ((0, 5), (2, 6)),
    ((2, 5), (3, 6)),
    ((0, 6, 7), (1, 2, 4)),
    ((0, 1, 6), (2, 3, 5)),
    ((0, 1, 2, 4, 7), (5,)),
]


def walk(tick):
    length = 2 * tick + 1
    state = [[0, 0] for _ in range(length)]
    state[tick][0] = 1
    for _ in range(tick):
        state = physical_step(state)
    masses = [sum(v*v for v in state[x]) for x in range(0, length, 2)]

    amplitudes = Counter()
    for path in product((0, 1), repeat=tick):
        index = path.count(0)
        rail = path[-1] if tick else 0
        signs = sum(r == s == 1 for r, s in zip((0,) + path, path))
        amplitudes[index, rail] += (-1) ** signs
    assert masses == [sum(amplitudes[i, r] ** 2 for r in (0, 1)) for i in range(tick + 1)]
    assert sum(masses) == 2 ** tick and all(masses)
    return masses


def incidence(left, right, size):
    return [int(i in left) - int(i in right) for i in range(size)]


def dot(row, weights):
    return sum(a*b for a, b in zip(row, weights, strict=True))


def independent_rows(rows):
    """Incremental exact echelon basis; keep each old pivot row normalized."""
    basis = {}
    for row in rows:
        residual = list(map(F, row))
        for i in range(len(residual)):
            coefficient = residual[i]
            if not coefficient:
                continue
            if i not in basis:
                basis[i] = [v/coefficient for v in residual]
                break
            residual = [x - coefficient*y for x, y in zip(residual, basis[i])]
    return len(basis)


def tie_rows(masses, masks):
    representative = {}
    for mask in masks:
        mass = sum(masses[i] for i in mask)
        if mass in representative:
            yield incidence(mask, representative[mass], len(masses))
        else:
            representative[mass] = mask


def mask_ranks(masses):
    size = len(masses)
    intervals = [tuple(range(i, j)) for i in range(size) for j in range(i+1, size+1)]
    subsets = (mask for k in range(1, size+1) for mask in combinations(range(size), k))
    return independent_rows(tie_rows(masses, intervals)), independent_rows(tie_rows(masses, subsets))


def inverse(matrix):
    size = len(matrix)
    augmented = [list(map(F, row)) + [F(i == j) for j in range(size)]
                 for i, row in enumerate(matrix)]
    for i in range(size):
        pivot = next(j for j in range(i, size) if augmented[j][i])
        augmented[i], augmented[pivot] = augmented[pivot], augmented[i]
        divisor = augmented[i][i]
        augmented[i] = [v/divisor for v in augmented[i]]
        for j in range(size):
            if j != i:
                factor = augmented[j][i]
                augmented[j] = [x-factor*y for x, y in zip(augmented[j], augmented[i])]
    result = [row[size:] for row in augmented]
    for i in range(size):
        for j in range(size):
            assert sum(matrix[i][k]*result[k][j] for k in range(size)) == (i == j)
    return result


def panel(masses, score):
    # All eight address programs share the same global terminal normalizer.
    probabilities = [F(n, sum(masses)) for n in masses]
    fine = [score(h/8) for h in probabilities]
    coarse = []
    for a, b in MASKS:
        p = sum(probabilities[i] for i in a)
        q = sum(probabilities[i] for i in b)
        assert p == q
        coarse.append([score(p/8), score(q/8), score((1-p-q)/8)])
    normalizer = sum(fine) + sum(map(sum, coarse))
    assert normalizer > 0
    conditioned = [v / sum(fine) for v in fine]
    return {"fine": [str(v / normalizer) for v in fine],
            "coarse": [[str(v / normalizer) for v in row] for row in coarse],
            "conditional_fine": list(map(str, conditioned)),
            "fine_contrasts": [str(dot(incidence(a,b,len(masses)), conditioned)) for a,b in MASKS]}


def run():
    ranks = []
    for tick in range(1, 11):
        masses = walk(tick)
        r_interval, r_all = mask_ranks(masses)
        assert r_interval <= r_all < len(masses)
        ranks.append({"tick":tick, "positions":len(masses), "masses":masses,
                      "interval_tie_rank":r_interval, "all_subset_tie_rank":r_all})
    m = walk(7)
    assert m == [1,17,5,9,17,41,37,1]
    rows = [incidence(a, b, len(m)) for a,b in MASKS]
    assert all(dot(v,m) == 0 for v in rows) and independent_rows(rows) == 7
    inverse_matrix = inverse(rows + [[1]*len(m)])
    assert [row[-1] for row in inverse_matrix] == [F(x,128) for x in m]
    box = []
    for signs in product((-1,1),repeat=7):
        error = [dot(row[:-1],signs) for row in inverse_matrix]
        box.append(sum(map(abs,error))/2)
    # Disturb two directions unconstrained by any interval tie.
    alt = [F(n,128) for n in m]
    shift = F(1,2048)
    alt[2] += shift
    alt[3] -= shift
    intervals = [tuple(range(i,j)) for i in range(8) for j in range(i+1,9)]
    pairs = list(combinations(intervals,2))
    def sign(x):
        return (x > 0) - (x < 0)
    assert all(sign(dot(incidence(a,b,8),m)) == sign(dot(incidence(a,b,8),alt)) for a,b in pairs)
    assert any(dot(row,alt) != 0 for row in rows)
    ordinary = panel(m,lambda x:x)
    cubic = panel(m,lambda x:x+x**3)
    assert all(F(x) == 0 for x in ordinary["fine_contrasts"])
    assert any(F(x) != 0 for x in cubic["fine_contrasts"])
    assert all(r[0] == r[1] for data in [ordinary,cubic] for r in data["coarse"])
    return {"mask_pairs": MASKS, "all_rank_scans": ranks,
            "inverse_with_normalization_last": [list(map(str,row)) for row in inverse_matrix],
            "max_TV_per_max_residual":str(max(box)),
            "interval_order_preserving_alternative":list(map(str,alt)),
            "all_interval_pairs_checked":len(pairs), "ordinary":ordinary,
            "identity_plus_cube":cubic}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    with args.output.open("x",encoding="utf-8",newline="\n") as out:
        out.write(json.dumps(run(),indent=2)+"\n")
