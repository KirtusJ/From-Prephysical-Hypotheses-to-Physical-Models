#!/usr/bin/env python3
"""S1 (lem:winding (iii)) and S2 (cor:threetwo) by explicit walks; reviewer's own program.
Command line: python3 s1s2_walks.py OUTFILE SAMPLES_PER_CONFIG   (OUTFILE mode 'x'); seed 20261115.
Carrier: two-rail ring Z_N, walks from (0,R), walk = tuple of bits (1 = left step); site after t steps
= (t-2*lambda_t) mod N; rail = R iff last step right. M = N/gcd(N,2). Event = all walks with site after
s steps in A_s. Exhaustive: all mask sequences (masks = subsets of the reachable sites, which is all that
matters) for N=1,2 to T=11, N=4 to T=8, N=3 to T=5, N=6 to T=4 ... ; random: each site in A_s with prob p,
p in {0.5,0.7,0.85,1.0 on a random subset of ticks}, T in [2M+1, 2M+7], N=3..8, events with >3000 walks dropped (counted).
PREDICATES (fixed before the first run). For every event, vertex y, level l:
 Q1 (ii)  n(l) n(l+2M) <= n(l+M)(n(l+M)-1)                 hypothesis: n(l)>0 and n(l+2M)>0
 Q2 (iii) if n(l)=1 or n(l+2M)=1: n(l) n(l+2M) <= n(l+M)(n(l+M)-1)/2   hypothesis: that, and all three levels occupied
 Q3 STRONGER (expected to fail somewhere if the hypothesis of (iii) is needed): n(l) n(l+2M) <= n(l+M)(n(l+M)-1)/2 always
 Q4 exchange: for each pair (w,w') at y with lambda l, l+2M (at most PAIRCAP pairs per (y,l), else skipped and counted):
    h,h' in S, end at y, lambda = l+M, h != h'; map (w,w')->(h,h') injective
 Q5 for two different pairs with images (h,h') and (h',h): tau1 != tau2, w1 != w2, w1' != w2'
    (hypothesis: such a swapped collision exists; number reported)
 Q6 (cor:threetwo) at every site where one rail has >=3 levels and the other rail is non-empty: other rail has >=2 levels
 Q7 (lem:windingrails as stated) l'-l>=M: nL(l)nR(l') <= nL(l+M)nR(l'-M); l'-l>=2M: nR(l)nL(l') <= nR(l+M)nL(l'-M)
 Q8 (item 4) no site has a walk on L at level l and one on R at level l+M with nL(l+M)*nR(l)=0
 Q9 no gaps; R and L levels at a site congruent mod M.
All failures written with the event.
"""
import sys, random, json, itertools, math
from collections import defaultdict
PAIRCAP=600
stats=defaultdict(int); fails=[]; examples={}
def fail(name,info):
    stats['FAIL_'+name]+=1
    if sum(1 for f in fails if f[0]==name)<5: fails.append((name,info))
def analyse(N,walks,masks):
    M=N//math.gcd(N,2); T=len(walks[0]); S=set(walks)
    stats['events']+=1
    byv=defaultdict(lambda: defaultdict(list))
    for w in walks:
        lam=sum(w); byv[((T-2*lam)%N, w[-1])][lam].append(w)
    for y,lv in byv.items():
        ls=sorted(lv)
        if any((b-a)!=M for a,b in zip(ls,ls[1:])): fail('Q9gap',(N,masks,y,ls))
        n=lambda l: len(lv.get(l,()))
        for l in ls:
            if n(l+2*M)==0: continue
            stats['Q1_qualify']+=1
            a,b,c=n(l),n(l+M),n(l+2*M)
            if a*c>b*(b-1): fail('Q1',(N,masks,y,l,(a,b,c)))
            if 2*a*c>b*(b-1):
                stats['Q3_violations']+=1
                if 'Q3' not in examples or T<examples['Q3'][2]: examples['Q3']=(N,masks,T,y,l,(a,b,c))
            if a==1 or c==1:
                stats['Q2_qualify']+=1
                if 2*a*c==b*(b-1): stats['Q2_equality']+=1
                if 2*a*c>b*(b-1): fail('Q2',(N,masks,y,l,(a,b,c)))
            if a*c>PAIRCAP: stats['Q4_skipped_levels']+=1; continue
            img={}
            for w in lv[l]:
                for w2 in lv[l+2*M]:
                    phi=0; tau=None
                    for t in range(T):
                        phi+=w2[t]-w[t]
                        if phi==M: tau=t+1; break
                    stats['Q4_pairs']+=1
                    if tau is None or not (0<tau<T): fail('Q4tau',(N,masks,w,w2)); continue
                    h=w2[:tau]+w[tau:]; h2=w[:tau]+w2[tau:]
                    ok = h in S and h2 in S and sum(h)==l+M and sum(h2)==l+M and h!=h2 and h[-1]==y[1] and h2[-1]==y[1] and (T-2*sum(h))%N==y[0]
                    if not ok: fail('Q4',(N,masks,w,w2,tau))
                    if (h,h2) in img: fail('Q4inj',(N,masks,w,w2))
                    img[(h,h2)]=(w,w2,tau)
            for (h,h2),(w,w2,tau) in img.items():
                if (h2,h) in img and h<h2:
                    v,v2,tau2=img[(h2,h)]
                    stats['Q5_qualify']+=1
                    if tau==tau2 or w==v or w2==v2: fail('Q5',(N,masks,w,w2,v,v2,tau,tau2))
    sites=defaultdict(dict)
    for (x,rail),lv in byv.items(): sites[x][rail]={l:len(v) for l,v in lv.items()}
    for x,d in sites.items():
        R=d.get(0,{}); L=d.get(1,{})
        if R and L and (min(R)-min(L))%M: fail('Q9cong',(N,masks,x))
        for one,oth in ((R,L),(L,R)):
            if len(one)>=3 and oth:
                stats['Q6_qualify']+=1
                if len(oth)<2: fail('Q6',(N,masks,x,R,L))
        if R and L:
            lo=min(min(R),min(L)); hi=max(max(R),max(L))
            rng_=range(lo,hi+1,M)
            for l in rng_:
                for l2 in rng_:
                    if l2-l>=M and L.get(l,0)*R.get(l2,0)>0:
                        stats['Q7a_qualify']+=1
                        if L.get(l,0)*R.get(l2,0)>L.get(l+M,0)*R.get(l2-M,0): fail('Q7a',(N,masks,x,l,l2,R,L))
                    if l2-l>=2*M and R.get(l,0)*L.get(l2,0)>0:
                        stats['Q7b_qualify']+=1
                        if R.get(l,0)*L.get(l2,0)>R.get(l+M,0)*L.get(l2-M,0): fail('Q7b',(N,masks,x,l,l2,R,L))
                    if l2-l==M and R.get(l,0)*L.get(l2,0)>0: stats['info_R_l_L_lplusM_sites']+=1
                if L.get(l,0) and R.get(l+M,0):
                    stats['Q8_qualify']+=1
                    if L.get(l+M,0)*R.get(l,0)==0: fail('Q8',(N,masks,x,l,R,L))
def step(N,walks,mask):
    out=[]
    for w in walks:
        t=len(w); lam=sum(w)
        for b in (0,1):
            if (t+1-2*(lam+b))%N in mask: out.append(w+(b,))
    return out
def exhaustive(N,Tmax):
    seen=set()
    def rec(walks,masks):
        if walks and len(walks[0])>=1: analyse(N,walks,masks); stats['exh_events_N%d'%N]+=1
        if not walks or len(walks[0])>=Tmax: return
        t=len(walks[0]); reach=sorted({(t+1-2*(sum(w)+b))%N for w in walks for b in (0,1)})
        for k in range(1,len(reach)+1):
            for mk in itertools.combinations(reach,k):
                nw=step(N,walks,set(mk)); key=frozenset(nw)
                if key in seen: continue
                seen.add(key); rec(nw,masks+[mk])
    rec([()],[])
def rand(N,samples,rng):
    M=N//math.gcd(N,2)
    for i in range(samples):
        T=rng.randint(2*M+1,2*M+7); p=rng.choice([0.5,0.7,0.85]); full=rng.random()<0.5
        walks=[()]; masks=[]
        for t in range(T):
            if full and rng.random()<0.6: mk=tuple(range(N))
            else: mk=tuple(s for s in range(N) if rng.random()<p)
            walks=step(N,walks,set(mk)); masks.append(mk)
            if not walks or len(walks)>3000: break
        if not walks: stats['rand_empty_N%d'%N]+=1; continue
        if len(walks)>3000: stats['rand_dropped_large_N%d'%N]+=1; continue
        stats['rand_events_N%d'%N]+=1; analyse(N,walks,masks)
if __name__=='__main__':
    out=open(sys.argv[1],'x'); samples=int(sys.argv[2]); rng=random.Random(20261115)
    for N,Tm in ((1,11),(2,11),(4,8),(3,5),(6,4),(5,4)):
        before=dict(stats); exhaustive(N,Tm)
        out.write(json.dumps({'phase':'exhaustive','N':N,'Tmax':Tm,'stats':dict(stats)})+'\n'); out.flush()
    for N in range(3,9):
        rand(N,samples,rng)
        out.write(json.dumps({'phase':'random','N':N,'samples':samples,'stats_cumulative':dict(stats)})+'\n'); out.flush()
    out.write(json.dumps({'final_stats':dict(stats),'failures':fails,'Q3_smallest_counterexample':examples.get('Q3')})+'\n'); out.close()
    print(json.dumps(dict(stats),indent=1)); print('FAILS',fails); print('Q3 example',examples.get('Q3'))
