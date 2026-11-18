"""Same closure as small_rings.py for one gain h of order q (G10 subsection after Thm 5.32; body.tex l.878):
site-state = (U,V) in N^q x N^q, extend: (x+1,R) gets U+V, (x-1,L) gets U+TV, (TV)(j)=V(j-1 mod q).
Predicates fixed first: C (control) for q=2 the per-site reachable counts equal those of small_rings.py
(N=3,B=3: 35 of 35; N=4,B=3: 15 of 35). Q: for each (q,N,B) is every (U,V) with total<=B reachable at every site?
Integers only; result file mode 'x'."""
import sys, json, itertools
def run(q,N,B):
    Z=(0,)*(2*q)
    def step(state):
        new=[[0]*(2*q) for _ in range(N)]
        for x,v in enumerate(state):
            if v==Z: continue
            a=new[(x+1)%N]; b=new[(x-1)%N]
            for j in range(q):
                a[j]+=v[j]+v[q+j]; b[q+j]+=v[j]+v[q+(j-1)%q]
        new=[tuple(v) if sum(v)<=B else Z for v in new]
        occ=[x for x in range(N) if new[x]!=Z]
        for r in range(len(occ)+1):
            for k in itertools.combinations(occ,r):
                ks=set(k); yield tuple(new[x] if x in ks else Z for x in range(N))
    fr={tuple((1,)+(0,)*(2*q-1) if x==0 else Z for x in range(N))}; seen=set(); site=[set() for _ in range(N)]
    while fr:
        nx=set()
        for s in fr:
            for t in step(s):
                if t not in seen:
                    seen.add(t); nx.add(t)
                    for x in range(N): site[x].add(t[x])
        fr=nx
    full=[v for v in itertools.product(range(B+1),repeat=2*q) if sum(v)<=B]
    return {"q":q,"N":N,"B":B,"states":len(seen),"pairs_total":len(full),
            "reachable_per_site":[sum(1 for v in full if v in s) for s in site],
            "Q_all":all(all(v in s for v in full) for s in site)}
f=open(sys.argv[2],'x'); out=[]
for q,N,B in json.loads(sys.argv[1]):
    r=run(q,N,B); out.append(r); print(r,flush=True)
json.dump(out,f,indent=1); f.close()
