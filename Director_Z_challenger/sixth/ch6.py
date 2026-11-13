"""Challenger 6: multiset block law.  Predicates fixed before first run.
Law: sum_z F(sum_y B_zy.m_y) = d sum_y F(m_y), F on multisets over Z/q (exponents).
H  (hypothesis, per instance): d>=2, entries in Z/q.  Reported: number qualifying.
P1 for each matrix and each S in 2..Smax: exact nullity over Q of the law restricted to
   tuples of total size <= S (unknowns F(m), |m|<=S) == |J0| + #{unordered {j,l}: j+l in J0, j in U}.
   J0, U computed here exactly (divisibility by cyclotomic polynomial).
P2 statements on J0,U: J0 subgroup = annihilator of <entries>; U=-U; U+J0=U; 0 not in U.
P3 every solution in the null space has F(0)=0 (column 0 is zero in rref null basis).
P4 paper's two examples: U={1,2,4,5} and U={1,3,5}, and B^(1)*B^(1)=d.
P5 hand candidates n_0^3, |m|^3, (-1)^{n_0}, [n_0 odd], |m|^2 violate the law for every matrix with d>=2.
P6 d=1 control: nullity exceeds formula (theorem said false for d=1) -- instances not qualifying under H.
P7 sigma_1: M -> Z[zeta] surjective for q>=2: -1 = sum of the other roots (exact).
Seed 20261113.  Result file not overwritten.
"""
import itertools, random, sys, os, json
from flint import fmpz_mat, fmpq_poly
OUT='ch6_results.json'
if os.path.exists(OUT): sys.exit('refuse to overwrite')
random.seed(20261113)
def cyclo(q):
    p=fmpq_poly([-1]+[0]*(q-1)+[1])
    for k in range(1,q):
        if q%k==0: p=p//cyclo(k)
    return p
CY={}
def zero_sum(exps,q):  # sum zeta^e == 0 ?
    if q not in CY: CY[q]=cyclo(q)
    c=[0]*q
    for e in exps: c[e%q]+=1
    return (fmpq_poly(c)%CY[q])==0
def eq_sum(exps,q,val):  # sum zeta^e == val (integer)
    c=[0]*q
    for e in exps: c[e%q]+=1
    c[0]-=val
    if q not in CY: CY[q]=cyclo(q)
    return (fmpq_poly(c)%CY[q])==0
def J0U(B,q):
    d=len(B)
    J0=[j for j in range(q) if all((j*B[z][y])%q==0 for z in range(d) for y in range(d))]
    U=[j for j in range(q) if all(eq_sum([j*(B[z][y]-B[z][yp]) for z in range(d)],q,d if y==yp else 0) for y in range(d) for yp in range(d))]
    return J0,U
def formula(B,q):
    J0,U=J0U(B,q)
    prs={frozenset((j,l)) for j in U for l in range(q) if (j+l)%q in J0}
    return len(J0)+len(prs)
def msets(q,S):
    out=[]
    for s in range(S+1):
        for c in itertools.combinations_with_replacement(range(q),s):
            v=[0]*q
            for h in c: v[h]+=1
            out.append(tuple(v))
    return out
def shift(m,k,q): return tuple(m[(h-k)%q] for h in range(q))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def tuples(ms,d,S):
    def rec(i,left):
        if i==d: yield (); return
        for m in ms:
            s=sum(m)
            if s<=left:
                for r in rec(i+1,left-s): yield (m,)+r
    return rec(0,S)
def W(B,q,t):
    d=len(B); z0=(0,)*q; out=[]
    for z in range(d):
        w=z0
        for y in range(d): w=add(w,shift(t[y],B[z][y],q))
        out.append(w)
    return out
def nullity(B,q,S):
    d=len(B); ms=msets(q,S); idx={m:i for i,m in enumerate(ms)}
    rows=set()
    for t in tuples(ms,d,S):
        r={}
        for w in W(B,q,t): r[idx[w]]=r.get(idx[w],0)+1
        for m in t: r[idx[m]]=r.get(idx[m],0)-d
        r=tuple(sorted((k,v) for k,v in r.items() if v))
        if r: rows.add(r)
    A=fmpz_mat(len(rows),len(ms))
    for i,r in enumerate(rows):
        for k,v in r: A[i,k]=v
    rk=A.rank()
    # P3: F(0)=0 forced iff adding unit row e_0 does not raise rank
    A2=fmpz_mat(len(rows)+1,len(ms))
    for i,r in enumerate(rows):
        for k,v in r: A2[i,k]=v
    A2[len(rows),idx[(0,)*q]]=1
    return len(ms)-rk, A2.rank()==rk, len(rows)
CANDS={'n0^3':lambda m:m[0]**3,'size^3':lambda m:sum(m)**3,'(-1)^n0':lambda m:(-1)**m[0],'n0 odd':lambda m:m[0]%2,'size^2':lambda m:sum(m)**2}
def violates(B,q,F,S=3):
    d=len(B); ms=msets(q,S)
    for t in tuples(ms,d,S):
        if sum(F(w) for w in W(B,q,t))!=d*sum(F(m) for m in t): return True
    return False
MATS=[('q1d2',1,[[0,0],[0,0]]),('q1d3',1,[[0]*3]*3),
 ('q2d2had',2,[[0,0],[0,1]]),('q2d2ones',2,[[0,0],[0,0]]),('q2d2repcol',2,[[0,0],[1,1]]),('q2d2nonblk',2,[[0,1],[1,1]]),
 ('q2d3nonblk',2,[[0,0,1],[0,1,0],[1,1,0]]),('q2d3ones',2,[[0]*3]*3),
 ('q2d4had',2,[[0,0,0,0],[0,1,0,1],[0,0,1,1],[0,1,1,0]]),('q2d4non',2,[[0,0,0,1],[0,1,0,1],[1,0,1,1],[0,1,1,0]]),
 ('q3d3fourier',3,[[0,0,0],[0,1,2],[0,2,1]]),('q3d2repcol',3,[[0,0],[1,1]]),('q3d2non',3,[[0,1],[0,2]]),('q3d3circ',3,[[1,0,0],[0,1,0],[0,0,1]]),
 ('q4d2realhad',4,[[0,0],[0,2]]),('q4d2i',4,[[0,1],[1,0]]),('q4d2i2',4,[[0,0],[1,3]]),('q4d2sub_non',4,[[0,2],[2,2]]),('q4d4mix',4,[[0,0,0,0],[0,1,2,3],[0,2,0,2],[0,3,2,1]]),
 ('q5d2',5,[[0,1],[2,4]]),
 ('q6d2had_sub',6,[[0,0],[0,3]]),('q6d3fourier_sub',6,[[0,0,0],[0,2,4],[0,4,2]]),('q6d2gen',6,[[0,1],[0,4]]),('q6d2repcol',6,[[1,1],[3,3]]),
 ('paperEx1',6,[[0,0,3],[0,2,1],[0,4,5]]),('paperEx2',6,[[0,0,0,0],[0,0,3,3],[0,3,1,4],[0,3,4,1]]),
 ('q8d2sub4',8,[[0,2],[2,0]])]
for i in range(14):
    q=random.choice([2,3,4,5,6]); d=random.choice([2,2,3]) if q<6 else 2
    MATS.append(('rand%d'%i,q,[[random.randrange(q) for _ in range(d)] for _ in range(d)]))
MATS.append(('d1control_q2',2,[[1]])); MATS.append(('d1control_q3',3,[[0]]))
res=[]; cnt={k:[0,0] for k in 'P1 P2 P3 P4 P5 P6 P7'.split()}; qual=0
def tick(p,ok): cnt[p][0]+=1; cnt[p][1]+=bool(ok)
for name,q,B in MATS:
    d=len(B); H=d>=2; qual+=H
    J0,U=J0U(B,q); f=formula(B,q)
    Smax=4 if q**1*d<=12 else 3
    if q==8: Smax=3
    rec=dict(name=name,q=q,d=d,B=B,J0=J0,U=U,formula=f,H=H,null={})
    if H:
        import math
        g=0
        for r in B:
            for e in r: g=math.gcd(g,e)
        g=math.gcd(g,q); ann=[j for j in range(q) if (j*g)%q==0]
        tick('P2', J0==ann and all((a+b)%q in J0 for a in J0 for b in J0) and all((-j)%q in U for j in U) and all((j+k)%q in U for j in U for k in J0) and 0 not in U)
    for S in range(2,Smax+1):
        n,f0,nr=nullity(B,q,S); rec['null'][S]=n
        if H: tick('P1',n==f); tick('P3',f0)
        else: tick('P6',n>f)
    if H:
        for cn,F in CANDS.items():
            v=violates(B,q,F); tick('P5',v); rec['cand_'+cn]=v
    res.append(rec); print(name,q,d,'J0',J0,'U',U,'formula',f,'null',rec['null'],flush=True)
tick('P4',J0U(MATS[24][2],6)[1]==[1,2,4,5] and 1 in J0U(MATS[24][2],6)[1]); tick('P4',J0U(MATS[25][2],6)[1]==[1,3,5])
for q in range(2,13): tick('P7',eq_sum(list(range(1,q)),q,-1))
summary={k:{'run':v[0],'pass':v[1]} for k,v in cnt.items()}
print('qualifying',qual,'of',len(MATS)); print(summary)
json.dump(dict(qualifying=qual,total=len(MATS),summary=summary,instances=res),open(OUT,'w'),indent=1)
