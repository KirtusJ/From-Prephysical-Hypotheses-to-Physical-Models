"""Examine the solution space of the reduced equations on the classes first seen by length 7
(output of winding_truncated_extract.py). Exploratory, no predicate. Arithmetic modulo the prime of the input.
Usage: python3 analyse_extract.py RESULT_OF_EXTRACT.json OUT.json  (refuses to overwrite)."""
import sys, json, os
R=json.load(open(sys.argv[1])); OUT=sys.argv[2]; assert not os.path.exists(OUT)
P=R["prime"]; cl=R["early_classes"]; ids=sorted(cl,key=int); pos={v:i for i,v in enumerate(ids)}; n=len(ids)
rows=[[0]*n for _ in R["early_rows_mod_p"]]
for r,row in zip(rows,R["early_rows_mod_p"]):
    for k,v in row.items(): r[pos[k]]=v%P
def fam(ms):
    j0=ms[0][0][1]%3; s=[[0,0,0],[0,0,0]]
    a=[0,0,0]
    for (i,j),c in ms:
        assert j%3==j0; a[((j-j0)//3)%3]+=c*(-1)**i
    cnt=sum(c for _,c in ms)
    return cnt,(a[0]+a[1]+a[2])**2,a[0]**2+a[1]**2+a[2]**2-a[0]*a[1]-a[1]*a[2]-a[2]*a[0]
F=[[fam(cl[v])[t]%P for v in ids] for t in range(3)]
inker=[all(sum(x*y for x,y in zip(r,f))%P==0 for r in rows) for f in F]
# nullspace by elimination
M=[r[:] for r in rows]; piv=[]; rk=0
for c in range(n):
    p=next((i for i in range(rk,len(M)) if M[i][c]),None)
    if p is None: continue
    M[rk],M[p]=M[p],M[rk]; inv=pow(M[rk][c],P-2,P); M[rk]=[x*inv%P for x in M[rk]]
    for i in range(len(M)):
        if i!=rk and M[i][c]:
            f=M[i][c]; M[i]=[(x-f*y)%P for x,y in zip(M[i],M[rk])]
    piv.append(c); rk+=1
free=[c for c in range(n) if c not in piv]
basis=[]
for fc in free:
    v=[0]*n; v[fc]=1
    for i,c in enumerate(piv): v[c]=(-M[i][fc])%P
    basis.append(v)
# reduce basis modulo the family: find a vector of the nullspace vanishing on as many early-seen classes as possible
def rank(vs):
    A=[v[:] for v in vs]; r=0
    for c in range(n):
        p=next((i for i in range(r,len(A)) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]; inv=pow(A[r][c],P-2,P); A[r]=[x*inv%P for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]: f=A[i][c]; A[i]=[(x-f*y)%P for x,y in zip(A[i],A[r])]
        r+=1
    return r
fs=R["early_first_seen"]
rep={"classes":n,"rows":len(rows),"nullity":len(free),"family_in_solution_space":inker,"rank_family":rank(F),"rank_family_plus_nullspace":rank(F+basis)}
for cut in range(3,8):
    idx=[i for i,v in enumerate(ids) if fs[v]<=cut]
    sub=lambda v:[v[i] for i in idx]
    def rk2(vs):
        A=[sub(v)+[0]*(n-len(idx)) for v in vs]; return rank(A)
    rep["restricted_to_first_seen_by_%d"%cut]={"classes":len(idx),"dim_nullspace":rk2(basis),"dim_family":rk2(F)}
# the extra direction: a nullspace vector outside the family, normalised to vanish on classes seen by length 6 if possible
ext=[b for b in basis]; 
G=F+ext
# solve for combination: find vector in span(basis) not in span(F): take basis vector and subtract family fit on classes seen by 6
idx6=[i for i,v in enumerate(ids) if fs[v]<=6]
found=None
for b in basis:
    if rank(F+[b])==4:
        # fit c with b - sum c_t F_t = 0 on idx6 (3 unknowns)
        import itertools
        A=[[F[t][i] for t in range(3)]+[b[i]] for i in idx6]
        r=0
        for c in range(3):
            p=next((k for k in range(r,len(A)) if A[k][c]),None)
            if p is None: continue
            A[r],A[p]=A[p],A[r]; inv=pow(A[r][c],P-2,P); A[r]=[x*inv%P for x in A[r]]
            for k in range(len(A)):
                if k!=r and A[k][c]: f=A[k][c]; A[k]=[(x-f*y)%P for x,y in zip(A[k],A[r])]
            r+=1
        consistent=all(row[3]==0 for row in A[r:]); coef=[A[t][3] for t in range(3)] if r==3 else None
        if consistent and coef:
            w=[(b[i]-sum(coef[t]*F[t][i] for t in range(3)))%P for i in range(n)]
            supp=[ids[i] for i in range(n) if w[i]]
            found={"vanishes_on_classes_seen_by_6":True,"support_size":len(supp),
                   "support":[{"class":cl[v],"first_seen":fs[v],"value_mod_p":w[pos[v]] if w[pos[v]]<P//2 else w[pos[v]]-P,"cosets":len({g[1] for g,_ in cl[v]}),"walks":sum(c for _,c in cl[v])} for v in supp[:40]]}
        else: found={"vanishes_on_classes_seen_by_6":False}
        break
rep["extra_direction"]=found
json.dump(rep,open(OUT,"x"),indent=1); print(json.dumps({k:v for k,v in rep.items() if k!="extra_direction"}));
if found: print({k:v for k,v in found.items() if k!="support"}); [print(s) for s in found.get("support",[])[:25]]
