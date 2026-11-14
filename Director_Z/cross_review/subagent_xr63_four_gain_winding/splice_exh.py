"""Adversarial: splicing theorem under ALL mask sequences (nonempty subsets of reachable wells), exhaustive.
S1: attained left counts at each complete port form an arithmetic progression of step D with no gap.
S2: span >= 2D implies >= 4 words. Rings/depths: N=3 depth 7, N=4 depth 9, N=5 depth 11 restricted to masks of size>=4 (stated).
Result file mode 'x'; failures counted, kept."""
import sys, json
from itertools import combinations
from math import gcd
def run(N, depth, minsize=1):
    D=N//gcd(N,2); c=dict(ring=N,depth=depth,minsize=minsize,events=0,ports=0,span2=0,gaps=0,few=0)
    def chk(st):
        c["events"]+=1; byp={}
        for (x,r,l),n in st.items(): byp.setdefault((x,r),{})[l]=n
        for d in byp.values():
            ls=sorted(d); c["ports"]+=1
            if ls!=list(range(ls[0],ls[-1]+1,D)): c["gaps"]+=1
            if ls[-1]-ls[0]>=2*D:
                c["span2"]+=1
                if sum(d.values())<4: c["few"]+=1
    def dfs(st,t):
        chk(st)
        if t==depth: return
        reach=sorted({(x+dx)%N for (x,_,_) in st for dx in (1,-1)})
        for k in range(min(minsize,len(reach)),len(reach)+1):
            for sub in combinations(reach,k):
                nx={}
                for (x,r,l),n in st.items():
                    for s,dx in (("R",1),("L",-1)):
                        y=(x+dx)%N
                        if y in sub: nx[(y,s,l+(s=="L"))]=nx.get((y,s,l+(s=="L")),0)+n
                dfs(nx,t+1)
    dfs({(0,"R",0):1},0); return c
out=[run(3,7),run(4,9),run(5,11,4)]
json.dump(out,open(sys.argv[1],"x"),indent=1); print(out)
