"""t_check.py -- exact checks for THEOREM_T (position product events). Seed 20261113. Result file mode 'x'.

Conventions. Vertices (x,R),(x,L); arcs to (x+1,R),(x-1,L); gain -1 only on (x,L)->(x-1,L). Start (0,R), gain +1.
m=(p,q)=(number of walks of gain +1, of gain -1) ending at a vertex. J(p,q)=(q,p). |m|=p+q. Simplex(M)={m: 1<=|m|<=M}.
All arithmetic is in Fractions / integers. Predicates, fixed before the first run:

P1  Unknowns F_R(m),F_L(m), m in Simplex(M). Equations F_R(U+V)+F_L(U+JV)=2F_R(U)+2F_L(V) for all U,V with |U|+|V|<=M
    (F(0,0)=0 substituted). Predicate: nullity == 2 and both a(p+q), (p-q)^2 (same on both rails) are solutions, M=2..7.
P2  Same, but only the families used in the proof: V=0; U=0; V=(1,1); V=(1,0). Predicate: nullity == 2, M=2..7.
P2f (recorded, no predicate) nullity when one of the four families is left out.
P3  Converse. Hypothesis tested per case: S is a set of walks of one length (any set, not only product). For random
    rational a,c and random events on the line and on rings N in {1,2,3,4,5,13}, lengths 1..7:
    mu(Ext S) == 2 mu(S) with F=a(p+q)+c(p-q)^2. Also all position product events of length <=4 on the line.
P4  (iii). For k in a grid of rationals != 2, system as P1 with factor k, M=5: every solution has
    Sigma(m)=F_R(m)+F_R(Jm)+F_L(m)+F_L(Jm)=0 for all m (functional vanishes on the null space). For k=2 it does not.
P4c Counterexamples kept: (a) line, F_y=lam^x (p+q), lam=2: mu(Ext S)==(5/2) mu(S) on random events, F>=0, not zero.
    (b) line, F_y=x(p+q): mu(Ext S)==2mu(S) on random events; values at walks R and L are 1,-1.
P5  (ii) single-input system on a ring Z_N, k=2, one orbit {m,Jm}, m!=Jm: unknowns A_x(m),A_x(Jm),B_x(m),B_x(Jm);
    equations A_{x+1}(m)+B_{x-1}(m)=2A_x(m), A_{x+1}(m)+B_{x-1}(Jm)=2B_x(m) and the same with m,Jm exchanged.
    Predicate: nullity == 1 (the constant) for N=1..40. Case m=Jm: unknowns A_x,B_x, nullity == 1.
P5k (iii, ring, site-dependent) same system with factor k != 2 from the grid: the functional sum_x (A+A'+B+B') vanishes
    on the null space, N=1..24.
P6  Replay of the cited preparation (prescribed order: corridor 0 first). Hypothesis tested per carrier:
    line, or ring with N/gcd(N,2) >= 11 (and N/gcd(N,2) > 11 reported separately). For all U,V with entries 0..2
    (81 targets): the event has exactly U at (x,R), V at (x,L), x=T-20, T=15+6(pR+qL)+5(qR+pL), and EVERY other vertex
    empty; at most 5 positions kept per tick. With prefix: same at prescribed sites x* in {-7,-1,0,3,40} (line) and
    all residues (rings 13, 24, 11, 22), targets with entries 0..1 (16).
P6s (recorded, no predicate) the same 81 targets on rings 3..10, 12, 14, 16, 18, 20: number passing.
"""
import json, random, sys, itertools
from fractions import Fraction as Fr
random.seed(20261113)
OUT='t_check_results.json'
res={}
J=lambda m:(m[1],m[0])
add=lambda a,b:(a[0]+b[0],a[1]+b[1])
def simplex(M): return [(p,s-p) for s in range(1,M+1) for p in range(s+1)]
def rref(rows,n):
    rows=[r[:] for r in rows]; piv=[]; r=0
    for c in range(n):
        i=next((i for i in range(r,len(rows)) if rows[i][c]!=0),None)
        if i is None: continue
        rows[r],rows[i]=rows[i],rows[r]; pv=rows[r][c]; rows[r]=[v/pv for v in rows[r]]
        for j in range(len(rows)):
            if j!=r and rows[j][c]!=0:
                f=rows[j][c]; rows[j]=[a-f*b for a,b in zip(rows[j],rows[r])]
        piv.append(c); r+=1
        if r==len(rows): break
    return rows[:r],piv
def nullbasis(rows,n):
    R,piv=rref(rows,n); free=[c for c in range(n) if c not in piv]; B=[]
    for f in free:
        v=[Fr(0)]*n; v[f]=Fr(1)
        for i,c in enumerate(piv): v[c]=-R[i][f]
        B.append(v)
    return B
def system(M,k,fam=None):
    S=simplex(M); idx={}
    for m in S: idx[('R',m)]=len(idx)
    for m in S: idx[('L',m)]=len(idx)
    n=len(idx); rows=[]
    Z=[(0,0)]+S
    for U in Z:
        for V in Z:
            if U==(0,0) and V==(0,0): continue
            if U[0]+U[1]+V[0]+V[1]>M: continue
            if fam is not None and not fam(U,V): continue
            r=[Fr(0)]*n
            r[idx[('R',add(U,V))]]+=1; r[idx[('L',add(U,J(V)))]]+=1
            if U!=(0,0): r[idx[('R',U)]]-=k
            if V!=(0,0): r[idx[('L',V)]]-=k
            rows.append(r)
    return rows,idx,n
def sat(rows,v): return all(sum(a*b for a,b in zip(r,v))==0 for r in rows)
# P1,P2
fams={'V0':lambda U,V:V==(0,0),'U0':lambda U,V:U==(0,0),'VC':lambda U,V:V==(1,1),'V10':lambda U,V:V==(1,0)}
p1=[];p2=[];p2f={}
for M in range(2,8):
    rows,idx,n=system(M,Fr(2))
    cnt=[Fr(0)]*n; sq=[Fr(0)]*n
    for (r,m),i in idx.items(): cnt[i]=Fr(m[0]+m[1]); sq[i]=Fr((m[0]-m[1])**2)
    nb=nullbasis(rows,n)
    p1.append({'M':M,'unknowns':n,'equations':len(rows),'nullity':len(nb),'count_ok':sat(rows,cnt),'square_ok':sat(rows,sq),
               'pass':len(nb)==2 and sat(rows,cnt) and sat(rows,sq)})
    rows2,_,_=system(M,Fr(2),lambda U,V:any(f(U,V) for f in fams.values()))
    nb2=nullbasis(rows2,n); p2.append({'M':M,'equations':len(rows2),'nullity':len(nb2),'pass':len(nb2)==2})
    p2f[M]={}
    for out in fams:
        rr,_,_=system(M,Fr(2),lambda U,V:any(f(U,V) for nm,f in fams.items() if nm!=out))
        p2f[M]['without_'+out]=len(nullbasis(rr,n))
res['P1']=p1;res['P2']=p2;res['P2f_nullity_with_one_family_removed']=p2f
# walks
def step(state,N):
    new={}
    for (x,r),m in state.items():
        y=(x+1,'R') if N is None else ((x+1)%N,'R'); new[y]=add(new.get(y,(0,0)),m)
        y=(x-1,'L') if N is None else ((x-1)%N,'L'); new[y]=add(new.get(y,(0,0)),m if r=='R' else J(m))
    return new
def walk_end(w,N):
    x=0;r='R';s=0
    for ch in w:
        if ch=='L' and r=='L': s^=1
        x+=1 if ch=='R' else -1; r=ch
    if N is not None: x%=N
    return (x,r),s
def state_of(S,N):
    st={}
    for w in S:
        y,s=walk_end(w,N); st[y]=add(st.get(y,(0,0)),(1,0) if s==0 else (0,1))
    return st
def ext(S): return [w+c for w in S for c in 'RL']
def mu(st,F): return sum((F(y,m) for y,m in st.items()),Fr(0))
# P3
p3={'cases':0,'qualify':0,'fail':[]}
for N in [None,1,2,3,4,5,13]:
    for T in range(1,8):
        allw=[''.join(t) for t in itertools.product('RL',repeat=T)]
        for _ in range(12):
            S=[w for w in allw if random.random()<random.choice([0.1,0.5,0.9])]
            a=Fr(random.randint(-9,9),random.randint(1,7)); c=Fr(random.randint(-9,9),random.randint(1,7))
            F=lambda y,m:a*(m[0]+m[1])+c*(m[0]-m[1])**2
            p3['cases']+=1
            if len(set(S))==len(S) and all(len(w)==T for w in S): p3['qualify']+=1
            else: continue
            st=state_of(S,N); st2=state_of(ext(S),N)
            assert st2==step(st,N) or not S, 'Ext != step'
            if mu(st2,F)!=2*mu(st,F): p3['fail'].append([N,T,S,str(a),str(c)])
# all position product events length<=4 on line
pp=0;ppf=[]
for T in range(1,5):
    pos=[list(range(-s,s+1,2)) for s in range(1,T+1)]
    subs=[[frozenset(c) for k in range(len(P)+1) for c in itertools.combinations(P,k)] for P in pos]
    allw=[''.join(t) for t in itertools.product('RL',repeat=T)]
    def poss(w):
        x=0;o=[]
        for ch in w: x+=1 if ch=='R' else -1; o.append(x)
        return o
    PW={w:poss(w) for w in allw}
    for A in itertools.product(*subs):
        S=[w for w in allw if all(PW[w][s] in A[s] for s in range(T))]
        F=lambda y,m:Fr(3,5)*(m[0]+m[1])+Fr(-7,2)*(m[0]-m[1])**2
        pp+=1
        if mu(state_of(ext(S),None),F)!=2*mu(state_of(S,None),F): ppf.append([T,[sorted(a) for a in A]])
p3['position_product_events_line_len<=4']=pp;p3['position_product_fail']=ppf
p3['pass']=(not p3['fail']) and not ppf
res['P3']=p3
# P4
grid=[Fr(a,b) for a,b in [(-2,1),(-1,1),(0,1),(1,2),(1,1),(3,2),(7,5),(17,12),(5,2),(3,1),(4,1),(10,3)]]
p4=[]
def sigma_vanishes(M,k):
    rows,idx,n=system(M,k); nb=nullbasis(rows,n)
    ok=all(v[idx[('R',m)]]+v[idx[('R',J(m))]]+v[idx[('L',m)]]+v[idx[('L',J(m))]]==0 for v in nb for m in simplex(M))
    return len(nb),ok
for k in grid:
    nl,ok=sigma_vanishes(5,k); p4.append({'k':str(k),'nullity':nl,'Sigma_vanishes_on_null_space':ok,'pass':ok})
nl,ok=sigma_vanishes(5,Fr(2)); p4.append({'k':'2','nullity':nl,'Sigma_vanishes_on_null_space':ok,'pass':(not ok)})
res['P4']=p4
# P4c
p4c={'a_fail':[],'b_fail':[],'a_cases':0,'b_cases':0}
for T in range(1,8):
    allw=[''.join(t) for t in itertools.product('RL',repeat=T)]
    for _ in range(15):
        S=[w for w in allw if random.random()<0.5]
        Fa=lambda y,m:(Fr(2)**y[0])*(m[0]+m[1]); Fb=lambda y,m:Fr(y[0])*(m[0]+m[1])
        st=state_of(S,None); st2=state_of(ext(S),None)
        p4c['a_cases']+=1;p4c['b_cases']+=1
        if mu(st2,Fa)!=Fr(5,2)*mu(st,Fa): p4c['a_fail'].append(S)
        if mu(st2,Fb)!=2*mu(st,Fb): p4c['b_fail'].append(S)
p4c['b_values_R_L']=[str(mu(state_of(['R'],None),lambda y,m:Fr(y[0])*(m[0]+m[1]))),str(mu(state_of(['L'],None),lambda y,m:Fr(y[0])*(m[0]+m[1])))]
p4c['pass']=not p4c['a_fail'] and not p4c['b_fail']
res['P4c']=p4c
# P5
def ringsys(N,k,sym):
    # unknown index: (x,which) which in A,A',B,B' (A'=A at Jm); if sym: A,B only
    names=['A','B'] if sym else ['A','Ap','B','Bp']
    idx={(x,w):x*len(names)+i for x in range(N) for i,w in enumerate(names)}; n=len(idx); rows=[]
    pr={'A':'A','B':'B'} if sym else {'A':'Ap','Ap':'A','B':'Bp','Bp':'B'}
    for x in range(N):
        for a,b in ([('A','B')] if sym else [('A','B'),('Ap','Bp')]):
            r=[Fr(0)]*n; r[idx[((x+1)%N,a)]]+=1; r[idx[((x-1)%N,b)]]+=1; r[idx[(x,a)]]-=k; rows.append(r)
            r=[Fr(0)]*n; r[idx[((x+1)%N,a)]]+=1; r[idx[((x-1)%N,pr[b])]]+=1; r[idx[(x,b)]]-=k; rows.append(r)
    return rows,n
p5=[]
for N in range(1,41):
    r1,n1=ringsys(N,Fr(2),False); r2,n2=ringsys(N,Fr(2),True)
    a=len(nullbasis(r1,n1)); b=len(nullbasis(r2,n2))
    const_ok=sat(r1,[Fr(1)]*n1) and sat(r2,[Fr(1)]*n2)
    p5.append({'N':N,'nullity_m_ne_Jm':a,'nullity_m_eq_Jm':b,'pass':a==1 and b==1 and const_ok})
res['P5']=p5
p5k=[]
for N in range(1,25):
    for k in grid:
        ok=True;nls=[]
        for sym in (False,True):
            rr,n=ringsys(N,k,sym); nb=nullbasis(rr,n); nls.append(len(nb))
            ok=ok and all(sum(v)==0 for v in nb)
        if not ok or any(nls): p5k.append({'N':N,'k':str(k),'nullities':nls,'sum_vanishes':ok})
res['P5k_nonzero_null_spaces']=p5k
res['P5k_pass']=all(e['sum_vanishes'] for e in p5k)
# P6
def schedule(U,V):
    """list of deficit sets per tick, prescribed order"""
    pR,qR=U; pL,qL=V
    L=[{0,1},{0,2},{0,3},{0,3},{0,4},{0,5},{0,6},{0,6}]
    P={0,4,6,10}
    def pulse(b,positive):
        ex=[[b+1],[b+2],[b+2],[b+3],[],[]] if positive else [[b+1],[b+2],[b+3],[],[]]
        return [P|set(e) for e in ex]
    for _ in range(qL): L+=pulse(0,True)      # corridor 0 stores JV=(qL,pL)
    for _ in range(pL): L+=pulse(0,False)
    for _ in range(pR): L+=pulse(6,True)      # corridor 6 stores U
    for _ in range(qR): L+=pulse(6,False)
    L.append({4,10})
    for i in range(1,7): L.append({4+i,10})
    return L
def run(U,V,N,xstar=None):
    T=15+6*(U[0]+V[1])+5*(U[1]+V[0]); x0=T-20
    st={(0,'R'):(1,0)}; t0=0; h=0; maxkeep=0
    if xstar is not None:
        h=xstar-x0
        if N is not None: h%=N
        w='R'*h if h>=0 else 'L'*(1-h)+'R'
        if walk_end(w,None)[1]==1: w+='RLRLLR'
        x=0
        for ch in w:
            x+=1 if ch=='R' else -1
            xx=x if N is None else x%N
            st={y:m for y,m in step(st,N).items() if y[0]==xx}
        t0=len(w)
    for t,D in enumerate(schedule(U,V),1):
        keep={h+t-2*d for d in D}
        if N is not None: keep={x%N for x in keep}
        maxkeep=max(maxkeep,len(keep))
        st={y:m for y,m in step(st,N).items() if y[0] in keep}
    xf=h+x0
    if N is not None: xf%=N
    want={}
    if U!=(0,0): want[(xf,'R')]=U
    if V!=(0,0): want[(xf,'L')]=V
    st={y:m for y,m in st.items() if m!=(0,0)}
    return st==want and maxkeep<=5, {str(k):v for k,v in st.items()}, len(schedule(U,V))==T
t81=[((a,b),(c,d)) for a in range(3) for b in range(3) for c in range(3) for d in range(3)]
t16=[((a,b),(c,d)) for a in range(2) for b in range(2) for c in range(2) for d in range(2)]
from math import gcd
p6=[]
for N in [None,11,13,15,17,19,21,22,23,24,25,26,28,30,31,46,47]:
    per=None if N is None else N//gcd(N,2)
    qual=(N is None) or per>=11
    ok=0;fails=[];Tok=True
    for U,V in t81:
        g,st,tk=run(U,V,N); Tok=Tok and tk
        if g: ok+=1
        else: fails.append([U,V,st])
    p6.append({'carrier':'line' if N is None else N,'period':per,'qualifies(>=11)':qual,'strict(>11)':N is None or per>11,
               'passed':ok,'of':81,'T_formula_ok':Tok,'first_fail':fails[:1],'pass':ok==81 and Tok})
res['P6']=p6
p6p=[]
for N,sites in [(None,[-7,-1,0,3,40]),(13,range(13)),(24,range(24)),(11,range(11)),(22,range(22))]:
    ok=0;tot=0;fails=[]
    for xs in sites:
        for U,V in t16:
            tot+=1; g,st,_=run(U,V,N,xs)
            if g: ok+=1
            else: fails.append([xs,U,V,st])
    p6p.append({'carrier':'line' if N is None else N,'passed':ok,'of':tot,'first_fail':fails[:1],'pass':ok==tot})
res['P6_prefix']=p6p
p6s=[]
for N in [3,4,5,6,7,8,9,10,12,14,16,18,20]:
    ok=0;ff=None
    for U,V in t81:
        g,st,_=run(U,V,N)
        if g: ok+=1
        elif ff is None: ff=[U,V,st]
    p6s.append({'N':N,'period':N//gcd(N,2),'passed':ok,'of':81,'first_fail':ff})
res['P6s_small_rings_no_predicate']=p6s
allp=(all(e['pass'] for e in p1+p2+p4+p5+p6+p6p) and p3['pass'] and p4c['pass'] and res['P5k_pass'])
res['ALL_PREDICATES_PASS']=allp
with open(OUT,'x') as f: json.dump(res,f,indent=1,default=str,sort_keys=True)
print('ALL',allp)
for k in ['P1','P2','P4','P6','P6_prefix','P6s_small_rings_no_predicate']:
    for e in res[k]: print(k,{a:b for a,b in e.items() if a!='first_fail'})
print('P2f',p2f[7]); print('P3',p3['cases'],p3['qualify'],len(p3['fail']),pp,len(ppf)); print('P4c',p4c['pass'],p4c['b_values_R_L'])
print('P5',all(e['pass'] for e in p5),[e for e in p5 if not e['pass']]); print('P5k',res['P5k_pass'],p5k[:6],len(p5k))
