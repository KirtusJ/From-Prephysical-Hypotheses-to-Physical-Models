"""Attack C on G1 v1.0. Exact (sympy rationals), no randomness. Usage: python3 attack_C.py OUTDIR
Sharp launch (0,R) on the unwrapped line. Per port: n_plus, n_minus = numbers of positive/negative routes.
Site conservation with the front (in (1,0),(0,0); out two ports with one positive route) forces Z_{t+1}/Z_t=2
whenever the response at one positive route is nonzero; so the system is linear:
  resp(outR)+resp(outL) = 2[resp(inR)+resp(inL)]  for every site, every t<T.  resp(empty)=0.
Predicates fixed before the first run:
 P1 (hypothesis) the front equation has the stated form at every t<T (count reported).
 P2 model PM: resp=F(n_plus,n_minus). count F=p+m and square F=(p-m)^2 both solve; nullspace dim == 2 for T>=6.
 P3 model S: resp=f(p-m): nullspace dim == 1 (the square) for T>=6.
 P4 model N: resp=h(p+m): nullspace dim == 1 (the count) for T>=6.
 P5 model ARC: detector resolves (site, rail, previous rail); resp=g(signed total on the arc), g(0)=0;
    equation 2g(a+b)+g(c+d)+g(-(c+d)) = 2[g(a)+g(b)+g(c)+g(d)], t>=1: nullspace dim == 0 for T>=6 (no solution with g(1)>0).
 Note fixed beforehand: (signed total, number of routes) is a bijective relabelling of (n_plus,n_minus); model SN == model PM.
Failed predicates are kept in the result file.
"""
import sys, json, os
from sympy import Matrix
def evolve(T):
    st={0:((1,0),(0,0))}; snaps=[st]
    for t in range(T):
        nx={}
        for x,((pr,mr),(pl,ml)) in st.items():
            R=nx.setdefault(x+1,[(0,0),(0,0)]); L=nx.setdefault(x-1,[(0,0),(0,0)])
            R[0]=(pr+pl,mr+ml); L[1]=(pr+ml,mr+pl)
        st={x:(tuple(v[0]),tuple(v[1])) for x,v in nx.items()}; snaps.append(st)
    return snaps
def null(eqs,key0):
    keys=sorted({k for e in eqs for k in e if k!=key0}); idx={k:i for i,k in enumerate(keys)}
    rows=[]
    for e in eqs:
        r=[0]*len(keys)
        for k,c in e.items():
            if k!=key0: r[idx[k]]+=c
        if any(r): rows.append(tuple(r))
    rows=sorted(set(rows)); M=Matrix(rows) if rows else Matrix.zeros(1,len(keys))
    return keys,idx,M,len(keys)-M.rank()
def insol(M,idx,keys,fn):
    v=Matrix([fn(k) for k in keys]); return all(z==0 for z in M*v)
out={"runs":[]}
TM=int(sys.argv[2]) if len(sys.argv)>2 else 14
for T in range(2,TM+1):
    sn=evolve(T); rec={"T":T}; fronts=0
    E={"PM":[], "S":[], "N":[], "ARC":[]}
    for t in range(T):
        a,b=sn[t],sn[t+1]
        for x,(r,l) in a.items():
            oR=b[x+1][0]; oL=b[x-1][1]
            if x==t and r==(1,0) and l==(0,0) and oR==(1,0) and oL==(1,0): fronts+=1
            for name,key in (("PM",lambda q:q),("S",lambda q:q[0]-q[1]),("N",lambda q:q[0]+q[1])):
                e={}
                for q,c in ((oR,1),(oL,1),(r,-2),(l,-2)): e[key(q)]=e.get(key(q),0)+c
                E[name].append(e)
            if t>=1:
                p=sn[t-1]
                def s(q): return q[0]-q[1]
                A=s(p[x-1][0]) if x-1 in p else 0; B=s(p[x-1][1]) if x-1 in p else 0   # arcs RR, LR into (x,R)
                C=s(p[x+1][0]) if x+1 in p else 0; D=-s(p[x+1][1]) if x+1 in p else 0  # arcs RL, LL into (x,L)
                assert A+B==s(r) and C+D==s(l)
                e={}
                for q,c in ((A+B,2),(C+D,1),(-(C+D),1),(A,-2),(B,-2),(C,-2),(D,-2)): e[q]=e.get(q,0)+c
                E["ARC"].append(e)
    rec["P1_front_ok"]=(fronts==T); rec["fronts"]=fronts
    k,i,M,d=null(E["PM"],(0,0)); rec["PM"]=dict(unknowns=len(k),rank=len(k)-d,dim=d,count_solves=insol(M,i,k,lambda q:q[0]+q[1]),square_solves=insol(M,i,k,lambda q:(q[0]-q[1])**2))
    if d>2 and len(k)<400:
        ns=M.nullspace(); rec["PM"]["extra_supports"]=[sorted(str(k[j]) for j in range(len(k)) if v[j]!=0)[:12] for v in ns][:8]
    k,i,M,d=null(E["S"],0); rec["S"]=dict(unknowns=len(k),dim=d,square_solves=insol(M,i,k,lambda q:q*q),abs_solves=insol(M,i,k,abs))
    k,i,M,d=null(E["N"],0); rec["N"]=dict(unknowns=len(k),dim=d,count_solves=insol(M,i,k,lambda q:q))
    k,i,M,d=null(E["ARC"],0); rec["ARC"]=dict(unknowns=len(k),dim=d,square_solves=insol(M,i,k,lambda q:q*q),abs_solves=insol(M,i,k,abs))
    if T>=6:
        rec["P2"]=rec["PM"]["dim"]==2 and rec["PM"]["count_solves"] and rec["PM"]["square_solves"]
        rec["P3"]=rec["S"]["dim"]==1; rec["P4"]=rec["N"]["dim"]==1; rec["P5"]=rec["ARC"]["dim"]==0
    out["runs"].append(rec); print(json.dumps(rec),flush=True)
os.makedirs(sys.argv[1],exist_ok=True)
with open(os.path.join(sys.argv[1],"attack_C.json"),"x") as f: json.dump(out,f,indent=1)
