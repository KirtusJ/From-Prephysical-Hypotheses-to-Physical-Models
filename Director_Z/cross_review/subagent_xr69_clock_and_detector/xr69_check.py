"""xr69 cross-review program (own derivation from the two notes' definitions; not from their checkers).
Seed 6969. Exact arithmetic (Fractions; field Q(zeta12) for beta in {-1,i,omega,rational unit points}).
No tolerances anywhere. Result file opened with mode 'x' (never overwritten).

PREDICATES (fixed before first run). Each records qualify / pass / fail; failures are kept.
NOTE A (common clock)
 A1  schedules {},{1},{1,3},{3} (tick 4 off AND on), start R: p_R(x) == (1+T_h(x))/2 as polynomials; start L: complement.
 A2  every schedule, t=1..5, both starts: fair-count R probability == 1/2.
 A3  polynomial p_R cross-checked against direct matrix product in Q(zeta12) at beta=-1,i,omega,(3+4i)/5,1.
 A4  eq (2): S_m from p_1,p_2 == int (x-m)^2 dnu + c(1/2+m^2), random mixtures incl. c=0, c=1, m=+-1.
 A5  S_m==0 iff (c==0 and all mass at x==m)  [hypothesis tested per case; both directions counted].
 A6  c <= S/(1/2+m^2) and mass{|x-m|>=delta} <= S/delta^2.
 A7  eq (3)/(V_m): from walk-computed q_h^+-, hypothesis E_0!=0 per case: ratios equal in all informative
     components, V_m == int (x-m)^2 dnu / T, common midpoint.
 A8  eq (4): lower=max|E0|/(2B); T' in {lower,(lower+1)/2,1} give valid columns reproducing all six vectors;
     T' = lower*(99/100) gives a negative column entry.
 A9  note example: lower == 10/21, T'=10/21 and 1 reproduce.
 A10 early clocks: t=1 all p==1/2; t=2 p in {1,(1+x)/2}; t=3 p in {1/2,1-x^2/2} (R start), complements for L.
 A11 t=3: -m matches m for all responses; t=2: mixture on +-1 matches pure m, |m|<1; m=0 at t=3: p==1 iff c=0,x=0.
 A12 (unreported) list of distinct p_R polynomials at t=4 (all 16) and t=5 (all 32) -- reported, not pass/fail,
     plus: at t=4 some schedule pair separates every interior m from every alias found at t=3.
 A13 adversary (premise test): gain omega at tick 1 and 1 at tick 3 within a flight -> S_{-1/2} under {1},{1,3};
     recorded value; and p under {3}.
NOTE B (detector)
 B1  U_beta^t: b_1==0, b_2==x, b_3==1-x^2 as polynomials; fair 1/2; (unreported) b_4,b_5 reported.
 B2  rail-only channel, random columns/event: hypothesis d!=0 per case: (Y-B)/d == b_t; K_L==2B-U; Y on segment.
 B3  eq (2): W_m == int (x-m)^2 dnu + c(1+m^2); W==0 iff pure target.
 B4  coherent meter, source (-1:1/5, i:4/5), by direct tr(rho E) in Q(zeta12): (45,29,21,41)/50, biases -1/2,3/4,
     2B-U==13/50; twirl: (45,25,21,41)/50, biases -1/5,4/5, W==1/4; pure omega through twirl W==0.
 B5  arbitrary Hermitian E (random, entries in Q(i)): (E+ZEZ)/2 diagonal; twirled response depends on populations only.
 B6  own adversarial search: 2-point sources on {1,-1,i,-i} x weights k/10 x effect Bloch grid (ex,ey,ez in k/5,
     norm<=1): count untwirled false passes of target m=-1/2 (W==0, d!=0, 0<=2B-U<=1, on-segment), then after
     twirl: W_twirled == true W (>0) when twirled d!=0; count twirled-blind cases (d==0).
 B7  biased sign bit (11/20) on the B6 false passes: count cases still passing W==0.
 B8  eq (3): lambda-dependent diagonal channel: normalized bias == E[v b]/E[v]; hypothesis v one sign per case:
     W == reweighted formula; bounds c<=(vmax/vmin)W/(1+m^2), mass<= (vmax/vmin)W/delta^2.
 B9  note's two alias examples reproduce -1/2, 3/4.
 B10 error identity and bound |bhat-b| <= (eY+2eB+eU)/|dhat|, hypothesis dhat!=0 and |b|<=1 per case;
     dW identity; raw-error bound for dW.
"""
import sys, json, random, hashlib
from fractions import Fraction as F
from itertools import product
random.seed(6969)
OUT = sys.argv[1]
R = {}
def pred(name, ok, qual=True, info=None):
    r = R.setdefault(name, {"qualify":0,"not_qualifying":0,"pass":0,"fail":0,"failures":[]})
    if not qual: r["not_qualifying"] += 1; return
    r["qualify"] += 1
    if ok: r["pass"] += 1
    else:
        r["fail"] += 1
        if len(r["failures"]) < 5: r["failures"].append(str(info))
# ---------- polynomials in x ----------
def padd(a,b):
    n=max(len(a),len(b)); a=list(a)+[F(0)]*(n-len(a)); b=list(b)+[F(0)]*(n-len(b))
    return ptrim([u+v for u,v in zip(a,b)])
def pmul(a,b):
    o=[F(0)]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b): o[i+j]+=u*v
    return ptrim(o)
def psc(a,s): return ptrim([u*s for u in a])
def ptrim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0: a.pop()
    return tuple(a)
def pev(a,x): return sum(c*x**k for k,c in enumerate(a))
CH=[(F(1),),(F(0),F(1))]
for _ in range(12): CH.append(padd(pmul((F(0),F(2)),CH[-1]),psc(CH[-2],-1)))
def pstr(a): return " + ".join(f"{c}*x^{k}" for k,c in enumerate(a) if c!=0) or "0"
# ---------- walk by signed exponent counts ----------
def walk(sw, start):
    st={"R":{},"L":{}}; st[start]={0:1}
    for on in sw:
        nr={}; nl={}
        for k,v in st["R"].items(): nr[k]=nr.get(k,0)+v; nl[k+on]=nl.get(k+on,0)+v
        for k,v in st["L"].items(): nr[k]=nr.get(k,0)+v; nl[k+on]=nl.get(k+on,0)-v
        st={"R":nr,"L":nl}
    return st
def ppoly(sw,start,port="R"):
    a=walk(sw,start)[port]; t=len(sw); p=(F(0),)
    for i,u in a.items():
        for j,v in a.items(): p=padd(p,psc(CH[abs(i-j)],F(u*v,2**t)))
    return p
def fair(sw,start):
    # count words: each word weight 2^-t; rail of last arc
    t=len(sw); return F(sum(1 for w in product("RL",repeat=t) if w[-1]=="R"),2**t) if t else F(1)
# ---------- field Q(zeta12), z^4 = z^2 - 1 ----------
class Z:
    def __init__(s,c): s.c=tuple(F(x) for x in c)
    def __add__(s,o): return Z([a+b for a,b in zip(s.c,o.c)])
    def __sub__(s,o): return Z([a-b for a,b in zip(s.c,o.c)])
    def __mul__(s,o):
        if not isinstance(o,Z): return Z([a*o for a in s.c])
        t=[F(0)]*7
        for i,a in enumerate(s.c):
            for j,b in enumerate(o.c): t[i+j]+=a*b
        for k in (6,5,4): t[k-2]+=t[k]; t[k-4]-=t[k]; t[k]=F(0)
        return Z(t[:4])
    def conj(s):
        zi=Z([0,1,0,-1]); p=Z([1,0,0,0]); o=Z([0,0,0,0])
        for a in s.c: o=o+p*a; p=p*zi
        return o
    def rat(s):
        assert s.c[1]==s.c[2]==s.c[3]==0, s.c
        return s.c[0]
ONE=Z([1,0,0,0]); ZERO=Z([0,0,0,0]); I_=Z([0,0,0,1]); OM=Z([-1,0,1,0])  # zeta^4 = zeta^2-1
assert (I_*I_).c==(-1,0,0,0) and (OM*OM*OM).c==(1,0,0,0) and (OM+OM.conj()).rat()==-1
def gz(re,im): return ONE*F(re)+I_*F(im)
BETAS={"-1":(ONE*-1,F(-1)),"i":(I_,F(0)),"omega":(OM,F(-1,2)),"(3+4i)/5":(gz(F(3,5),F(4,5)),F(3,5)),"1":(ONE,F(1)),"-i":(I_*-1,F(0))}
def evolve(gains,start="R"):
    """gains: list of field elements (per-tick L gain). unnormalised (factor 2^{-t/2} omitted)."""
    r,l=(ONE,ZERO) if start=="R" else (ZERO,ONE)
    for g in gains: r,l=r+l,(r-l)*g
    return r,l
def prob_eff(psi,E,t):
    r,l=psi; (a,b),(c,d)=E
    v=r.conj()*(a*r+b*l)+l.conj()*(c*r+d*l)
    return v.rat()/2**t
PR=((ONE,ZERO),(ZERO,ZERO))
# ================= NOTE A =================
HS={0:[(0,0,0)],1:[(1,0,0),(0,0,1)],2:[(1,0,1)]}
for h,lst in HS.items():
    for s3 in lst:
        for last in (0,1):
            sw=(s3[0],s3[1],s3[2],last)
            want=psc(padd((F(1),),CH[h]),F(1,2))
            pred("A1",ppoly(sw,"R")==want,info=(sw,"R",pstr(ppoly(sw,"R"))))
            pred("A1",ppoly(sw,"L")==padd((F(1),),psc(want,-1)),info=(sw,"L"))
allp={}
for t in range(1,6):
    for sw in product((0,1),repeat=t):
        for st in "RL":
            pred("A2",fair(sw,st)==F(1,2),info=(sw,st))
            p=ppoly(sw,st); allp[(sw,st)]=p
            pred("A2_norm",padd(p,ppoly(sw,st,"L"))==(F(1),),info=(sw,st))
            for nm,(b,x) in BETAS.items():
                psi=evolve([b if on else ONE for on in sw],st)
                pred("A3",prob_eff(psi,PR,t)==pev(p,x),info=(sw,st,nm))
def rfrac(lo,hi,den=None):
    d=den or random.choice([2,3,4,5,7,8,10,12]); return F(random.randint(lo*d,hi*d),d)
def rdist(n,zero_ok=True):
    while True:
        w=[random.choice([0,0,1,2,3,5,8]) if zero_ok else random.randint(1,8) for _ in range(n)]
        if sum(w): return [F(a,sum(w)) for a in w]
def rmix():
    k=random.randint(1,4); xs=[random.choice([F(-1),F(1),F(0),F(-1,2),rfrac(-1,1)]) for _ in range(k)]
    c=random.choice([F(0),F(0),F(1),rfrac(0,1)]); w=rdist(k,False)
    return [(x,wi*(1-c)) for x,wi in zip(xs,w)], c
P1=ppoly((1,0,0,0),"R"); P2=ppoly((1,0,1,0),"R"); P0=ppoly((0,0,0,0),"R")
def rate(p,mix,c): return c/2+sum(w*pev(p,x) for x,w in mix)
for n in range(4000):
    mix,c=rmix(); m=random.choice([F(-1),F(1),F(0),F(-1,2),rfrac(-1,1)])
    p1,p2=rate(P1,mix,c),rate(P2,mix,c)
    S=F(1,2)+m*m-2*m*(2*p1-1)+(2*p2-1)/2
    rhs=sum(w*(x-m)**2 for x,w in mix)+c*(F(1,2)+m*m)
    pred("A4",S==rhs,info=(mix,c,m,S,rhs))
    pure=(c==0 and all(x==m for x,w in mix if w>0))
    pred("A5_pure_implies_zero",S==0,qual=pure,info=(mix,c,m,S))
    pred("A5_nonpure_implies_positive",S>0,qual=not pure,info=(mix,c,m,S))
    pred("A6_count",c<=S/(F(1,2)+m*m),info=(mix,c,m))
    dl=random.choice([F(1,10),F(1,4),F(1,2),F(1)])
    pred("A6_tail",sum(w for x,w in mix if abs(x-m)>=dl)<=S/dl**2,info=(mix,c,m,dl))
    pred("A6_count_check_h0",c==2*(1-rate(P0,mix,c)),info=(mix,c))
    # detector
    no=random.randint(2,4); KR,KL=rdist(no),rdist(no); T=1-c
    q={}
    for h,P in enumerate((P0,P1,P2)):
        p=rate(P,mix,c)
        q[h,1]=[p*a+(1-p)*b for a,b in zip(KR,KL)]; q[h,-1]=[(1-p)*a+p*b for a,b in zip(KR,KL)]
    B=[(a+b)/2 for a,b in zip(KR,KL)]
    E=[[a-b for a,b in zip(q[h,1],q[h,-1])] for h in range(3)]
    pred("A7_midpoint",all([(a+b)/2 for a,b in zip(q[h,1],q[h,-1])]==B for h in range(3)),info=(KR,KL))
    inf=any(e!=0 for e in E[0])
    if inf:
        ys=[y for y in range(no) if E[0][y]!=0]
        rs=[[E[h][y]/E[0][y] for y in ys] for h in range(3)]
        pred("A7_ratio_consistent",all(len(set(r))==1 for r in rs),info=(KR,KL,mix,c))
        V=(1+rs[2][0])/2-2*m*rs[1][0]+m*m
        pred("A7_Vm",V==sum(w*(x-m)**2 for x,w in mix)/T,info=(mix,c,m,V))
        lower=max(abs(E[0][y])/(2*B[y]) for y in range(no) if B[y]>0)
        pred("A8_B0_implies_E0",all(E[0][y]==0 for y in range(no) if B[y]==0))
        pred("A8_true_T_in_interval",lower<=T<=1,info=(lower,T))
        for Tp,tag in ((lower,"lower"),((lower+1)/2,"mid"),(F(1),"one")):
            KRp=[b+e/(2*Tp) for b,e in zip(B,E[0])]; KLp=[b-e/(2*Tp) for b,e in zip(B,E[0])]
            valid=all(v>=0 for v in KRp+KLp) and sum(KRp)==1 and sum(KLp)==1
            # conditional measure: true one rescaled to mass Tp, count 1-Tp
            mixp=[(x,w*Tp/T) for x,w in mix]; cp=1-Tp; ok=valid
            for h,P in enumerate((P0,P1,P2)):
                p=rate(P,mixp,cp)
                ok=ok and [p*a+(1-p)*b for a,b in zip(KRp,KLp)]==q[h,1] and [(1-p)*a+p*b for a,b in zip(KRp,KLp)]==q[h,-1]
            pred("A8_reproduce_"+tag,ok,info=(KR,KL,mix,c,Tp))
        Tp=lower*F(99,100)
        pred("A8_below_lower_infeasible",any(b+e/(2*Tp)<0 or b-e/(2*Tp)<0 for b,e in zip(B,E[0])),info=(lower,))
    else:
        pred("A7_ratio_consistent",True,qual=False)
        pred("A7_E0zero_means_T0_or_blind",T==0 or KR==KL,info=(KR,KL,T))
        pred("A7_E0zero_all_contrasts_vanish",all(e==0 for h in range(3) for e in E[h]),info=(KR,KL,T))
# A9 example
KR=[F(3,4),F(1,8),F(1,8)]; KL=[F(1,8),F(1,2),F(3,8)]; T=F(2,3); B=[(a+b)/2 for a,b in zip(KR,KL)]
E0=[(a-b)*T for a,b in zip(KR,KL)]; low=max(abs(e)/(2*b) for e,b in zip(E0,B))
pred("A9_lower_10_21",low==F(10,21),info=low)
R["A9_columns"]={"T=10/21":[[str(b+e/(2*low)) for b,e in zip(B,E0)],[str(b-e/(2*low)) for b,e in zip(B,E0)]],
                 "T=1":[[str(b+e/2) for b,e in zip(B,E0)],[str(b-e/2) for b,e in zip(B,E0)]]}
# A10/A11
half=(F(1,2),); one=(F(1),); lin=(F(1,2),F(1,2)); quad=(F(1),F(0),F(-1,2))
comp=lambda p: padd(one,psc(p,-1))
for (sw,st),p in allp.items():
    t=len(sw)
    if t==1: pred("A10_t1",p==half,info=(sw,st))
    if t==2:
        w=lin if sw[0] else one; pred("A10_t2",p==(w if st=="R" else comp(w)),info=(sw,st,pstr(p)))
    if t==3:
        w=quad if (sw[0] and sw[1]) else half; pred("A10_t3",p==(w if st=="R" else comp(w)),info=(sw,st,pstr(p)))
        for m in [F(k,12) for k in range(-11,12) if k]:
            pred("A11_t3_alias_minus_m",pev(p,m)==pev(p,-m),info=(sw,st,m))
    if t==2:
        for m in [F(k,12) for k in range(-11,12)]:
            pred("A11_t2_alias_pm1",pev(p,m)==(1+m)/2*pev(p,F(1))+(1-m)/2*pev(p,F(-1)),info=(sw,st,m))
for n in range(2000):
    mix,c=rmix(); p=rate(quad,mix,c); pure=(c==0 and all(x==0 for x,w in mix if w>0))
    pred("A11_m0_t3_p1_iff",(p==1)==pure,info=(mix,c,p))
# t=3 unknown bank: alias x' for target 0
for xp in [F(k,10) for k in range(-9,10) if k]:
    D=F(1,5); Dp=D/(1-xp*xp); Bm=F(1,2)   # binary bank: K_R(A)=Bm+D/2, K_L(A)=Bm-D/2
    qual=0<=Bm-Dp/2 and Bm+Dp/2<=1
    # every 3-tick program contrast: D*(2p(0)-1) vs Dp*(2p(xp)-1)
    ok=all(D*(2*pev(p,F(0))-1)==Dp*(2*pev(p,xp)-1) for (sw,st),p in allp.items() if len(sw)==3)
    pred("A11_t3_unknown_bank_alias_m0",ok,qual=qual,info=(xp,))
# A12
R["A12_distinct_pR_startR"]={str(t):sorted({pstr(p) for (sw,st),p in allp.items() if len(sw)==t and st=="R"}) for t in (4,5)}
R["A12_t4_by_schedule"]={"".join(map(str,sw)):pstr(p) for (sw,st),p in allp.items() if len(sw)==4 and st=="R"}
for m in [F(k,12) for k in range(-11,12) if k]:
    pred("A12_t4_separates_m_from_minus_m",any(pev(p,m)!=pev(p,-m) for (sw,st),p in allp.items() if len(sw)==4),info=m)
# A13 adversary: varying gain inside a flight
m=F(-1,2)
p1=prob_eff(evolve([OM,ONE,ONE,ONE]),PR,4); p2=prob_eff(evolve([OM,ONE,ONE,ONE]),PR,4)  # tick-3 gain is 1 in flight
p3=prob_eff(evolve([ONE,ONE,ONE,ONE]),PR,4)   # program {3} with tick-3 gain 1
S=F(1,2)+m*m-2*m*(2*p1-1)+(2*p2-1)/2
R["A13_varying_gain_adversary"]={"p_{1}":str(p1),"p_{1,3}":str(p2),"S_m":str(S),"p_{3}":str(p3),
   "reading":"gain omega at tick 1, gain 1 at tick 3: settings {1},{1,3} give S=0 (false pass); setting {3} gives p=1 != 1/4. Excluded by the note's stated premise that the gain stays fixed during a flight."}
pred("A13_false_pass_exists_outside_premise",S==0,info=S)
# ================= NOTE B =================
bp={t:psc(padd(ppoly((1,)*t,"R"),(F(-1,2),)),2) for t in range(1,6)}
pred("B1_b1",bp[1]==(F(0),),info=pstr(bp[1])); pred("B1_b2",bp[2]==(F(0),F(1)),info=pstr(bp[2]))
pred("B1_b3",bp[3]==(F(1),F(0),F(-1)),info=pstr(bp[3]))
R["B1_unreported_b4_b5"]={"b4":pstr(bp[4]),"b5":pstr(bp[5])}
def bias(t,mix,c): return sum(w*pev(bp[t],x) for x,w in mix)   # count contributes 0
for n in range(4000):
    mix,c=rmix(); m=random.choice([F(-1),F(1),F(0),F(-1,2),rfrac(-1,1)])
    b2,b3=bias(2,mix,c),bias(3,mix,c)
    Wt=sum(w*(x-m)**2 for x,w in mix)+c*(1+m*m); W=1-b3-2*m*b2+m*m
    pred("B3_identity",W==Wt,info=(mix,c,m))
    pure=(c==0 and all(x==m for x,w in mix if w>0))
    pred("B3_pure_implies_zero",W==0,qual=pure); pred("B3_nonpure_positive",W>0,qual=not pure,info=(mix,c,m))
    no=random.randint(2,4); KR,KL=rdist(no),rdist(no)
    A=[y for y in range(no) if random.random()<0.5] or [0]
    ev=lambda d: sum(d[y] for y in A)
    U=KR; Bv=[(a+b)/2 for a,b in zip(KR,KL)]     # tick 0 sharp R; tick 1 p=1/2 (B1)
    d=ev(U)-ev(Bv)
    pred("B2_KL",[2*b-u for b,u in zip(Bv,U)]==KL)
    for t,bt in ((2,b2),(3,b3)):
        p=(1+bt)/2; Y=[p*a+(1-p)*b for a,b in zip(KR,KL)]
        pred("B2_recover_bias",d!=0 and (ev(Y)-ev(Bv))/d==bt,qual=(d!=0),info=(KR,KL,A,bt))
        pred("B2_segment",0<=p<=1)
    # B8 lambda-dependent visibility: labels = each coherent atom + count
    labs=[(x,w) for x,w in mix if w>0]+([("count",c)] if c>0 else [])
    mids=[rfrac(0,1,8) for _ in labs]
    signmode=random.choice(["pos","pos","neg","mixed"])
    vs=[]
    for mid in mids:
        cap=min(mid,1-mid)*2
        v=cap*random.choice([F(1,7),F(1,3),F(1,2),F(1)])
        if signmode=="neg" or (signmode=="mixed" and random.random()<0.5): v=-v
        vs.append(v)
    Ev=sum(w*v for (x,w),v in zip(labs,vs))
    onesign=all(v>0 for v in vs) or all(v<0 for v in vs)
    def obs(t):  # U,B,Y from per-label channel
        Ub=sum(w*(mid+v/2) for (x,w),mid,v in zip(labs,mids,vs)); Bb=sum(w*mid for (x,w),mid in zip(labs,mids))
        Yb=sum(w*(mid+v/2*(0 if x=="count" else pev(bp[t],x))) for (x,w),mid,v in zip(labs,mids,vs))
        return Ub,Bb,Yb
    if Ev!=0:
        nb={}
        for t in (2,3):
            Ub,Bb,Yb=obs(t); nb[t]=(Yb-Bb)/(Ub-Bb)
            pred("B8_eq3",nb[t]==sum(w*v*(0 if x=="count" else pev(bp[t],x)) for (x,w),v in zip(labs,vs))/Ev,info=(labs,vs))
        Wo=1-nb[3]-2*m*nb[2]+m*m
        if onesign:
            tot=sum(w*abs(v) for (x,w),v in zip(labs,vs))
            Wr=sum(w*abs(v)/tot*((1+m*m) if x=="count" else (x-m)**2) for (x,w),v in zip(labs,vs))
            pred("B8_reweighted",Wo==Wr,info=(labs,vs,m))
            vmin=min(abs(v) for v in vs); vmax=max(abs(v) for v in vs)
            pred("B8_bound_count",c<=vmax/vmin*Wo/(1+m*m),info=(labs,vs,m))
            dl=random.choice([F(1,10),F(1,4),F(1,2)])
            pred("B8_bound_tail",sum(w for x,w in mix if abs(x-m)>=dl)<=vmax/vmin*Wo/dl**2,info=(labs,vs,m,dl))
            pred("B8_zero_iff_pure",(Wo==0)==pure,info=(labs,vs,m))
        else:
            pred("B8_reweighted",True,qual=False)
            pred("B8_mixedsign_W_negative_or_falsezero(kept, not a claim)",not(Wo<0 or (Wo==0 and not pure)),info=(labs,vs,m,str(Wo)))
    # B10 errors
    if d!=0:
        bt=b3; p=(1+bt)/2; Yv=ev([p*a+(1-p)*b for a,b in zip(KR,KL)]); Uv=ev(U); Bb=ev(Bv)
        eY,eU,eB=[random.choice([F(0),F(1,1000),F(1,100),F(1,20),F(1,5)]) for _ in range(3)]
        Yh=Yv+eY*random.choice([-1,1,F(1,2),F(-1,3)]); Uh=Uv+eU*random.choice([-1,1,F(1,2)]); Bh=Bb+eB*random.choice([-1,1,F(-1,2)])
        dh=Uh-Bh
        if dh!=0:
            bh=(Yh-Bh)/dh
            pred("B10_identity",dh*(bh-bt)==(Yh-Yv)-(1-bt)*(Bh-Bb)-bt*(Uh-Uv))
            pred("B10_bound",abs(bh-bt)<=(eY+2*eB+eU)/abs(dh),qual=abs(bt)<=1,info=(Yv,Uv,Bb,eY,eU,eB))
            pred("B10_contrast_certified",d!=0,qual=abs(dh)>eU+eB)
        else: pred("B10_bound",True,qual=False)
        Y2=ev([(1+b2)/2*a+(1-b2)/2*b for a,b in zip(KR,KL)])
        pred("B10_dW_identity",d*W==(1+m*m)*Uv+(2*m-m*m)*Bb-2*m*Y2-Yv,info=(m,))
        e2=random.choice([F(0),F(1,100),F(1,10)]); s=[random.choice([-1,1,F(1,2)]) for _ in range(4)]
        raw=lambda u,b,y2,y3:(1+m*m)*u+(2*m-m*m)*b-2*m*y2-y3
        pred("B10_dW_raw_bound",abs(raw(Uv+s[0]*eU,Bb+s[1]*eB,Y2+s[2]*e2,Yv+s[3]*eY)-d*W)<=(1+m*m)*eU+abs(2*m-m*m)*eB+2*abs(m)*e2+eY)
# B4 coherent meter by direct trace
def eff(ex,ey,ez):  # (I + ex X + ey Y + ez Z)/2
    h=F(1,2); return ((ONE*(h*(1+ez)),gz(h*ex,-h*ey)),(gz(h*ex,h*ey),ONE*(h*(1-ez))))
def twirl(E,pb=F(1,2)):  # pb = probability of applying Z
    (a,b),(c,d)=E; k=1-2*pb; return ((a,b*k),(c*k,d))
def resp(src,E):  # src: list of (field beta, weight); 4 settings t=0..3, same detector
    return [sum(w*prob_eff(evolve([b]*t),E,t) for b,w in src) for t in range(4)]
def infer(r,m=F(-1,2)):
    U,Bb,Y2,Y3=r; d=U-Bb
    if d==0: return None
    b2,b3=(Y2-Bb)/d,(Y3-Bb)/d; return b2,b3,1-b3-2*m*b2+m*m
M=eff(0,F(1,5),F(4,5)); src=[(ONE*-1,F(1,5)),(I_,F(4,5))]
r=resp(src,M); pred("B4_untwirled_45_29_21_41",r==[F(45,50),F(29,50),F(21,50),F(41,50)],info=r)
pred("B4_false_pass",infer(r)==(F(-1,2),F(3,4),F(0)),info=infer(r)); pred("B4_left_column_13_50",2*r[1]-r[0]==F(13,50))
rt=resp(src,twirl(M)); pred("B4_twirled_45_25_21_41",rt==[F(45,50),F(25,50),F(21,50),F(41,50)],info=rt)
pred("B4_twirled_W_quarter",infer(rt)==(F(-1,5),F(4,5),F(1,4)),info=infer(rt))
rc=resp([(OM,F(1))],twirl(M)); pred("B4_pure_cubic_twirled_W0",infer(rc)[2]==0,info=(rc,infer(rc)))
R["B4_pure_cubic_twirled"]=[str(v) for v in rc]
rb=resp(src,twirl(M,F(1,2)+F(1,20))); R["B4_biased_bit_11_20"]={"resp":[str(v) for v in rb],"W":str(infer(rb)[2])}
# B5
for n in range(300):
    ex,ey,ez=[rfrac(-1,1,5) for _ in range(3)]
    q=ex*ex+ey*ey+ez*ez<=1
    Et=twirl(eff(ex,ey,ez))
    pred("B5_twirl_diagonal",Et[0][1].c==(0,0,0,0) and Et[1][0].c==(0,0,0,0),qual=q)
    nm=random.choice(list(BETAS)); b=BETAS[nm][0]; t=random.randint(0,4); psi=evolve([b]*t)
    pR=prob_eff(psi,PR,t)
    pred("B5_populations_only",prob_eff(psi,Et,t)==pR*(1+ez)/2+(1-pR)*(1-ez)/2,qual=q,info=(ex,ey,ez,nm,t))
# B6/B7 adversarial search
PH=[("1",ONE,F(1)),("-1",ONE*-1,F(-1)),("i",I_,F(0)),("-i",I_*-1,F(0))]
grid=[F(k,5) for k in range(-5,6)]; fp=[]; nsearch=0
cache={}
def base(b,E3):
    key=(b.c,E3)
    if key not in cache: cache[key]=[prob_eff(evolve([b]*t),eff(*E3),t) for t in range(4)]
    return cache[key]
for (n1,b1,x1),(n2,b2_,x2) in [(a,b) for i,a in enumerate(PH) for b in PH[i:]]:
    for k in range(1,10 if n1!=n2 else 2):
        w=F(k,10) if n1!=n2 else F(1)
        trueW=w*(x1+F(1,2))**2+(1-w)*(x2+F(1,2))**2
        for E3 in product(grid,repeat=3):
            if sum(v*v for v in E3)>1: continue
            nsearch+=1
            r=[w*u+(1-w)*v for u,v in zip(base(b1,E3),base(b2_,E3))]
            inf=infer(r)
            if inf and inf[2]==0 and 0<=2*r[1]-r[0]<=1 and all(min(r[0],2*r[1]-r[0])<=y<=max(r[0],2*r[1]-r[0]) for y in r[2:]):
                fp.append((n1,n2,str(w),E3,trueW))
R["B6_search_size"]=nsearch; R["B6_false_pass_count"]=len(fp)
R["B6_false_pass_examples"]=[(a,b,w,[str(v) for v in E3],str(tw)) for a,b,w,E3,tw in fp[:8]]
blind=0; still=0
for n1,n2,w,E3,trueW in fp:
    w=F(w); b1=dict((a,b) for a,b,_ in PH)[n1]; b2_=dict((a,b) for a,b,_ in PH)[n2]
    E=eff(*E3)
    def rr(pb): return [w*prob_eff(evolve([b1]*t),twirl(E,pb),t)+(1-w)*prob_eff(evolve([b2_]*t),twirl(E,pb),t) for t in range(4)]
    inf=infer(rr(F(1,2)))
    if inf is None: blind+=1; pred("B6_twirl_repairs",True,qual=False)
    else: pred("B6_twirl_repairs",inf[2]==trueW and trueW>0,info=(n1,n2,str(w),E3,str(inf[2]),str(trueW)))
    ib=infer(rr(F(11,20)))
    if ib is not None and ib[2]==0: still+=1
R["B6_twirled_blind_count(false signal removed but nothing measured)"]=blind
R["B7_biased_bit_still_false_pass_count"]=still
# B9
w=[F(3,10),F(6,10),F(1,10)]; xs=[F(-1),F(0),F(1)]; v=[1,1,-1]; Ev=sum(a*b for a,b in zip(w,v))
pred("B9_ex1",(sum(a*b*x for a,b,x in zip(w,v,xs))/Ev,sum(a*b*(1-x*x) for a,b,x in zip(w,v,xs))/Ev)==(F(-1,2),F(3,4)))
pred("B9_ex1_signed_masses",[a*b/Ev for a,b in zip(w,v)]==[F(3,8),F(3,4),F(-1,8)])
w=[F(1,2),F(1,2)]; xs=[F(-1),F(0)]
b2=sum(a*1*x for a,x in zip(w,xs))/sum(w); v3=[F(1,3),F(1)]; b3=sum(a*b*(1-x*x) for a,b,x in zip(w,v3,xs))/sum(a*b for a,b in zip(w,v3))
pred("B9_ex2",(b2,b3)==(F(-1,2),F(3,4)),info=(b2,b3))
b3c=sum(a*(1-x*x) for a,x in zip(w,xs)); R["B9_ex2_common_well_W"]=str(1-b3c-2*F(-1,2)*b2+F(1,4))
out={"seed":6969,"predicates":R}
with open(OUT,"x") as f: json.dump(out,f,indent=1,sort_keys=True,default=str)
tot_fail=sum(v["fail"] for v in R.values() if isinstance(v,dict) and "fail" in v)
for k in sorted(R):
    v=R[k]
    if isinstance(v,dict) and "fail" in v: print(f"{k:60s} qual={v['qualify']:6d} nonqual={v['not_qualifying']:5d} pass={v['pass']:6d} fail={v['fail']}")
print("TOTAL FAIL",tot_fail); sys.exit(1 if tot_fail else 0)
