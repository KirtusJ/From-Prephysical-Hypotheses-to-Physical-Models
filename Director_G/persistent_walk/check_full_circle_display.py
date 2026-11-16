"""Check a coherent preparation and a static readout against both versions of Fig. 7(c)."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from runpy import run_path
import json

import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
journal = run_path(str(HERE / 'check_journal_circle_order.py'))
response = run_path(str(HERE / 'check_circle_response_curve.py'))
figure, require = journal['figure'], journal['require']
# Upper off-diagonal u+iv, with common divisor 1024 on the entire matrix.
EFFECTS = ((98,27,34,-35), (480,229,-87,140), (25,58,24,-27), (692,33,-147,11),
           (84,84,-40,-72), (206,211,206,20), (96,42,-33,-13), (11,442,-26,-58),
           (52,38,-12,41), (485,9,-56,12))
BLOCH = (F(1,2), -F(1,2), F(1,4))
DISTINCT = (3,6,8,10,12,16,18)


def intensities(bloch):
    x,y,z = bloch
    require(x*x+y*y+z*z <= 1, 'launch outside Bloch ball')
    for p,s,u,v in EFFECTS:
        require(p > 0 and s > 0 and p+s <= 1024 and p*s > u*u+v*v, 'invalid site effect')
    walk = figure['walk']
    cols = [walk['launch'](10,rail) for rail in range(2)]
    values = {}
    for t in range(20):
        for m,(p,s,u,v) in enumerate(EFFECTS):
            ((a,ai),(cr,c)), ((br,b),(d,di)) = [col[(m-2) % 10] for col in cols]
            require((ai,cr,br,di) == (0,0,0,0), 'rail phase convention')
            h = p*(a*a*(1+z)+b*b*(1-z)-2*a*b*y)
            k = s*(c*c*(1+z)+d*d*(1-z)+2*c*d*y)
            re = 2*u*(a*d+b*c)*x
            im = -2*v*(a*c*(1+z)-b*d*(1-z)+(a*d-b*c)*y)
            values[t,m] = (h+k+re+im)/(1024*2**(t+1))
        cols = [walk['step'](col,'Hprime') for col in cols]
    return values


def read_bands(pdf, png):
    for path, digest in ((pdf,figure['PDF_SHA']), (png,figure['PNG_SHA'])):
        require(sha256(path.read_bytes()).hexdigest() == digest, 'different figure source')
    with fitz.open(pdf) as doc:
        ink = journal['legend'](doc[7])
        colors = journal['panel_colors'](doc,doc[7])['experiment']
    pdf_bands = {key:ink(color,4) for key,color in colors.items()}
    with Image.open(png) as image:
        rgb = figure['legend_reader'](image)
        both = {}
        for (t,m),(lo,hi) in pdf_bands.items():
            left,right = rgb(figure['cell'](image,'experiment',t,m),9)
            both[t,m] = max(left,lo),min(right,hi)
            require(both[t,m][0] <= both[t,m][1], 'disjoint rendering bands')
    return pdf_bands,both


def scale_bounds(first, second, latent, boxes):
    # If scales coincide, all these lower and upper bounds apply to N_first/N_second.
    lows, highs = [], []
    for m,n in product(range(10),repeat=2):
        x,z = latent[first,m],latent[second,n]
        if min(x,z) <= 0:
            continue
        lo,hi = boxes[first,m]
        other_lo,other_hi = boxes[second,n]
        if x <= z and other_hi > 0:
            lows.append((lo/other_hi,m,n))
        if x >= z and other_lo > 0:
            highs.append((hi/other_lo,m,n))
    return max(lows,default=None),min(highs,default=None)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('journal_pdf',type=Path)
    parser.add_argument('figure_png',type=Path)
    args = parser.parse_args()
    journal_bands,both = read_bands(args.journal_pdf,args.figure_png)
    latent = intensities(BLOCH)
    require(sum(q*q for q in BLOCH) == F(9,16), 'launch radius')
    margin = F(1,2048)
    inner = {key:(lo+margin,hi-margin) if latent[key]>0 else (lo,hi)
             for key,(lo,hi) in both.items()}
    knots,totals = response['fixed_curve'](latent,inner)
    require(knots == 90 and len(totals) == 19 and min(totals) == F(1157,2048)
            and max(totals) == F(1005,1024), 'interior band construction')
    # At t=0 only site 2 has input. Reuse its t=1 target coordinates from
    # the first positive site, with the displayed output now normalized to 1.
    first = response['round_points'](1,latent,inner)
    ref = next(m for m in range(10) if first[m][0]>0)
    input_ratio = latent[1,ref]/latent[0,2]
    output_ratio = 1/first[ref][1]
    for m in range(10):
        target = ref if m == 2 else 0
        require(input_ratio*latent[0,m] == first[target][0], 'round-zero input')
        q = output_ratio*first[target][1]
        require(q == int(m==2) and both[0,m][0] <= q <= both[0,m][1], 'round-zero display')

    # Removing the launch polarization cannot rescue the four directed differences.
    equal = intensities((F(0),F(0),F(0)))
    gaps = [equal[t,hi]-equal[t,lo] for t,lo,hi,_ in journal['ORDERS']]
    signed_sum = sum(gap*order[3] for gap,order in zip(gaps,journal['ORDERS']))
    require(min(gaps) < 0 and signed_sum == 0,
            'equal-launch order control')
    first_lower,first_upper = scale_bounds(1,6,latent,journal_bands)
    require(first_lower is None and first_upper is not None, 'one-sided scale control')
    tests = {}
    for t,h in combinations(DISTINCT,2):
        low,high = scale_bounds(t,h,latent,journal_bands)
        require(low is not None and high is not None and low[0] > high[0],
                'equal input scale survives this pairwise bound')
        tests[f'{t},{h}'] = dict(lower=str(low[0]),lower_sites=low[1:],
                                  upper=str(high[0]),upper_sites=high[1:])
    positive = sum(x>0 for (t,_),x in latent.items() if t>0)
    require(positive == 89, 'post-launch support')
    print(json.dumps(dict(renderings=2,display_cells=len(both),postlaunch_positive_cells=positive,
                          common_curve_knots=knots,launch_radius='3/4',launch_purity='25/32',
                          postlaunch_positive_cell_interior_margin=str(margin),
                          postlaunch_total_range=list(map(str,(min(totals),max(totals)))),
                          round_zero_relative_input_and_output=list(map(str,(input_ratio,output_ratio))),
                          equal_launch_signed_gaps=list(map(str,gaps)),
                          rounds_1_and_6_upper_only=str(first_upper[0]),distinct_scale_pairs=tests),indent=2))


if __name__ == '__main__':
    main()
