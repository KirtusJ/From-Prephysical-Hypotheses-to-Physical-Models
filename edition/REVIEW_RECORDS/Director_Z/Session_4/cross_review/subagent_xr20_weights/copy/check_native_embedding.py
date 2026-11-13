"""Audit the native five-sheet instrument with integer counts and exact field arithmetic."""

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from math import isqrt
from pathlib import Path

from check_probability_selection import (
    ONE, ZERO, conjugate_by, norm_square, plus, reduce_terms, scale, times,
)


def shifted(sheet, places):
    return tuple(sheet[(y - places) % len(sheet)] for y in range(len(sheet)))


def combine(a, b, sign=1):
    return tuple(x + sign*y for x, y in zip(a, b))


def mass(sheet):
    return sum(c*c for c in sheet)


def field_norm(counts, character=1):
    return norm_square(reduce_terms((character*y, c) for y, c in enumerate(counts)))


def propagate(state, steps):
    for _ in range(steps):
        output = defaultdict(lambda: (0,)*5)
        for (x, coin), vector in state.items():
            v = shifted(vector, x)
            for d in (1, -1):
                key = (x+d, d)
                output[key] = combine(output[key], v, -1 if d == coin == -1 else 1)
        state = output
    return state


def adaptive_tree(writer):
    """Keep all leaves, including zero-probability sheet outcomes."""
    leaf_count, zeros = 0, 0
    total = Fraction()
    errors = []

    def visit(state, depth, steps, transcript):
        nonlocal total, leaf_count, zeros
        (site, coin), = state.keys()
        block = (3, 2 if site > 0 else 3, 2 if coin == 1 else 1)[depth]
        new_steps = steps+block
        for (x, d), v in sorted(propagate(state, block).items()):
            resolve_sheet = depth == 2 or (depth == 1 and d == -1)
            for mask in (range(5) if resolve_sheet else (None,)):
                observed = v if mask is None else tuple(c if y == mask else 0 for y,c in enumerate(v))
                path = transcript + [f"{x},{d},{'*' if mask is None else mask}"]
                weight = mass(observed)
                if depth < 2 and weight:
                    visit({(x,d):observed}, depth+1, new_steps, path)
                    continue
                # Independent readout in all permuted character coordinates (Parseval).
                norms = [field_norm(observed, r) for r in range(5)]
                for u in (1, 2, 3, 4):
                    embedded = ZERO
                    for w in norms:
                        embedded = plus(embedded, conjugate_by(w,u))
                    if embedded != scale(5*weight, ONE):
                        errors.append((path,u,"character readout"))
                if field_norm(observed) != ZERO:
                    product = times(field_norm(observed),field_norm(observed,2))
                    if any(product[1:]) or product[0]<1:
                        errors.append((path,"field norm"))
                writer.writerow(("/".join(path),new_steps,*observed,weight,2**new_steps))
                total += Fraction(weight, 2**new_steps)
                leaf_count += 1
                zeros += int(weight==0)

    visit({(0,1):(1,0,0,0,0)},0,0,[])
    return dict(leaves=leaf_count,zero_leaves=zeros,mass=str(total),errors=errors)


def filter_trials():
    rows=[]
    vector=combine(shifted((1,0,0,0,0),1),shifted((1,0,0,0,0),-1),-1)
    checks=[]
    path_state_out = propagate({(0, 1): (1, 0, 0, 0, 0)}, 3)
    site, coin = -1, -1
    path_state = {(site, coin): path_state_out[site, coin]}
    for s in range(25):
        c=mass(vector)
        norm1,norm2=field_norm(vector),field_norm(vector,2)
        next_c=mass(combine(shifted(vector,1),shifted(vector,-1)))
        pair_sum=plus(norm1,norm2)
        check=dict(zero_constant=sum(vector)==0,field_norm=times(norm1,norm2)==scale(5,ONE),
                   trace=scale(2,pair_sum)==scale(5*c,ONE),
                   next_record=next_c==2*sum(vector[y]**2+vector[y]*vector[(y+2)%5] for y in range(5)))
        # Independent spatial paths for the whole recorded word, with the
        # displacement at each measured block included in the next sheet shift.
        direct=path_state[site,coin]
        check["literal_filter_word"]=any(direct==tuple(sign*x for x in shifted(vector,k))
                                           for k in range(5) for sign in (1,-1))
        successors=propagate(path_state,3)
        site+=coin
        next_direct=successors[site,coin]
        check["literal_next_record"]=mass(next_direct)==next_c
        path_state={(site,coin):next_direct}
        # If norm1=a and norm2=b, 4ab/(a+b)^2 = 4 e(1-e).
        checks.append(all(check.values()))
        rows.append(dict(constructive_after_destructive=s, canonical_counts=vector,actual_sheet_counts=direct,C=c,
                         norm_one=norm1,norm_two=norm2,field_norm=5,
                         next_constructive=str(Fraction(next_c,8*c)),
                         sheet_probabilities=[str(Fraction(j*j,c)) for j in direct],
                         checks=check,
                         leakage_times_one_minus_leakage=str(Fraction(4,5*c*c)),
                         branch_probability=str(Fraction(c,8**(s+1)))))
        vector=combine(shifted(vector,1),shifted(vector,-1))
    return rows,all(checks)


def infinite_coin_controls(bits):
    # Exactly floor(2^n (3+sqrt(5))/16), using integer square roots.
    rows=[]
    for n in range(1,bits+1):
        scale_factor=2**n
        lower=(3*scale_factor + isqrt(5*scale_factor**2))//16
        # Among the size-2^-n cells, all but one can decide U<alpha.
        rows.append(dict(bits=n,accept_cells=lower,reject_cells=scale_factor-lower-1,
                         undecided_cells=1,cell_denominator=scale_factor))
    return rows


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    with (out/"native_record_tree.csv").open("w",newline="",encoding="utf8") as f:
        writer=csv.writer(f)
        writer.writerow(("records_x_direction_sheet","total_steps","m0","m1","m2","m3","m4",
                         "probability_numerator","probability_denominator"))
        tree=adaptive_tree(writer)
    filters,filter_ok=filter_trials()
    coins=infinite_coin_controls(48)
    for row in coins:
        n,k=row["bits"],row["accept_cells"]
        den=2**n
        left,right=16*k-3*den,16*(k+1)-3*den
        row["bracket_exact"]=(left<0 or left**2<5*den**2) and right>0 and right**2>5*den**2
    checks=dict(tree_total=tree["mass"]=="1",tree_field_laws=not tree["errors"],
                zero_controls=tree["zero_leaves"]>0,filter_exact=filter_ok,
                named_sheet_profile=all(b["canonical_counts"][1:3] ==
                    (a["canonical_counts"][2],a["canonical_counts"][1]-a["canonical_counts"][2])
                    for a,b in zip(filters,filters[1:])),
                ordered_limit=filters[0]["C"]==filters[1]["C"]==2 and
                    all(c["C"]==3*b["C"]-a["C"] for a,b,c in zip(filters,filters[1:],filters[2:])),
                infinite_threshold=all(d["bracket_exact"] for d in coins) and
                    all(b["accept_cells"] in (2*a["accept_cells"],2*a["accept_cells"]+1)
                        for a,b in zip(coins,coins[1:])))
    report=dict(checks=checks,adaptive_tree=tree,filter=filters,random_threshold=coins)
    (out/"native_embedding.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print(checks,tree)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    main(parser.parse_args().output)
