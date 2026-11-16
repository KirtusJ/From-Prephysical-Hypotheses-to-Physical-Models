"""Cover all localized launch rail states with exact bounds from the published intensity bands."""
import json
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
from runpy import run_path

from PIL import Image

source = run_path(str(Path(__file__).with_name("check_circle_figure.py")))
walk, require = source["walk"], source["require"]
ROUNDS = (7, 13, 17, 19)
SITES = (1, 3, 5, 7, 9)


def effects():
    right, left = [walk["launch"](10, rail) for rail in (0, 1)]
    phase = walk["launch"](10, 0)
    phase[0] = [(1,0), (0,1)]
    coeff = {}
    for t in range(max(ROUNDS)+1):
        if t in ROUNDS:
            for site in SITES:
                x = (site-2) % 10
                for rail in (0, 1):
                    (a,b), (c,d) = right[x][rail], left[x][rail]
                    require(a*c+b*d == 0, "real coherence affects a single rail")
                    u, v = a*a+b*b, c*c+d*d
                    # The denominator for these three coefficients is 2**(t+1).
                    coeff[t,site,rail] = (u+v, u-v, -2*(a*d-b*c))
                    A, _, C = coeff[t,site,rail]
                    require(F(A+C, 2**(t+1)) == walk["probability"](phase[x][rail],t)/2,
                            "complex launch sign and scale")
            require(tuple(map(sum,zip(*(v for k,v in coeff.items() if k[0]==t)))) ==
                    (2**(t+1),0,0), "total probability")
        right, left, phase = [walk["step"](s,"Hprime") for s in (right,left,phase)]
    return coeff


def bounds_for_box(coeff, x, y, den):
    # Box [x/den,(x+1)/den] times [y/den,(y+1)/den].
    out = {}
    for key, (a,b,c) in coeff.items():
        corner = a*den + b*x + c*y
        lo = max(0, corner + min(0,b) + min(0,c))
        hi = corner + max(0,b) + max(0,c)
        # Boxes entirely away from the disk are removed by the caller. All
        # interval endpoints here have the common factor 1/(den*2**(t+1)).
        require(hi >= lo, "negative rail enclosure")
        out[key] = lo, hi
    return out


def upper_scale(bands, bounds, s, t):
    best = None
    for m in SITES:
        qmin, qmax = bands[s,m][0], bands[t,m][1]
        if qmin <= 0:
            continue
        ratios = []
        for rail in (0,1):
            first = bounds[s,m,rail][1]
            last = bounds[t,m,rail][0]
            if first > 0:
                ratios.append(F(last,first))
        if ratios and min(ratios)>0:
            # Suppress 2**(t-s). It cancels in the two-way product.
            val = qmax/qmin/min(ratios)
            if best is None or val < best[0]:
                best = (val,m)
    return best


def cover(coeff, bands, max_den=4096):
    pending = [(x,y,1) for x in (-1,0) for y in (-1,0)]
    counts = Counter()
    pairs = Counter()
    largest = F(0)
    area = F(0)
    while pending:
        x,y,den = pending.pop()
        near_x, near_y = max(0,x,-x-1), max(0,y,-y-1)
        leaf_area = F(1,den*den)
        if near_x**2+near_y**2 > den**2:
            counts["outside"] += 1
            area += leaf_area
            continue
        bounds = bounds_for_box(coeff,x,y,den)
        for s,t in combinations(ROUNDS,2):
            fwd, rev = upper_scale(bands,bounds,s,t), upper_scale(bands,bounds,t,s)
            if fwd and rev and fwd[0]*rev[0]<1:
                largest = max(largest,fwd[0]*rev[0])
                pairs[s,t,fwd[1],rev[1]] += 1
                counts["excluded"] += 1
                counts["finest_denominator"] = max(counts["finest_denominator"],den)
                area += leaf_area
                break
        else:
            if den >= max_den:
                return {"first_unresolved_box": [x, y, den]}
            pending.extend((2*x+i,2*y+j,2*den) for i in (0,1) for j in (0,1))
    require(area==4, "incomplete square cover")
    return dict(counts=counts, area=str(area), largest_used_product=str(largest),
                certificates={",".join(map(str,k)):v for k,v in sorted(pairs.items())})


def check_three_round_controls(coeff, bands):
    # z, y and their denominator; R,L gains by site; reciprocal round scales.
    cases = [
        (-7, 3, 8, [(126388,300),(300,300),(118015,15763),(300,10929),(25456,1781)],
         {7:10000, 13:13981, 19:22227}),
        (3, 2, 4, [(300,27795),(8165,300),(4837,12926),(7833,300),(300,28774)],
         {7:10000, 17:7430, 19:12694}),
        (0, 1, 1, [(19696,300),(9888,300),(3734,54741),(300,300),(4684,12915)],
         {13:10000, 17:9656, 19:33535})]
    results = []
    for z,y,d,gains,round_scales in cases:
        require(z*z + y*y <= d*d and min(min(g) for g in gains)>0, "physical control state")
        totals = {}
        for t,divisor in round_scales.items():
            total = F(0)
            for m,g in zip(SITES,gains):
                intensity = F(0)
                for rail in (0,1):
                    a,b,c = coeff[t,m,rail]
                    intensity += F((a*d+b*z+c*y)*g[rail], d*2**(t+1)*divisor)
                lo,hi = bands[t,m]
                require(lo<=intensity<=hi, "three-round witness")
                total += intensity
            require(total<=1, "witness exceeds available intensity")
            totals[t] = str(total)
        results.append(dict(launch_z_y=[str(F(z,d)),str(F(y,d))], gains_R_L=gains,
                            inverse_scales=round_scales, total_on_circle=totals))
    return results


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("figure_png",type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest()==source["PNG_SHA"],"source bytes")
    coeff = effects()
    with Image.open(args.figure_png) as image:
        read = source["legend_reader"](image)
        colors = {(t,m):source["cell"](image,"experiment",t,m) for t in ROUNDS for m in SITES}
        numeric = {(t,m):read(source["cell"](image,"numeric",t,m),8) for t in ROUNDS for m in SITES}
        covers = {}
        for slack in (8, 12):
            bands = {cell:read(rgb,slack) for cell,rgb in colors.items()}
            covers[slack] = cover(coeff,bands)
            require("counts" in covers[slack], f"incomplete cover at tolerance {slack}")
            if slack==8:
                controls = check_three_round_controls(coeff,bands)
        wider_bands = {cell: read(rgb, 16) for cell, rgb in colors.items()}
        wider_cutoff = cover(coeff, wider_bands, max_den=64)
        require("first_unresolved_box" in wider_cutoff, "higher-tolerance cutoff changed")
    for (t,m),(lo,hi) in numeric.items():
        p = sum(F(coeff[t,m,r][0],2**(t+1)) for r in (0,1))
        require(lo<=p<=hi, "numeric-panel common-state positive control")
    print(json.dumps(dict(rounds=ROUNDS, sites=SITES, numeric_equal_mixture_matches_at_eight=len(numeric),
                          experimental_covers=covers, tolerance_16_at_width_1_over_64=wider_cutoff,
                          three_round_controls_at_eight=controls),
                     indent=2))


if __name__ == "__main__":
    main()
