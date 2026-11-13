"""Exploration (not a predicate program): block law for functions of the MULTISET of gains.
F: N^q -> Q (count vector over C_q), block B (d x d, entries exponents mod q).
Law: sum_z F(sum_y shift_{B_zy} m_y) = d sum_y F(m_y) for all inputs m_y with every vector of size <= N in play.
Unknowns: F(m) for |m| <= N. Reports nullity mod two primes."""
import itertools, sys
from flint import nmod_mat
def comps(q, N):
    out=[]
    for tot in range(N+1):
        for c in itertools.combinations_with_replacement(range(q), tot):
            v=[0]*q
            for g in c: v[g]+=1
            out.append(tuple(v))
    return out
def shift(m,k,q): return tuple(m[(g-k)%q] for g in range(q))
def run(name,q,B,N,full=True):
    d=len(B); vs=comps(q,N); idx={v:i for i,v in enumerate(vs)}
    rows=set()
    cols = range(d) if full else range(2)
    ins=[vs if (full or y<2) else [tuple([0]*q)] for y in range(d)]
    for m in itertools.product(*ins):
        if sum(sum(x) for x in m)>N: continue
        row={}
        for z in range(d):
            o=[0]*q
            for y in range(d):
                s=shift(m[y],B[z][y],q)
                for g in range(q): o[g]+=s[g]
            i=idx[tuple(o)]; row[i]=row.get(i,0)+1
        for y in range(d):
            i=idx[m[y]]; row[i]=row.get(i,0)-d
        r=tuple(sorted((i,c) for i,c in row.items() if c))
        if r: rows.add(r)
    res=[]
    for p in (1000003, 998244353):
        M=nmod_mat(len(rows),len(vs),p)
        for a,r in enumerate(rows):
            for i,c in r: M[a,i]=c%p
        res.append(len(vs)-M.rank())
    print(f"{name} q={q} d={d} N={N} unknowns={len(vs)} eqs={len(rows)} nullity={res}", flush=True)
H=[[0,0],[0,1]]
for N in (4,6,8,10): run("H2 signs",2,H,N)
for N in (3,4,5,6): run("[[1,1],[1,-1]] in C4",4,[[0,0],[0,2]],N)
for N in (3,4,5,6): run("[[1,i],[1,-i]] in C4",4,[[0,1],[0,3]],N)
F3=[[0,0,0],[0,1,2],[0,2,1]]
for N in (3,4,5,6): run("F3",3,F3,N)
for N in (3,4,5): run("[[1,w],[1,?]]",3,[[0,0],[0,1]],N) if False else None
for N in (3,4,5): run("H2 in C6 [[1,1],[1,-1]]",6,[[0,0],[0,3]],N)
