"""Theorem Y(b) by linear algebra mod p = 2^31-1 (rank mod a prime; lower bound of rational rank, so
nullity mod p >= rational nullity; equality with the theorem's dimension then settles both).
Usage: python3 y_linalg.py RESULT.json   (file opened 'x'; no seed: no randomness)
Unknowns: f(m), m a nonempty multiset of Delta, |m|<=n, modulo translation by K=Delta (f(empty)=0).
Families of pairs (u,v), |u|,|v|>=1, |u|+|v|<=n, equation f(u+v)+f(u+T_delta v)=2f(u)+2f(v):
  ALL: all pairs.  R: u or v supported on one coset of <delta>.  R2: v on one coset, or u a singleton.
PREDICATES (fixed before first run), per case, with dim_F(c) = dimension of the solution space of family F
restricted to multisets of size <= c:
  P0 (sanity, hypothesis of the comparison): dim_ALL(n-2) == formula 1+#{ {chi,chi^-1}: chi(delta)=-1 }.
  P1: dim_R(n-2) == dim_ALL(n-2)    [claim of Y(b) when |Delta/<delta>| = 2; contrast cases reported, not claimed]
  P2: dim_R2(n-2) == dim_ALL(n-2)   [the smaller family the proof says it uses]
Cases with quotient order != 2 are contrast cases: P1,P2 reported as observations.
"""
import sys, json, itertools, numpy as np
P=2147483647
def rref(A):
    A=A%P; r=0; piv=[]
    for c in range(A.shape[1]):
        nz=np.nonzero(A[r:,c])[0]
        if len(nz)==0: continue
        i=r+nz[0]
        if i!=r: A[[r,i]]=A[[i,r]]
        A[r]=(A[r]*pow(int(A[r,c]),P-2,P))%P
        idx=np.nonzero(A[:,c])[0]; idx=idx[idx!=r]
        if len(idx): A[idx]=(A[idx]-(A[idx,c][:,None]*A[r][None,:])%P)%P
        piv.append(c); r+=1
        if r==A.shape[0]: break
    return A[:r],piv
def case(orders,delta,n):
    G=list(itertools.product(*[range(o) for o in orders])); ix={g:i for i,g in enumerate(G)}; k=len(G)
    add=lambda g,h:tuple((a+b)%o for a,b,o in zip(g,h,orders))
    tr=[[ix[add(g,h)] for g in G] for h in G]   # tr[h][i]=index of G[i]+h
    def trans(m,h):
        out=[0]*k
        for i,c in enumerate(m):
            if c: out[tr[h][i]]=c
        return tuple(out)
    dl=ix[tuple(delta)]
    # cosets of <delta>
    cos=[-1]*k; nc=0
    for i in range(k):
        if cos[i]<0:
            j=i
            while cos[j]<0: cos[j]=nc; j=tr[dl][j]
            nc+=1
    r=k//nc
    def onecoset(m): return len({cos[i] for i,c in enumerate(m) if c})<=1
    bysize=[[] for _ in range(n+1)]
    def gen(pos,left,cur):
        if pos==k:
            bysize[sum(cur)].append(tuple(cur)); return
        for c in range(left+1):
            cur.append(c); gen(pos+1,left-c,cur); cur.pop()
    gen(0,n,[])
    canon={}; unk={}; usize=[]
    def can(m):
        if m not in canon:
            c=min(trans(m,h) for h in range(k))
            if c not in unk: unk[c]=len(unk); usize.append(sum(c))
            canon[m]=unk[c]
        return canon[m]
    for s in range(1,n+1):
        for m in bysize[s]: can(m)
    nu=len(unk)
    rows={'ALL':set(),'R':set(),'R2':set()}; npairs={'ALL':0,'R':0,'R2':0}
    for a in range(1,n):
        for b in range(1,n-a+1):
            for u in bysize[a]:
                ou=onecoset(u)
                for v in bysize[b]:
                    ov=onecoset(v)
                    d={}
                    tv=trans(v,dl)
                    for m,cf in ((tuple(x+y for x,y in zip(u,v)),1),(tuple(x+y for x,y in zip(u,tv)),1),(u,-2),(v,-2)):
                        j=can(m); d[j]=d.get(j,0)+cf
                    row=tuple(sorted((j,c) for j,c in d.items() if c))
                    npairs['ALL']+=1
                    if row: rows['ALL'].add(row)
                    if ou or ov:
                        npairs['R']+=1
                        if row: rows['R'].add(row)
                    if ov or a==1:
                        npairs['R2']+=1
                        if row: rows['R2'].add(row)
    usize=np.array(usize)
    # formula
    cnt=0; seen=set()
    for c in G:
        ph=sum(ci*di/o for ci,di,o in zip(c,delta,orders))%1
        if abs(ph-0.5)<1e-9:
            neg=tuple((-ci)%o for ci,o in zip(c,orders))
            if neg not in seen: seen.add(c); cnt+=1
    formula=1+cnt
    res={'orders':orders,'delta':delta,'n':n,'r':r,'quotient_order':nc,'unknowns':nu,'formula_dim':formula,'pairs':npairs,'fam':{}}
    for F in ('ALL','R','R2'):
        B=np.zeros((0,nu),dtype=np.int64); piv=[]
        rl=list(rows[F])
        for s in range(0,len(rl),3000):
            A=np.zeros((len(rl[s:s+3000]),nu),dtype=np.int64)
            for i,row in enumerate(rl[s:s+3000]):
                for j,c in row: A[i,j]=c
            B,piv=rref(np.vstack([B,A]))
        free=[c for c in range(nu) if c not in set(piv)]
        Nn=np.zeros((nu,len(free)),dtype=np.int64)
        for t,fc in enumerate(free):
            Nn[fc,t]=1
            for i,pc in enumerate(piv): Nn[pc,t]=(-B[i,fc])%P
        dims={}
        for cut in range(n,1,-1):
            sub=Nn[usize<=cut]
            dims[cut]=len(rref(sub.copy())[1]) if sub.size else 0
        res['fam'][F]={'distinct_rows':len(rl),'rank':len(piv),'nullity':len(free),'dim_restricted_to_size_le':dims}
    c=n-2
    d=lambda F:res['fam'][F]['dim_restricted_to_size_le'][c]
    res['P0']=d('ALL')==formula; res['P1']=d('R')==d('ALL'); res['P2']=d('R2')==d('ALL')
    res['claimed']=(nc==2)
    return res
CASES=[([2,2],[1,0],8),([4],[2],8),([2],[1],8),([2,4],[0,1],6),([8],[2],6),([2,4],[1,2],6),([2,2,2],[1,0,0],5),
       ([6],[2],7),([2],[0],8),([6],[3],7),([2,4],[1,0],6),([4,2],[2,0],6),([3],[0],7),([4],[0],6),([2,2],[0,0],7),([8],[4],5),([10],[5],6),([10],[2],6),([12],[2],5),([12],[3],5)]
if __name__=='__main__':
    out=open(sys.argv[1],'x'); allr=[]
    for o,d,n in CASES:
        res=case(o,d,n); allr.append(res)
        print(o,d,n,'r',res['r'],'quot',res['quotient_order'],'formula',res['formula_dim'],
              {F:res['fam'][F]['dim_restricted_to_size_le'] for F in res['fam']},'P0',res['P0'],'P1',res['P1'],'P2',res['P2'],'claimed',res['claimed'],flush=True)
    json.dump(allr,out,indent=1); out.close()
