"""Challenger program A and D for THEOREM_T (own program; predicates fixed before first run).

Unknowns F_y(m), y=(x,R),(x,L), m in [0..2B]^2 \ {(0,0)} (F_y(0,0)=0).
Equations (E), factor 2: F_{x+1,R}(U+V)+F_{x-1,L}(U+JV) = 2F_{x,R}(U)+2F_{x,L}(V), U,V in [0..B]^2.
Rank is computed mod two primes p1,p2. nullity over Q <= nullity mod p; the known family gives a lower bound,
so "nullity mod p == lower bound" is an exact statement over Q.
"restricted dimension" = nullity(A) - nullity(A restricted to columns outside the inner set)
 = dimension of the solution space restricted to the inner set (box [0..B]^2, and for D sites |x|<=1).

PREDICATES
 A1 (ring N=1..14, B=1,2,3): restricted dimension to box [0..B]^2 at all sites == 2 (both primes).
 A2: the two functions (p+q),(p-q)^2 at all vertices lie in the kernel (integer check) and are independent on the box.
 D1 (line window x in [-W..W], equations at |x|<=W-1, B=1,2, W=3..7): restricted dimension to (|x|<=1, box B)
     is the same for all W>=W0 (stabilises); value reported (measured).
 D2: the five known solutions (p+q), (p-q)^2, x(p+q), and (p-q)f_x at R / (p-q)f_{x-1} at L for the two
     Fibonacci-type sequences f (f_{x+1}=f_x+f_{x-1}; seeds (0,1),(1,0)) lie in the kernel and are independent
     on the inner set; D2 met if stabilised restricted dimension == 5. If it is larger, a solution outside the
     stated family plus Remark (a) exists and must be examined for boundedness below (possible counterexample to (ii)).
Result file: resultAD.txt, opened in mode 'x'.
"""
import numpy as np, itertools, sys
P=[2147483629, 2147483587]
def rank_mod(M,p):
    M=M.copy()%p; r=0; rows,cols=M.shape
    for c in range(cols):
        piv=np.nonzero(M[r:,c])[0]
        if len(piv)==0: continue
        i=r+piv[0]
        if i!=r: M[[r,i]]=M[[i,r]]
        inv=pow(int(M[r,c]),p-2,p)
        M[r]=(M[r]*inv)%p
        nz=np.nonzero(M[:,c])[0]; nz=nz[nz!=r]
        if len(nz):
            M[nz]=(M[nz]-(M[nz,c][:,None]*M[r][None,:])%p)%p
        r+=1
        if r==rows: break
    return r
def build(sites,eqsites,B,nb):
    ms=[(p,q) for p in range(2*B+1) for q in range(2*B+1) if (p,q)!=(0,0)]
    idx={}
    for x in sites:
        for s in 'RL':
            for m in ms: idx[(x,s,m)]=len(idx)
    rows=[]
    box=[(p,q) for p in range(B+1) for q in range(B+1)]
    for x in eqsites:
        for U in box:
            for V in box:
                r={}
                def add(k,c):
                    if k[2]==(0,0): return
                    r[idx[k]]=r.get(idx[k],0)+c
                xp,xm=nb(x)
                add((xp,'R',(U[0]+V[0],U[1]+V[1])),1)
                add((xm,'L',(U[0]+V[1],U[1]+V[0])),1)
                add((x,'R',U),-2); add((x,'L',V),-2)
                if r: rows.append(r)
    A=np.zeros((len(rows),len(idx)),dtype=np.int64)
    for i,r in enumerate(rows):
        for j,c in r.items(): A[i,j]=c
    return A,idx
def restricted(A,idx,inner):
    out=[]
    cols=[j for k,j in idx.items() if not inner(k)]
    for p in P:
        n=A.shape[1]-rank_mod(A,p)
        n0=len(cols)-rank_mod(A[:,cols],p) if cols else 0
        out.append((n,n-n0))
    return out
def vec(idx,f):
    v=np.zeros(len(idx),dtype=object)
    for k,j in idx.items(): v[j]=f(*k)
    return v
out=open('resultAD.txt','x')
def W_(s):
    print(s); out.write(s+'\n'); out.flush()
met=fail=meas=0
W_('PART A: rings. columns: N B unknowns equations [(nullity, restricted dim) per prime] A2 verdict')
for B in (1,2,3):
    for N in range(1,15):
        sites=list(range(N))
        A,idx=build(sites,sites,B,lambda x:((x+1)%N,(x-1)%N))
        res=restricted(A,idx,lambda k: k[2][0]<=B and k[2][1]<=B)
        Ao=A.astype(object)
        v1=vec(idx,lambda x,s,m:m[0]+m[1]); v2=vec(idx,lambda x,s,m:(m[0]-m[1])**2)
        a2=all(x==0 for x in Ao.dot(v1)) and all(x==0 for x in Ao.dot(v2))
        ok=all(r[1]==2 for r in res) and a2
        if ok: met+=1
        else: fail+=1
        W_(f'{N} {B} {A.shape[1]} {A.shape[0]} {res} A2={a2} {"MET" if ok else "FAILED"}')
W_(f'PART A counts: met {met} failed {fail}')
W_('PART D: line window. columns: W B unknowns equations [(nullity, restricted dim to |x|<=1, box B)] known5-in-kernel')
dres={}
for B in (1,2):
    for Wd in range(3,8):
        sites=list(range(-Wd,Wd+1)); eqs=list(range(-Wd+1,Wd))
        A,idx=build(sites,eqs,B,lambda x:(x+1,x-1))
        res=restricted(A,idx,lambda k: abs(k[0])<=1 and k[2][0]<=B and k[2][1]<=B)
        Ao=A.astype(object)
        def fib(a,b):
            f={0:a,1:b}
            for x in range(1,Wd+2): f[x+1]=f[x]+f[x-1]
            for x in range(0,-Wd-3,-1): f[x-1]=f[x+1]-f[x]
            return f
        fs=[fib(0,1),fib(1,0)]
        known=[lambda x,s,m:m[0]+m[1], lambda x,s,m:(m[0]-m[1])**2, lambda x,s,m:x*(m[0]+m[1])]
        for f in fs:
            known.append(lambda x,s,m,f=f:(m[0]-m[1])*(f[x] if s=='R' else f[x-1]))
        kin=all(all(t==0 for t in Ao.dot(vec(idx,g))) for g in known)
        dres[(B,Wd)]=res
        W_(f'{Wd} {B} {A.shape[1]} {A.shape[0]} {res} known5={kin}')
for B in (1,2):
    vals=[tuple(r[1] for r in dres[(B,Wd)]) for Wd in range(3,8)]
    W_(f'D1 B={B}: restricted dims by W=3..7: {vals}; stabilised from W>=4: {len(set(vals[1:]))==1}; D2 (==5): {all(v==(5,5) for v in vals[1:])}')
out.close()
