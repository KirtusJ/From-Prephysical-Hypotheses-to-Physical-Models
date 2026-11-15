"""Own cross-check (fixed before first run).
P0 control: #order-2 elements of C2xC4 == 3.
P1 brute force: dim of real solutions F of F(U+V)+F(U+JV)=2F(U)+2F(V) on multisets of size<=4
   (equations for |U|+|V|<=4) over C2xC4 with J=mult by j, for j in each order-2 element:
   no switching == 14; with full switching (F(gU)=F(U)) == 3 for j=(0,2), 4 for (1,0),(1,2).
   Hypothesis test per instance: j has order 2 (fixed-point-free involution) -- counted.
P2 G10 Thm 5.18 formula, B=[[1,J]...]: |J0|+#unordered pairs in U equals brute no-switch dim.
P3 five-sheet mu10: brute dim no switching ==20, switching ==4 (size<=3 truncation, size<=4 if fast).
P4 witness rows (2,2,2,2,2),(0,..): faithful (s=1,2) Fourier values equal (both 0); s=0 values 10 vs 0;
   sum D^2 = 20 vs 0; (sum D)^2 = 100 vs 0.
P5 staircase g(x)=floor(x/2) mod M, start (0,R), minus only L->L, M in {5,6,7,9}: the n paths at
   (n-1,R), t=n+1, are all positive with gains a consecutive interval; W_n formula (2) and second
   difference 2C(n) hold for random weights with c+sum b=1, n=1..M+1.
P6 t=5 port (1,R): (gain,sign) multiset == note list; eq (3) holds for M in {5,6,7,9} random weights.
P7 at n=M+1 counting minus uniform-squares probability == 2/2^(M+2) in absolute value.
Result file refuses overwrite.
"""
import itertools, json, os, sys, random, cmath, math
import numpy as np
from fractions import Fraction
out=sys.argv[1]
if os.path.exists(out): sys.exit("refuse overwrite")
R={}
def ms_list(n,s):
    return [c for k in range(s+1) for c in itertools.combinations_with_replacement(range(n),k)]
def soldim(elems,mul,j,s,switch):
    n=len(elems); idx={e:i for i,e in enumerate(elems)}
    Ms=[tuple(sorted(m)) for m in ms_list(n,s)]; pos={m:i for i,m in enumerate(Ms)}
    Jm=lambda m: tuple(sorted(idx[mul(elems[a],j)] for a in m))
    rows=[]
    for U in Ms:
        for V in Ms:
            if len(U)+len(V)>s or U>V and False: continue
            r=np.zeros(len(Ms)); r[pos[tuple(sorted(U+V))]]+=1; r[pos[tuple(sorted(U+Jm(V)))]]+=1
            r[pos[U]]-=2; r[pos[V]]-=2; rows.append(r)
    if switch:
        for g in elems:
            for U in Ms:
                r=np.zeros(len(Ms)); r[pos[tuple(sorted(idx[mul(g,elems[a])] for a in U))]]+=1; r[pos[U]]-=1; rows.append(r)
    A=np.array(rows); return len(Ms)-np.linalg.matrix_rank(A)
C24=[(a,b) for a in range(2) for b in range(4)]
m24=lambda x,y:((x[0]+y[0])%2,(x[1]+y[1])%4)
o2=[e for e in C24 if e!=(0,0) and m24(e,e)==(0,0)]
R['P0']={'value':len(o2),'pass':len(o2)==3}
P1={};P2={}
for j in o2:
    hyp=all(m24(e,j)!=e for e in C24)
    d0=soldim(C24,m24,j,4,False); d1=soldim(C24,m24,j,4,True)
    exp1=3 if j==(0,2) else 4
    # G10 formula
    chars=[(a,b) for a in range(2) for b in range(4)]
    ev=lambda ch,x: (-1)**(ch[0]*x[0])*1j**(ch[1]*x[1])
    J0=[c for c in chars if abs(ev(c,j)-1)<1e-9]
    U=[c for c in chars if abs(ev(c,j)+1)<1e-9]
    pairs={frozenset([p,q]) for p in U for q in chars if abs(ev(p,j)*ev(q,j)-1)<1e-9 and q in chars}
    pairs={pr for pr in pairs}
    f=len(J0)+len(pairs)
    P1[str(j)]={'hyp_fpf':hyp,'nosw':int(d0),'sw':int(d1),'pass':hyp and d0==14 and d1==exp1}
    P2[str(j)]={'formula':f,'brute':int(d0),'pass':f==d0}
R['P1']=P1;R['P2']=P2
mu=[(s,k) for s in (0,1) for k in range(5)]
mm=lambda x,y:((x[0]+y[0])%2,(x[1]+y[1])%5)
R['P3']={'nosw':int(soldim(mu,mm,(1,0),3,False)),'sw':int(soldim(mu,mm,(1,0),3,True))}
R['P3']['pass']=R['P3']['nosw']==20 and R['P3']['sw']==4
def four(D,s,M): return sum(D[k]*cmath.exp(2j*math.pi*s*k/M) for k in range(M))
a=[2]*5;b=[0]*5
R['P4']={'faithful':[abs(four(a,s,5))<1e-9 and abs(four(b,s,5))<1e-9 for s in (1,2)],
 's0':[four(a,0,5).real,four(b,0,5).real],'sq':[sum(x*x for x in a),0],'tot':[sum(a)**2,0]}
R['P4']['pass']=all(R['P4']['faithful']) and R['P4']['s0']==[10,0] and R['P4']['sq'][0]==20 and R['P4']['tot'][0]==100
def walk(t,M):
    h={(0,'R'):[(0,1)]}  # list of (sheet residue unreduced, sign)
    for _ in range(t):
        nh={}
        for (x,d),L in h.items():
            g=x//2
            for d2 in 'RL':
                sg=-1 if (d=='L' and d2=='L') else 1
                nx=x+(1 if d2=='R' else -1)
                nh.setdefault((nx,d2),[]).extend((r+g,s*sg) for r,s in L)
        h=nh
    return h
def P(L,t,M,c,bs):
    N=len(L); D=[0]*M
    for r,s in L: D[r%M]+=s
    return (c*N+sum(bs[s]*abs(four(D,s,M))**2 for s in range(M)))/2**t
rng=random.Random(11)
P5={};P6={};P7={}
for M in (5,6,7,9):
    w=[rng.random() for _ in range(M+1)]; S=sum(w); c=w[0]/S; bs=[x/S for x in w[1:]]
    C=lambda h:sum(bs[s]*math.cos(2*math.pi*s*h/M) for s in range(M))
    ok=True; interval=True; Wl=[0]
    for n in range(1,M+3):
        L=walk(n+1,M)[(n-1,'R')]
        if len(L)!=n or any(s!=1 for _,s in L): interval=False
        gs=sorted(r for r,_ in L)
        if gs!=list(range(gs[0],gs[0]+n)): interval=False
        W=2**(n+1)*P(L,n+1,M,c,bs); Wl.append(W)
        if abs(W-(n+2*sum((n-h)*C(h) for h in range(1,n))))>1e-9: ok=False
    sd=all(abs(Wl[n+1]-2*Wl[n]+Wl[n-1]-2*C(n))<1e-9 for n in range(1,M+2))
    P5[M]={'interval_hyp':interval,'formula':ok,'second_diff':sd,'CM=1-c':abs(C(M)-(1-c))<1e-12,'pass':interval and ok and sd}
    L5=walk(5,M)[(1,'R')]
    lst=sorted(L5); note=sorted([(1,-1),(0,1),(-1,-1),(-1,1),(-2,1),(-3,-1)])
    e3=32*P(L5,5,M,c,bs); r3=4+2*c-4*C(1)+2*C(2)-4*C(3)+2*C(4)
    P6[M]={'list':[list(x) for x in lst],'list_match':lst==note,'eq3':abs(e3-r3)<1e-9,'applies(M>=5)':M>=5,'pass':lst==note and abs(e3-r3)<1e-9}
    L=walk(M+2,M)[(M,'R')]
    pc=P(L,M+2,M,1,[0]*M); pu=P(L,M+2,M,0,[1/M]*M)
    P7[M]={'diff':pc-pu,'pass':abs(abs(pc-pu)-2/2**(M+2))<1e-12}
R['P5']=P5;R['P6']=P6;R['P7']=P7
with open(out,'x') as f: json.dump(R,f,indent=1,default=str)
print(json.dumps(R,default=str)[:3000])
