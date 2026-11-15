"""Are the integer winding levels of the walks at a vertex visible in the multiset of their gains?

Carrier: ring of N sites, A = Z2 x Z_K, a = (0,1), b = c = 0, d = (1,-1) (delta = (1,0), r = 2).
For every position product event of length <= T and every vertex, record the multiset m of gains and,
with psi the character (-1)^(first coordinate), the numbers eps_j = sum of psi over the walks whose number of
left steps is lmin + j*M (lmin the least at that vertex, M = N/gcd(N,2)), and the autocorrelation
r_k = sum_j eps_j eps_(j+k), k = 0, 1, 2, ...  The rule |sum_w u^lambda(w) psi(w)|^2 = r_0 + sum_k 2 Re(u^(Mk)) r_k
is consistent on every event for every unit u (it is the squared sum of a character with value -1 on delta
on the carrier with every left step given the extra gain u). It is a function of the multiset of gains,
hence a rule of the kind classified, exactly as far as r is determined by m.

PREDICATES fixed before the first run (15 November 2026):
 V1  for every class of gain multisets under translation by H = A, all occurrences have the same (r_0, r_1, ...).
 V2  the same for exact gain multisets (no translation). V2 is implied by V1 and reported for comparison.
Reported with them: the number of classes, the number with two or more occurrences having different numbers of
levels (so that the comparison is not vacuous), the greatest number of levels, and for a failure the first case.
Usage: python3 level_visibility.py N K T RESULT.json   (refuses to overwrite)."""
import sys, os, json, collections, itertools
N,K,T=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]); OUT=sys.argv[4]; assert not os.path.exists(OUT)
M=N//2 if N%2==0 else N
A=[(i,j) for i in range(2) for j in range(K)]
def add(g,h): return ((g[0]+h[0])%2,(g[1]+h[1])%K)
a=(0,1%K); b=(0,0); c=(0,0); d=(1,(-1)%K)
masks=[frozenset(s) for k in range(1,N+1) for s in itertools.combinations(range(N),k)]
def step(field,mask):
    new=collections.Counter()
    for (x,r,g,l),n in field:
        y=(x+1)%N
        if y in mask: new[(y,0,add(g,a if r==0 else c),l)]+=n
        y=(x-1)%N
        if y in mask: new[(y,1,add(g,b if r==0 else d),l+1)]+=n
    return frozenset(new.items())
def canon(ms): return min(tuple(sorted((add(g,h),n) for g,n in ms.items())) for h in A)
level={frozenset({((0,0,(0,0),0),1)})}; seen=set(level)
byclass={}; byexact={}; fail1=None; fail2=None; maxlev=0; multi=collections.Counter()
for t in range(1,T+1):
    nxt=set()
    for f in level:
        for m in masks:
            g=step(f,m)
            if g and g not in seen: seen.add(g); nxt.add(g)
    level=nxt
    for f in level:
        by=collections.defaultdict(list)
        for (x,r,g,l),n in f: by[(x,r)].append((g,l,n))
        for v,items in by.items():
            lmin=min(l for _,l,_ in items); nl=(max(l for _,l,_ in items)-lmin)//M+1; maxlev=max(maxlev,nl)
            eps=[0]*nl; ms=collections.Counter()
            for g,l,n in items: eps[(l-lmin)//M]+=n*(-1)**g[0]; ms[g]+=n
            r=tuple(sum(eps[j]*eps[j+k] for j in range(nl-k)) for k in range(nl))
            while len(r)>1 and r[-1]==0: r=r[:-1]
            ex=tuple(sorted(ms.items())); cl=canon(ms)
            for key,store,which in ((cl,byclass,1),(ex,byexact,2)):
                if key not in store: store[key]=(r,nl,t)
                else:
                    r0,nl0,t0=store[key]
                    if nl0!=nl: multi[which]+=1
                    if r0!=r:
                        rec={"multiset":[[list(g),n] for g,n in key],"first":{"r":r0,"levels":nl0,"length":t0},"second":{"r":r,"levels":nl,"length":t}}
                        if which==1 and fail1 is None: fail1=rec
                        if which==2 and fail2 is None: fail2=rec
rep={"argv":sys.argv[1:],"M":M,"classes":len(byclass),"exact_multisets":len(byexact),"greatest_number_of_levels":maxlev,
     "occurrences_with_a_different_number_of_levels":{"classes":multi[1],"exact":multi[2]},
     "predicates":{"V1":"PASS" if fail1 is None else "FAIL","V2":"PASS" if fail2 is None else "FAIL"},"first_failure_V1":fail1,"first_failure_V2":fail2}
json.dump(rep,open(OUT,"x"),indent=1); print(json.dumps(rep))
