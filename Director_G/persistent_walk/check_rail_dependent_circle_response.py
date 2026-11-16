"""Test a static, rail-dependent intensity response against the authors' source figure."""
import json
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from runpy import run_path

from PIL import Image

figure = run_path(str(Path(__file__).with_name("check_circle_figure.py")))
walk, require = figure["walk"], figure["require"]
SITES = (1, 3, 5, 7, 9)
GAINS = {1:(1279,904), 3:(1046,175), 5:(6422,1071), 7:(296,1771), 9:(922,5448)}
DENOMINATORS = {1:1000, 11:1633, 13:1441}


def rail_probabilities():
    right, left, diagonal = [walk["launch"](10, rail) for rail in (0, 1, 0)]
    diagonal[0] = [(1,0), (1,0)]
    sharp, balanced = {}, {}
    for t in range(14):
        if t in (1, 7, 11, 13):
            for m in range(10):
                site = (m-2) % 10
                r, l, d = [[walk["probability"](a, t) for a in state[site]]
                           for state in (right, left, diagonal)]
                require(all(a+b == c for a,b,c in zip(r,l,d)), "mixture replay")
                sharp[t,m] = r
                balanced[t,m] = [c/2 for c in d]
        right, left, diagonal = [walk["step"](s, "Hprime") for s in (right,left,diagonal)]
    return sharp, balanced


def scale_interval(prob, band, m, first, last, cap=None):
    p, q = prob[first,m], prob[last,m]
    require(min(p+q) > 0, "positive rail support for ratio")
    if cap is None:
        ratios = [v/u for u,v in zip(p,q)]
    else:
        ratios = [(r*q[0]+q[1])/(r*p[0]+p[1]) for r in (1/cap, cap)]
    lo, hi = band(first,m)
    low, high = band(last,m)
    return low/hi/max(ratios), high/lo/min(ratios) if lo else None


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("figure_png", type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure["PNG_SHA"], "source bytes")
    sharp, balanced = rail_probabilities()
    samples, bounds = {}, {}
    with Image.open(args.figure_png) as image:
        read = figure["legend_reader"](image)
        for t, denominator in DENOMINATORS.items():
            row = {}
            for m in range(10):
                lo, hi = read(figure["cell"](image, "experiment", t, m), 8)
                p = sharp[t,m]
                if m % 2:
                    value = sum(g*a for g,a in zip(GAINS[m],p))/denominator
                else:
                    require(sum(p) == 0, "unoccupied even site")
                    value = F(0)
                require(lo <= value <= hi, "witness misses cell")
                row[m] = value
            require(sum(row.values()) <= 1, "reported circle intensity exceeds unity")
            samples[t] = dict(intensity=row, total=sum(row.values()))
        cases = [
            ("diagonal_or_equal_mixture", balanced, (11,13), (9,7), None, 32),
            ("sharp_R_with_round_seven", sharp, (7,13), (5,7), None, 47),
            ("sharp_R_capped_rail_contrast", sharp, (11,13), (5,9), F(23,4), 10)]
        for name, prob, times, sites, cap, first_overlap in cases:
            for slack in range(8, first_overlap+1):
                def band(t,m):
                    return read(figure["cell"](image, "experiment", t, m), slack)
                low = scale_interval(prob, band, sites[0], *times, cap=cap)[0]
                high = scale_interval(prob, band, sites[1], *times, cap=cap)[1]
                require(high is not None and (low > high) == (slack < first_overlap),
                        "scale bounds or tolerance boundary")
                if slack == 8:
                    bounds[name] = dict(rounds=times, sites=sites, lower=low, upper=high,
                                        first_overlap=first_overlap)
    contrast = max(F(max(g),min(g)) for g in GAINS.values())
    require(contrast < 6, "gain contrast of explicit witness")
    print(json.dumps(dict(relative_gains_R_L=GAINS, round_denominators=DENOMINATORS,
                          largest_within_site_gain_ratio=contrast,
                          experimental_panel_witness=samples, two_site_bounds=bounds),
                     indent=2, default=str))


if __name__ == "__main__":
    main()
