"""Wildcard attack on candidate Z6 "Odd Lap" (a stipulated candidate for disproof; nothing here is a claim about the world).
Own program: gains are carried as elements of A = Z2 x Z_(2M) (a=(0,0), b=(0,1), c=(0,0), d=(1,1)); classes and signs are
read from the GROUP ELEMENTS at each end vertex (g - kappa = (n, i*M): class i, sign (-1)^n), not from winding levels.
Hypothesis check per ring (H): delta=(1,0) has order 2; beta=M*B=(0,M) is not in <delta>; 2*beta=0 (k=0, even).
Rules: odd=(e0-e1)^2, even=(e0+e1)^2, count=number of walks.
Sweep experiment S(K): masks {t,-t} for t=1..K, then all sites, read at K+1 (the fork is S(M)).
PREDICATES, fixed before the first run (15 November 2026):
 A1 for every ring and every K with 1<=K<M: S(K) has exactly 4 end vertices, one walk each; odd=even=count=1 at each.
 A2 for K=M: exactly 2 end vertices, ((M+1)%N,R) and ((M-1)%N,L); odd weights (4,0) for M even, (0,4) for M odd; even exchanged; count (2,2).
 A3 the smallest K>=1 at which S(K) has fewer than 4 occupied end vertices is K=M (so the count of lit ports alone reads M).
 A4 for M even: N=2M is forced; for M odd: the mask {0} at step M after masks {t,-t}, t<M, has walks iff N=M (N odd).  [tested on pairs (9,18),(11,22)]
 D1 P3 on N=16: TV = 1/128,7/128,45/256,353/1024 at T=9..12 and 281487/524288 at T=24.
 D2 P5 on N=16: odd-lap return to (0,R) = 289/16384 at T=16, 0 at 17, 169/16384 at 18.
 D3 P4: odd total of all walks = 2^T for T<=3M.
 D4 P2: odd==even at every vertex for T<=M, all walks.
 E1 (FORM D4 support) the event 'fork with last mask a single site' has ONE end vertex with class sums (1,1) [site M-1 if M even... whichever port] and another choice gives (1,-1): searched over the two ports; both must occur.
 E2 for the fork itself (two end vertices) the totals P (even rule) and Q (odd rule) are equal, so the fork alone does not test O6 mixtures: c+P^2+c-Q^2 == (c+P+c-Q)^2 for c+=1/3.
Reported without predicate: S(K) for M<K<=2M+1 in both worlds.
Rings: candidates 16,18,20,9,11; controls outside the candidate (M<8): 6,8,10,7,12,14.
Usage: python3 seam_attack.py RESULT.json (mode 'x')."""
import sys, json, collections
from fractions import Fraction as Fr
OUT=sys.argv[1]; fout=open(OUT,'x')
def Mof(N): return N//2 if N%2==0 else N
def run(N,T,masks=None):
    M=Mof(N); G=2*M
    st=collections.Counter({(0,0,0,0):1})  # site, rail(0=R,1=L), g1 in Z2, g2 in Z_2M
    for t in range(1,T+1):
        new=collections.Counter()
        for (x,r,g1,g2),c in st.items():
            y=(x+1)%N
            if masks is None or y in masks[t-1]: new[(y,0,g1,g2)]+=c            # a (R->R) or c (L->R): (0,0)
            y=(x-1)%N
            if masks is None or y in masks[t-1]:
                if r==0: new[(y,1,g1,(g2+1)%G)]+=c                              # b=(0,1)
                else:    new[(y,1,g1^1,(g2+1)%G)]+=c                            # d=(1,1)
        st=new
    by=collections.defaultdict(list)
    for (x,r,g1,g2),c in st.items(): by[(x,r)].append((g1,g2,c))
    res={}
    for v,items in by.items():
        k1,k2=min(items)[:2]; e=[0,0]; n=0
        for g1,g2,c in items:
            d2=(g2-k2)%G; assert d2%M==0, "walks at one vertex not in one coset of <delta,beta>"
            e[d2//M]+=c*(-1)**(g1^k1); n+=c
        res[v]=(e[0],e[1],n)
    return res
def W(res): return ({v:(e[0]-e[1])**2 for v,e in res.items()},{v:(e[0]+e[1])**2 for v,e in res.items()},{v:e[2] for v,e in res.items()})
def S(N,K): return run(N,K+1,[{t%N,(-t)%N} for t in range(1,K+1)]+[set(range(N))])
rep={"argv":sys.argv,"rings":[],"predicates":{}}
P=dict(A1=True,A2=True,A3=True,A4=True,D1=True,D2=True,D3=True,D4=True,E1=True,E2=True); fails=[]
def chk(name,ok,info):
    if not ok: P[name]=False; fails.append([name,info])
CAND=(16,18,20,9,11); CTRL=(6,8,10,7,12,14)
for N in CAND+CTRL:
    M=Mof(N); row={"N":N,"M":M,"in_candidate":M>=8,"H":True,"sweep":[]}
    first=None
    for K in range(1,2*M+2):
        o,e,n=W(S(N,K)); 
        row["sweep"].append({"K":K,"ports":{f"{v[0]}{'RL'[v[1]]}":[o[v],e[v],n[v]] for v in sorted(o)}})
        if first is None and len(n)<4: first=K
        if K<M: chk("A1",len(n)==4 and all(o[v]==1==e[v]==n[v] for v in n),[N,K])
        if K==M:
            vr,vl=((M+1)%N,0),((M-1)%N,1)
            exp=(4,0) if M%2==0 else (0,4)
            chk("A2",set(n)=={vr,vl} and (o[vr],o[vl])==exp and (e[vl],e[vr])==exp and (n[vr],n[vl])==(2,2),[N,K])
            chk("E2",Fr(1,3)*sum(e.values())**2+Fr(2,3)*sum(o.values())**2==(Fr(1,3)*sum(e.values())+Fr(2,3)*sum(o.values()))**2,[N])
            cs=set()
            for site in ((M+1)%N,(M-1)%N):
                r=run(N,M+1,[{t%N,(-t)%N} for t in range(1,M+1)]+[{site}])
                chk("E1",len(r)==1,[N,site]); cs.add(tuple(sorted(list(r.values())[0][:2])))
            chk("E1",cs=={(1,1),(-1,1)},[N,sorted(cs)]); row["E1_class_sums"]=sorted(cs)
    row["first_K_with_fewer_than_4_ports"]=first; chk("A3",first==M,[N,first])
    tv=[];ret=[]
    for T in range(1,3*M+1):
        o,e,n=W(run(N,T))
        chk("D3",sum(o.values())==2**T,[N,T])
        if T<=M: chk("D4",o==e,[N,T])
        tv.append([T,str(Fr(sum(abs(o[v]-e[v]) for v in o),2*2**T))]); ret.append([T,str(Fr(o.get((0,0),0),2**T))])
    row["tv"]=tv; row["return_odd"]=ret
    if N==16:
        d=dict(tv); chk("D1",[d[9],d[10],d[11],d[12],d[24]]==["1/128","7/128","45/256","353/1024","281487/524288"],[d[9],d[10],d[11],d[12],d[24]])
        d=dict(ret); chk("D2",[d[16],d[17],d[18]]==["289/16384","0","169/16384"],[d[16],d[17],d[18]])
    rep["rings"].append(row)
a4=[]
for M_ in (9,11):
    for N in (M_,2*M_):
        r=run(N,M_,[{t%N,(-t)%N} for t in range(1,M_)]+[{0}]); a4.append([N,M_,len(r)>0])
        chk("A4",(len(r)>0)==(N==M_),[N,M_])
rep["A4_rows"]=a4; rep["predicates"]=P; rep["failed"]=fails
json.dump(rep,fout,indent=1); fout.close(); print(P); print("failed",fails)
for r in rep["rings"]:
    if r["N"] in (16,18):
        for s in r["sweep"]: print(r["N"],s["K"],s["ports"])
