"""Check what a calibrated or uncalibrated monotone response can hide on the circle."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import groupby
from pathlib import Path
from runpy import run_path
import json

from PIL import Image

counts = run_path(str(Path(__file__).with_name('check_circle_count_design.py')))
even, figure, require = counts['even'], counts['figure'], counts['require']
# For site m the Hermitian effect has diagonal entries p,s and upper entry i*z.
EFFECTS = ((156,184,-141), (229,744,-56), (1,264,0), (764,49,-191),
           (224,430,-281), (533,551,-35), (345,144,-80), (469,1,0),
           (108,263,33), (220,666,-185))


def static_intensities():
    walk = figure['walk']
    columns = [walk['launch'](10, rail) for rail in (0, 1)]
    result = {}
    for p, s, z in EFFECTS:
        require(p > 0 and p*s > z*z, 'nonpositive analyzer')
    for t in range(1, 20):
        columns = [walk['step'](state, 'Hprime') for state in columns]
        for m, (p, s, z) in enumerate(EFFECTS):
            value = 0
            for col in columns:
                (a, b), (c, d) = col[(m-2) % 10]
                value += p*(a*a+b*b)+s*(c*c+d*d)-2*z*(a*d-b*c)
            result[t, m] = F(value, 2**(t+1))
    return result


def round_points(t, latent, bands):
    # Equal inputs must receive exactly the same output, including at zero.
    by_input = sorted((latent[t, m], m) for m in range(10))
    points = {}
    previous = F(0)
    for x, items in groupby(by_input, key=lambda item: item[0]):
        sites = [m for _, m in items]
        lower = max(bands[t, m][0] for m in sites)
        upper = min(bands[t, m][1] for m in sites)
        y = F(0) if x == 0 else max(lower, previous + F(1, 10**6))
        require(lower <= y <= upper, 'no increasing interpolation in displayed band')
        for m in sites:
            points[m] = (x, y)
        previous = y
    require(0 < sum(y for _, y in points.values()) <= 1, 'on-circle total')
    return points


def fixed_curve(latent, bands):
    # Space successive positive input blocks apart, then do the same for the
    # outputs. A final common factor bounds the response strictly below one.
    knots = {F(0): F(0)}
    rows, right_x, right_y = [], F(1), F(1)
    for t in range(1, 20):
        points = round_points(t, latent, bands)
        positive = [(x,y) for x,y in points.values() if x > 0]
        a = 2*right_x/min(x for x, _ in positive)
        b = 2*right_y/min(y for _, y in positive)
        for x, y in positive:
            require(a*x not in knots or knots[a*x] == b*y, 'unequal values at common input')
            knots[a*x] = b*y
        right_x = max(a*x for x,_ in positive)
        right_y = max(b*y for _,y in positive)
        rows.append((t, a, b, points))
    divisor = 2*right_y
    knots = {x:y/divisor for x,y in knots.items()}
    order = sorted(knots)
    require(all(knots[x] < knots[z] for x,z in zip(order, order[1:])), 'response reverses order')
    require(knots[order[0]] == 0 and knots[order[-1]] == F(1,2), 'response endpoints')
    totals = []
    for t, a, b, points in rows:
        total = 0
        for m, (x, y) in points.items():
            predicted = divisor*knots[a*x]/b
            require(predicted == y and bands[t,m][0] <= predicted <= bands[t,m][1], 'fixed curve misses band')
            total += predicted
        totals.append(total)
    return len(knots), totals


def log_bounds(x):
    """Enclose -log(1-x) by 18 series terms and a geometric tail."""
    require(0 <= x < 1, 'occupancy outside logarithm domain')
    lo = sum(x**j/j for j in range(1, 19))
    return lo, lo + x**19/(19*(1-x))


def saturation_limits(bands):
    ratios = {}
    curves = {}
    for t, scores in zip(counts['ROUNDS'], counts['SCORES'], strict=True):
        endpoints = [bands[t,m][int(w > 0)] for m,w in zip(counts['SITES'], scores)]
        positive = [(w,q) for w,q in zip(scores,endpoints) if w > 0]
        negative = [(-w,q) for w,q in zip(scores,endpoints) if w < 0]
        ratios[t] = sum(w*q for w,q in negative)/sum(w*q for w,q in positive)
        require(ratios[t] > 1, 'linear sign lost')
        if t != 4:
            require(min(q for _,q in negative) >= max(q for _,q in positive), 'unordered correction factors')
        else:
            q0, q2, q4 = endpoints
            u, v, w = scores
            require(u < 0 < v and w > 0 and 0 < q2 < q0 < q4, 'round four endpoint ordering')
            require(bands[t,4][0] > max(bands[t,0][1], bands[t,2][1]), 'round four brightest site')
            require(-u*q0 > v*q2 and w*q4**2 > -u*q0**2, 'round four derivative controls')
            unscored = sum(bands[t,m][0] for m in range(10) if m not in counts['SITES'])
            require(sum(endpoints)+unscored <= 1, 'limiting round corner exceeds total')
            curves[t] = (scores, endpoints)
    ratio = min(ratios.values())
    require(ratio == ratios[4], 'limiting round')
    rail_lo, rail_hi = F(398272,10**7), F(398273,10**7)
    require(log_bounds(rail_lo)[1] < rail_lo*ratio and log_bounds(rail_hi)[0] > rail_hi*ratio,
            'resolved-channel threshold bracket')
    site_lo, site_hi = F(875927,10**7), F(875928,10**7)
    weights, qs = curves[4]
    def score_bounds(beta):
        terms = [(w, log_bounds(beta*q/qs[-1])) for w,q in zip(weights,qs)]
        return (sum(w*b[int(w<0)] for w,b in terms),
                sum(w*b[int(w>0)] for w,b in terms))
    require(score_bounds(site_lo)[1] < 0 < score_bounds(site_hi)[0], 'pooled-site threshold bracket')
    return dict(linear_ratios={t:str(x) for t,x in ratios.items()},
                resolved_limit_bracket=list(map(str,(rail_lo,rail_hi))),
                pooled_round4_limit_bracket=list(map(str,(site_lo,site_hi))))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('figure_png', type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure['PNG_SHA'], 'source figure digest')
    with Image.open(args.figure_png) as image:
        read = figure['legend_reader'](image)
        bands = {(t,m):read(figure['cell'](image,'experiment',t,m),9) for t in range(1,20) for m in range(10)}
    size, totals = fixed_curve(static_intensities(), bands)
    minors = counts['signed_minors'](even['transfer_vectors']())
    print(json.dumps(dict(cells=190, rounds=19, common_curve_knots=size,
                          minimum_on_circle_total=str(min(totals)), maximum_on_circle_total=str(max(totals)),
                          signed_minors_verified=sum(map(len,minors.values())), **saturation_limits(bands)), indent=2))


if __name__ == '__main__':
    main()
