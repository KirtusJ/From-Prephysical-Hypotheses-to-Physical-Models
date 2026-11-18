"""N=4: which site totals |U|+|V| <= 16 occur at T>=1? Predicate fixed first: the set is exactly {0,1,2,4,8,16}
(claim: totals on Z_4 are 0 or powers of two). Reuses closure logic; integers only; result file mode 'x'."""
import itertools, json
N=4;B=16
def step(state):
    new=[[0,0,0,0] for _ in range(N)]
    for x,(pR,qR,pL,qL) in enumerate(state):
        a=new[(x+1)%N]; a[0]+=pR+pL; a[1]+=qR+qL
        b=new[(x-1)%N]; b[2]+=pR+qL; b[3]+=qR+pL
    new=[tuple(v) if sum(v)<=B else (0,0,0,0) for v in new]
    occ=[x for x in range(N) if sum(new[x])]
    for r in range(len(occ)+1):
        for k in itertools.combinations(occ,r):
            yield tuple(new[x] if x in k else (0,0,0,0) for x in range(N))
fr={tuple((1,0,0,0) if x==0 else (0,0,0,0) for x in range(N))}; seen=set(); tot=set()
while fr:
    nx=set()
    for s in fr:
        for t in step(s):
            if t not in seen:
                seen.add(t); nx.add(t); tot|={sum(v) for v in t}
    fr=nx
f=open('result_n4_totals.json','x'); json.dump({"N":4,"B":B,"states":len(seen),"totals":sorted(tot),"predicate_holds":sorted(tot)==[0,1,2,4,8,16]},f); f.close()
print(len(seen),sorted(tot))
