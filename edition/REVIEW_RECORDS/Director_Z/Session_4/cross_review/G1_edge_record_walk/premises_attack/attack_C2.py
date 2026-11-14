"""Attack C follow-up, written after run1 failed P2/P3/P4 (dimension grows: values first seen at the last ticks are
under-constrained). Fairer question, predicates fixed before this run:
 Q1 projection of the solution space (equations through tick T) onto the responses at inputs visited by tick T0:
    for model PM (F(n+,n-)) this projected dimension stays > 2 as T grows (P6: >2 at T0=6 for every T in 8..14);
    for model S (f(signed total)) it equals 1 (P7).
 Q2 nonnegative extra solution: report an explicit F>=0 solving all equations through T, not in span{count,square} on T0-inputs.
Usage: python3 attack_C2.py OUTDIR
"""
import sys, json, os
sys.argv_backup=sys.argv; 
from sympy import Matrix
import importlib.util
src=open('attack_C.py').read().split("out={")[0]
sys.argv=[sys.argv[0],'x']; exec(src)
def system(T,key,key0):
    sn=evolve(T); E=[]
    for t in range(T):
        a,b=sn[t],sn[t+1]
        for x,(r,l) in a.items():
            e={}
            for q,c in ((b[x+1][0],1),(b[x-1][1],1),(r,-2),(l,-2)): e[key(q)]=e.get(key(q),0)+c
            E.append(e)
    return sn,null(E,key0)
out=[]
for T0 in (5,6):
  for T in range(8,15):
    rec=dict(T0=T0,T=T)
    for name,key,key0 in (("PM",lambda q:q,(0,0)),("S",lambda q:q[0]-q[1],0)):
        sn,(keys,idx,M,d)=system(T,key,key0)
        early=sorted({key(q) for t in range(T0+1) for pr in sn[t].values() for q in pr if key(q)!=key0})
        ns=M.nullspace()
        P=Matrix([[v[idx[k]] for k in early] for v in ns])
        rec[name]=dict(dim=d,early_unknowns=len(early),projected_dim=P.rank())
        if name=="PM" and T0==6 and T==14:
            # explicit extra solution: reduce basis restricted to early coords
            R,piv=P.T.rref(); rec["PM"]["note"]="pivots %s"%(list(piv),)
    out.append(rec); print(json.dumps(rec),flush=True)
os.makedirs(sys.argv_backup[1],exist_ok=True)
with open(os.path.join(sys.argv_backup[1],"attack_C2.json"),"x") as f: json.dump(out,f,indent=1)
