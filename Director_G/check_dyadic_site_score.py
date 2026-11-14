"""Propagate a sharp source, protected labels, localized copy and signed rail routing."""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import json
from itertools import product
from pathlib import Path


def check(condition, description):
    if not condition:
        raise ValueError(description)


def step(v, choose):
    # Every stage has one common denominator for all amplitudes or path weights.
    out = defaultdict(int)
    for (x, rail, label, bit), value in v.items():
        gate = choose(x, label)
        if gate == "H":
            terms = ((0,1),(1,1 if rail == 0 else -1))
        else:
            terms = ((rail ^ (gate == "X"), 1),)
        for c, sign in terms:
            out[x+1-2*c,c,label,bit] += value*sign
    return out


def prefix(depth, k, split):
    # Fresh label bits start at zero. With one occupied input, a balanced split
    # has equal positive numerators on the two labels.
    labels = [0]
    for j in range(depth):
        labels += [a+(1<<j) for a in labels]
    v = {(0,0,a,0):1 for a in labels}
    for tick in range(6):
        # Active labels: R,L,R,L,L,R (or the last two interchanged).
        # Spectators: six right moves. Between adjacent sites rails can be
        # switched or streamed unchanged. Gate schedule depends only on label.
        def choose(x,a):
            if a >= k:
                return "I"
            directions = (0,1,0,1,0,1) if split and a==k-1 else (0,1,0,1,1,0)
            old = directions[tick-1] if tick else 0
            return "X" if directions[tick] != old else "I"
        v = step(v,choose)
    check(all((x,r)==((6,0) if a>=k else (0,int(split and a==k-1)))
              for x,r,a,_ in v), "routing prefix")
    return v


def experiment(depth,k,split,copy):
    v = prefix(depth,k,split)
    # Use fixed common sqrt(2) denominators on both balanced layers. A
    # bypassed deterministic spectator layer contributes sqrt(2), so remove
    # the spectator before the interferometer and restore its two bypasses as 2.
    active = {key:value for key,value in v.items() if key[0]==0}
    spectator = {key:value for key,value in v.items() if key[0]==6}
    active = step(active,lambda x,a:"H")
    active = {(x,r,a,bit ^ int(copy and x==1)):value for (x,r,a,bit),value in active.items()}
    active = step(active,lambda x,a:"X")
    active = step(active,lambda x,a:"H")
    for (x,r,a,bit),value in spectator.items():
        active[x+3,r,a,bit] += 2*value
    masses=defaultdict(int)
    for (x,_,_,_),value in active.items():
        masses[x] += value*value
    n=2**depth
    expected={-1:4*(1 if split else 0), 1:4*(k-int(split)), 9:4*(n-k)}
    if copy:
        expected[-1]=expected[1]=2*k
    check(all(masses[x]==v for x,v in expected.items()) and sum(masses.values())==4*n,
          "forward physical site masses")
    return [Q(masses[x],4*n) for x in (-1,1,9)]


def rate(masses,f,bank):
    weights = [f(x) for x in masses] + [f(Q(0))]*(bank-len(masses))
    return weights[2]/sum(weights)


def fair_counts(n,k):
    counts = defaultdict(int)
    # Enumerate both fair-coin outputs on each active trajectory. Four
    # copies of each coasting label give every label the same exposure.
    for label,arm,exit_rail in product(range(n),(0,1),(0,1)):
        if label<k:
            x = (1-2*arm) + (1-2*(1-arm)) + (1-2*exit_rail)
        else:
            x = 9
        counts[x] += 1
    return [Q(counts[x],4*n) for x in (-1,1,9)]


def main():
    args=argparse.ArgumentParser(description=__doc__)
    args.add_argument("output",type=Path)
    path=args.parse_args().output
    rows=[]
    for depth in range(2,7):
        n=2**depth
        for k in range(2,n):
            panels=[experiment(depth,k,split,copy) for split in (False,True) for copy in (False,True)]
            ordinary=[rate(row,lambda x:x,20) for row in panels]
            affine=[rate(row,lambda x:Q(1,20)+x,20) for row in panels]
            squared=[rate(row,lambda x:x*x,20) for row in panels]
            check(len(set(ordinary))==len(set(affine))==1,"remote invariance")
            check(panels[1]==panels[3] and squared[0]!=squared[1],"nonlinear response and common copy")
            fair=fair_counts(n,k)
            check(fair==panels[1] and fair[0]==Q(k,2*n) and panels[0][0]==0,"fair-count dark read")
            rows.append(dict(labels=n,local=k,site_order=[-1,1,9],site_masses=panels,
                             ordinary_remote=ordinary,affine_remote=affine,squared_remote=squared,
                             fair_counts_all_settings=fair))
    # Linear constraints at N=8. A bump between grid points cannot
    # affect any tested masses, including the half-grid copy outcomes.
    sample={q for row in rows if row["labels"]==8 for panel in row["site_masses"] for q in panel}
    center=Q(21,64)
    width=Q(1,128)
    check(all(abs(x-center)>=width for x in sample) and (center*8).denominator!=1,
          "untested positive interval")
    with path.open("x",encoding="utf8",newline="\n") as out:
        json.dump(dict(rows=rows,fixed_bank=20,nonlinear_bump_center=str(center),
                       bump_half_width=str(width)),out,indent=2,default=str)
        out.write("\n")


if __name__=="__main__":
    main()
