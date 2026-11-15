"""Predicates fixed before run:
P0 control: walks len 6 from (0,R) ending at position 0.
Hyp per instance: H1,H2 are gadgets (all walks end at one vertex, nonempty), a>t1.
P1 every walk of the construction is an upper walk (prefix R, then H1 walk) or lower walk (L^a R H2-walk), i.e. no branch change.
P2 end vertices exactly (X,L) with pair in {u,swap u} and (X,R) with pair in {v,swap v}.
P3 branches share no vertex after time 0 (on A-sets as built from H1,H2 sets as given).
Run A: gadgets trimmed (A_s = vertices on surviving walks). Run B: gadgets with untrimmed junk in A_s."""
import itertools,random,sys
random.seed(1)
def succ(v):
    x,d=v; return [((x+1,'R'),1),((x-1,'L'),1 if d=='R' else -1)]
def walks(A):
    W=[[((0,'R'),)] ,]
    cur=[((0,'R'),1)]
    paths=[(((0,'R'),),1)]
    for S in A:
        paths=[(p+(w,),g*s) for p,g in paths for w,s in succ(p[-1]) if w in S]
    return paths
def pairs(paths):
    m={}
    for p,g in paths:
        e=p[-1]; c=m.setdefault(e,[0,0]); c[0 if g==1 else 1]+=1
    return {k:tuple(v) for k,v in m.items()}
def randevent(t):
    A=[];reach={(0,'R')}
    for s in range(t):
        nb={w for v in reach for w,_ in succ(v)}
        S=set(random.sample(sorted(nb),random.randint(1,len(nb)))) if nb else set()
        A.append(S);reach=S
    return A
def trim(A):
    P=walks(A);return [ {p[s+1] for p,_ in P} for s in range(len(A))]
def construct(A1,A2,a,u_end,v_end):
    t1,t2=len(A1),len(A2)
    up=[{(1,'R')}]+[{(x+1,d) for x,d in S} for S in A1]
    y=u_end[0]+1
    k=a+t2-t1
    for i in range(k): y+=1; up.append({(y,'R')})
    lo=[{(-s,'L')} for s in range(1,a+1)]+[{(-a+1,'R')}]+[{(x+1-a,d) for x,d in S} for S in A2]
    T=len(up); assert T==len(lo)==a+1+t2
    yl=v_end[0]+1-a; D=(y-yl)//2; assert (y-yl)%2==0 and D>=1
    for i in range(D): y-=1; up.append({(y,'L')}); yl+=1; lo.append({(yl,'R')})
    return up,lo,y
def check(A1,A2,a):
    P1=walks(A1);P2=walks(A2)
    e1=pairs(P1);e2=pairs(P2) if A2 else {(0,'R'):(1,0)}
    if len(e1)!=1 or len(e2)!=1: return None
    (ue,u),(ve,v)=list(e1.items())[0],list(e2.items())[0]
    up,lo,X=construct(A1,A2,a,ue,ve)
    A=[s|l for s,l in zip(up,lo)]
    Pall=walks(A)
    ok1=all(all(p[i+1] in up[i] for i in range(len(up))) or all(p[i+1] in lo[i] for i in range(len(lo))) for p,_ in Pall)
    m=pairs(Pall); sw=lambda z:(z[1],z[0])
    ok2=set(m)=={(X,'L'),(X,'R')} and m[(X,'L')] in (u,sw(u)) and m[(X,'R')] in (v,sw(v))
    ok3=all(not(s&l) for s,l in zip(up,lo))
    return ok1,ok2,ok3,(A1,A2,a,m)
ctl=sum(1 for p,_ in walks([{(x,d) for x in range(-7,8) for d in 'RL'}]*6) if p[-1][0]==0)
print("CONTROL",ctl)
for mode in ('A','B'):
    q=0;f=[0,0,0];ex=None;n=0
    while n<6000:
        n+=1
        t1=random.randint(0,4);t2=random.randint(0,4)
        A1=randevent(t1);A2=randevent(t2)
        if mode=='A': A1=trim(A1);A2=trim(A2)
        else:
            for A in (A1,A2):
                for S in A:
                    for _ in range(random.randint(0,3)): S.add((random.randint(-6,6),random.choice('RL')))
        for a in range(t1+1,t1+4):
            r=check(A1,A2,a)
            if r is None: break
            q+=1
            for i in range(3):
                if not r[i]: f[i]+=1; ex=ex or (i,r[3])
    print(mode,"qualifying",q,"fail P1,P2,P3",f,"example",ex)
