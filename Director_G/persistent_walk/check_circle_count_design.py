"""Plan a prospective categorical-count test of static coherent readout on the circle."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import ceil, factorial
from pathlib import Path
from runpy import run_path
import json

from PIL import Image

even = run_path(str(Path(__file__).with_name('check_even_circle_readout.py')))
figure = even['figure']
require = even['require']
ROUNDS, SITES = even['ROUNDS'], even['SITES']
# Rows are rounds. Columns are the recorded sites 0, 2 and 4.
SCORES = ((1165, -406, -247), (-5661, 513, 2826), (-1453, 1099, 1249),
          (0, -802, 943), (10000, 1256, -5541), (1604, 0, -656))
DIVISORS = (131072, 786432, 196608, 131072, 786432, 131072)
PREVIOUS_DIVISORS = (65536, 1048576, 98304, 65536, 12582912, 32768)


def signed_minors(vectors):
    minors = {}
    for j, site in enumerate(SITES):
        size = 2 if site == 2 else 3
        matrix = [[F(0) for _ in range(size)] for _ in range(size)]
        for tick, row in zip(ROUNDS, SCORES, strict=True):
            a, b, c, d = vectors[tick, site]
            require(d == a+b-c and (site != 2 or c == b), 'transfer subspace')
            for x, y in product(range(size), repeat=2):
                vector = (a, b, c)
                matrix[x][y] += F(row[j]*vector[x]*vector[y], 2**tick)
        minors[site] = [even['leading_minor'](matrix, k) for k in range(1, size+1)]
        require(min(minors[site]) > 0, 'nonpositive signed minor')
    return minors


def plan(bands, scores, divisors):
    rows = []
    for tick, weights, divisor in zip(ROUNDS, scores, divisors, strict=True):
        require(divisor > max(0, *weights), 'nonpositive betting factor')
        intervals = [bands[tick, site] for site in SITES]
        corner = [pair[int(w > 0)] for pair, w in zip(intervals, weights)]
        require(sum(corner) <= 1, 'least favorable endpoint is not categorical')
        caps = sum(p*w for p, w in zip(corner, weights))
        reciprocal = 1+sum(p*F(w, divisor-w) for p, w in zip(corner, weights))
        # Enumerate all box corners, even if their total exceeds one. The chosen
        # maximizer is itself a probability assignment with a zero-score remainder.
        for probs in product(*intervals):
            value = 1-sum(probs)+sum(p*F(divisor, divisor-w) for p, w in zip(probs, weights))
            require(value <= reciprocal, 'endpoint does not bound reciprocal moment')
        require(caps < 0 and 0 < reciprocal < 1, 'alternative has no guaranteed growth')
        budget = ceil(F(71, 10)/(1-reciprocal))
        require((budget-1)*(1-reciprocal) < F(71, 10) <= budget*(1-reciprocal), 'budget rounding')
        rows.append(dict(round=tick, divisor=divisor, score_cap=str(caps),
                         reciprocal_cap=str(reciprocal), count_budget=budget))
    return rows


def dependent_control(vectors):
    # Draw one shared uniform number. At each round put all negative-score
    # categories at the beginning of [0,1], then replay that round's one draw.
    neg_mass, means = [], []
    for tick, weights in zip(ROUNDS, SCORES, strict=True):
        probs = [F(sum(x*x for x in vectors[tick, m]), 2**(tick+1)) for m in SITES]
        require(sum(probs) <= 1, 'invalid equal-mixture probabilities')
        neg_mass.append(sum(p for w, p in zip(weights, probs) if w < 0))
        means.append(sum(p*w for w, p in zip(weights, probs)))
    require(max(means) > 0 and min(neg_mass) == F(67, 512), 'dependent replay control')
    return neg_mass, means


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('figure_png', type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure['PNG_SHA'], 'source figure digest')
    vectors = even['transfer_vectors']()
    minors = signed_minors(vectors)
    with Image.open(args.figure_png) as image:
        read = figure['legend_reader'](image)
        bands = {(t, m): read(figure['cell'](image, 'experiment', t, m), 9)
                 for t, m in product(ROUNDS, SITES)}
    rows = plan(bands, SCORES, DIVISORS)
    old_scores = tuple(zip(*(even['WEIGHTS'][m] for m in SITES), strict=True))
    baseline = plan(bands, old_scores, PREVIOUS_DIVISORS)
    require(sum(F(71, 10)**k/factorial(k) for k in range(19)) > 1200, 'exponential bound')
    masses, means = dependent_control(vectors)
    # A repeated strictly negative outcome crosses 20 within each stated cap.
    for row, weights in zip(rows, SCORES, strict=True):
        smallest_gain = F(-max(w for w in weights if w < 0), row['divisor'])
        require(1+row['count_budget']*smallest_gain >= 20, 'replay need not cross within budget')
    print(json.dumps(dict(sites=SITES, round_scores=SCORES, signed_leading_minors={
        m: list(map(str, seq)) for m, seq in minors.items()}, plan=rows,
        total_counts=sum(row['count_budget'] for row in rows),
        previous_score_budgets=[row['count_budget'] for row in baseline],
        previous_total=sum(row['count_budget'] for row in baseline),
        equal_mixture_means=list(map(str, means)), repeated_draw_negative_masses=list(map(str, masses)),
        repeated_draw_joint_crossing_lower_bound=str(min(masses))), indent=2))


if __name__ == '__main__':
    main()
