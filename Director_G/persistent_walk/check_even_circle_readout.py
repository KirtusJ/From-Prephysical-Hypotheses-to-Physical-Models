"""Test static coherent detection against six even rounds of the ten-site optical walk."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
from runpy import run_path
import json

from PIL import Image

HERE = Path(__file__).resolve().parent
figure = run_path(str(HERE / 'check_circle_figure.py'))
walk, require = figure['walk'], figure['require']
ROUNDS = (2, 4, 10, 14, 16, 18)
SITES = (0, 2, 4)
WEIGHTS = {0: (137, -559, -156, 1, 1026, 135),
           2: (-49, 49, 155, -81, 132, 1),
           4: (-24, 285, 104, 97, -552, -54)}


def transfer_vectors():
    columns = [walk['launch'](10, rail) for rail in (0, 1)]
    vectors = {}
    for t in range(max(ROUNDS)+1):
        if t in ROUNDS:
            for m in range(0, 10, 2):
                x = (m-2) % 10
                (a, ai), (cr, c) = columns[0][x]
                (br, b), (d, di) = columns[1][x]
                require((ai, br, cr, di) == (0, 0, 0, 0), 'transfer phases')
                vectors[t, m] = (a, b, c, d)
        columns = [walk['step'](col, 'Hprime') for col in columns]
    return vectors


def leading_minor(matrix, size):
    value = F(0)
    for perm in permutations(range(size)):
        inversions = sum(perm[j] > perm[k] for j in range(size) for k in range(j+1, size))
        term = (-1)**inversions
        for j, k in enumerate(perm):
            term *= matrix[j][k]
        value += term
    return value


def transfer_certificate(vectors):
    results = {}
    for m in SITES:
        dim = 2 if m == 2 else 3
        matrix = [[F(0) for _ in range(dim)] for _ in range(dim)]
        for t, weight in zip(ROUNDS, WEIGHTS[m], strict=True):
            a, b, c, d = vectors[t, m]
            require(d == a+b-c and (m != 2 or c == b), 'reduced transfer subspace')
            v = (a, b, c)[:dim]
            for i, j in product(range(dim), repeat=2):
                matrix[i][j] += F(weight*v[i]*v[j], 2**t)
        minors = [leading_minor(matrix, k) for k in range(1, dim+1)]
        require(min(minors) > 0, 'signed matrix is not positive definite')
        results[m] = list(map(str, minors))
    return results


def round_caps(bands):
    return [sum(WEIGHTS[m][i]*bands[t, m][int(WEIGHTS[m][i] > 0)] for m in SITES)
            for i, t in enumerate(ROUNDS)]


def wider_witness(vectors, bands):
    # H = [[p, q+ir], [q-ir, s]], in arbitrary common units.
    effects = {0: (22380, 4043, -5931, 5630), 2: (19896, 11363, -4006, 14192),
               4: (30446, -3310, -19655, 14553), 6: (1, 0, 0, 1), 8: (1, 0, 0, 1)}
    for p, q, r, s in effects.values():
        require(p > 0 and p*s > q*q+r*r, 'nonphysical witness detector')
    divisors = (10000, 9004, 6604, 9618, 7400, 19751)
    totals = []
    for t, divisor in zip(ROUNDS, divisors, strict=True):
        total = F(0)
        for m, (p, q, r, s) in effects.items():
            a, b, c, d = vectors[t, m]
            # Fixed launch (1, -1-i)/sqrt(3); output Gaussian integer numerators.
            ar, ai = a+b, -b
            br, bi = -d, c-d
            real = ar*br+ai*bi
            imag = ar*bi-ai*br
            num = p*(ar*ar+ai*ai)+s*(br*br+bi*bi)+2*(q*real-r*imag)
            value = F(num, 3*2**t*divisor)
            if m in SITES:
                lo, hi = bands[t, m]
                require(lo < value < hi, 'wider-band control outside a cell')
            total += value
        require(0 < total <= 1, 'wider-band on-circle total')
        totals.append(str(total))
    return totals


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('figure_png', type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure['PNG_SHA'], 'source figure digest')
    vectors = transfer_vectors()
    minors = transfer_certificate(vectors)
    with Image.open(args.figure_png) as image:
        read = figure['legend_reader'](image)
        def bands(panel, slack):
            return {(t, m): read(figure['cell'](image, panel, t, m), slack)
                    for t, m in product(ROUNDS, SITES)}
        caps8 = round_caps(bands('experiment', 8))
        caps9 = round_caps(bands('experiment', 9))
        caps10 = round_caps(bands('experiment', 10))
        numerics = bands('numeric', 8)
        totals = wider_witness(vectors, bands('experiment', 24))
    require(max(caps8) < 0 and max(caps9) < 0, 'no strict experimental contradiction')
    require(max(caps10) >= 0, 'ten-level certificate cutoff changed')
    for (t, m), (lo, hi) in numerics.items():
        prob = F(sum(x*x for x in vectors[t, m]), 2**(t+1))
        require(lo <= prob <= hi, 'numerical control excludes equal rail mixture')
    margin = min(-c/sum(abs(WEIGHTS[m][i]) for m in SITES) for i, c in enumerate(caps9))
    require(margin == F(1, 52155), 'uniform widening radius changed')
    print(json.dumps(dict(rounds=ROUNDS, sites=SITES, weights=WEIGHTS, leading_minors=minors,
                          experimental_caps_at_8=list(map(str, caps8)), experimental_caps_at_9=list(map(str, caps9)),
                          experimental_caps_at_10=list(map(str, caps10)), numeric_matches=len(numerics),
                          additive_widening_radius=str(margin), wider_witness_totals_at_24=totals), indent=2))


if __name__ == '__main__':
    main()
