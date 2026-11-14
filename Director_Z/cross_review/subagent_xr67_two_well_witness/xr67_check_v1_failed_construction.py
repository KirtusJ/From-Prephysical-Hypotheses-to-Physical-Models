"""xr67: own exact check of Director G's two-well witness (note text only as input).
Seed 20261113 (no randomness is used; all grids are exhaustive). No floats. Result file opened 'x'.
Arithmetic: Z[z]/(z^n-1), zero test by remainder modulo the cyclotomic polynomial Phi_n.
Convention: gains (a,b,c,d) on arcs R->R, R->L, L->R, L->L; start rail R; port = final rail
(two wells: site is fixed by parity); probability = |sum of gains|^2 / 2^t per original launch.

PREDICATES (fixed before first run)
P1  For beta=z^k, n<=24, gains (1,beta,1,-beta): 4*p2 = 2+2x and 8*p3 = 8-4x^2 exactly (x=Re beta);
    count gives 1/2, 1/2. Cubic: p2=1/4, p3=7/8.
P2  Normalisation hypothesis tested per instance: p_R+p_L=1 at t=1,2,3 for every (n,k). Report count.
A1  W_m(pure beta) == (x-m)^2 exactly for m=-1/2, every n<=24, k; W_m(count)=1+m^2=5/4.
A2  Since W is affine in (p2,p3) and weights sum to 1, W(mixture)=sum w_i (x_i-m)^2 + c(1+m^2).
    Search: any grid component other than Re beta=-1/2 with W=0?  Expect none. Any mixture
    (support<=2 over all grid phases, weights in sixths, c in quarters) with W=0 other than
    mixtures of beta*, conj beta* with c=0?  Expect none. Negative W: impossible by A1 (square of
    a real element, nonneg rational weights) -- recorded as argued, not searched numerically.
B1  All gain assignments (a,b,c,d) in powers of zeta_n, n<=12: 'unitary' (a*conj c + b*conj d = 0)
    iff rail-normalised at t=1,2,3. Count qualifying.
B2  For unitary assignments p2,p3 equal those of (1,u,1,-u) with u=bc/a^2 (so claim extends, target
    read as Re(bc/a^2)).  Expect true for all.
B3  MEASURE: non-unitary assignments (outside the stated hypothesis) whose unnormalised squared
    'rates' equal (1/4,7/8); list them. No expectation fixed.
B4  MEASURE: unitary assignments with phase NOT on arc R->L (b=1) reaching W=0; shows the witness
    reads the invariant bc/a^2, not 'the phase on a named arc'.
C1  Independent factors: observed q_j = eta_j p_j. For pure x=-1/2+d, d in {1/10,1/100,1/1000,-1/10},
    eta2=1/(2(1+x)), eta3=7/(8-4x^2) give observed (1/4,7/8) hence W_obs=0. Report etas; d>0 needs
    both eta<=1 (loss only).  Expect: false zero at arbitrarily small miscalibration.
C2  Common factor eta at both clocks: for h=1/eta, need S>=mu^2 with mu=h/2-1, S=2-7h/4, i.e.
    (h+4)(h-1)<=0. Expect: no false zero for eta<1 (loss), false zeros for eta>1; exhibit a two-point
    mixture for eta=1+e, e in {1/10,1/100,1/1000}, forward-computed.
C3  Common rail bias r=eta_R/eta_L (self-normalised reads p'=rp/(rp+1-p)): pure false zeros are roots
    of (2x+1)(5x^2+3x-1); mixtures: feasible iff 2r(1+3r)^2 >= (r+7)(1-3r)^2. Exhibit r=1-e mixtures.
C4  Grid phases n<=24: for each pure grid phase != target list (eta2,eta3) needed; report those with
    both <=1 and the one minimising max(1-eta2,1-eta3) (comparison by exact rational bracketing).
C5  Target under common loss eta: W_obs = 5(1-eta)/4 > 0 (target falsely rejected).
"""
import json, sys
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt
from sympy import cyclotomic_poly, Symbol, Poly
SEED=20261113
zs=Symbol('z')
_phi={}
def phi(n):
    if n not in _phi: _phi[n]=[int(c) for c in Poly(cyclotomic_poly(n,zs),zs).all_coeffs()][::-1]
    return _phi[n]
def red(v,n):
    v=list(v); p=phi(n); d=len(p)-1
    for i in range(len(v)-1,d-1,-1):
        c=v[i]
        if c:
            for j in range(d+1): v[i-d+j]-=c*p[j]
    return v[:d]
def iszero(v,n): return not any(red(v,n))
def mul(u,v,n):
    w=[0]*n
    for i,a in enumerate(u):
        if a:
            for j,b in enumerate(v):
                if b: w[(i+j)%n]+=a*b
    return w
def conj(u,n): return [u[(-i)%n] for i in range(n)]
def mono(k,n,s=1):
    v=[0]*n; v[k%n]=s; return v
def add(u,v): return [a+b for a,b in zip(u,v)]
def sc(u,c): return [c*a for a in u]
def const(c,n):
    v=[0]*n; v[0]=c; return v
def walk(g,n,t):
    """g: dict arc->(exponent,sign). returns {rail: amplitude sum vector}"""
    out={'R':[0]*n,'L':[0]*n}; cnt={'R':0,'L':0}
    for w in product('RL',repeat=t):
        r='R'; e=0; s=1
        for st in w:
            ee,ss=g[r+st]; e+=ee; s*=ss; r=st
        out[r][e%n]+=s; cnt[r]+=1
    return out,cnt
def norm2(u,n): return mul(u,conj(u,n),n)
res={'seed':SEED,'predicates':{},'failed':[]}
def rec(name,ok,**kw):
    res['predicates'][name]=dict(ok=ok,**kw)
    if ok is False: res['failed'].append(name)

# ---- P1, P2, A1
p1=True; p2ok=True; a1=True; ninst=0; zero_components=[]; nonzero=0
for n in range(1,25):
    for k in range(n):
        ninst+=1
        g={'RR':(0,1),'RL':(k,1),'LR':(0,1),'LL':(k,-1)}
        twox=add(mono(k,n),mono(-k,n))            # 2x
        fourx2=mul(twox,twox,n)                    # 4x^2
        P={}
        for t in (1,2,3):
            o,c=walk(g,n,t)
            nr=norm2(o['R'],n); nl=norm2(o['L'],n)
            if not iszero(add(add(nr,nl),const(-2**t,n)),n): p2ok=False
            if c['R']*2!=2**t: p1=False
            P[t]=nr
        if not iszero(add(P[2],sc(add(const(2,n),twox),-1)),n): p1=False
        if not iszero(add(P[3],sc(add(const(8,n),sc(fourx2,-1)),-1)),n): p1=False
        # W with m=-1/2: W = 2(1-p3) +(2p2-1) + 1/4 ; 8W = 16-2*N3 +4*N2-8+2 = 10 - 2 N3 + 4 N2... (p3=N3/8,p2=N2/4)
        W8=add(add(const(10,n),sc(P[3],-2)),sc(P[2],4))   # 8W
        sq=add(add(fourx2,sc(twox,2)),const(1,n))         # (2x+1)^2 = 4(x+1/2)^2 ; 8(x-m)^2 = 2*sq
        if not iszero(add(W8,sc(sq,-2)),n): a1=False
        if iszero(W8,n): zero_components.append((n,k))
        else: nonzero+=1
        if n==3 and k==1:
            cub=(iszero(add(P[2],const(-1,n)),n), iszero(add(P[3],const(-7,n)),n))
rec('P1',p1 and all(cub),instances=ninst,cubic_p2_is_1_4=cub[0],cubic_p3_is_7_8=cub[1])
rec('P2',p2ok,instances=ninst,qualifying=ninst if p2ok else None)
rec('A1',a1,instances=ninst,W_count='5/4')
tz=[(n,k) for n,k in zero_components if not (n%3==0 and k in (n//3,2*n//3))]
# A2 mixture search by components
comps=[(n,k) for n in range(1,25) for k in range(n)]
zset=set(zero_components)
nm=0; falsezero=[]
for i in range(len(comps)):
    for j in range(i,len(comps)):
        for c4 in range(0,5):
            for w6 in range(0,7):
                c=F(c4,4); w1=(1-c)*F(w6,6); w2=(1-c)-w1
                nm+=1
                # W=0 iff every positive-weight term is zero (terms nonneg by A1)
                z=(c==0) and (w1==0 or comps[i] in zset) and (w2==0 or comps[j] in zset)
                if z:
                    bad=(w1>0 and comps[i] in tz) or (w2>0 and comps[j] in tz)
                    if bad: falsezero.append((comps[i],comps[j],str(c),str(w1)))
rec('A2',len(tz)==0 and not falsezero,grid_components=len(comps),zero_components=zero_components,
    zero_components_not_target=tz,mixtures_tested=nm,false_zero_mixtures=falsezero,
    note='negativity excluded by exact identity A1, not by numerical search')

# ---- B
b1=True;b2=True;nass=0;nunit=0;b3=[];b4=[];b3count=0
for n in range(1,13):
    for a,b,c,d in product(range(n),repeat=4):
        for sd in (1,-1):
            nass+=1
            g={'RR':(a,1),'RL':(b,1),'LR':(c,1),'LL':(d,sd)}
            # unitary: z^(a-c) + sd z^(b-d) = 0
            unit=iszero(add(mono(a-c,n),mono(b-d,n,sd)),n)
            P={};normed=True
            for t in (1,2,3):
                o,_=walk(g,n,t); nr=norm2(o['R'],n); nl=norm2(o['L'],n)
                if not iszero(add(add(nr,nl),const(-2**t,n)),n): normed=False
                P[t]=nr
            if unit!=normed: b1=False
            if unit:
                nunit+=1
                u=(b+c-2*a)%n
                o2,_=walk({'RR':(0,1),'RL':(u,1),'LR':(0,1),'LL':(u,-1)},n,2)
                o3,_=walk({'RR':(0,1),'RL':(u,1),'LR':(0,1),'LL':(u,-1)},n,3)
                if not (iszero(add(P[2],sc(norm2(o2['R'],n),-1)),n) and iszero(add(P[3],sc(norm2(o3['R'],n),-1)),n)): b2=False
                hit=iszero(add(P[2],const(-1,n)),n) and iszero(add(P[3],const(-7,n)),n)
                if hit and b==0 and len(b4)<12: b4.append(dict(n=n,a=a,b=b,c=c,d=d,sign_LL=sd))
            else:
                if iszero(add(P[2],const(-1,n)),n) and iszero(add(P[3],const(-7,n)),n):
                    b3count+=1
                    if len(b3)<12: b3.append(dict(n=n,a=a,b=b,c=c,d=d,sign_LL=sd))
rec('B1',b1,assignments=nass,qualifying_unitary=nunit)
rec('B2',b2,qualifying=nunit)
rec('B3','measured',nonunitary_with_target_rates=b3count,examples=b3)
rec('B4','measured',examples_phase_not_on_RL=b4)

# ---- C (rational arithmetic)
def rates(mix,c):
    """mix: list of (weight, x) rational; returns p2,p3"""
    assert sum(w for w,_ in mix)+c==1 and all(w>=0 and -1<=x<=1 for w,x in mix) and 0<=c<=1
    mu=sum(w*x for w,x in mix); S=c+sum(w*x*x for w,x in mix)
    return (1+mu)/2, 1-S/2
def W(q2,q3,m=F(-1,2)): return 2*(1-q3)-2*m*(2*q2-1)+m*m
c1=[];ok=True
for d in (F(1,10),F(1,100),F(1,1000),F(-1,10)):
    x=F(-1,2)+d; p2,p3=rates([(F(1),x)],F(0))
    e2=F(1,4)/p2; e3=F(7,8)/p3
    w=W(e2*p2,e3*p3); ok&=(w==0)
    c1.append(dict(x=str(x),eta2=str(e2),eta3=str(e3),W_obs=str(w),W_true=str(W(p2,p3)),loss_only=bool(e2<=1 and e3<=1)))
rec('C1',ok,cases=c1)
c2=[];ok=True
# no false zero for eta<1: check inequality on grid h=1+j/1000
for j in range(1,1001):
    h=1+F(j,1000); mu=h/2-1; S=2-7*h/4
    if S>=mu*mu: ok=False
for e in (F(1,10),F(1,100),F(1,1000)):
    eta=1+e; h=1/eta; mu=h/2-1; S=2-7*h/4; var=S-mu*mu
    # two-point symmetric mixture needs sqrt(var) rational; instead use c>0: choose pure x=mu' with count c:
    # (1-c) x = mu, c+(1-c) x^2 = S -> c + mu^2/(1-c) = S ; solve quadratic in c exactly if rational, else 3-point.
    # use three-point: masses at x1=mu-s, x2=mu+s with s rational, s^2>=var, plus adjust: weights w at mu±s and 1-2w at mu: var=2w s^2
    s=F(1,4); w=var/(2*s*s)
    mix=[(w,mu-s),(w,mu+s),(1-2*w,mu)]
    p2,p3=rates(mix,F(0)); wo=W(eta*p2,eta*p3); ok&=(wo==0 and var>0)
    c2.append(dict(eta=str(eta),mixture=[(str(a),str(b)) for a,b in mix],p2=str(p2),p3=str(p3),W_obs=str(wo),W_true=str(W(p2,p3))))
rec('C2',ok,no_false_zero_for_loss_checked_h_grid=1000,cases=c2)
c3=[];ok=True
for e in (F(1,10),F(1,100),F(1,1000),F(-1,100)):
    r=1-e; p2=1/(3*r+1); p3=7/(r+7); mu=2*p2-1; S=2*(1-p3); var=S-mu*mu
    feas=2*r*(1+3*r)**2>=(r+7)*(1-3*r)**2
    ent=dict(r=str(r),feasible=bool(feas),var=str(var))
    if feas != (var>=0): ok=False
    if feas:
        s=F(1,4); w=var/(2*s*s); mix=[(w,mu-s),(w,mu+s),(1-2*w,mu)]
        t2,t3=rates(mix,F(0)); o2=r*t2/(r*t2+1-t2); o3=r*t3/(r*t3+1-t3); wo=W(o2,o3); ok&=(wo==0)
        ent.update(mixture=[(str(a),str(b)) for a,b in mix],W_obs=str(wo),W_true=str(W(t2,t3)))
    c3.append(ent)
# pure roots: 10x^3+11x^2+x-1 = (2x+1)(5x^2+3x-1)
from sympy import expand, symbols
xx=symbols('x'); ok&=(expand((2*xx+1)*(5*xx**2+3*xx-1)-(10*xx**3+11*xx**2+xx-1))==0)
rec('C3',ok,cases=c3,pure_false_zero_roots='x=(-3±sqrt29)/10 with r=(1-x)/(3(1+x))')
# C4: grid phases, exact via sympy cos with rational bracketing through evalf-free comparison: use sympy's exact sign
from sympy import cos, pi, Rational, nsimplify, simplify, Max, sign
c4=[];seen=set()
for n in range(1,25):
    for k in range(n):
        fr=F(k,n)
        if fr in seen or fr>F(1,2): continue
        seen.add(fr)
        x=cos(2*pi*Rational(k,n))
        if simplify(x+Rational(1,2))==0 or simplify(x+1)==0: continue
        e2=1/(2*(1+x)); e3=7/(8-4*x**2)
        lo=bool(e2<=1) and bool(e3<=1)
        c4.append((n,k,e2,e3,lo))
lossonly=[(n,k,e2,e3) for n,k,e2,e3,lo in c4 if lo]
def badness(t): return Max(1-t[2],1-t[3])
best=lossonly[0]
for t in lossonly[1:]:
    if bool(badness(t)<badness(best)): best=t
rec('C4','measured',grid_phases=len(c4),loss_only_imitators=[(n,k,str(simplify(e2)),str(simplify(e3))) for n,k,e2,e3 in lossonly],
    closest=dict(n=best[0],k=best[1],eta2=str(simplify(best[2])),eta3=str(simplify(best[3])),
                 eta2_dec=str(best[2].evalf(8)),eta3_dec=str(best[3].evalf(8))))
ok=all(W(F(j,100)*F(1,4),F(j,100)*F(7,8))==F(5,4)*(1-F(j,100)) for j in range(1,101))
rec('C5',ok)
with open(sys.argv[1],'x') as f: json.dump(res,f,indent=1,sort_keys=True)
print(json.dumps({k:v['ok'] for k,v in res['predicates'].items()}), 'failed:',res['failed'])
