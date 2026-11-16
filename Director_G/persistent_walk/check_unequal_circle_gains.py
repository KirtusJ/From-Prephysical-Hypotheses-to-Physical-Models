"""Test three independent site gains against reflection-invariant position records."""
import json
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from runpy import run_path

from PIL import Image

fixed = run_path(str(Path(__file__).with_name("check_fixed_site_return.py")))
figure, walk, require = fixed["figure"], fixed["walk"], fixed["require"]
SITES = (5, 7, 9)


def model():
    right, left = [walk["launch"](10, rail) for rail in (0, 1)]
    ratio = {}
    for t in range(14):
        if t in (7, 9, 11, 13):
            p7 = fixed["mass"](right, [5], t)
            ratio[t] = fixed["mass"](right, [3, 7], t) / p7
        if t == 9:
            # Unnormalized site-5 Gram matrix, with denominator 2^9.
            u, v = right[3], left[3]
            gram = (sum(a*a+b*b for a,b in u), sum(a*a+b*b for a,b in v),
                    sum(a*c+b*d for (a,b),(c,d) in zip(u,v)),
                    sum(a*d-b*c for (a,b),(c,d) in zip(u,v)))
        right, left = [walk["step"](s, "Hprime") for s in (right, left)]
    require(gram == (13, 85, 0, -9), "round-nine site-five Gram matrix")
    # Subtract 11.89 times identity from this Hermitian numerator. Both leading
    # principal minors are strictly positive, so every normalized input has
    # site-5 probability strictly greater than 11.89 / 512 at round nine.
    floor = F(1189, 100)
    a, b, re, im = gram
    require(a > floor and (a-floor)*(b-floor) > re*re+im*im, "positive definite control")
    return ratio, gram, floor/512


def site_bands(image, reader, t, slack):
    return [reader(figure["cell"](image, "experiment", t, m), slack) for m in SITES]


def pair_constraints(bands, ratio):
    a, p, b = bands
    return ((a[1], b[1], ratio*p[0]), (a[0], b[0], ratio*p[1]))


def certificate(low, high):
    a, b, lower = low
    c, d, upper = high
    require(c > 0 and d > 0, "positive comparison denominators")
    multiplier = max(a/c, b/d)
    return lower - multiplier*upper


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("figure_png", type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure["PNG_SHA"], "figure digest")
    ratios, gram, floor = model()
    margins = {}
    with Image.open(args.figure_png) as image:
        reader = figure["legend_reader"](image)
        for slack in range(4, 39):
            bands = {t: site_bands(image, reader, t, slack) for t in ratios}
            constraints = {t: pair_constraints(bands[t], ratios[t]) for t in ratios}
            values = {t: certificate(constraints[t][0], constraints[13][1]) for t in (7, 11)}
            require((values[7] > 0) == (slack <= 29), "round-seven margin")
            require((values[11] > 0) == (slack <= 37), "round-eleven margin")
            if slack in (8, 29, 30, 37, 38):
                margins[slack] = values
            if slack == 8:
                original = bands
                kept = constraints
    # With x=g7/g5, y=g7/g9 the bands imply a*x+b*y >= L
    # at nine and c*x+d*y <= U at thirteen. Eliminate y exactly.
    a, b, lower = kept[9][0]
    c, d, upper = kept[13][1]
    require(b > 0 and c - d*a/b > 0, "elimination sign")
    cap = (upper - d*lower/b) / (c - d*a/b)
    # A positive control for the looser pair-sum relaxation at 9 and 13.
    x, y = F(1,10), F(9,10)
    for t in (9, 13):
        (a0,b0,l0), (a1,b1,u1) = kept[t]
        require(a0*x+b0*y >= l0 and a1*x+b1*y <= u1, "pair-sum witness")
    p9 = F(41,64)
    required = original[9][1][0]*floor/(original[9][0][1]*p9)
    require(required > cap, "single-site contradiction")
    print(json.dumps(dict(ideal_pair_to_target=ratios, experiment_bands_5_7_9=original,
                          round_11_and_13_constraints=[kept[11][0],kept[13][1]],
                          separation_margins=margins, round_9_gram_numerators=gram,
                          round_9_probability_lower_bound=floor,
                          required_g7_over_g5_strict_lower=required,
                          allowed_g7_over_g5_upper=cap, bound_gap=required-cap,
                          pair_only_witness_9_13=[x,y]), indent=2, default=str))


if __name__ == "__main__":
    main()
