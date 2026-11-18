"""Recompute four optical source vectors, segment comparisons and the classical fit.

Usage: python check_source_segments.py PER_RUN.xlsx
Requires openpyxl. The optional --sharp-hidden replay uses SciPy and SymPy.
"""
import argparse
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from check_cairo_cycle import require
from check_three_readings import RUNS_HASH, table as read_workbook
SOURCES = ("P_1,0", "P_1,1", "P_2,0", "P_2,1")


def pool(data, runs):
    vectors = []
    for source in SOURCES:
        totals = [sum(data[r, source][j] for r in runs) for j in range(8)]
        vectors.append([F(a, a+b) for a,b in zip(totals[::2], totals[1::2])])
    return vectors


def directions(table):
    a,b,c,d = table
    return ([x-y for x,y in zip(a,b)],
            [x-y for x,y in zip(c,d)],
            [x-y for x,y in zip(b,d)])


def plane_weights(table):
    u, v, offset = directions(table)
    det = u[0]*v[2] - u[2]*v[0]
    require(det != 0, "Selected source directions must be independent")
    p = (offset[2]*v[0]-offset[0]*v[2])/det
    q = (offset[2]*u[0]-offset[0]*u[2])/det
    require(0 < p < 1 and 0 < q < 1, "Reader-plane intersection inside both segments")
    return p,q


def analyze(table, weights):
    p,q = weights
    u,v,offset = directions(table)
    gaps = [k + p*x - q*y for x,y,k in zip(u,v,offset)]
    e = [[w*(2*plus-1) - (1-w)*(2*minus-1) for plus,minus in zip(table[2*i],table[2*i+1])]
         for i,w in enumerate(weights)]
    fixed_score = e[0][0] - e[0][2] - e[1][0] - e[1][2]
    exploratory_score = -e[0][1] - e[0][2] + e[1][1] - e[1][2]
    return gaps, fixed_score, exploratory_score


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def separator(table):
    """Unit l1 combination constant along both segments (readers 1,2,3)."""
    u,v,offset = directions(table)
    h = [F(0), u[2]*v[3]-u[3]*v[2], u[3]*v[1]-u[1]*v[3], u[1]*v[2]-u[2]*v[1]]
    scale = sum(map(abs,h))
    if dot(h,offset)<0:
        scale = -scale
    h = [x/scale for x in h]
    require(dot(h,u)==dot(h,v)==0, "Separating functional parallel to both directions")
    return h


def endpoint_gap(h, table):
    points = [dot(h,vec) for vec in table]
    return min(points[:2]) - max(points[2:])


def minimax_certificate(table):
    """Exact primal and dual for distance in maximum output-probability norm.

    In these five tables, active differences on readers 1,2,3 have common
    absolute value with signs given by the separating reader; solve for p,q,d.
    """
    import sympy as sp
    h = separator(table)
    u,v,offset = directions(table)
    active = [j for j in range(4) if h[j]]
    m = sp.Matrix([[u[j], -v[j], -int(h[j] > 0) + int(h[j] < 0)] for j in active])
    p,q,d = map(F, m.inv()*sp.Matrix([-offset[j] for j in active]))
    require(0 <= p <= 1 and 0 <= q <= 1, "Segment weights")
    errors = [k + p*x - q*y for x,y,k in zip(u,v,offset)]
    require(max(map(abs,errors)) == d == endpoint_gap(h,table), "Exact minimax certificate")
    return p,q,d


def hidden_certificate(table, weights):
    """Use an LP to find a basis, then verify its complete solution over rationals."""
    import numpy as np
    from scipy.optimize import linprog
    import sympy as sp
    patterns = list(product((0,1),repeat=4))
    eq, target = [], []
    for i,w in enumerate(weights):
        for a in (0,1):
            mass = w if a == 0 else 1-w
            for j in (-1,0,1,2,3):
                row = [0]*80
                for b, pattern in enumerate(patterns):
                    if j == -1 or pattern[j] == 0:
                        row[(2*i+a)*16+b] = 1
                eq.append(row)
                target.append(mass if j == -1 else mass*table[2*i+a][j])
    inequalities = []
    for i,b in product(range(2),range(16)):
        row = [0]*80
        row[64+b] = 1
        row[32*i+b] = row[32*i+16+b] = -1
        inequalities.append(row)
    solution = linprog([0]*64+[-1]*16,A_eq=eq,b_eq=np.array(target,float),
                       A_ub=inequalities,b_ub=[0]*32,bounds=(0,None),method="highs")
    require(solution.success, "Classical overlap linear program")
    basis = [j for j,m in enumerate(solution.x) if m>1e-9]
    tight = [row for row,slack in zip(inequalities,solution.ineqlin.residual) if slack<1e-9]
    all_rows = eq+tight
    rhs = target+[0]*len(tight)
    system = sp.Matrix([[row[j] for j in basis]+[val] for row,val in zip(all_rows,rhs)])
    reduced,piv = system.rref()
    require(piv == tuple(range(len(basis))), "Basis must define a rational solution")
    x = [F(0)]*80
    for i,j in enumerate(basis):
        x[j] = F(reduced[i,-1])
    require(min(x)>=0 and all(dot(row,x)==val for row,val in zip(eq,target)), "Primal equalities")
    require(all(dot(row,x)<=0 for row in inequalities), "Primal overlap bounds")
    distance = 1-sum(x[64:])
    lower = (analyze(table,weights)[2]-2)/2
    require(distance==lower, "Exploratory CHSH must exactly attain overlap optimum")
    return distance


def explore_secondary(data):
    """Retrospective sensitivity of a maximum-retention training objective."""
    import numpy as np
    from scipy.optimize import linprog

    labels = [f"P_{i},{a}" for i in range(1, 5) for a in (0, 1)]
    def all_sources(runs):
        result = []
        for source in labels:
            cells = np.sum([data[r,source] for r in runs], axis=0)
            result.append(cells[::2]/(cells[::2] + cells[1::2]))
        return np.array(result)
    splits = [(range(1,51),range(51,101)), (range(51,101),range(1,51)),
              (range(1,101,2),range(2,101,2)), (range(2,101,2),range(1,101,2))]
    for training, testing in splits:
        train, test = all_sources(training), all_sources(testing)
        left, _, _ = np.linalg.svd(train-train.mean(axis=0), full_matrices=False)
        for rank in (4,3):
            # Four normalized mixture rows use all eight original procedures.
            # Orthogonal coordinates avoid ill-conditioning in the four raw columns.
            design = np.zeros((4+rank,4,8))
            for i, sign in enumerate((1,1,-1,-1)):
                design[i,i] = 1
                design[4:,i] = sign*left[:,:rank].T
            # Retain as much weight as possible on each original target procedure.
            optimum = linprog(-np.eye(4,8).ravel(), A_eq=design.reshape(4+rank,32),
                              b_eq=[1]*4+[0]*rank, bounds=(0,1), method="highs")
            require(optimum.success, "Secondary preparation fit")
            weights = optimum.x.reshape(4,8)
            scores = weights @ test
            e0, e1 = scores[0]-scores[1], scores[2]-scores[3]
            fixed = e0[0]-e0[2]-e1[0]-e1[2]
            max_gap = max(abs((scores[0]+scores[1]-scores[2]-scores[3])/2))
            print("held",testing,"rank",rank,"score",round(float(fixed),6),
                  "largest raw discrepancy",round(float(max_gap),7))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook",type=Path)
    parser.add_argument("--sharp-hidden",action="store_true")
    parser.add_argument("--secondary",action="store_true",help="Exploratory train/test mixture fits")
    args=parser.parse_args()
    data=read_workbook(args.workbook, RUNS_HASH, per_run=True)
    required=set(product(range(1,101), SOURCES))
    require(required <= data.keys(), "Target preparations present in every run")
    full=pool(data,range(1,101))
    weights=plane_weights(full)
    gaps,score,alt=analyze(full,weights)
    require(gaps[0]==gaps[2]==0, "Exact equality on selected readers")
    print("Weights",*(float(w) for w in weights),"fixed score",float(score),"alternate",float(alt))
    print("Four gaps",*[float(x) for x in gaps])
    for name,rr,ss in [("first-last",range(1,51),range(51,101)),("last-first",range(51,101),range(1,51)),
                       ("odd-even",range(1,101,2),range(2,101,2)),("even-odd",range(2,101,2),range(1,101,2))]:
        tr,te=pool(data,rr),pool(data,ss)
        h=separator(tr)
        held_gaps, held_score, _ = analyze(te,plane_weights(tr))
        print(name, "train",float(endpoint_gap(h,tr)),"held",float(endpoint_gap(h,te)),
              "fixed weights on held score",float(held_score),"M4",float(held_gaps[3]))
    if args.secondary:
        explore_secondary(data)
    if args.sharp_hidden:
        print("Minimax source-segment gap",*(float(v) for v in minimax_certificate(full)))
        print("Minimum hidden TV",float(hidden_certificate(full,weights)))


if __name__=="__main__":
    main()
