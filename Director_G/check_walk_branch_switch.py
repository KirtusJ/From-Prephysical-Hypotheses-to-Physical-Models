"""Bare signed walk, one coherent bit, and an addressed terminal bit-basis switch."""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path


def check(condition, label):
    if not condition:
        raise ValueError(label)


def flight(n,t):
    v={(0,0):1}
    for _ in range(t):
        nxt=defaultdict(int)
        for (x,c),a in v.items():
            nxt[(x+1)%n,0]+=a
            nxt[(x-1)%n,1]+=(1-2*c)*a
        v=nxt
    return v


def operations(n,t,local):
    v=flight(n,t)
    sites=sorted({x for x,c in v})
    out=[]
    for mix in (False,True):
        rows=defaultdict(int)
        for (x,c),a in v.items():
            left,right=a,(-a if x==local[1]%n else a)
            for b in (0,1):
                if mix and x in {z%n for z in local}:
                    mass=Q((left+(1-2*b)*right)**2,2)
                else:
                    mass=Q((left,right)[b]**2)
                rows[x,c,b]=mass
        check(sum(rows.values())==2**(t+1),"whole table mass")
        out.append(rows)
    for x in sites:
        for c in (0,1):
            check(sum(out[0][x,c,b] for b in (0,1))==sum(out[1][x,c,b] for b in (0,1)),
                  "both coordinate marginals invariant")
    return v,sites,out


def report(n,t,local,monitors,rail=None):
    v,sites,settings=operations(n,t,local)
    rails=(0,1) if rail is None else (rail,)
    def rows(z):
        return [[sum(z[x,c,b] for c in rails) for x in sites] for b in (0,1)]
    table=[rows(z) for z in settings]
    z0,z1=table[0][0],table[1][0]
    check(table[0][0]==table[0][1] and sorted(z1)==sorted(table[1][1]),"branch tables agree on spectra")
    for z in table:
        for x in monitors:
            j=sites.index(x%n)
            check(z[0][j]==z[1][j]==z0[j],"unchanged remote cells")
    a,b=[z0[sites.index(x%n)] for x in monitors]
    check(a>b>0,"distinct positive monitors")
    def ratio(q,m,z):
        powered=[s**q if s else 0 for s in z]
        return m**q/sum(powered)
    def limit(m,z):
        return Q(1,z.count(max(z))) if m==max(z) else Q(0)
    def weighted(f):
        return f(a,z0)-f(a,z1)-a/b*(f(b,z0)-f(b,z1))
    values={str(q):weighted(lambda m,z:ratio(q,m,z)) for q in (0,1,2,4,8,16)}
    check(values["1"]==0 and all(val>0 for q,val in values.items() if q!="1"),"finite sign")
    values["infinity"]=weighted(limit)
    return dict(n=n,t=t,local=local,monitors=monitors,rail=rail,sites=sites,
                signed_rails=[[v.get((x,r),0) for r in (0,1)] for x in sites],
                rows=table,witness=values)


def main():
    arg=argparse.ArgumentParser(description=__doc__)
    arg.add_argument("out",type=Path)
    rows=[report(18,3,(-3,-1),(1,3)), report(10,6,(2,6),(4,8)),
          report(18,8,(-2,0),(4,8),0), report(18,8,(-2,0),(4,-8),1)]
    check([r["witness"]["infinity"] for r in rows]==[0,1,0,0],"infinite boundaries")
    check(rows[0]["witness"]["2"]==Q(1,21) and rows[1]["witness"]["2"]==Q(4225,36557)
          and rows[1]["witness"]["0"]==Q(1,5),"native square and zero limits")
    with arg.parse_args().out.open("x",encoding="utf8",newline="\n") as out:
        json.dump(rows,out,indent=2,default=str)
        out.write("\n")


if __name__=="__main__":
    main()
