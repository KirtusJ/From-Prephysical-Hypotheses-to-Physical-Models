"""Builder program for G1 (exact arithmetic, no randomness; seed 20261113 unused).
Predicates fixed before first run:
 P1a box system F(a+b)+F(a+sb)=2F(a)+2F(b), all a,b in [0..B]^2 staying in box, F(0,0)=0, B=6:
     nullity == 2 and count (p+q) and square (p-q)^2 both in the null space.
 P1b quadratic ansatz F=al p+be q+ga p^2+de pq+ep q^2 under sharp-launch site conservation with
     factor 2, ticks 0..T-1 on the unwrapped line: nullity == 2 at some T<=10; report first such T.
 P1c sharp launch counts: tick3 (-1,L)=(1,1); tick4 (0,L)=(2,1), (2,L)=(1,0).
 P4a every splitter in [-2..2]^4 with ab+cd=0, a^2+c^2=b^2+d^2>0 is square-consistent to T=7.
 P4b every square-consistent splitter is orthogonal/equal-length (EXPECTED TO FAIL on degenerate ones; list).
 P4c no non-orthogonal splitter admits f=|k| (EXPECTED TO FAIL; list).
 Hypothesis per splitter: 'informative' = some tick has >=2 occupied sites or a site with u!=0!=v.
"""
import json, itertools
from fractions import Fraction as Fr
def nullity(rows, n):
    rows=[r[:] for r in rows]; rank=0
    for c in range(n):
        piv=next((i for i in range(rank,len(rows)) if rows[i][c]!=0),None)
        if piv is None: continue
        rows[rank],rows[piv]=rows[piv],rows[rank]
        pv=rows[rank][c]
        for i in range(len(rows)):
            if i!=rank and rows[i][c]!=0:
                f=Fr(rows[i][c],pv); rows[i]=[x-f*y for x,y in zip(rows[i],rows[rank])]
        rank+=1
    return n-rank
res={}
# P1a
B=6; idx={(p,q):i for i,(p,q) in enumerate(itertools.product(range(B+1),repeat=2))}; n=len(idx)
rows=[]; 
r=[0]*n; r[idx[(0,0)]]=1; rows.append(r)
pts=list(idx)
for a in pts:
    for b in pts:
        s=(a[0]+b[0],a[1]+b[1]); d=(a[0]+b[1],a[1]+b[0])
        if s in idx and d in idx:
            r=[0]*n; r[idx[s]]+=1; r[idx[d]]+=1; r[idx[a]]-=2; r[idx[b]]-=2; rows.append(r)
nu=nullity(rows,n)
ok=lambda v: all(sum(x*y for x,y in zip(r,v))==0 for r in rows)
cnt=[p+q for (p,q) in pts]; sq=[(p-q)**2 for (p,q) in pts]
res['P1a']={'B':B,'equations':len(rows),'nullity':nu,'count_in':ok(cnt),'square_in':ok(sq),'pass':nu==2 and ok(cnt) and ok(sq)}
# sharp launch counts
def step(st):
    new={}
    sites={x for (x,_) in st}
    for x in sites:
        pR,qR=st.get((x,'R'),(0,0)); pL,qL=st.get((x,'L'),(0,0))
        new[(x+1,'R')]=(pR+pL,qR+qL); new[(x-1,'L')]=(pR+qL,qR+pL)
    return new
hist=[{(0,'R'):(1,0)}]
for t in range(11): hist.append(step(hist[-1]))
res['P1c']={'t3(-1,L)':hist[3][(-1,'L')],'t4(0,L)':hist[4][(0,'L')],'t4(2,L)':hist[4][(2,'L')]}
res['P1c']['pass']=res['P1c']=={'t3(-1,L)':(1,1),'t4(0,L)':(2,1),'t4(2,L)':(1,0)}
mon=lambda pq:[pq[0],pq[1],pq[0]**2,pq[0]*pq[1],pq[1]**2]
rows=[]; first=None; trace=[]
for t in range(10):
    st=hist[t]; nx=hist[t+1]
    for x in {x for (x,_) in st}:
        R=st.get((x,'R'),(0,0)); L=st.get((x,'L'),(0,0))
        r=[i+j-2*k-2*l for i,j,k,l in zip(mon(nx[(x+1,'R')]),mon(nx[(x-1,'L')]),mon(R),mon(L))]
        rows.append(r)
    nu=nullity(rows,5); trace.append((t+1,nu))
    if nu==2 and first is None: first=t+1
res['P1b']={'nullity_by_T':trace,'first_T_nullity2':first,'pass':first is not None and trace[-1][1]==2}
# B4
def run(a,b,c,d,T=7):
    st={(0,'R'):1}; ticks=[]
    for t in range(T):
        new={}; sites=[]
        for x in {x for (x,_) in st}:
            u=st.get((x,'R'),0); v=st.get((x,'L'),0)
            o1=a*u+b*v; o2=c*u+d*v
            new[(x+1,'R')]=o1; new[(x-1,'L')]=o2
            if (u,v)!=(0,0): sites.append((u,v,o1,o2))
        ticks.append(sites); st=new
    return ticks
def consistent(ticks,g):
    for sites in ticks:
        rat=set()
        for u,v,o1,o2 in sites:
            den=g(u)+g(v); num=g(o1)+g(o2)
            if den==0:
                if num!=0: return False
            else: rat.add(Fr(num,den))
        if len(rat)>1: return False
    return True
O=[];S=[];A=[];info={}
for sp in itertools.product(range(-2,3),repeat=4):
    a,b,c,d=sp; ticks=run(*sp)
    info[sp]=any(len(s)>=2 or any(u!=0 and v!=0 for u,v,_,_ in s) for s in ticks)
    if a*b+c*d==0 and a*a+c*c==b*b+d*d and a*a+c*c>0: O.append(sp)
    if consistent(ticks,lambda k:k*k): S.append(sp)
    if consistent(ticks,abs): A.append(sp)
SO=[s for s in S if s not in O]; AO=[s for s in A if s not in O]
res['P4']={'splitters':625,'informative':sum(info.values()),'orth':len(O),'square_consistent':len(S),
 'P4a_pass':all(o in S for o in O),'P4b_pass':not SO,'square_not_orth':SO,'square_not_orth_informative':[s for s in SO if info[s]],
 'P4c_pass':not AO,'abs_not_orth_informative':[s for s in AO if info[s]],'abs_not_orth_count':len(AO),
 'abs_and_orth_informative':[s for s in A if s in O and info[s]]}
with open('result_b1_b4.json','x') as fh: json.dump(res,fh,indent=1,default=str)
print(json.dumps(res,default=str)[:3500])
