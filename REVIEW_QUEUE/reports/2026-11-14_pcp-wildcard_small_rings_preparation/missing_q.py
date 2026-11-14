"""List the unreachable site-states (U|V) for period-3 rings, q>=3. Predicate fixed first (after seeing counts only):
the missing set is the same at every site and the same for N=3 and N=6. Result file mode 'x'."""
import itertools, json
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
    return [sorted(v for v in full if v not in s) for s in site]
out={}
for q,N,B in [(3,3,3),(3,6,3),(4,3,2),(4,6,2),(5,3,2),(2,3,5),(6,3,2)]:
    m=run(q,N,B); out[f"q{q}_N{N}_B{B}"]={"same_every_site":all(x==m[0] for x in m),"missing":m[0]}
    print(q,N,B,all(x==m[0] for x in m),len(m[0])); 
    for v in m[0][:12]: print("   U=",v[:q],"V=",v[q:])
out["pred_N3_eq_N6"]= out["q3_N3_B3"]["missing"]==out["q3_N6_B3"]["missing"] and out["q4_N3_B2"]["missing"]==out["q4_N6_B2"]["missing"]
print(out["pred_N3_eq_N6"])
json.dump(out,open('result_missing_q.json','x'),indent=1)
