"""Micro-review of thm:vertexlaw. Predicates fixed before run:
 P1 dim(GL solutions, F_y(0)=0, total size<=3) == sum_T |C|/|Gamma_T| + sum_{unordered} dim K   (two primes)
 P2 (case 3) dim without F(0)=0 == P1 dim + |V|-1
 P3 trivial character not in U(D)
Group Z_q additive; arcs {(y,z):gain}."""
import itertools, json
from flint import nmod_mat
def isp(n):
    i=2
    while i*i<=n:
        if n%i==0: return False
        i+=1
    return True
PR=[p for p in range(10**6,10**6+20000) if p%12==1 and isp(p)][:2]
def msets(q,S):
    return [c for c in itertools.product(range(S+1),repeat=q) if sum(c)<=S]
def tr(m,k,q): return tuple(m[(h-k)%q] for h in range(q))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def rank(rows,ncol,p):
    if not rows: return 0
    return nmod_mat(len(rows),ncol,[x%p for r in rows for x in r],p).rank()
def gl_dim(V,arcs,q,d,S,p,zero=True):
    ms=msets(q,S); z0=tuple([0]*q)
    idx={}
    for y in range(V):
        for m in ms:
            if zero and m==z0: continue
            idx[(y,m)]=len(idx)
    rows=[]
    for fam in itertools.product(ms,repeat=V):
        if sum(map(sum,fam))>S: continue
        r=[0]*len(idx)
        for z in range(V):
            w=z0
            for y in range(V):
                if (y,z) in arcs: w=add(w,tr(fam[y],arcs[(y,z)],q))
            if (z,w) in idx: r[idx[(z,w)]]+=1
        for y in range(V):
            if (y,fam[y]) in idx: r[idx[(y,fam[y])]]-=d
        rows.append(r)
    return len(idx)-rank(rows,len(idx),p)
def root(q,p):
    for g in range(2,p):
        w=pow(g,(p-1)//q,p)
        if all(pow(w,k,p)!=1 for k in range(1,q)): return w
def formula(V,arcs,q,d,p):
    succ={y:[z for z in range(V) if (y,z) in arcs] for y in range(V)}
    def reach(y):
        s={y};st=[y]
        while st:
            u=st.pop()
            for z in succ[u]:
                if z not in s: s.add(z);st.append(z)
        return s
    R={y:reach(y) for y in range(V)}
    classes=[]
    for y in range(V):
        if all(y in R[z] for z in R[y]):
            T=frozenset(R[y])
            if T not in classes: classes.append(T)
    lin=0;info=[]
    for T in classes:
        b=min(T); seen=set(); st=[(z,arcs[(b,z)]%q) for z in succ[b]]
        while st:
            s=st.pop()
            if s in seen: continue
            seen.add(s)
            for z in succ[s[0]]: st.append((z,(s[1]+arcs[(s[0],z)])%q))
        G={g for (v,g) in seen if v==b}
        lin+=q//len(G); info.append((sorted(T),sorted(G)))
    w=root(q,p) if q>1 else 1
    ch=lambda j,g: pow(w,(j*g)%q,p)
    quad=0;K={}
    for a in range(q):
        for l in range(a,q):
            rows=[]
            for y in range(V):
                for y2 in range(V):
                    r=[0]*V
                    for z in range(V):
                        if (y,z) in arcs and (y2,z) in arcs:
                            r[z]=(r[z]+ch(a,arcs[(y,z)])*ch(l,arcs[(y2,z)]))%p
                    if y==y2: r[y]=(r[y]-d)%p
                    rows.append(r)
            k=V-rank(rows,V,p)
            if k: K[f"{a},{l}"]=k
            quad+=k
    # U(D)
    U=[]
    for a in range(q):
        ok=True
        for y in range(V):
            for y2 in range(V):
                s=sum(ch((-a)%q,arcs[(y,z)])*ch(a,arcs[(y2,z)]) for z in range(V) if (y,z) in arcs and (y2,z) in arcs)%p
                if s!=(d if y==y2 else 0)%p: ok=False
        if ok: U.append(a)
    return lin,quad,K,info,U
c3={(0,0):0,(0,1):0,(1,0):0,(1,1):1}
def shift(a,k): return {(y+k,z+k):g for (y,z),g in a.items()}
cases={
 "2 K2loops C=1":(2,{(0,0):0,(0,1):0,(1,0):0,(1,1):0},1,2),
 "3 Hadamard C2":(2,c3,2,2),
 "4 all +1 in C2":(2,{(0,0):0,(0,1):0,(1,0):0,(1,1):0},2,2),
 "5a case3 + source c (gains 1,1)":(3,{**c3,(2,0):0,(2,1):0},2,2),
 "5b case3 + source c (gains 1,-1)":(3,{**c3,(2,0):0,(2,1):1},2,2),
 "6 two copies of 3":(4,{**c3,**shift(c3,2)},2,2),
 "7 3-cycle-complement C2":(3,{(0,1):1,(0,2):0,(1,2):0,(1,0):0,(2,0):0,(2,1):0},2,2),
 "8 loop, 3 vertices C3":(3,{(0,0):1,(0,1):0,(1,2):0,(1,0):2,(2,0):0,(2,1):1},3,2),
 "9 Hadamard gains in C4 (Gamma index 2)":(2,{(0,0):0,(0,1):0,(1,0):0,(1,1):2},4,2),
 "10 d=3 Fourier C3":(3,{(y,z):(y*z)%3 for y in range(3) for z in range(3)},3,3),
 "11 case3 + 2 sources, K4-ish":(4,{**c3,(2,0):0,(2,1):1,(3,2):0,(3,0):1},2,2),
}
out={}
for name,(V,arcs,q,d) in cases.items():
    assert all(sum(1 for z in range(V) if (y,z) in arcs)==d for y in range(V))
    res=[]
    for p in PR:
        S=3
        g=gl_dim(V,arcs,q,d,S,p)
        lin,quad,K,info,U=formula(V,arcs,q,d,p)
        res.append((g,lin,quad))
    g2=gl_dim(V,arcs,q,d,2,PR[0])
    out[name]=dict(computed=[r[0] for r in res],formula=[r[1]+r[2] for r in res],lin=lin,quad=quad,K=K,classes=info,U=U,dim_S2=g2,
                   P1="PASS" if all(r[0]==r[1]+r[2] for r in res) else "FAIL",P3="PASS" if 0 not in U else "FAIL")
    print(name,out[name])
V,arcs,q,d=cases["3 Hadamard C2"]
dz=[gl_dim(V,arcs,q,d,3,p,zero=False) for p in PR]
out["P2 case3 no F(0)=0"]=dict(dim=dz,expected=out["3 Hadamard C2"]["computed"][0]+V-1,P2="PASS" if all(x==out["3 Hadamard C2"]["computed"][0]+V-1 for x in dz) else "FAIL")
V,arcs,q,d=cases["5a case3 + source c (gains 1,1)"]
out["P2 case5a"]=dict(dim=gl_dim(V,arcs,q,d,3,PR[0],zero=False),expected=out["5a case3 + source c (gains 1,1)"]["computed"][0]+V-1)
print(out["P2 case3 no F(0)=0"],out["P2 case5a"])
import os
assert not os.path.exists("results.json")
json.dump(out,open("results.json","w"),indent=1)
