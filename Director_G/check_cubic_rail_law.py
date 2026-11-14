"""Audit the cubic switched-walk reference points and positive-mixture comparisons."""
import argparse
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
import json
from math import gcd
from pathlib import Path


POLE = (Q(0), Q(0), Q(1))
WORDS = ("", "1010", "101001", "10100101")


def check(test, message):
    if not test:
        raise ValueError(message)


def state(bits, start=POLE):
    x, y, z = start
    for bit in bits:
        x, y, z = z, -y, x
        if bit == "1":
            x, y = (-x-3*y)/2, (x-y)/2
        check(x*x+3*y*y+z*z == 1, "norm")
    return (x, y, z)


def coefficients(point):
    x,y,z = point
    return ((1+2*z)/3, (2-2*z+12*y)/9, (2-2*z-6*x-6*y)/9, (2-2*z+6*x-6*y)/9)


def law(z, kind):
    if kind == "quadratic":
        return (1+z)/2 + (1-z*z)/8
    return (1+z**(3 if kind=="cubic" else 1))/2


def audit_word(word, ref):
    clock = max(8,len(word))
    padded = word+"0"*(clock-len(word))
    s = state(padded)
    check(s==state(word), "idle")
    residues=[v.numerator*pow(v.denominator,-1,3)%3 for v in (s[0],s[2])]
    check(residues==[0,1],"even native R admissibility")
    lams = coefficients(s)
    check(sum(lams)==1 and all(sum(w*p[k] for w,p in zip(lams,ref))==s[k] for k in range(3)), "barycenter")
    scale = 9*2**len(word)
    signed = [int(w*scale) for w in lams]
    check(all(Q(n,scale)==w for n,w in zip(signed,lams)), "rational denominator")
    left = [scale]+[max(0,-n) for n in signed]
    right = [0]+[max(0,n) for n in signed]
    unit = gcd(*(left+right))
    left, right = [n//unit for n in left], [n//unit for n in right]
    check(sum(left)==sum(right), "allocation")
    rates={}
    for name in ("ordinary","quadratic","cubic"):
        values=[law(p[2],name) for p in [s,*ref]]
        one,two=[sum(n*f for n,f in zip(c,values))/sum(c) for c in (left,right)]
        rates[name]=[one,two,one-two]
    check(rates["ordinary"][2]==0, "affine rule")
    return dict(word=word, clock=clock, s=s, coefficients=lams, first=left, second=right, means=rates)


def equal_pair_panels(rows):
    """Keep each inequivalent equal-midpoint collision, including null contrasts."""
    examples = {}
    for row in rows:
        examples.setdefault(tuple(row["s"]), row["word"])
    midpoints = {}
    for first, second in combinations_with_replacement(examples, 2):
        midpoint = tuple((x + y) / 2 for x, y in zip(first, second))
        pair = [examples[first], examples[second]]
        means = {kind: (law(first[2], kind) + law(second[2], kind)) / 2
                 for kind in ("ordinary", "quadratic", "cubic")}
        midpoints.setdefault(midpoint, []).append(dict(words=pair, means=means))
    collisions = []
    for midpoint, pairs in midpoints.items():
        for left, right in combinations(pairs, 2):
            check(left["means"]["ordinary"] == right["means"]["ordinary"], "affine midpoint")
            collisions.append(dict(midpoint=midpoint, left=left, right=right))
    return dict(states=len(examples), pairs=sum(map(len, midpoints.values())), collisions=collisions)


def subset_maxima():
    # A gradient stored as coefficients of X,Y,Z has Euclidean norm squared
    # gx^2 + gy^2/3 + gz^2 since the physical y equals sqrt(3) Y.
    coeffs = [(Q(1,3),0,0,Q(2,3)),(Q(2,9),0,Q(4,3),-Q(2,9)),
              (Q(2,9),-Q(2,3),-Q(2,3),-Q(2,9)),(Q(2,9),Q(2,3),-Q(2,3),-Q(2,9))]
    rows=[]
    for size in range(5):
        for subset in combinations(range(4),size):
            c,x,y,z=[sum((coeffs[i][k] for i in subset),Q(0)) for k in range(4)]
            sq=x*x+y*y/3+z*z
            # sqrt(sq)-c <= (sqrt(52)-2)/9; both sides after
            # adding c and multiplying by 9 have nonnegative right side.
            shift=9*c-2
            if shift < 0:
                check(sq==0 and c==0, "empty subset")
            else:
                diff=81*sq-52-shift**2
                check(diff<=0 or diff**2<=4*shift**2*52, "uniform coefficient bound")
            rows.append(dict(subset=subset, intercept=c, gradient_squared=sq))
    check(rows[2]["gradient_squared"]==Q(52,81) and rows[2]["intercept"]==Q(2,9), "bottom singleton")
    return rows


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("output",type=Path)
    target=ap.parse_args().output/"cubic_rail_law.json"
    ref=[state(w+"0"*(8-len(w))) for w in WORDS]
    check(ref==[POLE,(0,Q(1,2),-Q(1,2)),(-Q(3,4),-Q(1,4),-Q(1,2)),(Q(3,4),-Q(1,4),-Q(1,2))],"named references")
    checked={}
    for size in range(0,9,2):
        words=["".join(bits) for bits in product("01",repeat=size)]
        checked[size]=[audit_word(w,ref) for w in words]
    example=next(row for row in checked[4] if row["word"]=="1110")
    check(example["s"]==(Q(3,4),Q(1,8),Q(5,8)) and example["first"]==[4,0,0,2,0]
          and example["second"]==[0,3,1,0,2], "six-slot schedule")
    check(example["means"]["quadratic"][2]==Q(9,256) and example["means"]["cubic"][2]!=0,"nonlinear controls")
    # Retain all computed exceptional and small contrasts, grouping repeated identical kinematic endpoints.
    points={}
    for group in checked.values():
        for row in group:
            point=tuple(row["s"])
            if point not in points:
                points[point]=dict(first_word=row,words=[])
            points[point]["words"].append(row["word"])
    neg=tuple(-v for v in POLE)
    l=coefficients(neg)
    check(l==(-Q(1,3),Q(4,9),Q(4,9),Q(4,9)),"separate sharp L source")
    record=dict(reference_words=WORDS, reference_states=ref, launch_L_coefficients=l, example=example,
                checked_by_length={k:len(g) for k,g in checked.items()},repeated_points=list(points.values()),
                subset_constants=subset_maxima())
    panels = {size: equal_pair_panels(rows) for size, rows in checked.items() if size <= 6}
    for size in (0, 2, 4):
        for row in panels[size]["collisions"]:
            check(row["left"]["means"]["quadratic"] == row["right"]["means"]["quadratic"],
                  "earlier separating midpoint")
    six = panels[6]["collisions"]
    witness = next(row for row in six if row["left"]["words"] == ["000000", "001011"]
                   and row["right"]["words"] == ["001111", "101111"])
    check(witness["midpoint"] == (Q(-3,8), Q(-1,8), Q(1,4)), "six-tick midpoint")
    check(witness["left"]["means"] == dict(ordinary=Q(5,8), quadratic=Q(43,64), cubic=Q(23,32))
          and witness["right"]["means"] == dict(ordinary=Q(5,8), quadratic=Q(371,512), cubic=Q(287,512)),
          "two-slot predictions")
    record["equal_pair_panels"] = panels
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("x",encoding="utf8",newline="\n") as stream:
        json.dump(record,stream,default=str,indent=2)
        stream.write("\n")


if __name__=="__main__":
    main()
