"""Predicates fixed before run (P1..P13). Exact arithmetic (sympy / integers / Fractions).
P1 coefficient of b0*b1*b2 in sum_z (b0+w^z b1+w^2z b2)^3 is 18; two-input instances of BL hold for a^3 (d=q=3 Fourier), three-input fails.
P2 Re(5^4)=625, Re((3+4i)^4)=-527; Re(a^4) satisfies (V) for (1,i,-1,-i) on Gaussian box |re|,|im|<=4.
P3 U sets: example1 {1,2,4,5}, example2 {1,3,5}; B^(1)*B^(1)=d in both.
P4 real Hadamard d=2,4, q=4: |a|^2, Re a^2, Im a^2 all satisfy BL on random Gaussian integer inputs.
P5 local spectra: q=1,2 full; q=4 four points; q=3, 5..12 empty (exact, angles in units of pi/ (4q) grid + interval logic).
P6 abundance example: D aperiodic, Dhat strongly connected, period 2, at each length 1..40 exactly <=2 gains per vertex.
P7 M-identity symbolic for general k.
P8 fitted exponent of row 2 of Table avg vs period is -1.1 (rounded).
P9 real quadratic forms count N(2N+1); phi(q)/2==1 iff q in {3,4,6} for 3<=q<=200.
P10 q=4 Hadamard: sigma_2 and Re sigma_1^2 satisfy MBL; q=2 all-ones: n_{g} count satisfies MBL (random multisets).
P11 d=4 normalized real Hadamard, q=2, R=Z: two-input instances of BL alone on box [-n,n] leave solution space of dimension 1 (would contradict 'two inputs only: conclusion false for d>=3').
P12 thm:multiset dimension formula vs exact nullity of truncated system (sizes<=3) for random matrices q<=4,d=2,3; hypothesis d>=2 always true; report count.
P13 d=3 elimination and Mk derivation numerically consistent: quadratic f satisfies both displayed equations.
"""
import itertools, random, cmath, math
from fractions import Fraction
import sympy as sp
random.seed(1)
res={}
# P1
b0,b1,b2=sp.symbols('b0 b1 b2'); w=sp.exp(2*sp.pi*sp.I/3)
e=sp.expand(sum((b0+w**z*b1+w**(2*z)*b2)**3 for z in range(3)))
e=sp.simplify(e); co=sp.simplify(sp.Poly(e,b0,b1,b2).coeff_monomial(b0*b1*b2))
two=all(sp.simplify(sp.expand(sum((b0+w**(z*k)*b1)**3 for z in range(3))-3*b0**3-3*b1**3))==0 for k in (1,2))
three=sp.simplify(e-3*(b0**3+b1**3+b2**3))
res['P1']=(co,two,three)
# P2
f=lambda a:(a**4).real
G=[complex(x,y) for x in range(-4,5) for y in range(-4,5)]
okV=all(abs(sum(f(a+u*b) for u in (1,1j,-1,-1j))-4*f(a)-4*f(b))<1e-6 for a in G for b in G)
res['P2']=(f(5+0j),f(3+4j),okV)
# P3
def Uset(Bexp,q):
    d=len(Bexp);U=[]
    for j in range(q):
        ok=True
        for y in range(d):
            for y2 in range(d):
                # sum_z zeta^{j(B_zy - B_zy2)} exact via sympy
                s=sp.nsimplify(sum(sp.exp(2*sp.pi*sp.I*sp.Rational(j*(Bexp[z][y]-Bexp[z][y2]),q)) for z in range(d)))
                s=sp.simplify(s)
                if s!=(d if y==y2 else 0): ok=False
        if ok:U.append(j)
    return U
B1=[[0,0,3],[0,2,3+4],[0,4,3+2]]   # 1,1,-1 ; 1,w,-w^2 ; 1,w^2,-w ; w=zeta^2
B2=[[0,0,0,0],[0,0,3,3],[0,3,1,4],[0,3,4,1]]
res['P3']=(Uset(B1,6),Uset(B2,6))
# P4
H2=[[1,1],[1,-1]];H4=[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
forms=[lambda a:abs(a)**2,lambda a:(a*a).real,lambda a:(a*a).imag]
ok4=True
for H in (H2,H4):
    d=len(H)
    for _ in range(500):
        be=[complex(random.randint(-9,9),random.randint(-9,9)) for _ in range(d)]
        for F in forms:
            if abs(sum(F(sum(H[z][y]*be[y] for y in range(d))) for z in range(d))-d*sum(F(x) for x in be))>1e-6: ok4=False
res['P4']=ok4
# P5 exact: angle theta in spectrum iff dist(theta mod pi, 0) <= pi/4. use rationals in units of pi.
def inS(t): # t Fraction, angle/pi
    t=t%1
    return min(t,1-t)<=Fraction(1,4)
out={}
for q in range(1,13):
    grid=[Fraction(k,8*q*3) for k in range(0,2*8*q*3)]
    pts=[t for t in grid if all(inS(t+Fraction(2*j,q)) for j in range(q))]
    out[q]=len(pts) if len(pts)<10 else 'many(%d of %d)'%(len(pts),len(grid))
    if q==4: out['q4pts']=[str(p) for p in pts]
res['P5']=out
# P6
arcs=[(0,2,0),(0,3,1),(1,0,1),(1,1,3),(2,0,0),(2,1,0),(3,2,0),(3,3,3)]
q=4
import numpy as np
A=np.zeros((4,4),complex)
for s,t,e_ in arcs:A[t,s]=1j**e_
normp=np.allclose(A.conj().T@A,2*np.eye(4))
def period_sc(nodes,succ):
    # BFS levels gcd; strong connectivity
    def reach(s,succ):
        seen={s};st=[s]
        while st:
            u=st.pop()
            for v in succ[u]:
                if v not in seen:seen.add(v);st.append(v)
        return seen
    pred={n:[] for n in nodes}
    for u in nodes:
        for v in succ[u]:pred[v].append(u)
    s=nodes[0]
    sc=len(reach(s,succ))==len(nodes)==len(reach(s,pred))
    lev={s:0};st=[s];g=0
    while st:
        u=st.pop(0)
        for v in succ[u]:
            if v not in lev:lev[v]=lev[u]+1;st.append(v)
            else:g=math.gcd(g,lev[u]+1-lev[v])
    return sc,g
succD={x:[t for s,t,_ in arcs if s==x] for x in range(4)}
nodesH=[(x,g) for x in range(4) for g in range(4)]
succH={(x,g):[(t,(g+e_)%4) for s,t,e_ in arcs if s==x] for (x,g) in nodesH}
scD,r0=period_sc(list(range(4)),succD); scH,r=period_sc(nodesH,succH)
mx=0
for start in range(4):
    cur={(start,0)}
    for L in range(1,41):
        cur={v for u in cur for v in succH[u]}
        for x in range(4):
            mx=max(mx,len([1 for (y,g) in cur if y==x]))
res['P6']=dict(normp=normp,scD=scD,r0=r0,scH=scH,r=r,max_gains_per_vertex_per_length=mx)
# P7
k=sp.symbols('k')
fa={n:sp.Symbol(n) for n in ['f_amb','f_akb','f_a','f_b','f_mb','f_ak1b','f_apb']}
M_ab=k*fa['f_amb']+fa['f_akb']-(k+1)*fa['f_a']-k*(k+1)*fa['f_b']
M_apb_b=k*fa['f_a']+fa['f_ak1b']-(k+1)*fa['f_apb']-k*(k+1)*fa['f_b']
M_akb_mb=k*fa['f_ak1b']+fa['f_a']-(k+1)*fa['f_akb']-k*(k+1)*fa['f_mb']
lhs=(k+1)*M_ab-k*M_apb_b+M_akb_mb
rhs=k*(k+1)*(fa['f_apb']+fa['f_amb']-2*fa['f_a']-fa['f_b']-fa['f_mb'])
res['P7']=sp.expand(lhs-rhs)
# P8
per=[64,128,256,512,1024,2048];row=[0.0735,0.0273,0.0135,0.0071,0.0029,0.0016]
res['P8']=float(np.polyfit(np.log(per),np.log(row),1)[0])
# P9
res['P9']=[q_ for q_ in range(3,201) if sp.totient(q_)==2]
# P10
def mbl_ok(F,Bexp,q,trials=300,maxc=4):
    d=len(Bexp)
    for _ in range(trials):
        ms=[[random.randint(0,maxc) for _ in range(q)] for _ in range(d)]
        tot=0
        for z in range(d):
            wv=[0]*q
            for y in range(d):
                for h in range(q): wv[(h+Bexp[z][y])%q]+=ms[y][h]
            tot+=F(wv)
        if abs(tot-d*sum(F(m) for m in ms))>1e-6:return False
    return True
sig=lambda j,q:(lambda m:sum(n*cmath.exp(2j*cmath.pi*j*h/q) for h,n in enumerate(m)))
H4e=[[0 if v==1 else 2 for v in rw] for rw in H4]
res['P10']=dict(sigma2=mbl_ok(lambda m:sig(2,4)(m).real,H4e,4),Re_s1sq=mbl_ok(lambda m:(sig(1,4)(m)**2).real,H4e,4),
   Im_s1sq=mbl_ok(lambda m:(sig(1,4)(m)**2).imag,H4e,4),
   count_gain1_q2_allones=mbl_ok(lambda m:m[0],[[0,0],[0,0]],2), count_q2_allones_d3=mbl_ok(lambda m:m[0],[[0]*3]*3,2))
# P11 two-input BL for H4 over Z on box
n=6; idx={v:i for i,v in enumerate(range(-3*n,3*n+1))}
rows=[]
for y,y2 in itertools.combinations(range(4),2):
    for a in range(-n,n+1):
        for b in range(-n,n+1):
            r_=[0]*len(idx)
            for z in range(4): r_[idx[H4[z][y]*a+H4[z][y2]*b]]+=1
            r_[idx[a]]-=4;r_[idx[b]]-=4; r_[idx[0]]-=4*2  # other two inputs zero: d*Phi(0) each
            rows.append(r_)
# also the continuation sum has no extra terms (all 4 outputs listed)
Mx=sp.Matrix(rows); 
# restrict unknowns to those in [-n,n] by counting nullity on columns appearing with |v|<=n: use equations with all args within [-n,n]
rows2=[r_ for r_ in rows if all(r_[idx[v]]==0 for v in idx if abs(v)>n)]
cols=[idx[v] for v in range(-n,n+1)]
M2=sp.Matrix([[r_[c] for c in cols] for r_ in rows2])
res['P11']=dict(unknowns=len(cols),equations=len(rows2),nullity=len(cols)-M2.rank())
# P12
def multis(q,S):
    return [m for m in itertools.product(range(S+1),repeat=q) if sum(m)<=S]
def formula(Bexp,q):
    d=len(Bexp)
    J0=[j for j in range(q) if all((j*Bexp[z][y])%q==0 for z in range(d) for y in range(d))]
    U=Uset(Bexp,q)
    pairs={frozenset((j,l)) for j in U for l in range(q) if (j+l)%q in J0}
    return len(J0)+len(pairs)
cnt=0;agree=0;bad=[]
S=3
for q in (1,2,3,4):
    for d in (2,3):
        for _ in range(6):
            Bexp=[[random.randrange(q) for _ in range(d)] for _ in range(d)]
            if q>1 and random.random()<0.4: # force some Fourier-type
                Bexp=[[ (z*y*(q//d if q%d==0 else 1))%q for y in range(d)] for z in range(d)]
            ML=multis(q,S); ix={m:i for i,m in enumerate(ML)}
            rows=[]
            for ms in itertools.product(ML,repeat=d):
                if sum(sum(m) for m in ms)>S: continue
                r_=[0]*len(ML)
                for z in range(d):
                    wv=[0]*q
                    for y in range(d):
                        for h in range(q): wv[(h+Bexp[z][y])%q]+=ms[y][h]
                    r_[ix[tuple(wv)]]+=1
                for m in ms:r_[ix[m]]-=d
                rows.append(r_)
            nul=len(ML)-sp.Matrix(rows).rank()
            cnt+=1
            if nul==formula(Bexp,q):agree+=1
            else:bad.append((q,d,Bexp,nul,formula(Bexp,q)))
res['P12']=dict(instances=cnt,qualify_d_ge_2=cnt,agree=agree,bad=bad)
# P13
ok=True
for _ in range(200):
    a=complex(random.randint(-9,9),random.randint(-9,9));b=complex(random.randint(-9,9),random.randint(-9,9))
    g=lambda x:abs(x)**2
    for d in (3,5,7):
        kk=d-2
        if abs(g(a+(d-1)*b)+(d-1)*g(a-b)-d*g(a)-d*(d-1)*g(b))>1e-6:ok=False
        if abs(kk*g(a-b)+g(a+kk*b)-(kk+1)*g(a)-kk*(kk+1)*g(b))>1e-6:ok=False
res['P13']=ok
for k_,v in res.items():print(k_,v)
