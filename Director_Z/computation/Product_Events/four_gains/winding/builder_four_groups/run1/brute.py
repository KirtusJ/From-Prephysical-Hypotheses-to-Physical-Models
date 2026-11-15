"""Independent brute force from the draft's definitions: walks from site 0, step t moves site by +1 (right, lambda
unchanged) or -1 (left, lambda+1) [site after t steps = t - 2 lambda mod N], every site after step t in A_t.
Profile at x after T steps: u_j = #R-ending (last step right) with lambda=l0+jM, v_j = #L-ending with lambda=l0+jM.
w_{2j}=v_j, w_{2j+1}=u_j, l0 least lambda; output w with trailing zeros removed.
Enumerates all mask sequences (A_t nonempty subsets) for T<=TMAX via DFS on walk-count vectors.
Predicate fixed before run: profile set equals exact_bfs's (for profiles with total<=CAP) restricted to those
reached here; reported as 'brute subset of model' and list of model profiles of total<=CAPB not reached here.
Usage: python3 brute.py N TMAX OUT"""
import sys
N=int(sys.argv[1]); TMAX=int(sys.argv[2]); out=open(sys.argv[3],'x')
from math import gcd
M=N//gcd(N,2)
# state: dict (site, lastdir, lambda) -> count ; lastdir 'R'/'L'
prof=set()
def rec(state,t):
    # record profiles
    by={}
    for (x,d,l),c in state.items(): by.setdefault(x,[]).append((d,l,c))
    for x,lst in by.items():
        l0=min(l for d,l,c in lst)
        w={}
        for d,l,c in lst:
            j=(l-l0)//M; w[2*j+(1 if d=='R' else 0)]=w.get(2*j+(1 if d=='R' else 0),0)+c
        prof.add(tuple(w.get(i,0) for i in range(max(w)+1)))
    if t==TMAX: return
    step(state,t)
def step(state,t):
    nxt={}
    for (x,d,l),c in state.items():
        for nd,nx,nl in (('R',(x+1)%N,l),('L',(x-1)%N,l+1)):
            k=(nx,nd,nl); nxt[k]=nxt.get(k,0)+c
    sites=sorted({k[0] for k in nxt})
    for mask in range(1,1<<len(sites)):
        A={sites[i] for i in range(len(sites)) if mask>>i&1}
        rec({k:c for k,c in nxt.items() if k[0] in A},t+1)
step({(0,'-',0):1},0)
for p in sorted(prof,key=lambda p:(sum(p),p)): print(p,file=out)
