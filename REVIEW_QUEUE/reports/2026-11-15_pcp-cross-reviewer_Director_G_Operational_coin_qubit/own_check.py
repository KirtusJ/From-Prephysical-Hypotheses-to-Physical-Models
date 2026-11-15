"""Own check of Operational_coin_qubit.md (cross-review, same sources; not independent).
Predicates fixed before first run:
P1 cap24,L=6: meeting counts by j over 2^23 = (1339052,6232407,640002), timeout 177147.
P2 S(cap24) == 134503435/67108864 (float, |diff|<1e-12: double rounding, ~25 terms).
P3 S(cap20) = 1.99946666... (first 8 decimals).  P4 contact off cap24 S = 0.504257366...
P5 concurrence 2|det psi| = |sin(h g)| for g=0..2; = sqrt3/2 at g=1.
P6 literal coordinate propagation (L=6, M=3, cap 12, both ports): every complete transcript has
   prob 2^(1-d) and normalized Kraus equals note's formula (row placement, signs, T^(a sum)).
   Hypothesis per instance: transcript prob>0 and the two arms occupy distinct cells.
P7 mirror excursion k=1..5 (L=6): accepted operator = (-1)^(k-1) 2^((1-2k)/2) X diag(w^{k^2},w^{-k^2}) H.
   Hypothesis per instance: k<L, M|L.
P8 Bloch axes after 0,1,2 G: (0,0,1),(-1,0,0),(0,sqrt3/2,1/2); Gram det of R,L,GR,G^2R = 3/16.
Unreported: L=9 cap 24 and L=6 cap 30 S values (predicate: total probability 1).
"""
import numpy as np, json, os, itertools
from fractions import Fraction as F
w=np.exp(-2j*np.pi/3); H=np.array([[1,1],[1,-1]])/np.sqrt(2)
X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);Y=np.array([[0,-1j],[1j,0]])
res={}
def step(state,start,L):
    g={}
    for (site,c),a in state.items():
        for d in (1,-1):
            out=(site+d)%(2*L); dl=(out-start)%(2*L); r=min(dl,2*L-dl)
            v=a*w**(site%3)*(-1 if c==d==-1 else 1)/np.sqrt(2)
            g.setdefault(r,{}); g[r][(out,d)]=g[r].get((out,d),0)+v
    return g
def formula(path):
    d=len(path)-1; j=sum(path[:-1])%3; U=np.zeros((2,2),complex)
    for ai,a in enumerate((1,-1)):
        moves=[a*(path[i+1]-path[i]) for i in range(d)]
        ll=sum(1 for m1,m2 in zip(moves,moves[1:]) if m1==m2==-1)
        fin=a*(path[-1]-path[-2]); row=0 if fin==1 else 1
        U[row]+=w**(a*j)*(-1)**ll*H[ai]
    return U
# P6
mx=0;n=0;hyp_fail=0;pfail=0
for start in (0,6):
    stack=[({(start,1):np.array([1,0j]),(start,-1):np.array([0j,1])},[0])]
    while stack:
        st,path=stack.pop(); t=len(path)-1
        if t>0 and path[-1] in (0,6):
            p=sum(np.vdot(v,v).real for v in st.values())/2  # avg over input basis = trace/2
            cells=len(st)
            if p<=0 or cells!=2: hyp_fail+=1
            if abs(p-2.0**(1-t))>1e-12: pfail+=1
            site=(start+path[-1])%12
            U=np.stack([st.get((site,dd),np.zeros(2)) for dd in (1,-1)])/np.sqrt(2.0**(1-t))
            mx=max(mx,np.abs(U-formula(path)).max()); n+=1; continue
        if t==12: continue
        for r,ch in step(st,start,6).items(): stack.append((ch,path+[r]))
res['P6']=dict(transcripts=n,hyp_fail=hyp_fail,prob_fail=pfail,max_resid=mx,ok=bool(mx<1e-12 and pfail==0 and hyp_fail==0))
# P7
p7=[]
for k in range(1,6):
    hyp=k<6 and 6%3==0
    st={(0,1):np.array([1,0j]),(0,-1):np.array([0j,1])}; path=[0]
    for jj in range(1,2*k+1):
        want=min(jj,2*k-jj); st=step(st,0,6)[want]
    U=np.stack([st.get((0,dd),np.zeros(2)) for dd in (1,-1)])
    pred=(-1)**(k-1)*2**((1-2*k)/2)*X@np.diag([w**(k*k),w**(-k*k)])@H
    p7.append(dict(k=k,hyp=hyp,resid=float(np.abs(U-pred).max())))
res['P7']=dict(rows=p7,ok=all(r['resid']<1e-12 for r in p7))
# P8
G=X@np.diag([w,1/w])@H
def axis(M): return [round(float(np.real(np.trace(M.conj().T@P@M)/2)),12) for P in (X,Y,Z)]
ax=[axis(np.linalg.matrix_power(G,n)) for n in range(3)]
R=np.array([1,0j]);Lv=np.array([0,1+0j]);preps=[R,Lv,G@R,G@G@R]
rho=[np.outer(v,v.conj()) for v in preps];Gm=np.array([[np.trace(a@b).real for b in rho] for a in rho])
res['P8']=dict(axes=ax,gram_det=float(np.linalg.det(Gm)),ok=bool(np.allclose(ax,[[0,0,1],[-1,0,0],[0,np.sqrt(3)/2,.5]]) and abs(np.linalg.det(Gm)-3/16)<1e-12))
# Source & CHSH
h=2*np.pi/3
def psi(g):
    v=np.zeros(4,complex)
    for u,vv in itertools.product((1,-1),repeat=2):
        v[2*(u==-1)+(vv==-1)]=0.5*np.exp(-1j*h*(-u-vv+g*(u==vv)))
    return v
res['P5']=[dict(g=g,C=float(2*abs(psi(g)[0]*psi(g)[3]-psi(g)[1]*psi(g)[2])),sin=abs(np.sin(h*g))) for g in range(3)]
def corr(ps,A,B): return float(np.vdot(ps,np.kron(A,B)@ps).real)
def excursions(cap,L):
    act={(1,1,0,(0,0)):F(1)}; meet={}; cnt={}
    for t in range(1,cap):
        nxt={}
        for (r,dl,j,ll),p in act.items():
            for d in (1,-1):
                # arm + moves d, arm - moves -d; LL if previous and current both -1 on that arm
                llp=ll[0]+(dl==-1 and d==-1); llm=ll[1]+(dl==1 and d==1)
                key=(r+d,d,(j+r)%3,(llp,llm))
                if r+d in (0,L): k=(d,(j+r)%3,(-1)**(llp+llm)); meet[k]=meet.get(k,0)+p/2
                else: nxt[key]=nxt.get(key,0)+p/2
        act=nxt
    return meet,sum(act.values())
def chsh(cap,L,g,gpol=1):
    pp=psi(gpol); ps=psi(g)
    t=np.array([sum(corr(pp,A,P) for A in (Z,X)) for P in (X,Y,Z)])
    meet,to=excursions(cap,L); E0={'Z':0.,'X':0.}; cj=[F(0)]*3
    for (d,j,s),p in meet.items():
        cj[j]+=p
        perm=X if d==-1 else np.eye(2)
        U=perm@np.diag([w**j,s*w**(-j)])@H
        sc={}
        for nm,O in (('X',X),('Z',Z)):
            M=U.conj().T@O@U; bl=np.array([np.real(np.trace(M@P))/2 for P in (X,Y,Z)]); sc[nm]=float(t@bl)
        b='Z' if abs(sc['Z'])>=abs(sc['X']) else 'X'; sg=1 if sc[b]>=0 else -1
        O=U.conj().T@(X if b=='X' else Z)@U
        for A,nm in ((Z,'Z'),(X,'X')): E0[nm]+=float(p)*sg*corr(ps,A,O)
    for A,nm in ((Z,'Z'),(X,'X')): E0[nm]+=float(to)*corr(ps,A,-X)
    E1={nm:corr(ps,A,-X) for A,nm in ((Z,'Z'),(X,'X'))}
    S=E0['Z']+E1['Z']+E0['X']-E1['X']
    return S,[int(c*2**(cap-1)) for c in cj],int(to*2**(cap-1)),float(sum(meet.values())+to),[[E0['Z'],E1['Z']],[E0['X'],E1['X']]]
S24,cj,to,tot,E=chsh(24,6,1)
res['P1']=dict(counts=cj,timeout=to,ok=cj==[1339052,6232407,640002] and to==177147)
res['P2']=dict(S=S24,E=E,target=134503435/67108864,ok=abs(S24-134503435/67108864)<1e-12)
S20=chsh(20,6,1)[0];res['P3']=dict(S=S20,ok=f"{S20:.8f}"=="1.99946666" or abs(S20-1.99946666)<1e-8)
S0=chsh(24,6,0)[0];res['P4']=dict(S=S0,ok=abs(S0-0.504257366)<1e-9)
for cap,L in ((24,9),(30,6),(22,6)):
    s,c,tt,tot,_=chsh(cap,L,1); res[f'unrep_L{L}_cap{cap}']=dict(S=s,counts=c,timeout=tt,total=tot,ok=abs(tot-1)<1e-15)
with open('own_results.json','x') as f: json.dump(res,f,indent=1,default=str)
print(json.dumps(res,default=str)[:3000])
