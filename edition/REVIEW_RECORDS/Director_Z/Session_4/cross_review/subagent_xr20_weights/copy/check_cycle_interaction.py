"""Construct a shared interaction from integer counts on a cycle and test its shape."""

import argparse
import csv
import json
from decimal import Decimal, getcontext
from math import ceil, log2
from pathlib import Path


def atan_inverse(q):
    x=Decimal(1)/q
    power=x
    value=x
    for j in range(1,1000):
        power *= -x*x
        updated=value+power/(2*j+1)
        if updated==value:
            return value
        value=updated
    raise ArithmeticError("atan series did not stabilize")


def cosine(x):
    term=value=Decimal(1)
    for j in range(1,500):
        term *= -x*x/((2*j)*(2*j-1))
        updated=value+term
        if updated==value:
            return value
        value=updated
    raise ArithmeticError("cosine series did not stabilize")


def count_table(n, depth):
    row = [1]+[0]*(n-1)
    for _ in range(depth):
        row = [row[(d-1)%n]+2*row[d]+row[(d+1)%n] for d in range(n)]
    return row


def config(n, depth, pi, writer):
    counts = count_table(n, depth)
    gaps = [counts[0]-c for c in counts]
    top = gaps[n//2]
    amplitude_scale = 37
    observed = []
    rounding_residual = 0
    for d,gap in enumerate(gaps):
        # Round L times the rational profile with ties upward.
        gain = (4*amplitude_scale*gap+top)//(2*top)
        residual = abs(gain*top-2*amplitude_scale*gap)
        rounding_residual = max(residual,rounding_residual)
        ideal = 1-cosine(2*pi*d/n)
        err = abs(2*Decimal(gap)/top-ideal)
        observed.append(err)
        writer.writerow((n,depth,d,gain,format(err,".34E"),str(2*residual <= top)))
    ratio = (cosine(2*pi/n)/cosine(pi/n))**2
    bound = (n-3)*ratio**depth
    err = max(observed)
    return dict(N=n,depth=depth,largest_shape_error=format(err,".44E"),bound=format(bound,".44E"),
                normalization_bits=top.bit_length(),count_total=(sum(counts)==4**depth),
                reflection=(counts[1:]==counts[:0:-1]),positive_scale=(top>0),
                rounded=(2*rounding_residual <= top),within_bound=bool(err<=bound+Decimal("1e-145")))


def propagate_count_interaction(n, depth, kappa):
    from math import pi
    from check_periodic_force import exact_walk, vector_norm
    delta=2*pi/n
    m_sheet=40001
    ticks=max(1, round(0.5/delta**2))
    scale=round(m_sheet*kappa*delta**2/(2*pi))
    c=count_table(n,depth)
    denominator=c[0]-c[n//2]
    gains=[(4*scale*(c[0]-v)+denominator)//(2*denominator) for v in c]
    walk, obs=exact_walk(n,1.,ticks,kappa,m_sheet,"quantum",relative_gains=gains)
    ideal, _=exact_walk(n,1.,ticks,kappa,0,"quantum")
    discrepancy=vector_norm(walk-ideal)
    return dict(N=n,depth=depth,ticks=ticks,kappa=kappa,scale=scale,gains=gains,
                compared_with_unrounded_cosine=discrepancy,actual_angles_bound=ticks*obs["maximum_step_rounding_error"],
                norm_error=obs["walk_norm_error"],applied_gain_max=obs["max_abs_integer_gain"])


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    getcontext().prec=160
    pi = 16*atan_inverse(5)-4*atan_inverse(239)
    with (out/"cycle_interaction.csv").open("w",encoding="utf8",newline="") as stream:
        writer=csv.writer(stream)
        writer.writerow(("sites","depth","separation","gain_for_L37","shape_error","nearest_integer_bound"))
        rows=[config(n,m,pi,writer) for n in (8,12,16,20,24) for m in (1,n,n*n*ceil(log2(n)))]
    checks={key:all(row[key] for row in rows) for key in
            ("count_total","reflection","positive_scale","rounded","within_bound")}
    flights=[propagate_count_interaction(n,m,k) for n in (8,16,24)
             for m in (1,n*n*ceil(log2(n))) for k in (1,-1)]
    checks["count_built_spinor_bound"]=all(f["norm_error"]<1e-12 and
            f["compared_with_unrounded_cosine"]<=f["actual_angles_bound"]+1e-12 for f in flights)
    report=dict(checks=checks,configurations=rows,integer_gain_flights=flights,
                scope="Raw integer count recurrence. Shape residuals use 160 decimal digits. All configurations included.")
    (out/"cycle_interaction.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print(checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    main(parser.parse_args().output)
