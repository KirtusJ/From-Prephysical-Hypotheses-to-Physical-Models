"""Lemma X and Corollary X.1, exact. Usage: python3 x_lemma.py RESULT.json SEED
Walk = tuple of steps (0=R,1=L) from (0,R); site after t steps = t-2*lambda_t mod N; rail = last step (start R).
Event = all walks whose site after t steps is in mask A_t. M = N/gcd(N,2).
PREDICATES (fixed before first run). Hypothesis tested per pair/instance; qualifying numbers reported.
 X1-pairs: for every w at (x,L) lambda l, w' at (x,R) lambda l', l'-l in MZ, l'-l>=M (boundary l'-l==M counted separately):
   a) tau = least t with Phi(t)=M exists and 0<tau<T-1;  b) h,h' in S;  c) h ends (x,L), lambda l+M; h' ends (x,R), lambda l'-M;
   d) map injective on the pairs of that (x,l,l').
 X2-pairs: w at (x,R) l, w' at (x,L) l', l'-l>=2M (boundary ==2M counted): a) tau exists, 0<tau<=T-1; b),c) (h at (x,R) l+M, h' at (x,L) l'-M), d).
 X1-count: n_L(l) n_R(l') <= n_L(l+M) n_R(l'-M) for l'-l>=M.   X2-count: n_R(l) n_L(l') <= n_R(l+M) n_L(l'-M) for l'-l>=2M.
 NOTCLAIMED (kept as failed predicate if it fails): X2-count at l'-l == M.
 X.1: no event/site with n_L(l)>0, n_R(l+M)>0 and n_L(l+M)*n_R(l)==0 (request (empty,{1},{1},empty) is an instance);
      no event/site with n_R(l)>0, n_L(l+2M)>0 and n_R(l+M)*n_L(l+M)==0 (request ({1},empty,empty,{1})).
Events: exhaustive nonempty-mask sequences N=1 (T<=9), N=2 (T<=6), N=3 (T<=5), N=4 (T<=4), N=5 (T<=3); random N=1..9, T<=13.
Pair building for all pairs when #pairs of an (x,l,l') <= 4000, else first 4000 (injectivity then on that subset).
"""
import sys, json, itertools, random
from collections import defaultdict
def walks(N,masks):
    cur=[((),0,0)]
    for t,A in enumerate(masks,1):
        nxt=[]
        for w,lam,_ in cur:
            for s in (0,1):
                l2=lam+s; site=(t-2*l2)%N
                if site in A: nxt.append((w+(s,),l2,site))
        cur=nxt
    return cur
C=defaultdict(int)
FAIL=[]
def check(N,masks):
    M=N//2 if N%2==0 else N; T=len(masks)
    ws=walks(N,masks); S={w for w,_,_ in ws}
    by=defaultdict(list)
    for w,lam,site in ws: by[(site,w[-1],lam)].append(w)
    C['events']+=1
    sites={k[0] for k in by}
    for x in sites:
        lev=sorted({k[2] for k in by if k[0]==x})
        n=lambda rail,l: len(by.get((x,rail,l),()))
        for l in lev:
            for l2 in lev:
                d=l2-l
                if d<=0 or d%M: continue
                for kind,ra,rb,mind in (('X1',1,0,M),('X2',0,1,2*M),('X2atM',0,1,M)):
                    if kind=='X2atM' and d!=M: continue
                    if d<mind: continue
                    na,nb=n(ra,l),n(rb,l2)
                    if na*nb==0: continue
                    C[kind+'_count_qual']+=1
                    if d==mind: C[kind+'_count_boundary']+=1
                    ok=na*nb<=n(ra,l+M)*n(rb,l2-M)
                    if not ok:
                        C[kind+'_count_FAIL']+=1
                        if len(FAIL)<20: FAIL.append([kind,N,[sorted(a) for a in masks],x,l,l2,na,nb,n(ra,l+M),n(rb,l2-M)])
                    if kind=='X2atM': continue
                    if kind=='X1' and d==M: C['X.1a_qual']+=1; C['X.1a_FAIL']+= (n(1,l+M)*n(0,l)==0)
                    if kind=='X2' and d==2*M: C['X.1b_qual']+=1; C['X.1b_FAIL']+= (n(0,l+M)*n(1,l+M)==0)
                    img=set(); cnt=0
                    for w in by[(x,ra,l)]:
                        for w2 in by[(x,rb,l2)]:
                            if cnt>=4000: break
                            cnt+=1; C[kind+'_pairs']+=1
                            if d==mind: C[kind+'_pairs_boundary']+=1
                            phi=0; tau=None
                            for t in range(1,T+1):
                                phi+=w2[t-1]-w[t-1]
                                if phi==M: tau=t; break
                            lim=T-1 if kind=='X1' else T
                            if tau is None or not (0<tau<lim): C[kind+'_tau_FAIL']+=1; continue
                            if tau==T-1: C[kind+'_tau_eq_T-1']+=1
                            h=w2[:tau]+w[tau:]; h2=w[:tau]+w2[tau:]
                            if h not in S or h2 not in S: C[kind+'_member_FAIL']+=1
                            if not (h[-1]==ra and sum(h)==l+M and (T-2*sum(h))%N==x and h2[-1]==rb and sum(h2)==l2-M and (T-2*sum(h2))%N==x): C[kind+'_end_FAIL']+=1
                            img.add((h,h2))
                    if len(img)!=cnt: C[kind+'_inj_FAIL']+=1
if __name__=='__main__':
    out=open(sys.argv[1],'x'); seed=int(sys.argv[2]); rng=random.Random(seed)
    for N,Tmax in ((1,9),(2,6),(3,5),(4,4),(5,3)):
        subs=[set(c) for k in range(1,N+1) for c in itertools.combinations(range(N),k)]
        for T in range(1,Tmax+1):
            for ms in itertools.product(subs,repeat=T): check(N,ms); C['exh_N%d'%N]+=1
    for it in range(6000):
        N=rng.randint(1,9); T=rng.randint(2,13 if N>2 else 10); p=rng.choice([0.5,0.7,0.85,1.0])
        ms=[]
        for t in range(T):
            A={x for x in range(N) if rng.random()<p} or {rng.randrange(N)}
            ms.append(A)
        check(N,ms); C['rand_N%d'%N]+=1
    res={'seed':seed,'counts':dict(sorted(C.items())),'first_failures':FAIL}
    json.dump(res,out,indent=1); out.close(); print(json.dumps(res['counts'],indent=0)); print(FAIL[:3])
