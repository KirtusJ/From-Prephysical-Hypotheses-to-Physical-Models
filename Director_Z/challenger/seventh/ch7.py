"""Challenger 7 program. Exact arithmetic (integer ranks via python-flint). Seed 20261113.
PREDICATES (fixed before first run):
P1 abelian, any B, d>=2: nullity of (MBL) on multisets of size<=3 == |J0| + #{unordered {psi,lam}: psi*lam in J0, psi in U}.
P2 abelian: |J0|==|C|/|C_B|; U==U^-1; U*J0==U; trivial not in U; U is a union of same-kernel classes.
P3 C2xC2 examples: ex1 entries generate C, U = 3 nontrivial chars, nullity 4; ex2 entries generate C, U = {char with kernel {1,b}}, nullity 2.
P4 nonabelian (S3,Q8), hypothesis H==C tested per instance: nullity(size<=3) == 1 + sum over rho in U of (real: d(d+1)/2, quaternionic: d(d-1)/2, complex pair: d^2).
P5 all instances: nullity at size bound 2 == nullity at size bound 3 (and bound 4 where run).
P6 linear lemma over GF(2), V=F_2^3, all T, all subspaces W: hypothesis T^-1(W) subset W tested; then im T + W == V.
P7 S3 remark examples: [[1,c],[1,t]]: U={sign}, nullity 2. Fourier(c) degree 3 with rows/cols multiplied by generators,
   four side conventions (row L/R, col L/R), hypothesis H==C tested: U=={rho2} and nullity 4.
P8 S3: sign and rho2 both in U  =>  6 | d (count qualifying).
P9 nonabelian, any H: dimension of linear solutions (nullity at size bound 1 minus F(0) unknown... i.e. size-1 law) == |C|/|H|. 
"""
import itertools, random, os, sys, json
from math import gcd
import flint
random.seed(20261113)
OUT='results_ch7.txt'
if os.path.exists(OUT): sys.exit('refusing to overwrite '+OUT)
log=[]
cnt={}
def rec(p,ok,info):
    c=cnt.setdefault(p,[0,0]); c[0 if ok else 1]+=1
    log.append(f"{p} {'MET' if ok else 'FAILED'} {info}")

class Grp:
    def __init__(s,els,mul):
        s.els=els; s.n=len(els); ix={e:i for i,e in enumerate(els)}
        s.ix=ix; s.mul=[[ix[mul(a,b)] for b in els] for a in els]
        s.id=[i for i in range(s.n) if all(s.mul[i][j]==j for j in range(s.n))][0]
        s.inv=[[j for j in range(s.n) if s.mul[i][j]==s.id][0] for i in range(s.n)]
    def gen(s,S):
        H={s.id}|set(S)
        while True:
            H2=H|{s.mul[a][b] for a in H for b in H}
            if H2==H: return H
            H=H2

def nullity(G,B,S):
    d=len(B); types=[(y,h) for y in range(d) for h in range(G.n)]
    ms=[tuple(c) for k in range(S+1) for c in itertools.combinations_with_replacement(range(G.n),k)]
    ix={m:i for i,m in enumerate(ms)}
    rows=set()
    for k in range(S+1):
        for c in itertools.combinations_with_replacement(types,k):
            r={}
            for z in range(d):
                w=tuple(sorted(G.mul[B[z][y]][h] for (y,h) in c))
                r[ix[w]]=r.get(ix[w],0)+1
            for y in range(d):
                m=tuple(sorted(h for (yy,h) in c if yy==y))
                r[ix[m]]=r.get(ix[m],0)-d
            t=tuple(sorted((i,v) for i,v in r.items() if v))
            if t: rows.add(t)
    rows=list(rows)
    M=flint.fmpz_mat(len(rows),len(ms))
    for i,t in enumerate(rows):
        for j,v in t: M[i,j]=v
    return len(ms)-M.rank()

# ---------- cyclotomic zero test
def prem(p,q):
    p=p[:]
    while len(p)>=len(q):
        c=p[-1]
        if c:
            for i in range(len(q)): p[len(p)-len(q)+i]-=c*q[i]
        p.pop()
    return p
def pdiv(p,q):
    p=p[:]; out=[0]*(len(p)-len(q)+1)
    while len(p)>=len(q):
        c=p[-1]; out[len(p)-len(q)]=c
        for i in range(len(q)): p[len(p)-len(q)+i]-=c*q[i]
        p.pop()
    assert not any(p); return out
_cy={}
def cyc(n):
    if n not in _cy:
        p=[-1]+[0]*(n-1)+[1]
        for dd in range(1,n):
            if n%dd==0: p=pdiv(p,cyc(dd))
        _cy[n]=p
    return _cy[n]
def rootsum_zero(exps,e):
    p=[0]*e
    for x in exps: p[x%e]+=1
    if e==1: return sum(p)==0
    return not any(prem(p,cyc(e)))

# ---------- abelian
def abgrp(ns):
    els=list(itertools.product(*[range(n) for n in ns]))
    return Grp(els,lambda a,b:tuple((x+y)%n for x,y,n in zip(a,b,ns)))
def lcm(a,b): return a*b//gcd(a,b)
def abel_data(G,ns,B):
    e=1
    for n in ns: e=lcm(e,n)
    d=len(B)
    chars=list(itertools.product(*[range(n) for n in ns]))
    def ex(k,h): return sum(ki*hi*(e//n) for ki,hi,n in zip(k,G.els[h],ns))%e
    J0=[k for k in chars if all(ex(k,B[z][y])==0 for z in range(d) for y in range(d))]
    U=[k for k in chars if all(rootsum_zero([ex(k,B[z][y])-ex(k,B[z][yp]) for z in range(d)],e) for y in range(d) for yp in range(d) if y!=yp)]
    mulc=lambda a,b:tuple((x+y)%n for x,y,n in zip(a,b,ns))
    invc=lambda a:tuple((-x)%n for x,n in zip(a,ns))
    ker=lambda k:frozenset(h for h in range(G.n) if ex(k,h)==0)
    pairs={frozenset((p,l)) for p in U for l in chars if mulc(p,l) in J0}
    triv=tuple(0 for _ in ns)
    H=G.gen({B[z][y] for z in range(d) for y in range(d)})
    p2=(len(J0)*len(H)==G.n and set(U)=={invc(u) for u in U} and {mulc(u,j) for u in U for j in J0}==set(U)
        and triv not in U and all((k in U) for u in U for k in chars if ker(k)==ker(u)))
    return J0,U,len(J0)+len(pairs),p2,H,ker

def randB(G,d,norm):
    B=[[random.randrange(G.n) for _ in range(d)] for _ in range(d)]
    if norm:
        for i in range(d): B[0][i]=G.id; B[i][0]=G.id
    return B

abgroups=[((2,2),[2,3,4]),((6,),[2,3]),((2,4),[2,3,4]),((3,3),[2,3]),((2,2,2),[2,4])]
for ns,ds in abgroups:
    G=abgrp(ns); insts=[]
    for d in ds:
        for t in range(6): insts.append(randB(G,d,t%2==0))
    # structured: pairing matrices B_zy = "z*y" bilinear for products of equal cyclic, and Kronecker of 2x2
    if ns==(2,2):
        f=lambda a,b:G.ix[(a,b)]
        insts.append([[f(0,0)]*4,[f(0,0),f(1,0),f(0,1),f(1,1)],[f(0,0),f(0,1),f(1,1),f(1,0)],[f(0,0),f(1,1),f(1,0),f(0,1)]])
        insts.append([[f(0,0)]*4,[f(0,0),f(0,0),f(1,0),f(1,0)],[f(0,0),f(1,0),f(0,0),f(1,0)],[f(0,0),f(1,0),f(1,0),f(0,1)]])
        insts.append([[f(0,0),f(0,0)],[f(0,0),f(1,0)]]); insts.append([[f(0,0),f(0,1)],[f(1,0),f(0,0)]])
    if ns==(2,4):
        f=lambda a,b:G.ix[(a,b)]
        insts.append([[f(0,0),f(0,0)],[f(0,0),f(0,2)]]); insts.append([[f(0,0),f(0,0)],[f(0,0),f(1,2)]])
        insts.append([[f(0,0),f(0,1)],[f(0,1),f(0,0)]]); insts.append([[f(0,0),f(1,1)],[f(0,1),f(1,0)]])
        insts.append([[f(0,0)]*4,[f(0,0),f(1,0),f(0,2),f(1,2)],[f(0,0),f(0,2),f(1,0),f(1,2)],[f(0,0),f(1,2),f(1,2),f(0,0)]])
    if ns==(3,3):
        f=lambda a,b:G.ix[(a,b)]
        insts.append([[f(0,0)]*3,[f(0,0),f(1,0),f(2,0)],[f(0,0),f(2,0),f(1,0)]])
        insts.append([[f(0,0)]*3,[f(0,0),f(1,1),f(2,2)],[f(0,0),f(2,2),f(1,1)]])
        insts.append([[f(0,1)]*3,[f(0,0),f(1,0),f(2,0)],[f(0,0),f(2,0),f(1,0)]])
    if ns==(2,2,2):
        f=lambda a,b,c:G.ix[(a,b,c)]
        insts.append([[f(0,0,0),f(0,0,0)],[f(0,0,0),f(1,1,1)]])
        insts.append([[f(0,0,0)]*4,[f(0,0,0),f(1,0,0),f(0,1,0),f(1,1,0)],[f(0,0,0),f(0,1,0),f(1,1,0),f(1,0,0)],[f(0,0,0),f(1,1,0),f(1,0,0),f(0,1,1)]])
    for B in insts:
        d=len(B); J0,U,dim,p2,H,ker=abel_data(G,ns,B)
        n3=nullity(G,B,3); n2=nullity(G,B,2)
        info=f"C={ns} B={[[G.els[x] for x in r] for r in B]} |J0|={len(J0)} U={U} formula={dim} null2={n2} null3={n3}"
        rec('P1',n3==dim,info); rec('P2',p2,info); rec('P5',n2==n3,info)
        if G.n<=4 and d<=3:
            n4=nullity(G,B,4); rec('P5',n4==n3,info+f" null4={n4}")
    if ns==(2,2):
        for name,B,expU,expdim in [('ex1',insts[-4],{(1,0),(0,1),(1,1)},4),('ex2',insts[-3],{(1,0)},2)]:
            J0,U,dim,p2,H,ker=abel_data(G,ns,B)
            n3=nullity(G,B,3)
            ok=len(H)==4 and set(U)==expU and n3==expdim
            if name=='ex2': ok=ok and ker((1,0))==frozenset({G.ix[(0,0)],G.ix[(0,1)]})
            rec('P3',ok,f"{name} gen={len(H)==4} U={U} null3={n3}")

# ---------- S3
perms=list(itertools.permutations(range(3)))
S3=Grp(perms,lambda a,b:tuple(a[b[i]] for i in range(3)))
def sgn(p): return -1 if sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2 else 1
def S3_U(B):
    d=len(B); res={'sign':True,'rho2':True}
    for y in range(d):
        for yp in range(d):
            if y==yp: continue
            E=[S3.mul[S3.inv[B[z][y]]][B[z][yp]] for z in range(d)]
            if sum(sgn(S3.els[g]) for g in E)!=0: res['sign']=False
            Mx=[[0]*3 for _ in range(3)]
            for g in E:
                p=S3.els[g]
                for i in range(3): Mx[p[i]][i]+=1
            # restricted to sum-zero subspace
            for v in ([1,-1,0],[0,1,-1]):
                if any(sum(Mx[i][j]*v[j] for j in range(3)) for i in range(3)): res['rho2']=False
    return res
def S3_formula(B):
    u=S3_U(B); return 1+(1 if u['sign'] else 0)+(3 if u['rho2'] else 0),u
c=S3.ix[(1,2,0)]; c2=S3.mul[c][c]; t=S3.ix[(1,0,2)]; e=S3.id; t2=S3.mul[c][t]; t3=S3.mul[c2][t]
def run_na(G,name,B,formula,tag=''):
    d=len(B); H=G.gen({B[z][y] for z in range(d) for y in range(d)})
    n3=nullity(G,B,3); n2=nullity(G,B,2)
    # linear part: a with sum_z a_{B_zy h}=d a_h
    M=flint.fmpz_mat(d*G.n,G.n)
    for y in range(d):
        for h in range(G.n):
            for z in range(d): M[y*G.n+h,G.mul[B[z][y]][h]]=int(M[y*G.n+h,G.mul[B[z][y]][h]])+1
            M[y*G.n+h,h]=int(M[y*G.n+h,h])-d
    ldim=G.n-M.rank()
    f,u=formula(B)
    info=f"{name}{tag} B={[[G.els[x] for x in r] for r in B]} |H|={len(H)} U={u} formula={f} null2={n2} null3={n3} ldim={ldim}"
    rec('P9',ldim*len(H)==G.n,info); rec('P5',n2==n3,info)
    if len(H)==G.n: rec('P4',n3==f,info)
    else: log.append('P4 NOT-QUALIFYING(H!=C) measured only '+info)
    return n3,u,len(H)==G.n
n3,u,q=run_na(S3,'S3',[[e,c],[e,t]],S3_formula,' remark-ex1'); rec('P7',q and u=={'sign':True,'rho2':False} and n3==2,f"ex1 U={u} null={n3}")
gens=[(t,t2,c),(e,t,c),(t,e,e),(c,t,t3)]
for rs in gens:
  for ss in [(e,e,e),(e,t,c),(t,t2,t3),(c,c2,t)]:
    for rside in 'LR':
      for cside in 'LR':
        B=[[None]*3 for _ in range(3)]
        for z in range(3):
            for y in range(3):
                x=[e,c,c2][(z*y)%3]
                x=S3.mul[rs[z]][x] if rside=='L' else S3.mul[x][rs[z]]
                x=S3.mul[ss[y]][x] if cside=='L' else S3.mul[x][ss[y]]
                B[z][y]=x
        n3,u,q=run_na(S3,'S3',B,S3_formula,f' fourier rows{rside} cols{cside}')
        if q: rec(f'P7-row{rside}-col{cside}',u=={'sign':False,'rho2':True} and n3==4,f"U={u} null={n3} B={[[S3.els[x] for x in r] for r in B]}")
nq=0
for d in (2,3,4):
    for k in range(8 if d<4 else 4):
        B=randB(S3,d,k%2==0); n3,u,q=run_na(S3,'S3',B,S3_formula,' random')
for B in ([[e,e],[e,t]],[[e,t],[c,t2]],[[e,t],[t2,c]],[[e,e,e],[e,c,c2],[e,c2,c]],[[t,e,e],[e,c,c2],[e,c2,c]],[[e,c],[t,t2]],[[e,t],[t,e]]):
    run_na(S3,'S3',B,S3_formula,' chosen')
# P8: search for both in U, d=2..6 random + record
both=0;tot=0
for d in (2,3,4,5,6,7):
    for k in range(4000):
        B=randB(S3,d,True); u=S3_U(B); tot+=1
        if u['sign'] and u['rho2']:
            both+=1; rec('P8',d%6==0,f"d={d} B={B}")
log.append(f"P8 searched {tot} random normalized S3 matrices d=2..7, qualifying (both in U): {both}")

# ---------- Q8
units=[(s,k) for s in (1,-1) for k in range(4)]
def qv(u):
    v=[0,0,0,0]; v[u[1]]=u[0]; return v
def qmul(a,b):
    a1,b1,c1,d1=a; a2,b2,c2_,d2=b
    return [a1*a2-b1*b2-c1*c2_-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2_, a1*c2_-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2_-c1*b2+d1*a2]
def umul(a,b):
    v=qmul(qv(a),qv(b)); k=[i for i in range(4) if v[i]][0]; return (v[k],k)
Q8=Grp(units,umul)
def Q8_formula(B):
    d=len(B); chars=[(a,b) for a in (1,-1) for b in (1,-1)]
    def chv(ch,g):
        s,k=Q8.els[g]; return [1,ch[0],ch[1],ch[0]*ch[1]][k]
    okc={ch:True for ch in chars}; okr=True
    for y in range(d):
        for yp in range(d):
            if y==yp: continue
            E=[Q8.mul[Q8.inv[B[z][y]]][B[z][yp]] for z in range(d)]
            for ch in chars:
                if sum(chv(ch,g) for g in E)!=0: okc[ch]=False
            v=[0,0,0,0]
            for g in E:
                s,k=Q8.els[g]; v[k]+=s
            if any(v): okr=False
    return 1+sum(okc.values())+(1 if okr else 0),{'chars':[ch for ch in chars if okc[ch]],'rho2':okr}
o,i_,j_,k_=[Q8.ix[(1,x)] for x in range(4)]; mo,mi,mj,mk=[Q8.ix[(-1,x)] for x in range(4)]
for B in ([[o,i_],[j_,k_]],[[o,i_],[o,j_]],[[o,i_],[j_,mk]],[[o,o],[i_,j_]],[[o,o],[o,mo]],[[i_,j_],[j_,i_]]):
    run_na(Q8,'Q8',B,Q8_formula,' chosen')
for k in range(6): run_na(Q8,'Q8',randB(Q8,2,k%2==0),Q8_formula,' random')

# ---------- P6 lemma over GF(2), dim 3
vecs=list(range(8))
def span(gs):
    S={0}
    for g in gs: S|={s^g for s in S}
    return frozenset(S)
subs={span(gs) for r in range(4) for gs in itertools.combinations(range(1,8),r)}
qual=0;tot=0
for cols in itertools.product(range(8),repeat=3):
    def T(v):
        r=0
        for b in range(3):
            if v>>b&1: r^=cols[b]
        return r
    im=frozenset(T(v) for v in vecs)
    for W in subs:
        tot+=1
        pre={v for v in vecs if T(v) in W}
        if pre<=W:
            qual+=1
            ok=len({a^b for a in im for b in W})==8
            c_=cnt.setdefault('P6',[0,0]); c_[0 if ok else 1]+=1
            if not ok: log.append(f"P6 FAILED cols={cols} W={sorted(W)}")
log.append(f"P6 instances {tot}, qualifying (T^-1(W) subset W): {qual}")
with open(OUT,'x') as f:
    f.write('\n'.join(log)+'\n\nSUMMARY met/failed\n'+json.dumps(cnt,indent=1)+'\n')
print(json.dumps(cnt)); print([l for l in log if 'FAILED' in l][:12]); print([l for l in log if l.startswith(('P8 s','P6 i'))])
