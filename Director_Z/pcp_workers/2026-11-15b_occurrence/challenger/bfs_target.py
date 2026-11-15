"""bfs_target.py -- independent check (challenger) that the profile w=(1,2,3,3,2) does not occur for given M.
Model (body/draft, unrolled lattice): n_0=delta_0; n_t(e)=[e mod M in E_t](n_{t-1}(e)+n_{t-1}(e-1)), E_t any subset of Z/M.
Profile at residue c: v_j=n(c-1+jM), u_j=n(c+jM), w=(v0,u0,v1,u1,...), leading zero pairs and trailing zeros removed.
Bounds (stronger form of the lemma: after trimming every occupied point reaches the target, so WHOLE-state total <= B;
span <= (K+1)M). Different from the worker's: whole-state total, states kept with absolute residue (translation only by
multiples of M), Python, direct target test instead of collecting all profiles.
PREDICATES fixed before first run:
 T0 control: with M=4 the profile (1,2,1) (B=4,K=2) IS found (it occurs: two steps all open).
 T1: for targets (1,2,3,3,2),(0,1,2,3,3,2),(2,3,3,2,1),(0,2,3,3,2,1) with B=11,K=3: search closes and none is found.
 Report number of states. Result file never overwritten.
"""
import sys, os
M=int(sys.argv[1]); B=int(sys.argv[2]); K=int(sys.argv[3]); targets=[tuple(map(int,t.split(','))) for t in sys.argv[4:]]
out=f"bfs_M{M}_B{B}_K{K}_{'_'.join('-'.join(map(str,t)) for t in targets)}.txt"
if os.path.exists(out): sys.exit("refuse to overwrite "+out)
def norm(off,arr):
    i=0
    while arr[i]==0: i+=1
    j=len(arr)
    while arr[j-1]==0: j-=1
    s=off+i; q=s//M  # translate by multiple of M only
    return (s-q*M, arr[i:j])
def profiles(st):
    off,arr=st; res=set()
    for c in range(M):
        d={}
        for k,x in enumerate(arr):
            e=off+k
            if x and e%M in ((c-1)%M,c): d[e]=x
        if not d: continue
        # level j: v_j at c-1+jM, u_j at c+jM; choose j0 with base = c-1+j0*M <= min
        mn=min(d); j0=(mn-(c-1))//M; base=c-1+j0*M
        w=[0]*(max(d)-base+1)
        for e,x in d.items(): w[e-base]=x
        # w index: even = v, odd = u, positions differ by... v_j at base+jM, u_j at base+1+jM
        ww=[]
        for j in range((len(w)+M)//M+1):
            ww.append(d.get(base+j*M,0)); ww.append(d.get(base+1+j*M,0))
        while ww and ww[-1]==0: ww.pop()
        res.add(tuple(ww))
    return res
start=norm(0,(1,)); seen={start}; fr=[start]; found=set(); tset=set(targets)
found|=profiles(start)&tset
while fr:
    nx=[]
    for off,arr in fr:
        ext=(0,)+arr+(0,)  # positions off-1 .. off+len
        L=len(arr)+1; base=off
        vals=[(arr[k] if k<len(arr) else 0)+(arr[k-1] if k>=1 else 0) for k in range(L)]  # e=off+k
        occ={ (off+k)%M for k in range(L) if vals[k]}
        occ=sorted(occ)
        for mask in range(1,1<<len(occ)):
            E={occ[i] for i in range(len(occ)) if mask>>i&1}
            a=tuple(v if (off+k)%M in E else 0 for k,v in enumerate(vals))
            if sum(a)>B: continue
            st=norm(off,a)
            if len(st[1])-1>(K+1)*M: continue
            if st in seen: continue
            seen.add(st); nx.append(st); found|=profiles(st)&tset
    fr=nx
msg=f"M={M} B={B} K={K} states={len(seen)} closed=1 found={sorted(found)} targets={targets}"
print(msg); open(out,"w").write(msg+"\n")
