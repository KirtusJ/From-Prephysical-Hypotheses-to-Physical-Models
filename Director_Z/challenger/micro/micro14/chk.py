# micro-review boundary check for THEOREM_T.tex. Own program; exact integers.
import itertools, math
from collections import Counter
def walks(T): return list(itertools.product('RL',repeat=T))
def pos(w,s): return sum(1 if c=='R' else -1 for c in w[:s])
def gain(w):
    g=1; prev='R'
    for c in w:
        if c=='L' and prev=='L': g=-g
        prev=c
    return g
def key(p,N): return p if N is None else p%N
def subsets(K):
    K=sorted(K)
    for r in range(len(K)+1):
        for c in itertools.combinations(K,r): yield frozenset(c)
def m(S,N,integer=False):
    d={}
    for w in S:
        rail=w[-1] if w else 'R'
        y=(pos(w,len(w)) if integer else key(pos(w,len(w)),N),rail)
        p,q=d.get(y,(0,0)); d[y]=(p+1,q) if gain(w)==1 else (p,q+1)
    return d
def ext(S): return frozenset(w+(c,) for w in S for c in 'RL')
def add(a,b): return (a[0]+b[0],a[1]+b[1])
J=lambda a:(a[1],a[0])
def run(N,Tmax=4):
    st=Counter()
    for T in range(1,Tmax+1):
        W=walks(T); W1=walks(T+1)
        K=[sorted({key(pos(w,s),N) for w in W}) for s in range(1,T+1)]
        allK1={key(pos(w,T+1),N) for w in W1}
        distinct=set()
        for A in itertools.product(*[list(subsets(k)) for k in K]):
            S=frozenset(w for w in W if all(key(pos(w,s),N) in A[s-1] for s in range(1,T+1)))
            st['prescriptions']+=1; distinct.add(S)
            if not S: st['empty_prescriptions']+=1
            E=ext(S)
            # item1: Ext S is pp with A_{T+1}=all
            E2=frozenset(w for w in W1 if all(key(pos(w,s),N) in A[s-1] for s in range(1,T+1)) and key(pos(w,T+1),N) in allK1)
            if E!=E2: st['FAIL_ext_pp']+=1
            mS=m(S,N)
            # item3: collisions
            if N is not None:
                if m(S,N,True)!={ (y[0],y[1]):v for y,v in m(S,N,True).items()} : pass
                mi=m(S,None,True); red={}
                ends={}
                for w in S: ends.setdefault((key(pos(w,T),N),w[-1]),set()).add(pos(w,T))
                if any(len(v)>1 for v in ends.values()):
                    st['events_with_integer_collision_T%d'%T]+=1
            sites=K[T-1]+[max(K[T-1])+7 if N is None else None]
            for x in sites:
                if x is None: continue
                Sp=frozenset(w for w in S if key(pos(w,T),N)==x)
                Sq=frozenset(w for w in W if all(key(pos(w,s),N) in (A[s-1] if s<T else A[s-1]&{x}) for s in range(1,T+1)))
                st['site_cases']+=1
                if Sp!=Sq: st['FAIL_restrict_pp']+=1
                U=mS.get((x,'R'),(0,0)); V=mS.get((x,'L'),(0,0))
                mp=m(Sp,N)
                if mp.get((x,'R'),(0,0))!=U or mp.get((x,'L'),(0,0))!=V or any(y[0]!=x for y in mp): st['FAIL_Sprime_counts']+=1
                me=m(ext(Sp),N)
                yR=(key(x+1,N),'R'); yL=(key(x-1,N),'L')
                exp={}
                if add(U,V)!=(0,0): exp[yR]=add(U,V)
                if add(U,J(V))!=(0,0): exp[yL]=add(U,J(V))
                if me!=exp: st['FAIL_daughters']+=1
                if N is not None:
                    # same test with integer (unreduced) counts at integer site x
                    mi=m(S,None,True)
                    if mi.get((x,'R'),(0,0))!=U or mi.get((x,'L'),(0,0))!=V: st['cases_where_integer_count_differs_from_modN_T%d'%T]+=1
            # item 6 and (iv): on line F=x(p+q); everywhere F=a(p+q)+c(p-q)^2 with a=3,c=5
            f=lambda d:sum(3*(p+q)+5*(p-q)**2 for p,q in d.values())
            if f(m(E,N))!=2*f(mS): st['FAIL_iv']+=1
            if N is None:
                g=lambda d:sum(y[0]*(p+q) for y,(p,q) in d.items())
                if g(m(E,N))!=2*g(mS): st['FAIL_item6']+=1
                st['item6_cases']+=1
        st['distinct_events']+=len(distinct)
        st['distinct_T%d'%T]=len(distinct)
    return st
for N in [None,1,2,3,4,5]:
    print('carrier','line' if N is None else 'ring %d'%N, dict(sorted(run(N).items())))
# item 6 on ALL events (all subsets of walks) up to length 4 on the line: linear, check per subset
bad=0;tot=0
for T in range(0,5):
    W=walks(T)
    x=[pos(w,T) for w in W]
    for mask in range(1<<len(W)):
        S=[W[i] for i in range(len(W)) if mask>>i&1]
        a=sum(pos(w,T) for w in S); b=sum(pos(w,T+1) for w in ext(S))
        tot+=1; bad+= (b!=2*a)
print('item6 all events T=0..4 line: cases',tot,'fail',bad)
# item 2: length 0 event
S0=frozenset([()]); print('len0 m',m(S0,None),'ext m',m(ext(S0),None))
# is U=(1,0),V=0 at x=0 realised with T>=1 on the line? A1={-1},A2={0}
S=frozenset(w for w in walks(2) if pos(w,1)==-1 and pos(w,2)==0); print('T=2 replacement',S,m(S,None))
# item 5
print('admitted',[n for n in range(1,31) if n//math.gcd(n,2)>=11])
print('equal 11',[n for n in range(1,31) if n//math.gcd(n,2)==11])
