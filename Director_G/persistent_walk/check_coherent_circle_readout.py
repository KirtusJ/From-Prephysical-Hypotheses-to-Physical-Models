"""Fit the circle figure with a coherent analyzer and bound the effect of terminal rail dephasing."""
import json
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
from runpy import run_path

from PIL import Image

HERE = Path(__file__).resolve().parent
three = run_path(str(HERE / 'check_three_circle_sites.py'))
figure = three['figure']
walk, require = figure['walk'], three['require']
ROUNDS, SITES = three['ROUNDS'], three['launch']['SITES']
GAINS = ((15720, 10202), (39715, 1986), (7551, 17982), (431, 8613), (61387, 4102))
DIVISORS = (10000, 15885, 20598, 13782)


def dephasing_bound(image, reader):
    """Increase the 8-level site bands by epsilon times an upper bound on the round total."""
    bands = three['cell_bands'](image, reader, 'experiment', 8, SITES)
    totals = {t: sum(bands[t, m][1] for m in SITES) for t in ROUNDS}
    cert = json.loads((HERE / 'three_circle_site_certificate.json').read_text())
    # The reciprocal-scale column for round t is sum(lower*L - upper*U).
    # Increasing each band by epsilon*totals[t] reduces that column by
    # epsilon*totals[t]*sum(lower+upper), independently of the launch box.
    candidates = []
    for row in cert['weights']:
        for i, t in enumerate(ROUNDS):
            margin = F(0)
            weight = 0
            for j, m in enumerate(three['SITES']):
                offset = 2*(len(three['SITES'])*i+j)
                upper, lower = row[offset:offset+2]
                lo, hi = bands[t, m]
                margin += lower*lo - upper*hi
                weight += lower + upper
            if weight:
                candidates.append(margin/(weight*totals[t]))
    epsilon = min(candidates)
    require(epsilon == F(46484, 14295555), 'conditional shape bound changed')
    widened = {(t, m): (lo-epsilon*totals[t], hi+epsilon*totals[t])
               for (t, m), (lo, hi) in bands.items()}
    # The previous checker requires every separating column strictly positive.
    # At the exact endpoint some scale columns vanish. Verify the original
    # cover topology, then check each widened leaf with the endpoint signs.
    coeff = three['launch']['effects']()
    cover = three['verify_cover'](coeff, bands, cert)
    for x, y, den, idx in cert['boxes']:
        columns = three['separating_columns'](coeff, widened, (x, y, den), cert['weights'][idx])
        require(min(columns[:6]) > 0 and min(columns[6:]) >= 0, 'invalid widened certificate')
    return bands, epsilon, cover['excluded']


def intensity(state, site, t, gains, divisor, left_sign):
    (a, b), (c, d) = state[(site-2) % 10]
    c, d = left_sign*c, left_sign*d
    # Project onto (2,-1+2i)/3 and its orthogonal partner (-1-2i,-2)/3.
    plus = (2*a-c+2*d)**2 + (2*b-d-2*c)**2
    minus = (-a-2*b-2*c)**2 + (-b+2*a-2*d)**2
    require(plus + minus == 9*(a*a+b*b+c*c+d*d), 'analyzer normalization')
    return F(gains[0]*plus + gains[1]*minus, 21*9*2**t*divisor)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('figure_png', type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure['PNG_SHA'], 'figure digest')
    with Image.open(args.figure_png) as image:
        bands, epsilon, leaves = dephasing_bound(image, figure['legend_reader'](image))
    state = walk['launch'](10, 0)
    state[0] = [(4, 0), (1, -2)]  # Fixed pure input, with normalization sqrt(21).
    checks = {}
    slack = []
    for t in range(max(ROUNDS)+1):
        if t in ROUNDS:
            divisor = DIVISORS[ROUNDS.index(t)]
            arms = [[intensity(state, m, t, g, divisor, s) for m, g in zip(SITES, GAINS)]
                    for s in (1, -1)]
            original, reversed_phase = arms
            for m, val in zip(SITES, original):
                lo, hi = bands[t, m]
                slack.append(min(val-lo, hi-val))
            require(sum(original) <= 1, 'original fit exceeds available intensity')
            # A randomized terminal sign cancels off-diagonal terms in the
            # unnormalized intensities. Normalize only after pooling the arms.
            pooled = [(a+b)/2 for a, b in zip(*arms)]
            marginal = [v/sum(original) for v in original]
            conditional_flip = [v/sum(reversed_phase) for v in reversed_phase]
            conditional_pool = [v/sum(pooled) for v in pooled]
            tv_flip = sum(abs(a-b) for a, b in zip(marginal, conditional_flip))/2
            tv_pool = sum(abs(a-b) for a, b in zip(marginal, conditional_pool))/2
            checks[t] = dict(original=list(map(str, original)), pi_phase_before_renormalizing=list(map(str, reversed_phase)),
                             original_sum=str(sum(original)), conditional_TV_pi=str(tv_flip),
                             conditional_TV_dephased=str(tv_pool),
                             conditional_site9=[str(marginal[-1]), str(conditional_flip[-1])])
        state = walk['step'](state, 'Hprime')
    require(len(slack) == 20 and min(slack) > 0, 'an experimental cell excludes this witness')
    require(max(F(v['conditional_TV_dephased']) for v in checks.values()) > epsilon, 'dephasing control')
    require(F(checks[17]['conditional_TV_pi']) > F(58, 100), 'sign-flip control')
    print(json.dumps(dict(sites=SITES, gains=GAINS, reciprocal_scales=DIVISORS, rounds=checks,
                          smallest_intersection_margin=str(min(slack)), covered_boxes=leaves,
                          necessary_conditional_TV_strictly_above=str(epsilon)), indent=2))


if __name__ == '__main__':
    main()
