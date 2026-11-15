"""Check a three-copy witness by tracing the actual translated memory labels."""

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def orientations(i, k):
    return [(i, k)] if i == k else [(i, k), (k, i)]


def cycle(i, j):
    return (int((j - i) % 3 == 1) - int((j - i) % 3 == 2))


def coefficient(i, k, j, l):
    left, right = orientations(i, k), orientations(j, l)
    return sum(F(cycle(a, b) * cycle(c, d), 6)
               for a, c in left for b, d in right) / (len(left) * len(right))


def addresses(copies, persistent, i, j):
    if persistent:
        return (int(i == j),)
    return tuple(int(i == j == c) for c in range(copies))


def density(copies, persistent, amplitudes):
    indices = list(product(range(copies), repeat=2))
    norm = sum(a*a for a in amplitudes)
    offsets = {ij: addresses(copies, persistent, *ij) for ij in indices}
    rho = {}
    for i, j in indices:
        for k, l in indices:
            overlap = F(1)
            for a, b in zip(offsets[i, j], offsets[k, l]):
                overlap *= F(sum(n * amplitudes[(z+a-b) % len(amplitudes)]
                                 for z, n in enumerate(amplitudes)), norm)
            rho[i, j, k, l] = overlap / copies**2
    return rho


def local_analyzer(pair):
    i, k = pair
    if i == k:
        return [("hit", {i: 1}, 1, 1), *[("other" + str(j), {j: 1}, 1, 0)
                                                for j in range(3) if j != i]]
    unused = next(j for j in range(3) if j not in pair)
    return [("+", {i: 1, k: 1}, 2, 1), ("-", {i: 1, k: -1}, 2, -1),
            ("other", {unused: 1}, 1, 0)]


def analyze(rho):
    pairs = [(i, k) for i in range(3) for k in range(i, 3)]
    score = F(0)
    lines = []
    for x, y in product(pairs, repeat=2):
        i, k = x
        j, l = y
        coef = coefficient(i, k, j, l)
        if not coef:
            continue
        probabilities = {}
        moment = F(0)
        for aname, a, anorm, aval in local_analyzer(x):
            for bname, b, bnorm, bval in local_analyzer(y):
                value = sum(rho[i, j, k, l] * ai * bj * ak * bl
                            for i, ai in a.items() for j, bj in b.items()
                            for k, ak in a.items() for l, bl in b.items()) / (anorm * bnorm)
                assert value >= 0
                probabilities[f"{aname}/{bname}"] = str(value)
                moment += aval * bval * value
        assert sum(map(F, probabilities.values())) == 1
        score += coef * moment
        lines.append({"first": x, "second": y, "coefficient": str(coef),
                      "conditional_outcomes": probabilities, "moment": str(moment)})
    return score, lines


def trial(amplitudes, persistent):
    norm = sum(a*a for a in amplitudes)
    gamma = F(sum(a * amplitudes[(i + 1) % len(amplitudes)]
                  for i, a in enumerate(amplitudes)), norm)
    t = 1 if persistent else gamma**2
    xi = 1 - 2*gamma + t
    rho = density(3, persistent, amplitudes)
    for i, j in product(range(3), repeat=2):
        image = sum(rho[i, j, k, l] * cycle(k, l) for k, l in product(range(3), repeat=2))
        transposed = sum(rho[i, l, k, j] * cycle(k, l) for k, l in product(range(3), repeat=2))
        assert image == 0 and transposed == -xi * cycle(i, j) / 9
    score, settings = analyze(rho)
    assert score == -xi / 18
    assert len(settings) == 21
    assert sum(abs(F(r["coefficient"])) for r in settings) == F(11, 4)
    # With only two active copies and real gamma in the fresh-bus model, the
    # partial transpose splits into two explicit 2x2 blocks in the Bell basis.
    r2 = density(2, persistent, amplitudes)
    bell = [[1,0,0,1], [0,1,1,0], [1,0,0,-1], [0,1,-1,0]]
    source = [(0,0), (0,1), (1,0), (1,1)]
    pt = [[2*sum(v[a]*w[b]*r2[i,l,k,j] for a,(i,j) in enumerate(source)
                 for b,(k,l) in enumerate(source)) for w in bell] for v in bell]
    assert pt == [[2,2*gamma,0,0],[2*gamma,1+t,0,0],[0,0,0,0],[0,0,0,1-t]]
    return {"gamma": str(gamma), "t": str(t), "conditional_score": str(score),
            "per_launch_score": str(score * F(9, 64)), "settings": settings}


def report():
    heralded = sum(sum(a) == sum(b) == 1 for a, b in product(list(product(range(2), repeat=3)), repeat=2))
    assert heralded == 9
    return {
        "herald_probability": "9/64",
        "blank_fresh": trial([1, 0, 0, 0, 0], False),
        "blank_persistent": trial([1, 0, 0, 0, 0], True),
        "signed_fresh": trial([1, -1, 0, 0, 0], False),
        "invariant_persistent": trial([1, 1, 1, 1, 1], True),
    }


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
