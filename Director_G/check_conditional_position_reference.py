"""Check a test using the new position conditional on each saved science outcome."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

from check_appended_position_read import fold, panel, powered, summed

J = (-3,-1,1,3)
M = (1,1,5,1)
N = (1,3,3,1)


def row_kernels(length, x, rail):
    signed, words = panel(length,(x,rail),3)
    sites = [fold(x+rail*j,length) for j in J]
    cells = [sorted(a*a for (y,r),a in signed.items() if y==site and a)
             for site in sites]
    assert cells == [[1],[1],[1,4],[1]]
    assert [summed(words,False)[y] for y in sites] == list(N)
    return cells


def reference(q, split):
    raw = [(1,), (1,), (1,4) if split else (5,), (1,)]
    weighted = [sum(v**q for v in group) for group in raw]
    return [F(p,sum(weighted)) for p in weighted]


def all_rows(h, mixture):
    result = [[F(0) for j in J] for _ in h]
    for frac,q,split in mixture:
        row = powered(h,q)
        column = reference(q,split)
        for i,w in enumerate(row):
            for j,s in enumerate(column):
                result[i][j] += frac*w*s
    return result


def rows_as_strings(rows):
    return [[str(p) for p in row] for row in rows]


def run():
    checked = []
    for length in range(4,49):
        for x in range(length):
            for rail in (-1,1):
                row_kernels(length,x,rail)
        checked.append(length)
    # For the fully rail-resolved option there are four unit cells and one
    # mass-four cell. A mixture can reproduce the whole suffix marginal.
    w0 = (F(1,2)-F(4,5))/(F(1,5)-F(4,5))
    assert w0 == F(1,2)
    h = [F(1,4),F(3,4)]
    mixture = [(w0,0,True),(1-w0,2,True)]
    rows = all_rows(h,mixture)
    suffix = [sum(col) for col in zip(*rows)]
    assert suffix == [F(n,8) for n in M]
    row_mass = [sum(r) for r in rows]
    residual = [r[0]-m/8 for r,m in zip(rows,row_mass)]
    assert row_mass == [F(3,10),F(7,10)]
    assert residual == [F(3,200),-F(3,200)]
    # If the science field is correlated with q the signed residuals in
    # every row can cancel, even when the reported old marginal is biased.
    other=[]
    for frac,q,hh in [(F(1,2),0,[F(1,4),F(3,4)]),
                      (F(1,2),2,[F(1,2),F(1,2)])]:
        other.append(all_rows(hh,[(frac,q,True)]))
    changing=[[p+v for p,v in zip(r,s)] for r,s in zip(*other)]
    assert all(row[0] == sum(row)/8 for row in changing)
    assert [sum(r) for r in changing] == [F(1,2),F(1,2)]
    assert [F(1,2)*(v+F(1,2)) for v in h] == [F(3,8),F(5,8)]
    return {"offsets":J,"squared_site_numerators":M,"unsigned_counts":N,
            "checked_lengths":checked,
            "fixed_two_science_weights":{"input":[str(v) for v in h],
            "q_0_and_2_fully_resolved_half_mixture_joint":rows_as_strings(rows),
            "science_marginal":[str(v) for v in row_mass],
            "relative_position_marginal":[str(v) for v in suffix],
            "row_residuals":[str(v) for v in residual]},
            "type_dependent_science":{"joint":rows_as_strings(changing),
            "mean_kinematic":["3/8","5/8"],"reported_old":["1/2","1/2"]}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    record = run()
    with args.output.open("x",encoding="utf-8",newline="\n") as sink:
        sink.write(json.dumps(record,indent=2)+"\n")
