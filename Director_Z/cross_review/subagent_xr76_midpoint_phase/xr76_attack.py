"""xr76 own program for 'A midpoint sign tests coin balance with a terminal rail read'.
Written from the note's definitions, not from its checker. Seed 760076. Exact Gaussian
rationals (Fraction pairs) except P5f (floats; tolerance 1e-12 = ~10 double operations
with a 1e3 margin; the measured maximum deviation is recorded).
Conventions: basis (R,L) = index (0,1); U[out][in]; launch R; q=|U[1][0]|^2;
A=U[0][0], B=U[1][1]; plate P_l=diag(1,l); C_l=|(U P_l U)[1][0]|^2; L_t=|(U^t)[1][0]|^2;
rates per original launch; count branch = independent fair direction per tick (1/2 at
every clock, plate-insensitive); nu has mass 1-c.

PREDICATES (fixed before first run). H = hypothesis tested per case.
P1  H: U exactly unitary. (1-L2-C_{-1})/4 == (q-1/2)^2.
P2  H: unitary, q<1. 1-C_l == 4(q-1/2)^2+q(1-q)|1-l*eta|^2 for each plate l; q=1: C_l==0.
P3  H: weights>=0, c>=0, sum 1, coins unitary. mixture D == sum w(q-1/2)^2 ;
    W=L3+2(1-a)L2+(a^2-1)L1 == c/2((a-1)^2+1)+sum w q(r-a)^2.
P4  H: unitary. L2==q r and C_{-1}==q(4(1-q)-r) (formulas used for the cubic numbers).
P5  cubic numbers from P4 formulas: balanced (3/4,1/4); pair 7/16,9/16 -> (3/4,15/64);
    deficit 1/64 == 4*(1/256).  P5f: float unitaries with those (q,r) reproduce them.
P6  oriented plate: U_beta (with global and rail phases), l=-conj(beta): C==1; conjugate
    coin gives (Re beta)^2.  P6c converse on panel: H: C_l==1 exactly; then q==1/2 and
    eta==-beta.  P6s sharpness: c==2e and nu(|q-1/2|>=d)==e/(4d^2) attained.
P7  note's false pass: H(1-q) P_{-1} H(q) flip ==1, free clocks t<=6 of the pair equal
    balanced coin, bare L2 equal, so measured D==0 while true int (q-1/2)^2>0.
P8  ATTACK universal false pass: for every unitary U there is V with V P_{-1} U |R>=|L>.
P9  ATTACK inactive plate (l=1 in place of -1): exact unbalanced ensemble, measured D==0.
P10 kernel: H: unitary. |(U^t)[flip]|^2 == q*h_t(r), t<=8, both directions.
P11 redraw concealment: exact pairs (q,1-q) at common r with a balanced exact target;
    all gap sequences in {1..4}^4 x outcomes x start rail: redraw == target.
P12 negative control: persistent coin differs from target on some transcript (expected).
P13 ATTACK redraw only after outcome L (not 'regardless'): expected to differ.
P14 ATTACK midpoint sign under redraw-per-launch model: D==d^2>0 (consistent with note).
P15 loss per launch: eps in grid, D_meas>=D_true, no measured zero for unbalanced.
P16 ATTACK post-selected normalisation rho=epsR/epsL=9/10 on cubic pair: D_post<=0;
    rail confusion x=1/65 per launch: D_meas==0.
"""
import json, random, sys, cmath, math
from fractions import Fraction as F
from itertools import product
random.seed(760076)
Z0=(F(0),F(0)); ONE=(F(1),F(0)); NEG=(F(-1),F(0)); I_=(F(0),F(1))
def add(z,w): return (z[0]+w[0],z[1]+w[1])
def mul(z,w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def cj(z): return (z[0],-z[1])
def neg(z): return (-z[0],-z[1])
def n2(z): return z[0]*z[0]+z[1]*z[1]
def mm(X,Y): return tuple(tuple(add(mul(X[i][0],Y[0][j]),mul(X[i][1],Y[1][j])) for j in (0,1)) for i in (0,1))
def dag(X): return tuple(tuple(cj(X[j][i]) for j in (0,1)) for i in (0,1))
ID=((ONE,Z0),(Z0,ONE))
def unitary(X): return mm(dag(X),X)==ID and mm(X,dag(X))==ID
def plate(l): return ((ONE,Z0),(Z0,l))
def sc(s,X): return tuple(tuple(mul(s,z) for z in r) for r in X)
def powm(X,t):
    Y=ID
    for _ in range(t): Y=mm(X,Y)
    return Y
def unit(m,n):  # rational unit phase
    d=m*m+n*n; return (F(m*m-n*n,d),F(2*m*n,d))
PH=[ONE,NEG,I_,neg(I_),unit(2,1),unit(3,2),unit(1,2),unit(5,2),unit(-1,3)]
def su2(s):
    L=sum(v*v for v in s); w,x,y,z=[F(k,1+L) for k in (1-L,*(2*v for v in s))]
    a=(w,x); b=(y,z); return ((a,b),(neg(cj(b)),cj(a)))
def coin(s,g,m):  # global phase g, rail conjugation diag(1,m)
    return mm(plate(m),mm(sc(g,su2(s)),plate(cj(m))))
S=(F(1,2),F(1,2))
def ubeta(b): return ((S,S),(mul(b,S),neg(mul(b,S))))
XM=((Z0,ONE),(ONE,Z0)); ZM=plate(NEG)
panel=[coin(tuple(random.randint(-6,6) for _ in range(3)),random.choice(PH),random.choice(PH)) for _ in range(400)]
panel+= [XM,ZM,ID,sc(I_,XM),((Z0,I_),(ONE,Z0))]+[ubeta(b) for b in PH]
panel+= [mm(plate(m),mm(sc(g,ubeta(b)),plate(cj(m)))) for b in PH for g in PH[:4] for m in PH[4:6]]
panel.append(((ONE,ONE),(ONE,NEG)))   # deliberately NOT unitary: hypothesis filter must reject
res={}; fails=[]
def rec(name,qual,p,f,extra=None):
    res[name]=dict(qualifying=qual,passed=p,failed=f,**(extra or {}))
def Q(U): return n2(U[1][0])
def C(U,l,V=None): return n2(mm(V or U,mm(plate(l),U))[1][0])
def Lt(U,t): return n2(powm(U,t)[1][0])
def R_(U): return n2(add(U[0][0],U[1][1]))
HALF=F(1,2)
good=[U for U in panel if unitary(U)]
# P1
p=f=0
for U in good:
    ok=(1-Lt(U,2)-C(U,NEG))/4==(Q(U)-HALF)**2; p+=ok; f+=not ok
    if not ok: fails.append(("P1",str(U)))
rec("P1",len(good),p,f,dict(cases=len(panel),nonreal_entries=sum(any(z[1]!=0 for r in U for z in r) for U in good)))
# P2
p=f=q1=0;n=0
for U in good:
    q=Q(U)
    for l in PH:
        n+=1
        if q==1: ok=C(U,l)==0; q1+=1
        else:
            A=U[0][0];B=U[1][1]   # |1-l eta|^2 = |A-lB|^2/|A|^2
            ok=1-C(U,l)==4*(q-HALF)**2+q*(1-q)*n2(add(A,neg(mul(l,B))))/n2(A)
        p+=ok; f+=not ok
        if not ok: fails.append(("P2",str(U),str(l)))
rec("P2",n,p,f,dict(q_equals_1_cases=q1))
# P3
p=f=0;n=0
for trial in range(200):
    k=random.randint(1,4); us=random.sample(good,k)
    raw=[F(random.randint(0,9),10) for _ in range(k+1)]
    if sum(raw)==0: continue
    w=[x/sum(raw) for x in raw]; c=w[-1]; w=w[:-1]; n+=1
    a=F(random.randint(0,40),20)
    L=[c/2+sum(wi*Lt(U,t) for wi,U in zip(w,us)) for t in (1,2,3)]
    Cm=c/2+sum(wi*C(U,NEG) for wi,U in zip(w,us))
    ok=(1-L[1]-Cm)/4==sum(wi*(Q(U)-HALF)**2 for wi,U in zip(w,us))
    ok2=L[2]+2*(1-a)*L[1]+(a*a-1)*L[0]==c/2*((a-1)**2+1)+sum(wi*Q(U)*(R_(U)-a)**2 for wi,U in zip(w,us))
    p+=ok and ok2; f+=not(ok and ok2)
    if not(ok and ok2): fails.append(("P3",trial,ok,ok2))
rec("P3",n,p,f)
# P4
p=sum(Lt(U,2)==Q(U)*R_(U) and C(U,NEG)==Q(U)*(4*(1-Q(U))-R_(U)) for U in good)
rec("P4",len(good),p,len(good)-p)
# P5
a=F(3,2); qs=[F(7,16),F(9,16)]
bal=(HALF*a, HALF*(4*HALF-a)); pair=(sum(q*a for q in qs)/2, sum(q*(4*(1-q)-a) for q in qs)/2)
ok=bal==(F(3,4),F(1,4)) and pair==(F(3,4),F(15,64)) and bal[1]-pair[1]==F(1,64)==4*F(1,256)
rec("P5",1,int(ok),int(not ok),dict(balanced=[str(x) for x in bal],pair=[str(x) for x in pair]))
dev=0.0
def fl(q,r,g=cmath.exp(0.7j)):
    x=math.sqrt(r)/2; y=math.sqrt(1-q-x*x); A=complex(x,y); B=cmath.exp(1.1j)*math.sqrt(q)
    return [[g*A,g*B],[-g*B.conjugate(),g*A.conjugate()]]
def fmm(X,Y): return [[X[i][0]*Y[0][j]+X[i][1]*Y[1][j] for j in (0,1)] for i in (0,1)]
l2=cm=0
for q in (7/16,9/16):
    U=fl(q,1.5); l2+=abs(fmm(U,U)[1][0])**2/2; cm+=abs(fmm(U,fmm([[1,0],[0,-1]],U))[1][0])**2/2
dev=max(abs(l2-0.75),abs(cm-15/64)); ok=dev<1e-12
rec("P5f",1,int(ok),int(not ok),dict(max_deviation=dev))
# P6
p=f=n=0; conj=[]
for b in PH:
    l=neg(cj(b))
    for g in PH[:3]:
        for m in PH[3:6]:
            n+=1; T=mm(plate(m),mm(sc(g,ubeta(b)),plate(cj(m)))); Tc=ubeta(cj(b))
            ok=unitary(T) and C(T,l)==1 and C(Tc,l)==b[0]**2; p+=ok; f+=not ok
    conj.append((str(b[0]),str(C(ubeta(cj(b)),l))))
rec("P6",n,p,f,dict(re_beta_and_conjugate_rate=conj))
p=f=n=0
for b in PH:
    l=neg(cj(b))
    for U in good:
        if C(U,l)==1:
            n+=1; ok=Q(U)==HALF and mul(U[1][1],cj(U[0][0]))==neg(mul(b,(n2(U[0][0]),F(0)))); p+=ok; f+=not ok
            if not ok: fails.append(("P6c",str(U)))
rec("P6c",n,p,f,dict(tested=len(PH)*len(good)))
def Hq(u,v): return (((u,F(0)),(v,F(0))),((v,F(0)),(-u,F(0))))   # q=v^2
BAL=ubeta(ONE)                                        # q=1/2, eta=-1
e_c=F(1,10)                                           # count mass c with balanced coin
e=1-(e_c/2+(1-e_c)*C(BAL,NEG)); s1=(e_c==2*e)
m=F(1,3); Hb=Hq(F(4,5),F(3,5)); d=abs(Q(Hb)-HALF)
e2=1-(m*C(Hb,NEG)+(1-m)*C(BAL,NEG)); s2=(m==e2/(4*d*d))
rec("P6s",2,int(s1)+int(s2),2-int(s1)-int(s2),dict(e_count=str(e),e_imbalance=str(e2),d=str(d)))
# P7
p=f=n=0
for (u,v) in [(F(4,5),F(3,5)),(F(12,13),F(5,13)),(F(15,17),F(8,17)),(F(1),F(0))]:
    n+=1; H1,H2=Hq(u,v),Hq(v,u)
    clocks=all((Lt(H1,t)+Lt(H2,t))/2==Lt(BAL,t) for t in range(1,7))
    sign=(n2(mm(H2,mm(ZM,H1))[1][0])+n2(mm(H1,mm(ZM,H2))[1][0]))/2
    bare=(Lt(H1,2)+Lt(H2,2))/2
    true=((Q(H1)-HALF)**2+(Q(H2)-HALF)**2)/2
    ok=unitary(H1) and unitary(H2) and clocks and sign==1 and bare==Lt(BAL,2) and (1-bare-sign)/4==0 and true>0
    p+=ok; f+=not ok
rec("P7",n,p,f,dict(meaning="pass = false pass reproduced: measured D=0, true imbalance>0"))
# P8
p=0
for U in good:
    v0,v1=U[0][0],neg(U[1][0]); V=((neg(v1),v0),(cj(v0),cj(v1)))
    p+= unitary(V) and n2(mm(V,mm(ZM,U))[1][0])==1
rec("P8",len(good),p,len(good)-p,dict(meaning="pass = a setting-dependent second coin saturates the sign rate for this U",
    unbalanced_among_them=sum(Q(U)!=HALF for U in good)))
# P9
UA=((( F(3,5),F(0)),(F(0),F(4,5))),((F(0),F(4,5)),(F(3,5),F(0))))
w=F(625,1152); l2=w*Lt(UA,2)+(1-w)*Lt(XM,2); c1=w*C(UA,ONE)+(1-w)*C(XM,ONE)
true=w*(Q(UA)-HALF)**2+(1-w)*(Q(XM)-HALF)**2; cm=w*C(UA,NEG)+(1-w)*C(XM,NEG)
ok=unitary(UA) and (1-l2-c1)/4==0 and true>0
rec("P9",1,int(ok),int(not ok),dict(meaning="pass = false pass with inactive plate",L2=str(l2),C_inactive=str(c1),
    true_imbalance=str(true),D_with_working_plate=str((1-l2-cm)/4)))
# P10
def cheb(t,r):  # U_{t-1}(x)^2 as polynomial in r=4x^2 : s_t = U_{t-1}(x) satisfies s_{t+1}=2x s_t - s_{t-1}
    # track s_t = alpha + beta*(2x) with (2x)^2=r
    s0=(F(0),F(0)); s1=(F(1),F(0))
    for _ in range(t-1): s0,s1=s1,(s1[1]*r-s0[0], s1[0]-s0[1])
    return s1[0]**2+s1[1]**2*r if s1[0]*s1[1]==0 else None
p=f=n=0
for U in good:
    q,r=Q(U),R_(U)
    for t in range(1,9):
        n+=1; Pw=powm(U,t); h=cheb(t,r); ok=h is not None and n2(Pw[1][0])==q*h and n2(Pw[0][1])==q*h
        p+=ok; f+=not ok
        if not ok: fails.append(("P10",t,str(U)))
rec("P10",n,p,f)
# P11-13
def pairs():
    out=[]
    for (x,y,yp,b) in [(F(0),F(3,5),F(4,5),ONE),(F(1,2),F(7,10),F(1,10),I_)]:
        U1=(((x,y),(x,yp)),((-x,yp),(x,-y))); U2=(((x,yp),(x,y)),((-x,y),(x,-yp)))
        out.append((U1,U2,ubeta(b)))
    return out
GAPS=(1,2,3,4); DEPTH=4
def run(models, redraw):   # models: list of (weight, coin); returns dict transcript->prob
    out={}
    pw={(i,t):powm(Um,t) for i,(_,Um) in enumerate(models) for t in GAPS}
    for start in (0,1):
        for gaps in product(GAPS,repeat=DEPTH):
            for outs in product((0,1),repeat=DEPTH):
                if redraw=="always":
                    pr=F(1); rail=start
                    for g,o in zip(gaps,outs):
                        pr*=sum(wt*n2(pw[(i,g)][o][rail]) for i,(wt,_) in enumerate(models)); rail=o
                elif redraw=="never":
                    pr=F(0)
                    for i,(wt,_) in enumerate(models):
                        x=wt; rail=start
                        for g,o in zip(gaps,outs): x*=n2(pw[(i,g)][o][rail]); rail=o
                        pr+=x
                else:  # redraw only after outcome L(=1): posterior weights carried after R
                    post=[wt for wt,_ in models]; rail=start
                    for g,o in zip(gaps,outs):
                        post=[x*n2(pw[(i,g)][o][rail]) for i,x in enumerate(post)]; rail=o
                        if o==1:
                            tot=sum(post); post=[tot*wt for wt,_ in models]
                    pr=sum(post)
                out[(start,gaps,outs)]=pr
    return out
info=[]; q11=p11=d12=d13=n11=0
for U1,U2,T in pairs():
    hyp=unitary(U1) and unitary(U2) and unitary(T) and Q(U1)+Q(U2)==1 and R_(U1)==R_(U2)==R_(T) and Q(T)==HALF and Q(U1)!=HALF
    n11+=1
    if not hyp: continue
    q11+=1
    tgt=run([(F(1),T)],"always"); red=run([(HALF,U1),(HALF,U2)],"always")
    per=run([(HALF,U1),(HALF,U2)],"never"); half=run([(HALF,U1),(HALF,U2)],"onL")
    same=sum(tgt[k]==red[k] for k in tgt); p11+= same==len(tgt)
    d12+=sum(tgt[k]!=per[k] for k in tgt); d13+=sum(tgt[k]!=half[k] for k in tgt)
    # P14 sign test per launch (coin fixed within launch, redrawn between launches)
    Dm=(1-(Lt(U1,2)+Lt(U2,2))/2-(C(U1,NEG)+C(U2,NEG))/2)/4
    info.append(dict(r=str(R_(T)),q=[str(Q(U1)),str(Q(U2))],transcripts=len(tgt),redraw_equal=same,
        persistent_differ=sum(tgt[k]!=per[k] for k in tgt),redraw_on_L_only_differ=sum(tgt[k]!=half[k] for k in tgt),
        D_sign_test=str(Dm),d_squared=str((Q(U1)-HALF)**2)))
rec("P11",q11,p11,q11-p11,dict(cases=n11,detail=info))
rec("P12",q11,int(d12>0),int(d12==0),dict(meaning="pass = persistent coin is revealed",differing=d12))
rec("P13",q11,int(d13>0),int(d13==0),dict(meaning="pass = outcome-dependent redraw is revealed (outside the note's hypothesis)",differing=d13))
ok=all(i["D_sign_test"]==i["d_squared"] for i in info)
rec("P14",q11,q11 if ok else 0,0 if ok else q11)
# P15
p=f=n=0; zeros=0
for U in good:
    for eps in (F(1,2),F(9,10),F(99,100),F(1)):
        n+=1; Dt=(Q(U)-HALF)**2; Dm=(1-eps*(Lt(U,2)+C(U,NEG)))/4
        ok=Dm>=Dt and not (Dm==0 and Dt>0); p+=ok; f+=not ok; zeros+= Dm==0
rec("P15",n,p,f,dict(measured_zero_cases=zeros,note="loss gives false failure of a balanced coin, never a false pass, per original launch"))
# P16
x1,x2=F(3,4),F(15,64); rho=F(9,10)
ps=lambda x: x/(x+rho*(1-x)); Dp=(1-ps(x1)-ps(x2))/4
xc=F(1,65); Dc=(1-(x1+xc*(1-x1))-(x2+xc*(1-x2)))/4
ok=Dp<=0 and Dc==0
rec("P16",2,2 if ok else 0,0 if ok else 2,dict(meaning="pass = false pass exists outside the note's per-launch, no-confusion hypotheses",
    D_postselected_rho_9_10=str(Dp),D_confusion_1_65=str(Dc),D_true="1/256"))
res["_rejected_by_hypothesis"]=dict(panel=len(panel),unitary=len(good),nonunitary=len(panel)-len(good))
res["_failed_cases"]=[list(map(str,x)) for x in fails]
with open(sys.argv[1],"x",encoding="utf-8",newline="\n") as fh:
    json.dump(res,fh,indent=1,sort_keys=True); fh.write("\n")
for k in sorted(res):
    if k[0]=="P": print(k,res[k]["qualifying"],res[k]["passed"],res[k]["failed"])
print("failed cases kept:",len(fails))
sys.exit(1 if any(res[k]["failed"] for k in res if k[0]=="P") else 0)
