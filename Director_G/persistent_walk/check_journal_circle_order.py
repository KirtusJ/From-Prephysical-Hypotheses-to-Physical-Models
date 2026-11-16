"""Read the journal's native CMYK scale and check four optical-circle site orders."""
from argparse import ArgumentParser
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from runpy import run_path
import json
import re

import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
counts = run_path(str(HERE / 'check_circle_count_design.py'))
even, figure, require = counts['even'], counts['figure'], counts['require']
# Each comparison lists round, dimmer site, brighter site and integer multiplier.
ORDERS = ((2, 0, 4, 1545), (6, 0, 4, 1648), (8, 4, 0, 7444), (14, 0, 4, 1280))


def legend(page):
    # Native DeviceCMYK nonstroking color followed by a filled horizontal strip.
    pattern = (rb'^([.\d]+) ([.\d]+) ([.\d]+) ([.\d]+) k\n'
               rb'262\.908 ([.\d]+) 7 ([.\d]+) re\nf$')
    strips = []
    start, span = F('270.306'), F('174.993')
    for row in re.findall(pattern, page.read_contents(), re.M):
        cyan, magenta, yellow, black, y, h = (F(v.decode('ascii')) for v in row)
        if not (start <= y < start+span and 0 < h < 6):
            continue
        ends = [(edge-start)*256/span for edge in (y,y+h)]
        require(all(abs(v-round(v)) < F(1,300) for v in ends), 'strip outside uniform grid')
        lo, hi = (round(v) for v in ends)
        require(hi > lo and lo == (strips[-1][2] if strips else 0), 'noncontiguous color scale')
        strips.append(((cyan, magenta, yellow, black), lo, hi))
    require(len(strips) == 249 and strips[-1][2] == 256, 'incomplete vector legend')

    @lru_cache(None)
    def band(color, slack, metric=max):
        errors = [metric(abs(byte-255*c) for byte,c in zip(color, ink)) for ink,_,_ in strips]
        cap = min(errors)+slack
        chosen = [(lo,hi) for error,(_,lo,hi) in zip(errors,strips) if error <= cap]
        return F(min(lo for lo,_ in chosen),256), F(max(hi for _,hi in chosen),256)
    return band


def panel_colors(doc, page):
    found = sorted({(item['bbox'][0],item['xref']) for item in page.get_image_info(xrefs=True)
                    if 364 < item['bbox'][1] < 365 and 539 < item['bbox'][3] < 541})
    require(len(found) == 2, 'missing panel')
    panels = {}
    for name,(_,xref) in zip(('numeric','experiment'), found):
        require(all(doc.xref_get_key(xref,key)[1] == value for key,value in
                    [('Width','308'),('Height','614'),('BitsPerComponent','8')]), 'indexed panel layout')
        ref = doc.xref_get_key(xref,'ColorSpace')
        require(ref[0] == 'xref', 'unknown panel color space')
        space = doc.xref_object(int(ref[1].split()[0]))
        match = re.fullmatch(r'\[ /Indexed /DeviceCMYK (\d+) (\d+) 0 R \]', space)
        require(match is not None, 'expected an indexed CMYK palette')
        palette = doc.xref_stream(int(match[2]))
        raw = doc.xref_stream(xref)
        require(len(palette) == 4*(int(match[1])+1) and len(raw) == 308*614, 'wrong palette or image size')
        colors = {}
        for t in range(20):
            for m in range(10):
                x, y = (2*m+1)*308//20, (2*t+1)*614//40
                indices = {raw[(y+dy)*308+x+dx] for dx in (-3,0,3) for dy in (-3,0,3)}
                require(len(indices) == 1, 'cell center crosses a palette boundary')
                index = indices.pop()
                colors[t,m] = tuple(palette[4*index:4*index+4])
        panels[name] = colors
    return panels


def propagate():
    walk = figure['walk']
    cols = [walk['launch'](10,j) for j in (0,1)]
    mass, quadratic, pure = {}, {}, {}
    for t in range(20):
        for m in range(10):
            ((a, ai),(cr, c)), ((br, b),(d, di)) = [col[(m-2)%10] for col in cols]
            require((ai,cr,br,di) == (0,0,0,0), 'unexpected transfer phase')
            quadratic[t,m] = tuple(F(k,2**(t+1)) for k in
                                   (a*a+b*b, c*c+d*d, -2*(a*c-b*d)))
            mass[t,m] = sum(quadratic[t,m][:2])
            if m in (0,4):
                p,s = (1,3) if m == 0 else (5,2)
                pure[t,m] = F(p*b*b+s*d*d,2**t)
        cols = [walk['step'](col,'Hprime') for col in cols]
    for m in (0,4):
        sums = [sum(w*(int(m == hi)-int(m == lo))*quadratic[t,m][j]
                    for t,lo,hi,w in ORDERS) for j in range(3)]
        require(sums == [0,0,0], 'signed order identity')
    return mass, pure


def gaps(bands):
    return [bands[t,hi][0]-bands[t,lo][1] for t,lo,hi,_ in ORDERS]


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('journal_pdf',type=Path)
    parser.add_argument('figure_png',type=Path)
    args = parser.parse_args()
    require(sha256(args.journal_pdf.read_bytes()).hexdigest() == figure['PDF_SHA'], 'different journal bytes')
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure['PNG_SHA'], 'different PNG bytes')
    with fitz.open(args.journal_pdf) as doc:
        page = doc[7]
        band = legend(page)
        colors = panel_colors(doc,page)
    def read(panel, slack, metric=max):
        return {k:band(col,slack,metric) for k,col in colors[panel].items()}
    mass, pure = propagate()
    hits = []
    for slack in range(5):
        numeric = read('numeric',slack)
        hits.append([sum(numeric[t,m][0] <= value <= numeric[t,m][1]
                         for (t,m),value in mass.items() if (t-m)%2 == parity) for parity in (0,1)])
    require(hits[-1] == [100,100] and all(sum(pair)<200 for pair in hits[:-1]), 'numeric-panel control')
    # Choose the L1 allowance by exactly the same numerical-panel control.
    l1_coverage = []
    for slack in range(6):
        numeric = read('numeric',slack,sum)
        l1_coverage.append(sum(numeric[k][0] <= value <= numeric[k][1] for k,value in mass.items()))
    l1_gaps = gaps(read('experiment',5,sum))
    require(l1_coverage[-1] == 200 and max(l1_coverage[:-1]) < 200 and min(l1_gaps) > 0,
            'alternate color metric')
    pdf_gaps = {s:gaps(read('experiment',s)) for s in (4,5,6,7,8)}
    require(min(pdf_gaps[4]) > 0 and min(pdf_gaps[5]) > 0, 'four strict journal orders')
    for s in (6,7):
        require(min(pdf_gaps[s]) == 0 and max(pdf_gaps[s]) > 0, 'weak order sensitivity')
    require(min(pdf_gaps[8]) < 0, 'wider bands retain all four orders')
    with Image.open(args.figure_png) as image:
        rgb = figure['legend_reader'](image)
        png_gaps = gaps({(t,m):rgb(figure['cell'](image,'experiment',t,m),9)
                         for t,_,_,_ in ORDERS for m in (0,4)})
    require(png_gaps[2] < 0 and min(png_gaps[:2]+png_gaps[3:]) > 0, 'PNG round-eight control')
    alternative = [pure[t,hi]-pure[t,lo] for t,lo,hi,_ in ORDERS]
    require(min(alternative) > 0, 'polarized launch control')
    exp = read('experiment',4)
    caps = even['round_caps'](exp)
    require(max(caps)<0, 'linear score control')
    plan = counts['plan'](exp,counts['SCORES'],counts['DIVISORS'])
    print(json.dumps(dict(numeric_panel_hits=hits,sum_metric_control_hits=l1_coverage,
                          sum_metric_order_gaps_at_5=list(map(str,l1_gaps)),journal_order_gaps={
        s:list(map(str,v)) for s,v in pdf_gaps.items()},png_order_gaps_at_9=list(map(str,png_gaps)),
        polarized_launch_differences=list(map(str,alternative)),linear_score_caps=list(map(str,caps)),
        conditional_count_budget=sum(row['count_budget'] for row in plan)),indent=2))


if __name__ == '__main__':
    main()
