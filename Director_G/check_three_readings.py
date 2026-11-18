"""Replay the trine simulator and, optionally, the two published photon count files."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path

from check_cairo_cycle import require


SIGNS = tuple(product((-1, 1), repeat=3))
STATES = tuple(b for b in SIGNS if abs(sum(b)) == 1)
SCORE_PAIRS = ((0, 0), (0, 2), (1, 0), (1, 2))
POOLED_HASH = "be168293d7755c273fbaff71c9c3d66f54773aa9d40f0ec46c39bd3765a64bfb"
RUNS_HASH = "11d000550a4248135a2032a2712c24a118cdf529fb0c01a1e11e4bf76993cd5e"


def score(values):
    return values[0] - sum(values[1:])


def reset(setting, answer):
    return {b: F(1, 2) if b[setting] == -sum(b) else F(1, 4)
            for b in STATES if b[setting] == answer}


def check_models():
    mixtures = []
    for i in range(3):
        law = {}
        for answer in (-1, 1):
            posterior = reset(i, answer)
            require(sum(posterior.values()) == 1, "Reset normalization")
            for j in range(3):
                expected = answer if i == j else F(-answer, 2)
                require(sum(w*b[j] for b, w in posterior.items()) == expected, "Next read")
            for b, w in posterior.items():
                law[b] = w/2
        mixtures.append(law)
    for i, j in permutations(range(3), 2):
        distance = sum(abs(mixtures[i][b]-mixtures[j][b]) for b in STATES)/2
        require(distance == F(1, 4), "Hidden distance of averaged sources")

    for corner in permutations((-1, 0, 1)):
        compatible = [b for b in STATES if all(x == 0 or x == y for x, y in zip(corner, b))]
        require(len(compatible) == 2 and all(x+y == 2*z for x,y,z in zip(*compatible, corner)),
                "Hexagon corner must be realized by two memory states")
    for a, b in product(SIGNS, repeat=2):
        require(abs(score([a[i]*b[j] for i, j in SCORE_PAIRS])) == 2, "Classical score")
    for mass, diagonal, off_axis in ((F(9, 10), F(4, 5), F(-2, 5)),
                                     (F(15, 16), F(7, 8), F(-3, 8))):
        law = {(b, b): mass/6 for b in STATES}
        for bit in (-1, 1):
            law[((-bit,)*3, (bit,)*3)] = (1-mass)/2
        for i, j in product(range(3), repeat=2):
            value = sum(p*a[i]*b[j] for (a,b),p in law.items())
            require(value == (diagonal if i == j else off_axis), "Boundary model")
    print("Six-state reset and 1/4 hidden distance verified; preparation-independent visibility threshold 4/5.")


def table(path, expected_hash, per_run):
    from openpyxl import load_workbook

    require(sha256(path.read_bytes()).hexdigest() == expected_hash, "Workbook SHA-256")
    book = load_workbook(path, read_only=True, data_only=True)
    try:
        rows = iter(book.active.values)
        next(rows)
        headers = next(rows)
        start = headers.index("[0|M1]")
        expected = [f"[{b}|M{j}]" for j in range(1,5) for b in (0,1)]
        require(list(headers[start:start+8]) == expected, "Outcome headers")
        counts = {}
        for row in rows:
            prep = row[start-1]
            if prep is None:
                continue
            key = (row[0] if per_run else 0, prep)
            values = tuple(row[start:start+8])
            require(key not in counts and all(type(v) is int and v >= 0 for v in values),
                    "Unique, nonnegative integer coincidence rows")
            counts[key] = values
        return counts
    finally:
        book.close()


def check_photons(pooled_path, runs_path):
    pooled = table(pooled_path, POOLED_HASH, False)
    runs = table(runs_path, RUNS_HASH, True)
    require(len(pooled) == 8 and len(runs) == 800, "Number of preparations and runs")
    for i, a in product(range(4), range(2)):
        label = f"P_{i+1},{a}"
        summed = tuple(sum(runs[k,label][h] for k in range(1,101)) for h in range(8))
        pooled_label = f"P_4,{1-a}" if i == 3 else label
        require(summed == pooled[0,pooled_label], "Compare workbooks including auxiliary exchange")

    def probability(i, a, j):
        row = pooled[0,f"P_{i+1},{a}"]
        return F(row[2*j], row[2*j]+row[2*j+1])

    correlations = [probability(i,0,j)-probability(i,1,j) for i,j in SCORE_PAIRS]
    differences = [sum(probability(0,a,j)-probability(1,a,j) for a in range(2))/2
                   for j in range(4)]
    matched = []
    for i, a in product(range(3),range(2)):
        row = pooled[0,f"P_{i+1},{a}"]
        matched.append((row[2*i+a], row[2*i]+row[2*i+1]))
    print("Four correlations:", [round(float(v), 10) for v in correlations])
    print(f"Four-cell score: {float(score(correlations)):.10f}")
    print("Raw source-average differences:", [round(float(v), 10) for v in differences])
    print("Opposite clicks / matched coincidences:", sum(d-n for n,d in matched), sum(d for n,d in matched))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photons", nargs=2, type=Path, metavar=("POOLED", "PER_RUN"))
    args = parser.parse_args()
    check_models()
    if args.photons:
        check_photons(*args.photons)
