"""Check coarse/fine gain pooling with pure marginal sources and physical whole-site masks.

Run python -B check_cover_comparison.py OUTDIR. The output must be new.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

from check_compact_residue_preparation import compile_masks
from check_equal_clock_lags import branches, path, ring_filter, return_to_home


def require(condition, msg):
    if not condition:
        raise ValueError(msg)


def embed(u, m, n):
    require(n % m == 0, "orders do not form a cover")
    return Counter({(s,j*(n//m)):k for (s,j),k in u.items()})


def pooled(u,v,m,n):
    out=Counter()
    for (s,j),k in embed(u,m,n).items():
        for (t,h),l in v.items():
            out[s*t,(j+h)%n]+=k*l
    return out


def cells(u):
    return [[s,j,k] for (s,j),k in sorted(u.items())]


def masks(u, order):
    items=[key for key,k in sorted(u.items()) for _ in range(k)]
    rows,_,_=compile_masks(order,items,[],0)
    return [{(t-2*d)%(4*order) for d in row} for t,row in enumerate(rows,1)]


def read(rows, order, target):
    physical=ring_filter(rows,order,4*order,0)
    require(all(x==target and c=="R" for x,c,j,s in physical), "unexpected final mode")
    return Counter({(s,j):k for (x,c,j,s),k in physical.items()})


def pad(rows, total, order):
    gap=total-len(rows)
    require(gap>=0 and gap%2==0,"incompatible common-clock padding")
    # Named port (0,R) on every retained branch. Each LR loop shifts the sheet by -1.
    return rows+[{4*order-1},{0}]*(gap//2)


def universal(m,n):
    b=Counter({(1,0):5})
    h=Counter({(1,0):3,(-1,0):1,(1,1):1})
    e,f=embed(b,m,n),embed(h,m,n)
    source=[(m,b),(m,h),(n,e),(n,f)]
    rows=[masks(u,o) for o,u in source]
    times=[len(row) for row in rows]
    require(times[0]==times[1] and times[2]==times[3],"setting changes local clocks")
    for row,(o,u) in zip(rows,source):
        require(read(row,o,0)==u,"local physical histogram")
    fine=pooled(b,f,m,n)
    require(fine==pooled(h,e,m,n) and sum(fine.values())==25,"unshifted coincidence")
    t=max(times)
    b1,h1,e1,f1=[read(pad(row,t,o),o,0) for row,(o,u) in zip(rows,source)]
    padded=pooled(b1,f1,m,n)
    require(padded==pooled(h1,e1,m,n),"padding did not preserve the common fiber")
    # Symbolic keys: the count ratio 1 exceeds each character ratio (5+4 cos)/25.
    # Two character keys agree precisely at equal folded residues modulo m.
    fold=lambda s:min(s%m,(-s)%m)
    coarse=["count",*range(m//2+1)]
    large=["count",*range(n//2+1)]
    hits=[(i,j) for i in coarse for j in large if
          (i=="count" and j=="count") or (i!="count" and j!="count" and i==fold(j))]
    require(len(hits)==len(large),"fine label has no unique coarse restriction")
    return dict(M=m,N=n,coarse_ticks=times[0],fine_ticks=times[2],padded_ticks=t,
                coincidence_word_pairs=sum(padded.values()),unpadded=cells(fine),padded=cells(padded),
                all_pure_agreements=hits)


def two_word(m):
    n=2*m
    coarse=("RLR","LRR")
    fine=branches(n-2)
    def panel(words,order,ref):
        paths=[path(w,0) for w in words]
        rows=[set(pair) for pair in zip(paths[0][0],paths[1][0])]
        target=paths[0][0][-1]%(4*order)
        c=read(rows,order,target)
        i=read([{x} for x in paths[ref][0]],order,target)
        require(sum(c.values())==2 and sum(i.values())==1 and
                (paths[0][2]==paths[1][2]), "native coherent arm pair")
        return c,i,[q[1] for q in paths],paths[0][2]
    c,i,cg,cs=panel(coarse,m,0)
    d,j,fg,fs=panel(fine,n,1)
    x,y=pooled(c,j,m,n),pooled(i,d,m,n)
    require(x==y and fg[0]-fg[1]==n-2 and cg[0]-cg[1]==1,"physical dyadic arm alignment")
    # Mischoosing the fine reference generally changes the common fiber.
    wrong=pooled(c,Counter({(fs,fg[0]%n):1}),m,n)
    require(wrong!=y,"wrong reference gave a false matched fiber")
    return dict(M=m,N=n,coarse_ticks=len(coarse[0]), fine_ticks=len(fine[0]),
                coarse_words=coarse,fine_words=fine,coarse_signed_lift=[cs,cg],fine_signed_lift=[fs,fg],
                shared=cells(x),wrong_fine_reference=cells(wrong))


def equal_lag_cover(m,n):
    d=n//m
    lags=range(6,10)
    def four_paths(lag):
        if lag==7:
            return "RRLRLLR","LLRLRRR"
        if lag==9:
            return "RRRLLLR","LLLRRRR"
        require((lag%2==0 and lag>=4) or lag>=13,"no template for requested lag")
        return branches(lag)
    clock=0
    for lag in (*lags,*(d*l for l in lags)):
        top,_=four_paths(lag)
        x=top.count("R")-top.count("L")
        clock=max(clock,len(top)+abs(x+1)+1)
    require(clock%2==0,"odd common-clock return")

    def local(order,lag,home):
        words=return_to_home(four_paths(lag),clock)
        paths=[path(w,home) for w in words]
        require(all(p[0][-1]==home for p in paths) and paths[0][2]==paths[1][2]
                and paths[0][1]-paths[1][1]==lag, "two coherent line paths")
        def collect(masks):
            census=ring_filter(masks,order,4*order,home)
            require(all((x,c)==(home,"R") for x,c,j,s in census), "cyclic return port")
            return Counter({(s,j):k for (x,c,j,s),k in census.items()})
        fork=collect(zip(paths[0][0],paths[1][0]))
        ref=collect([{x} for x in paths[0][0]])
        expected=Counter((s,j%order) for _,j,s in paths)
        require(fork==expected and sum(ref.values())==1, "aliased or lost path")
        return fork,ref

    records=[]
    for home_m,home_n in ((0,0),(4*m-1,4*n-2)):
        for lag in lags:
            fork_m,ref_m=local(m,lag,home_m)
            fork_n,ref_n=local(n,d*lag,home_n)
            a=pooled(fork_m,ref_n,m,n)
            b=pooled(ref_m,fork_n,m,n)
            require(a==b and sum(a.values())==2, "nonmatching fine total histogram")
            records.append(dict(coarse_lag=lag,fine_lag=d*lag,homes=[home_m,home_n],
                                coarse_words=cells(fork_m),fine_words=cells(fork_n),pooled=cells(a)))
    # Compare exact cosines by equality of residues up to sign; zero is shared by
    # counting only when the character lies on an odd quarter turn for that stroke.
    def key(label,l):
        if label=="count":
            return "zero"
        j=(l*label)%m
        return "zero" if (4*j)%m==0 and (2*j)%m!=0 else min(j,m-j)
    coarse=["count",*range(m//2+1)]
    signatures={s:tuple(key(s,l) for l in lags) for s in coarse}
    require(len(set(signatures.values()))==len(coarse),"four-lag pure-label degeneracy")
    for t in ["count",*range(n//2+1)]:
        ref="count" if t=="count" else min(t%m,(-t)%m)
        require([s for s in coarse if signatures[s]==tuple(key(t,l) for l in lags)]==[ref],
                "stronger or weaker than the required restriction")
    return dict(M=m,N=n,stroke=d,local_ticks=clock,records=records,
                coarse_signatures=[[s,v] for s,v in signatures.items()])


def run():
    cases=[(3,6),(4,8),(5,10),(6,12),(3,12),(4,12),(8,24)]
    # A mixture can match the common ratio of a pure source. Coarse 4 label 1;
    # fine 8 gives half its weight to labels 0 and 2, restricting to 0 and 2.
    coarse, mixed = Fraction(5,25), (Fraction(9,25)+Fraction(1,25))/2
    require(coarse==mixed and coarse!=Fraction(9,25), "non-pure marginal control")
    return dict(scope="Assumes pure marginal rules for the cover classification. All trials on original rings.",
                cover_cases=[universal(m,n) for m,n in cases],
                native_dyadic=[two_word(m) for m in (3,4,5,6,8)],
                four_common_lags=[equal_lag_cover(m,n) for m,n in [(3,3),*cases]],
                mixed_false_pass=dict(M=4,N=8,coarse_label=1,fine_half_weights=[0,2],
                                      transfer_ratio=coarse),
                probability_scale="Before common-clock padding divide by 2^(T_M+T_N); after it divide by 4^T.")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    result=run()
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"cover_comparison.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,default=str,separators=(",",":"))
        f.write("\n")
