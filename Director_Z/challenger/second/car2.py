import sys,time
from car import run
bad=[]
for (d,q) in [(5,5),(4,8),(3,9),(5,10),(7,7),(6,12),(3,12)]:
    for m in (1,2):
        for seed in range(2):
            t=time.time()
            p,phi,ok,npres=run(d,q,m,seed,nev=6000)
            if ok and p!=phi: bad.append((d,q,m,seed,p,phi))
            print("  t=%.1f"%(time.time()-t),flush=True)
print("MISMATCH among hyp-true:",bad,flush=True)
