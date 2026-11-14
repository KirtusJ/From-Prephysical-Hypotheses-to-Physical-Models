"""Builder program: vertex product events on the signed line, start (0,R), F_y = F_d, factor 2.
Written before reading FINDINGS.md / programs of Product_Events.  Seed 20261113 (no random draws are used).

Carrier (from THEOREM.md Lemma 1): vertices (x,d); arcs (x,R)->(x+1,R) gain +, (x,R)->(x-1,L) gain +,
(x,L)->(x+1,R) gain +, (x,L)->(x-1,L) gain -.  Event = all walks of length t from (0,R) whose s-th vertex
lies in A_s.  Pair m=(p,q) = numbers of walks of gain +1,-1 ending at a vertex.

Construction under test, joint(H1,H2,a): H1 (length t1, all walks end at y1=(x1,d1), pair u), H2 (t2, y2, pair v;
t2=0 means the empty event, pair (1,0)), a>t1.  Upper branch: step R, H1 shifted by (time 1, pos 1), then R^k,
k=a+t2-t1.  Lower: L^a, R, H2 shifted by (time a+1, pos 1-a).  At T0=a+1+t2 upper site xU, lower xL, D=(xU-xL)/2;
upper L^(D-1), lower R^(D-1); last step upper L, lower R to position X.

PREDICATES (fixed before first run):
H0 (hypothesis, per call): a>t1, H1 and H2 each end at one vertex; number of calls qualifying is reported.
Q1 for every call: D>=1 and the exact family of the event (transfer DP over the vertex sets) is supported on
   {(X,R),(X,L)} with m(X,L) in {u,swap u} and m(X,R) in {v',swap v'}, v'=v if a odd else swap v.
   For total length <=18 the DP family equals the family by brute enumeration of all 2^T step sequences.
Q2 every pair (p,q)!=(0,0) with p+q<=NMAX is realized alone at an R vertex and alone at an L vertex,
   by gadgets generated only from (1,0) with joint(.,empty) and one-step extensions.
Q3 unknowns F_R(m),F_L(m), 1<=|m|<=NMAX.  Equations mu(Ext S)=2 mu(S), both sides from the DP family of S and of
   its full continuation, for S = each single gadget (at R and at L) and each joint(H_u,H_v), |v|<=2, |u|+|v|<=NMAX.
   Exact rational nullity is 2 and the null space is spanned by F_R=F_L=p+q and F_R=F_L=(p-q)^2.
Q4 (expected to show the |v|=2 equations are needed): with joints restricted to v=(1,0),(0,1) the nullity is >2
   (hand count 4 at NMAX=6).
"""
import sys, json, itertools, random
from fractions import Fraction
import sympy
random.seed(20261113)
NMAX=6
swap=lambda m:(m[1],m[0])
add=lambda a,b:(a[0]+b[0],a[1]+b[1])

def step(fam):
    out={}
    for (x,d),m in fam.items():
        r=(x+1,'R'); out[r]=add(out.get(r,(0,0)),m)
        l=(x-1,'L'); out[l]=add(out.get(l,(0,0)),m if d=='R' else swap(m))
    return out
def family(A):
    fam={(0,'R'):(1,0)}
    for As in A:
        fam={y:m for y,m in step(fam).items() if y in As}
    return fam
def brute(A):
    fam={}
    for seq in itertools.product('RL',repeat=len(A)):
        x=0; prev='R'; g=0; ok=True
        for s,d in enumerate(seq):
            x+= 1 if d=='R' else -1
            if prev=='L' and d=='L': g^=1
            prev=d
            if (x,d) not in A[s]: ok=False;break
        if ok:
            m=fam.get((x,prev),(0,0)); fam[(x,prev)]=(m[0]+(g==0),m[1]+(g==1))
    return fam
def shift(A,dx): return [{(x+dx,d) for (x,d) in As} for As in A]
def endv(A):
    if not A: return (0,'R')
    f=family(A); assert len(f)==1; return next(iter(f))

calls=dict(total=0,qual=0,q1fail=0,brute=0,brutefail=0)
def joint(H1,H2,a):
    calls['total']+=1
    t1,t2=len(H1),len(H2)
    f1=family(H1); f2=family(H2) if H2 else {(0,'R'):(1,0)}
    if not(a>t1 and len(f1)==1 and len(f2)==1): return None
    calls['qual']+=1
    (y1,u),=f1.items(); (y2,v),=f2.items()
    k=a+t2-t1; T0=a+1+t2
    A=[set() for _ in range(T0)]
    A[0].add((1,'R'))
    for s,As in enumerate(shift(H1,1)): A[1+s]|=As
    xU=y1[0]+1
    for i in range(k): xU+=1; A[t1+1+i].add((xU,'R'))
    for s in range(1,a+1): A[s-1].add((-s,'L'))
    A[a].add((1-a,'R'))
    for s,As in enumerate(shift(H2,1-a)): A[a+1+s]|=As
    xL=1-a+y2[0]
    D=(xU-xL)//2
    ok = (xU-xL)%2==0 and D>=1
    for i in range(1,D): A.append({(xU-i,'L'),(xL+i,'R')})
    X=xU-D; A.append({(X,'L'),(X,'R')})
    fam=family(A)
    vp=v if a%2 else swap(v)
    ok = ok and set(fam)=={(X,'R'),(X,'L')} and fam[(X,'L')] in (u,swap(u)) and fam[(X,'R')] in (vp,swap(vp))
    if not ok: calls['q1fail']+=1
    if len(A)<=18:
        calls['brute']+=1
        if brute(A)!=fam: calls['brutefail']+=1
    return A,X,fam

# Q2: gadgets
gad={('R',(1,0)):[{(1,'R')}]}
def reg(A):
    f=family(A)
    if len(f)!=1: return
    (y,m),=f.items()
    if m[0]+m[1]>NMAX: return
    key=(y[1],m)
    if key not in gad or len(A)<len(gad[key]): gad[key]=A; return True
def closure(A):
    f=family(A); (y,m),=f.items(); x=y[0]
    B=A+[{(x+1,'R')}]; reg(B)
    C=A+[{(x-1,'L')}]; reg(C); reg(C+[{(x-2,'L')}]); reg(C+[{(x-2,'L')},{(x-1,'R')}]); reg(C+[{(x,'R')}])
closure(gad[('R',(1,0))])
joints=[]
for N in range(1,NMAX):
    for key in sorted(k for k in gad if sum(k[1])==N and k[0]=='R'):
        H=gad[key]; a=len(H)+1; a+= (a%2==0)
        r=joint(H,[],a)
        A,X,fam=r
        for tgt in ((X+1,'R'),(X-1,'L')):
            B=A+[{tgt}]; reg(B); closure(B)
allp=[(p,n-p) for n in range(1,NMAX+1) for p in range(n+1)]
missing=[(d,m) for d in 'RL' for m in allp if (d,m) not in gad]

# Q3
idx={(d,m):i for i,(d,m) in enumerate((d,m) for d in 'RL' for m in allp)}
def eqn(A):
    f=family(A); g=step(f)
    row=[0]*len(idx)
    for (y,m) in g.items():
        if sum(m)>NMAX: return None
        row[idx[(y[1],m)]]+=1
    for (y,m) in f.items(): row[idx[(y[1],m)]]-=2
    return row
rows_single=[]; rows_lone=[]; rows_two=[]
for (d,m),A in sorted(gad.items()):
    r=eqn(A)
    if r: rows_single.append(r)
for (d,u),H in sorted(gad.items()):
    if d!='R': continue
    for (d2,v),H2 in sorted(gad.items()):
        if d2!='R' or sum(v)>2 or sum(u)+sum(v)>NMAX: continue
        a=len(H)+1
        H2e=[] if v==(1,0) else H2
        res=joint(H,H2e,a)
        r=eqn(res[0])
        if r: (rows_lone if sum(v)==1 else rows_two).append(r)
def nullity(rows):
    M=sympy.Matrix(rows); return M.cols-M.rank(), M
n3,M3=nullity(rows_single+rows_lone+rows_two)
n4,_=nullity(rows_single+rows_lone)
vn=sympy.Matrix([m[0]+m[1] for (d,m) in idx]); vs=sympy.Matrix([(m[0]-m[1])**2 for (d,m) in idx])
span_ok = (M3*vn).is_zero_matrix and (M3*vs).is_zero_matrix and sympy.Matrix.hstack(vn,vs).rank()==2
res=dict(NMAX=NMAX,calls=calls,Q1=calls['q1fail']==0 and calls['brutefail']==0 and calls['total']==calls['qual'],
 Q2=not missing,missing=missing,gadget_lengths={f"{d}{m}":len(A) for (d,m),A in sorted(gad.items())},
 n_eq=dict(single=len(rows_single),lone=len(rows_lone),two=len(rows_two)),unknowns=len(idx),
 Q3_nullity=n3,Q3=(n3==2 and span_ok),Q4_nullity_lone_only=n4,Q4=n4>2)
with open(sys.argv[1],'x') as fh: json.dump(res,fh,indent=1)
print(json.dumps({k:v for k,v in res.items() if k!='gadget_lengths'}))
print(max(res['gadget_lengths'].values()))
