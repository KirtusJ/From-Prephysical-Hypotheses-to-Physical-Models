"""Enumerate a reciprocal two-sheet cycle in physical and cover coordinates."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import log
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def cover_walk(length, ticks):
    size = 2*length
    right, left, count = ([0]*size for _ in range(3))
    right[0] = count[0] = 1
    for _ in range(ticks):
        right, left = ([right[(j-1)%size] + left[(j-1)%size] for j in range(size)],
                       [right[(j+1)%size] - left[(j+1)%size] for j in range(size)])
        count = [count[(j-1)%size] + count[(j+1)%size] for j in range(size)]
    return [(r,l,n) for r,l,n in zip(right,left,count)]


def seam_words(length, ticks, with_sheet=True):
    amplitudes, counts = Counter(), Counter()
    for word in product((1,-1), repeat=ticks):
        x = sheet = 0
        prev = sign = 1
        for step in word:
            dest = (x+step)%length
            # The swap is its own inverse on the same undirected edge.
            if with_sheet and {x,dest} == {0,length-1}:
                sheet ^= 1
            if step == prev == -1:
                sign = -sign
            x, prev = dest, step
        amplitudes[x,sheet,prev] += sign
        counts[x,sheet] += 1
    return [(amplitudes[x,s,1], amplitudes[x,s,-1], counts[x,s])
            for s in (0,1) for x in range(length)]


def partition_panel(rows):
    support = {j: [v*v for v in row[:2] if v] for j,row in enumerate(rows) if any(row[:2])}
    mixed = [j for j,row in support.items() if len(row)==2]
    a,b,c = 81,225,576
    lam = log(c/b)/log(c/a)
    scores = {11: lam/a, 3: -1/b, 7: (1-lam)/c}
    out = []
    for bits in product((False,True), repeat=len(mixed)):
        split = dict(zip(mixed,bits))
        cells = [(j,m) for j,rail in support.items()
                 for m in (rail if split.get(j,False) else [sum(rail)])]
        maximum = max(m for j,m in cells)
        require([j for j,m in cells if m==maximum] == [5], "maximum changes position")
        sample = []
        for q in (0,.25,.5,.99,1,1.01,2,8,16,64,256):
            w = [(j,(m/maximum)**q) for j,m in cells]
            z = sum(v for _,v in w)
            d = sum(scores.get(j,0)*v for j,v in w)/z
            h = sum(v for j,v in w if j==5)/z
            require(d>0 if q!=1 else abs(d)<1e-16, "Jensen sample")
            require(q!=1 or abs(h-680/2048)<1e-15, "ordinary peak")
            require(q<16 or h>=1/(1+7*(576/676)**16), "large power")
            sample.append([q,d,h])
        out.append(dict(split_coordinates=[j for j in mixed if split[j]],
                        maximum=maximum, samples_q_D_H=sample))
    count_score = sum(scores.get(j,0)*n for j,(_,_,n) in enumerate(rows))/2048
    require(576**2*81 > 225**3 and 463*225 > 3*81*341, "positive count bound")
    return {"lambda":lam,"count_score":count_score,"count_peak":str(Fraction(rows[5][2],2048)),
            "ordinary_peak":str(Fraction(680,2048)), "high_power_peak_lower_at_16":
            1/(1+7*(576/676)**16), "partitions": out}


def analyze():
    rows = cover_walk(6,11)
    require(rows==seam_words(6,11), "physical seam vs cover recurrence")
    require(sum(r*r+l*l for r,l,n in rows)==2**11 and sum(n for r,l,n in rows)==2**11,
            "norm or path count")
    flat = seam_words(6,11,with_sheet=False)
    require(all(row==(0,0,0) for row in flat[6:]) and rows!=flat, "trivial connection")
    prior = []
    for ticks in range(3,12):
        for length in range(3,ticks+1):
            sample = cover_walk(length,ticks)
            masses = sorted({r*r+l*l for r,l,_ in sample if bool(r) != bool(l)})
            prior.append([length,ticks,masses])
    witnesses = [(length,ticks) for length,ticks,masses in prior if len(masses)>=3]
    require(witnesses == [(6,11)], "unexpected wrapped three-mass witnesses")
    dark = cover_walk(4,9)
    require(dark==seam_words(4,9) and dark[1]==(0,0,136), "dark coordinate control")
    return {"sharp_launch":"well 0, sheet 0, R", "physical_site": "j mod L",
            "sheet":"floor(j/L)", "all_cover_rows_R_L_unsigned":rows,
            "trivial_connection_rows":flat, "robustness":partition_panel(rows),
            "other_dark_example_L4_t9":dark, "wrapped_scan_L_t_distinct_pure_masses":prior}


if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("output",type=Path)
    path=ap.parse_args().output
    with path.open("x",encoding="utf8",newline="\n") as out:
        json.dump(analyze(),out,indent=2,allow_nan=False)
        out.write("\n")
