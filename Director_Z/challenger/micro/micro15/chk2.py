import itertools
P=2**61-1
def T(m): return (m[-1],)+m[:-1]
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def rank(rows,ncol):
    piv={}
    for r in rows:
        r=dict(r)
        while r:
            c=min(r)
            if c in piv:
                f=r[c]; pr=piv[c]
                for k,v in pr.items():
                    nv=(r.get(k,0)-f*v)%P
                    if nv: r[k]=nv
                    else: r.pop(k,None)
            else:
                inv=pow(r[c],-1,P); piv[c]={k:v*inv%P for k,v in r.items()}; break
    return len(piv)
def nullity(q,B):
    st=list(itertools.product(range(B+1),repeat=q)); idx={s:i for i,s in enumerate(st)}; n=len(st)
    rows=[]
    for U in st:
        for V in st:
            a,b=add(U,V),add(U,T(V))
            if a in idx and b in idx:
                r={}
                for k,v in ((idx[a],1),(n+idx[b],1),(idx[U],-2),(n+idx[V],-2)): r[k]=(r.get(k,0)+v)%P
                rows.append({k:v for k,v in r.items() if v})
    z=idx[tuple([0]*q)]; rows+= [{z:1},{n+z:1}]
    return 2*n-rank(rows,2*n)
for q,B in [(3,2),(4,2),(4,3),(2,4),(1,5)]:
    print(q,B,nullity(q,B),flush=True)
F=lambda m:sum(m)+3*(m[0]-m[1])**2
a=F((1,1))/2; print('a',a,'c',F((1,0))-a,'F(1,0)',F((1,0)))
for q in (2,4,6):
    m=[1]*q; print(q,sum(m[0::2]),sum(m[1::2]))
