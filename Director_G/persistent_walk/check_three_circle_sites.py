"""Check the three-site optical-circle exclusion and its deletion controls."""
import json
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
from runpy import run_path

from PIL import Image

HERE = Path(__file__).resolve().parent
launch = run_path(str(HERE / 'check_common_circle_launch.py'))
figure = launch['source']
require = launch['require']
ROUNDS = (7, 13, 17, 19)
SITES = (3, 5, 9)


def cell_bands(image, reader, panel, tolerance, sites):
    return {(t, m): reader(figure['cell'](image, panel, t, m), tolerance)
            for t, m in product(ROUNDS, sites)}


def separating_columns(coeff, bands, box, weights):
    """Weighted sum of necessary upper and lower inequalities at each cell."""
    x, y, den = box
    limits = launch['bounds_for_box'](coeff, x, y, den)
    columns = [F(0)] * 10
    for row, (t, m) in enumerate(product(ROUNDS, SITES)):
        upper, lower = weights[2*row:2*row+2]
        for rail in (0, 1):
            low, high = limits[t, m, rail]
            columns[2*SITES.index(m)+rail] += F(upper*low - lower*high, den*2**(t+1))
        left, right = bands[t, m]
        columns[6+ROUNDS.index(t)] += lower*left - upper*right
    return columns


def verify_cover(coeff, bands, cert):
    weights = cert['weights']
    require(all(len(row) == 24 and all(type(v) is int and v >= 0 for v in row)
                for row in weights), 'invalid inequality multipliers')
    leaves = {(x, y, den): i for x, y, den, i in cert['boxes']}
    require(len(leaves) == len(cert['boxes']) and leaves, 'empty or duplicate certificate boxes')
    require(all(type(v) is int for row in cert['boxes'] for v in row), 'box indices must be integers')
    maximum = max(den for x, y, den in leaves)
    area = F(0)
    outside = 0
    smallest_margin = None
    pending = [(x, y, 1) for x, y in product((-1, 0), repeat=2)]
    while pending:
        x, y, den = box = pending.pop()
        if max(0, x, -x-1)**2 + max(0, y, -y-1)**2 > den**2:
            outside += 1
        elif box in leaves:
            index = leaves.pop(box)
            require(0 <= index < len(weights), 'invalid multiplier index')
            margin = min(separating_columns(coeff, bands, box, weights[index]))
            require(margin > 0, f'nonpositive separating column at {box}')
            smallest_margin = margin if smallest_margin is None else min(smallest_margin, margin)
        else:
            require(den < maximum, f'uncovered rectangle {box}')
            pending.extend((2*x+i, 2*y+j, 2*den) for i, j in product(range(2), repeat=2))
            continue
        area += F(1, den**2)
    require(not leaves and area == 4, 'incomplete or overlapping cover')
    return dict(excluded=len(cert['boxes']), outside=outside, area=str(area),
                finest_width=str(F(1, maximum)), smallest_weighted_column=str(smallest_margin))


def witness(coeff, bands, sites, rounds, z, y, gains, divisors):
    """Complete the omitted sites with small positive gains, including both rails."""
    require(z*z + y*y <= 1 and all(v > 0 for v in gains+divisors), 'invalid witness')
    max_total = F(0)
    for t, scale in zip(rounds, divisors, strict=True):
        total = F(0)
        for m in launch['SITES']:
            if m in sites:
                j = sites.index(m)
                pair = gains[2*j:2*j+2]
            else:
                pair = (F(1, 1000), F(1, 1000))
            pred = F(0)
            for rail, gain in enumerate(pair):
                a, b, c = coeff[t, m, rail]
                pred += gain*(a+b*z+c*y)/(2**(t+1)*scale)
            if m in sites:
                lo, hi = bands[t, m]
                require(lo <= pred <= hi, f'witness outside band at {t}, {m}')
            total += pred
        require(total <= 1, 'full on-circle intensity above one')
        max_total = max(total, max_total)
    return str(max_total)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('figure_png', type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure['PNG_SHA'], 'source figure digest')
    cert = json.loads((HERE / 'three_circle_site_certificate.json').read_text())
    coeff = launch['effects']()
    all_sites = launch['SITES']
    with Image.open(args.figure_png) as image:
        read = figure['legend_reader'](image)
        bounds = {s: cell_bands(image, read, 'experiment', s, all_sites) for s in (8, 15, 16)}
        numeric = cell_bands(image, read, 'numeric', 8, SITES)
    require(all(bounds[15][key][0] <= lo <= hi <= bounds[15][key][1]
                for key, (lo, hi) in bounds[8].items()), 'tolerance nesting')
    for (t, m), (lo, hi) in numeric.items():
        prob = sum(F(coeff[t, m, rail][0], 2**(t+1)) for rail in (0, 1))
        require(lo <= prob <= hi, 'numerical panel positive control')
    cover = verify_cover(coeff, bounds[15], cert)
    three_round = witness(coeff, bounds[8], all_sites, (7, 13, 17), F(11, 12), F(-1, 3),
                          [644,2164,814,7161,4,4776,1069,4,1588,554], [1000,1811,2276])
    other_triples = launch['check_three_round_controls'](coeff, bounds[8])
    require({tuple(case['inverse_scales']) for case in other_triples} ==
            {(7,13,19), (7,17,19), (13,17,19)}, 'other round deletions')
    pairs = [((3,5), F(0), F(1), [264,2,96,1577], [1000,281,253,1158]),
             ((3,9), F(0), F(1), [501,3,189,1075], [1000,521,480,2074]),
             ((5,9), F(-1,2), F(1,2), [6407,28,7,877], [1000,219,5819,2694])]
    pair_totals = {','.join(map(str, sites)): witness(coeff, bounds[8], sites, ROUNDS, z, y, g, k)
                   for sites, z, y, g, k in pairs}
    widened = witness(coeff, bounds[16], SITES, ROUNDS, F(21,32), F(1,2),
                      [7166,1,3688,17513,1,23171], [10000,2624,6554,14262])
    print(json.dumps(dict(cover_at_15=cover, numerical_panel_matches=len(numeric),
                          all_four_round_deletions_fit_at_8=True, new_round_witness_max_total=three_round,
                          site_deletion_max_totals_at_8=pair_totals, three_site_max_total_at_16=widened), indent=2))


if __name__ == '__main__':
    main()
