"""Exact minimax equal-prior risk given only unconditional one-pair tables."""
from fractions import Fraction as Q
from check_paired_exposure import cells, rates


def main():
    tables = []
    for s,g,l in rates():
        p,q = [cells(s,Q(1,10**8)*v) for v in (g,l)]
        overlap = [min(a,b) for a,b in zip(p,q)]
        tables.append((1-sum(overlap),s,p,q,overlap))
    gap, mass = max((row[0],row[1]) for row in tables)
    assert 0 < gap < 1
    for distance, _, p, q, overlap in tables:
        common = [x/(1-distance) for x in overlap]
        for table in (p,q):
            residual = [(x-(1-gap)*c)/gap for x,c in zip(table,common)]
            assert min(residual)>=0 and sum(residual)==sum(common)==1
            assert [(1-gap)*c+gap*r for c,r in zip(common,residual)]==table
    risk = (1-gap)/2
    _,_,p,q,_ = next(row for row in tables if row[1]==mass)
    direct = sum(min(a,b) for a,b in zip(p,q))/2
    assert risk==direct
    print('best mass',float(mass),'max TV',float(gap),'risk',float(risk))
    assert Q(499999994226,10**12) < risk < Q(499999994228,10**12)


if __name__=='__main__':
    main()
