"""Micro-review of thm:multiset / cor:multiset boundary cases.
Predicates (fixed before run), per case and size bound N in {2,3,4}:
 P1 nullity of (MBL) truncated to total size <= N equals |J0| + #{unordered {j,l}: j+l in J0, j in U}
 P2 with F(m)=0 imposed for 1<=|m|<=2, nullity is 0 (determined by sizes one and two; F(0)=0 forced)
 P3 (when entries generate C) nullity equals 1 + #classes {j,-j} in U
Rank is computed mod two primes; J0 and U exactly (polynomial remainder mod x^q-1 and cyclotomic test via all embeddings is avoided:
 a sum of roots of unity is tested exactly by reducing mod Phi_q)."""
import itertools, json, math
from flint import nmod_mat, fmpz_poly
PR=[1000003,998244353]
def phi(q):
    x=fmpz_poly([0,1]); p=x**q-1
    for e in range(1,q):
        if q%e==0: p=p//phi(e)   # exact division
    return p
def zero_sum(exps,q):
    c=[0]*q
    for e in exps: c[e%q]+=1
    if q==1: return sum(c)==0
    r=fmpz_poly(c)
    P=phi(q)
    _,rem=divmod(r,P)
    return rem==0
def sets(B,q):
    d=len(B)
    J0=[j for j in range(q) if all((j*b)%q==0 for row in B for b in row)]
    U=[]
    for j in range(q):
        ok=True
        for y in range(d):
            for y2 in range(d):
                if y==y2: continue
                if not zero_sum([j*(B[z][y2]-B[z][y]) for z in range(d)],q): ok=False
        if ok: U.append(j)
    return J0,U
def formula(J0,U,q):
    return len(J0)+sum(1 for j in range(q) for l in range(j,q) if (j+l)%q in J0 and j in U)
def run(name,q,B,Ns=(2,3,4)):
    d=len(B); J0,U=sets(B,q); f=formula(J0,U,q)
    g=0
    for row in B:
        for b in row: g=math.gcd(g,b)
    gen = math.gcd(g,q)==1
    out={'case':name,'q':q,'d':d,'B_exponents':B,'J0':J0,'U':U,'formula':f,'entries_generate':gen}
    if gen: out['cor_count']=1+len({frozenset((j,(-j)%q)) for j in U})
    for N in Ns:
        ms=[tuple(sorted(c)) for n in range(N+1) for c in itertools.combinations_with_replacement(range(q),n)]
        idx={m:i for i,m in enumerate(ms)}
        rows=set()
        for n in range(N+1):
            for c in itertools.combinations_with_replacement(range(d*q),n):
                row={}
                for y in range(d):
                    m=tuple(sorted(e%q for e in c if e//q==y))
                    row[idx[m]]=row.get(idx[m],0)-d
                for z in range(d):
                    w=tuple(sorted((e%q+B[z][e//q])%q for e in c))
                    row[idx[w]]=row.get(idx[w],0)+1
                rows.add(tuple(sorted((k,v) for k,v in row.items() if v)))
        rows=[r for r in rows if r]
        extra=[((idx[m],1),) for m in ms if 1<=len(m)<=2]
        res=[]
        for rs in (rows,rows+extra):
            nl=[]
            for p in PR:
                A=[[0]*len(ms) for _ in rs]
                for i,r in enumerate(rs):
                    for k,v in r: A[i][k]=v%p
                nl.append(len(ms)-nmod_mat(A,p).rank())
            res.append(nl)
        out[f'N{N}']={'unknowns':len(ms),'eqs':len(rows),'nullity_2primes':res[0],'nullity_with_size12_zero':res[1],
          'P1':'met' if res[0]==[f,f] else 'FAILED','P2':'met' if res[1]==[0,0] else 'FAILED'}
        if gen: out[f'N{N}']['P3']='met' if res[0]==[out['cor_count']]*2 else 'FAILED'
    print(json.dumps(out)); return out
R=[]
R.append(run('q1 d2',1,[[0,0],[0,0]],(2,3,4,6)))
R.append(run('q1 d3',1,[[0]*3]*3,(2,3,4,6)))
R.append(run('q2 all ones',2,[[0,0],[0,0]]))
R.append(run('q2 hadamard',2,[[0,0],[0,1]]))
R.append(run('q4 real hadamard d2',4,[[0,0],[0,2]]))
R.append(run('q4 real hadamard d4',4,[[0,0,0,0],[0,2,0,2],[0,0,2,2],[0,2,2,0]],(2,3)))
R.append(run('q3 d2 [[1,1],[1,w]]',3,[[0,0],[0,1]]))
R.append(run('q2 equal columns [[1,1],[-1,-1]]',2,[[0,0],[1,1]]))
R.append(run('q3 equal columns [[1,1],[w,w]]',3,[[0,0],[1,1]]))
R.append(run('q4 B=[[1,1],[1,-1]]*i-mix [[1,i],[1,-i]]',4,[[0,1],[0,3]]))
R.append(run('q4 fourier d4',4,[[ (z*y)%4 for y in range(4)] for z in range(4)],(2,3)))
R.append(run('q6 d4 paper example (3=q/2 in U)',6,[[0,0,0,0],[0,0,3,3],[0,3,1,4],[0,3,4,1]],(2,3)))
R.append(run('q6 d3 paper example',6,[[0,0,3],[0,2,1],[0,4,5]],(2,3)))
import os
assert not os.path.exists('results.json')
json.dump(R,open('results.json','w'),indent=1)
