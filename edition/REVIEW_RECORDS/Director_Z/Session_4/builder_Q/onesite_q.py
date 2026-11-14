"""onesite_q.py -- exact solution space of the one-site equation for gains in Z_q.

CARRIER. Arc digraph of the line/ring: vertices (x,R),(x,L); arcs from either to (x+1,R)
and (x-1,L); all gains 0 (additive Z_q) except the fixed gain h on (x,L)->(x-1,L).
A multiset of gains is m in N^q; (T m)(g) = m(g-h) (every gain multiplied by h).
ONE-SITE EQUATION (two unknown functions, F_R(0)=F_L(0)=0):
   (E)  F_R(U+V) + F_L(U+TV) = 2 F_R(U) + 2 F_L(V)   for all U,V with |U|+|V| <= n.
Unknowns: F_R(m), F_L(m) for 1 <= |m| <= n.  Arithmetic: ranks modulo the prime
p = 2^61-1 (nullity mod p >= nullity over Q; the lower bound over Q comes from P2).

PREDICATES (fixed before the first run):
 P1  h=1 (a generator): at the largest n run for q, nullity == 1 + [q even]
     (count |m|; and for q even (sum_g (-1)^g m_g)^2 = |sigma_psi(m)|^2, psi(h)=-1,
      the only character in which the step is norm-preserving; none for q odd).
     Smaller n are reported as measured, whatever they give.
 P2  the functions F_R=F_L=|m| and (q even) F_R=F_L=eps(m)^2 satisfy every instance of
     (E) in the box, in exact integers.  Number of instances reported.
 P3  (side, h not a generator, order r, k=q/r; conjectural prediction, full multisets
     on Z_q) nullity at largest n == k + [r even]*k(k+1)/2.
 CONTROL q=2,h=1: nullity 2.
Hypothesis check per case: h generator tested (gcd(h,q)==1) before P1; number qualifying reported.
Seed 20261113 (used only to shuffle the order of equations; the result does not depend on it).
Result file opened with mode 'x'.
"""
import itertools, json, random, sys, math
P=(1<<61)-1
random.seed(20261113)
def msets(q,n):
    out=[]
    for s in range(n+1):
        for c in itertools.combinations_with_replacement(range(q),s):
            m=[0]*q
            for g in c: m[g]+=1
            out.append(tuple(m))
    return out
def run(q,h,n):
    ms=msets(q,n); size={m:sum(m) for m in ms}
    idx={}
    for m in ms:
        if size[m]>0:
            idx[('R',m)]=len(idx); idx[('L',m)]=len(idx)
    nun=len(idx)
    T=lambda m: tuple(m[(g-h)%q] for g in range(q))
    add=lambda a,b: tuple(x+y for x,y in zip(a,b))
    eps=lambda m: sum((-1)**g*m[g] for g in range(q))
    pairs=[(U,V) for U in ms for V in ms if size[U]+size[V]<=n]
    random.shuffle(pairs)
    piv={}; neq=0; p2=True
    for U,V in pairs:
        row={}
        for (k,m,c) in (('R',add(U,V),1),('L',add(U,T(V)),1),('R',U,-2),('L',V,-2)):
            if size[m]>0:
                i=idx[(k,m)]; row[i]=(row.get(i,0)+c)%P
        row={i:v for i,v in row.items() if v}
        neq+=1
        # P2
        W1,W2=add(U,V),add(U,T(V))
        if sum(W1)+sum(W2)!=2*sum(U)+2*sum(V): p2=False
        if q%2==0 and h%2==1 and eps(W1)**2+eps(W2)**2!=2*eps(U)**2+2*eps(V)**2: p2=False
        while row:
            c=max(row)
            if c in piv:
                f=row[c]
                for i,v in piv[c].items():
                    nv=(row.get(i,0)-f*v)%P
                    if nv: row[i]=nv
                    else: row.pop(i,None)
            else:
                inv=pow(row[c],P-2,P)
                piv[c]={i:v*inv%P for i,v in row.items()}
                break
    return dict(q=q,h=h,n=n,unknowns=nun,equations=neq,rank=len(piv),nullity=nun-len(piv),P2=p2)
plan={2:[2,3,4,6,10],3:[2,3,4,5,6,7],4:[2,3,4,5,6],5:[2,3,4,5,6],6:[2,3,4,5]}
side=[(4,2,5),(4,0,4),(6,2,4),(6,3,4),(6,4,4),(3,0,5),(2,0,6)]
res={'prime':P,'seed':20261113,'main':[],'side':[]}
qual=0;ok1=True
for q in plan:
    assert math.gcd(1,q)==1; qual+=1
    for n in plan[q]:
        r=run(q,1,n); r['predicted']=1+(q%2==0)
        r['is_largest_n']=(n==plan[q][-1])
        if r['is_largest_n']: r['P1']=(r['nullity']==r['predicted']); ok1&=r['P1']
        res['main'].append(r); print(r,flush=True)
ok3=True
for q,h,n in side:
    r=run(q,h,n); o=q//math.gcd(h,q); k=q//o
    r['order_h']=o; r['predicted']=k+(k*(k+1)//2 if o%2==0 else 0); r['P3']=(r['nullity']==r['predicted']); ok3&=r['P3']
    res['side'].append(r); print(r,flush=True)
res['qualifying_main_q']=qual; res['P1_all']=ok1; res['P2_all']=all(r['P2'] for r in res['main']+res['side']); res['P3_all']=ok3
with open('onesite_q_result.json','x') as f: json.dump(res,f,indent=1)
print(res['P1_all'],res['P2_all'],res['P3_all'])
