"""Test the edge calibration for distinct fixed R and L detector scores.

Use exact elimination on both signed near-front strips with and without a
final output swap. Preserve columns beyond the reported magnitude cutoff.
Separately sum every actual port for the square and an edge-blind perturbation.
Run python -B check_separate_rail_scores.py NEW_DIRECTORY.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json

from check_parity_direction import tick


def require(test, reason):
    if not test:
        raise ValueError(reason)


def balance(pair, swapped):
    u,v = pair
    a,b = (u-v,u+v) if swapped else (u+v,u-v)
    row = Counter()
    for key,value in [((0,a),1),((1,b),1),((0,u),-2),((1,v),-2)]:
        if key[1]:
            row[key] += value
    return {k:v for k,v in row.items() if v}


def row_basis(rows):
    basis = {}
    for source in rows:
        vector = {k:F(v) for k,v in source.items()}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                basis[pivot] = {k:v/value for k,v in vector.items()}
                break
            for k,coefficient in basis[pivot].items():
                new = vector.get(k,0)-value*coefficient
                if new:
                    vector[k] = new
                else:
                    vector.pop(k,None)
    return basis


def rank(rows):
    return len(row_basis(rows))


def perturb(rail,k):
    return k*k+int((rail,k) in {(0,-3),(1,-2)})


def run():
    bound = 33
    fields = [{(0,0):1}]
    for _ in range(bound+5):
        fields.append(tick(fields[-1]))
    def rails(t,x):
        return tuple(fields[t].get((x,c),0) for c in (0,1))
    units = [rails(t,x) for t,x in ((0,0),(1,-1),(2,-2),(3,-1))]
    require(units == [(1,0),(0,1),(0,-1),(-1,0)],"native signed units")
    original = [balance(p,False) for p in units]
    paired = list(original)
    even = []
    conditions = []
    for n in range(1,bound+2):
        right,left = rails(n+1,n-1),rails(n+3,-n-1)
        require(right==(n,1) and left==((-1)**(n+1),(-1)**n*n),"signed edge strips")
        conditions.append(dict(n=n,right=right,left=left))
        for pair in (right,left):
            normal,crossed = (balance(pair,sw) for sw in (False,True))
            original.append(normal)
            paired.extend((normal,crossed))
    for row in original:
        require(sum(c*perturb(*key) for key,c in row.items())==0,"unswitched raw strips")
    for row in paired:
        require(sum(c*k*k for (_,k),c in row.items())==0,"square in signed kernel")
    for row in original:
        merged = Counter()
        for (rail,k),coefficient in row.items():
            merged[rail,abs(k)] += coefficient
        even.append({key:c for key,c in merged.items() if c})
    dimensions = {}
    for name,rows,count in (("bare_signed",original,4*bound),("crossed_signed",paired,4*bound),
                            ("bare_even",even,2*bound)):
        nuisance = [{key:c for key,c in row.items() if abs(key[1])>bound} for row in rows]
        dimensions[name] = count-rank(rows)+rank(nuisance)
    require(dimensions==dict(bare_signed=65,crossed_signed=1,bare_even=1),"projected dimensions")
    panels = []
    for t,field in enumerate(fields):
        square = sum(k*k for k in field.values())
        changed = sum(perturb(c,k) for (_,c),k in field.items())
        require(square==2**t,"complete panel norm")
        panels.append(dict(t=t,square=square,perturbed=changed))
    first = next(p for p in panels if p["square"]!=p["perturbed"])
    require(first==dict(t=5,square=32,perturbed=33),"first normalized countercheck")
    # Each row fixes the total of a full panel relative to the sharp R score.
    total_rows = []
    for t,field in enumerate(fields[:21]):
        row = Counter((c,k) for (_,c),k in field.items() if k)
        row[0,1] -= 2**t
        total_rows.append({key:c for key,c in row.items() if c})
    with_totals = original+total_rows
    dimensions["bare_signed_with_20_panel_ticks"] = 4*bound-rank(with_totals)+rank(
        [{key:c for key,c in row.items() if abs(key[1])>bound} for row in with_totals])
    require(dimensions["bare_signed_with_20_panel_ticks"]==57,"panel-constrained dimension")
    # Include every interior parent with the assumed common per-rail shape.
    target = {(c,k) for field in fields[:13] for (_,c),k in field.items() if k}
    all_rows = []
    interior = []
    for t,field in enumerate(fields[:32]):
        all_rows.extend(balance(tuple(field.get((x,c),0) for c in (0,1)),False)
                        for x in range(-t,t+1,2))
        if t+1 in (14,18,24,32):
            outside = [{key:c for key,c in row.items() if key not in target} for row in all_rows]
            dim = len(target)-rank(all_rows)+rank(outside)
            interior.append([t+1,dim])
    require(len(target)==49 and interior==[[14,2],[18,1],[24,1],[32,1]],
            "all visited early scores from native interior")
    return dict(target_cutoff=bound,signed_units=units,edge_inputs=conditions,
                projected_dimensions=dimensions,all_port_normalizers=panels,
                early_score_labels=sorted(target),all_native_constraints=interior)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    dest=parser.parse_args().directory
    result=run()
    dest.mkdir(parents=True,exist_ok=True)
    with (dest/"separate_rail_scores.json").open("x",encoding="utf8",newline="\n") as stream:
        json.dump(result,stream,indent=2)
        stream.write("\n")
