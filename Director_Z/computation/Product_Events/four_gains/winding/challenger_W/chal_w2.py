#!/usr/bin/env python3
"""Challenger program for STATEMENTS.md (winding).  Own program; exact integer arithmetic only.

Conventions: walk of length T = integer code, bit t (0-based) = 1 iff step t+1 is LEFT.
Site after t steps = t - 2*lambda_t mod N.  Rail after last step: L iff last step left.
Start (0,R).  Groups: tuples, componentwise addition mod moduli (written additively).

PREDICATES (fixed before first run):
 CTRL  N=4,T=4, all walks: table n(l) at (0,R) and (0,L).
 F0    for every walk (all codes, T<=Tf) and every gain 4-tuple of the group:
       direct product of arc gains == kappa*g_delta (R end) / kappa*b*delta/d*g_delta (L end),
       kappa=a^(T-2lam)(bc)^lam ; and (a/d)^M == beta^-1 delta^-M ; kappa(lam+M)=kappa(lam)*beta.
 W1p   Lemma W(1): all l with n(l)>0 at a vertex congruent mod M.
 W2p   Lemma W(2) counts: n(l+M)n(l'-M) >= n(l)n(l') for all l<l' occurring-or-not, l'-l in MZ, >=2M.
 W3p   Lemma W(3) counts: n(l+M)(n(l+M)-1) >= n(l)n(l+2M).
 WS    summary: occurring l gap-free AP of difference M; every inner value has n>=2.
 H     for every pair (w,w') at a vertex with l'-l>=2M (hypothesis; count qualifying pairs):
       Ha 0<tau<T ; Hb sites of w,w' at tau equal ; Hc h,h' in S ; Hd h,h' end at y (site and rail) ;
       He lam(h)=l+M, lam(h')=l'-M ; Hf map injective per (vertex,l,l') ; Hg if l'=l+2M then h!=h'.
 X3    search: vertex with exactly three walks at three different lambda (== three cosets when s>=3). Expect none.
 C1    (Cor W1) for gains with s>=3 (hypothesis counted): coset mod <delta> of gain of walk with lam=l0+jM
       == kappa0*beta^j<delta> (times b*delta/d on L); cosets j,j' equal iff s | j-j' (j,j' in 0..2s);
       no vertex with exactly 3 walks in 3 different cosets.
 P     (W2) prefixes: 'L,R' with masks {N-1},{0} and 'N x R' with masks {1..N-1},{0}: number of walks ==1,
       ends (0,R), D_delta gain 1, for N>=3 ; counts recorded for N=1,2 (hypothesis N>=3 not met).
 A     (W2a) for events S' and sites x where walks ending at x are nonempty and share lambda (hypothesis counted):
       Ai (T0-2lam1-x0)/N integer ; Ap after p=(-i mod ord a^N), q=(mu0-lam1 mod ord bc) prefixes:
       walks at site x in bijection, m_S(x,R)=T_k0 m^delta_S'(x,R), m_S(x,L)=T_{k0 b delta/d} m^delta_S'(x,L).
 E     P+ feasibility record (not a predicate of the statement): achieved (|U|,|V|) with common lambda in exhaustive layers.
"""
import sys, time, random, itertools, argparse
from collections import defaultdict, Counter
ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,required=True); ap.add_argument('--out',required=True)
ap.add_argument('--tlim',type=float,default=40.0)
args=ap.parse_args()
out=open(args.out,'x')
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.write(s+'\n'); out.flush()
P('CMD', ' '.join(sys.argv)); rng=random.Random(args.seed)
pc=lambda x: bin(x).count('1')
def Mof(N): return N//(2 if N%2==0 else 1)
def site(c,t,N): return (t-2*pc(c&((1<<t)-1)))%N
def vertex(c,T,N): return (site(c,T,N),(c>>(T-1))&1)   # rail 1 = L
def extend(ev,T,mask,N):
    r=[]
    for c in ev:
        for b in (0,1):
            c2=c|(b<<T)
            if (mask>>site(c2,T+1,N))&1: r.append(c2)
    return r
FAIL=Counter(); CNT=Counter(); OUTL=[]
def fail(k,info):
    FAIL[k]+=1
    if len(OUTL)<60: OUTL.append((k,info))
def analyse(ev,T,N,hyb=True):
    M=Mof(N); S=set(ev); byv=defaultdict(lambda: defaultdict(list))
    for c in ev: byv[vertex(c,T,N)][pc(c)].append(c)
    res=False
    for y,d in byv.items():
        CNT['vertices']+=1
        ls=sorted(d)
        if any((l-ls[0])%M for l in ls): fail('W1p',(N,T,y,ls))
        n=lambda l: len(d.get(l,()))
        if len(ls)>1: res=True
        for l in ls:
            for l2 in ls:
                if l2-l>=2*M and (l2-l)%M==0:
                    CNT['W2p_qual']+=1
                    if n(l+M)*n(l2-M)<n(l)*n(l2): fail('W2p',(N,T,y,l,l2))
            if n(l+2*M)>0:
                CNT['W3p_qual']+=1
                if n(l+M)*(n(l+M)-1)<n(l)*n(l+2*M): fail('W3p',(N,T,y,l))
        if len(ls)>1:
            CNT['WS_qual']+=1
            if ls!=list(range(ls[0],ls[-1]+1,M)): fail('WS_gap',(N,T,y,ls))
            if any(n(l)<2 for l in ls[1:-1]): fail('WS_inner',(N,T,y,ls))
        if sum(map(len,d.values()))==3 and len(ls)==3: fail('X3',(N,T,y,ls,sorted(ev)))
        if not hyb: continue
        for l in ls:
            for l2 in ls:
                if not(l2-l>=2*M): continue
                img=set(); npairs=0
                for w in d[l]:
                    for w2 in d[l2]:
                        npairs+=1; CNT['H_pairs']+=1; CNT['H_pairs_N%d'%N]+=1; CNT['H_pairs_N%d_exact2M'%N]+=(l2==l+2*M)
                        tau=None
                        for t in range(T+1):
                            lo=(1<<t)-1
                            if pc(w2&lo)-pc(w&lo)==M: tau=t;break
                        if tau is None or not(0<tau<T): fail('Ha',(N,T,w,w2,tau)); continue
                        CNT['tau=%s'%('1' if tau==1 else ('T-1' if tau==T-1 else 'mid'))]+=1
                        if site(w,tau,N)!=site(w2,tau,N): fail('Hb',(N,T,w,w2,tau))
                        lo=(1<<tau)-1; h=(w2&lo)|(w&~lo); h2=(w&lo)|(w2&~lo)
                        if h not in S or h2 not in S: fail('Hc',(N,T,w,w2,tau))
                        if vertex(h,T,N)!=y or vertex(h2,T,N)!=y: fail('Hd',(N,T,w,w2,tau))
                        if pc(h)!=l+M or pc(h2)!=l2-M: fail('He',(N,T,w,w2,tau))
                        if l2==l+2*M:
                            CNT['Hg_qual']+=1
                            if h==h2: fail('Hg',(N,T,w,w2,tau))
                        if (w&lo)==(w2&lo): CNT['shared_prefix_to_tau']+=1
                        k=1
                        while k<T and ((w>>(k-1))&1)==((w2>>(k-1))&1): k+=1
                        if k>1: CNT['pairs_sharing_first_step']+=1
                        img.add((h,h2))
                if len(img)!=npairs: fail('Hf',(N,T,y,l,l2,npairs,len(img)))
    return res
# ---------------- CTRL
ev=[0]; 
for t in range(4): ev=extend(ev,t,15,4)
for y in ((0,0),(0,1)):
    P('CTRL N=4 T=4 vertex (0,%s):'%'RL'[y[1]], dict(sorted(Counter(pc(c) for c in ev if vertex(c,4,4)==y).items())))
# ---------------- Lemma W exhaustive layers
SAMPLES=defaultdict(list); PPLUS=defaultdict(set)
TMAX={1:13,2:12,3:8,4:7,5:6,6:5,7:4}
for N in range(1,8):
    t0=time.time(); layer={frozenset([0]):[0]}; done=0; nev=0
    for T in range(1,TMAX[N]+1):
        new={}; trunc=False
        for ev in layer.values():
            for mask in range(1,1<<N):
                e=extend(ev,T-1,mask,N)
                if not e: continue
                k=frozenset(e)
                if k not in new: new[k]=e
            if time.time()-t0>args.tlim: trunc=True;break
        if trunc: break
        for e in new.values():
            if time.time()-t0>3*args.tlim: trunc=True;break
            multi=analyse(e,T,N); nev+=1
            if multi and len(SAMPLES[N])<400: SAMPLES[N].append((T,e))
            bs=defaultdict(lambda:[set(),0,0])
            for c in e:
                x,r=vertex(c,T,N); bs[x][0].add(pc(c)); bs[x][1+r]+=1
            for x,(ls,u,v) in bs.items():
                if len(ls)==1: PPLUS[N].add((u,v))
        if trunc: break
        layer=new; done=T
    P('EXH N=%d: all mask sequences (nonempty masks) complete to T=%d, distinct events analysed=%d (layer T=%d %s)'%(N,done,nev,done+1,'TRUNCATED by time, partial layer discarded/partly analysed' if done<TMAX[N] else 'n/a'))
P('after EXH: CNT',dict(CNT)); P('after EXH: FAIL',dict(FAIL))
# ---------------- random dense events, longer T
for N,T in ((3,11),(3,12),(4,10),(5,12),(6,11),(7,13),(8,12),(2,12),(1,12)):
    for rep in range(6):
        p=rng.choice([0.6,0.8,0.9,1.0]); ev=[0]
        for t in range(T):
            mask=sum(1<<x for x in range(N) if rng.random()<p) or (1<<rng.randrange(N))
            ev=extend(ev,t,mask,N)
        CNT['rand_events']+=1
        if not ev: CNT['rand_empty']+=1; continue
        big=len(ev)>1500
        multi=analyse(ev,T,N,hyb=not big)
        if big: CNT['rand_hyb_skipped_big']+=1
        if multi and len(ev)<600 and len(SAMPLES[N])<460: SAMPLES[N].append((T,ev))
P('after RAND: CNT',dict(CNT)); P('after RAND: FAIL',dict(FAIL))
for N in sorted(PPLUS):
    s=PPLUS[N]; P('E N=%d achieved (|U|,|V|) with common lambda at a site, entries<=4:'%N, sorted(t for t in s if max(t)<=4))
# ---------------- group utilities
class G:
    def __init__(s,mods): s.m=mods; s.e=tuple(0 for _ in mods); s.elts=list(itertools.product(*[range(k) for k in mods]))
    def mul(s,x,y): return tuple((a+b)%k for a,b,k in zip(x,y,s.m))
    def pw(s,x,n): return tuple((a*n)%k for a,k in zip(x,s.m))
    def inv(s,x): return s.pw(x,-1)
    def gen(s,gs):
        H={s.e}; fr=[s.e]
        while fr:
            x=fr.pop()
            for g in gs:
                y=s.mul(x,g)
                if y not in H: H.add(y); fr.append(y)
        return frozenset(H)
    def order(s,x):
        n=1; y=x
        while y!=s.e: y=s.mul(y,x); n+=1
        return n
def gain(Gp,c,T,ab):
    a,b,cc,d=ab; g=Gp.e; rail=0
    for t in range(T):
        st=(c>>t)&1; g=Gp.mul(g,(a,b,cc,d)[2*rail+st]); rail=st
    return g
def derived(Gp,ab,N):
    a,b,c,d=ab; bc=Gp.mul(b,c); delta=Gp.mul(Gp.mul(a,d),Gp.inv(bc)); M=Mof(N)
    B=Gp.mul(bc,Gp.pw(a,-2)); beta=Gp.pw(B,M); D=Gp.gen([delta]); s=1
    while Gp.pw(beta,s) not in D: s+=1
    return bc,delta,B,beta,D,s
# ---------------- F0
for mods,Tf in (((4,),9),((6,),7),((2,3),7),((2,2),7)):
    Gp=G(mods); nw=0
    for ab in itertools.product(Gp.elts,repeat=4):
        a,b,c,d=ab; bc=Gp.mul(b,c); delta=Gp.mul(Gp.mul(a,d),Gp.inv(bc)); bdd=Gp.mul(Gp.mul(b,delta),Gp.inv(d))
        abd=(Gp.e,Gp.e,Gp.e,delta)
        for N in range(1,9):
            M=Mof(N); B=Gp.mul(bc,Gp.pw(a,-2)); beta=Gp.pw(B,M)
            if Gp.pw(Gp.mul(a,Gp.inv(d)),M)!=Gp.mul(Gp.inv(beta),Gp.pw(delta,-M)): fail('F0_adM',(mods,ab,N))
            if Gp.gen([delta,Gp.pw(Gp.mul(a,Gp.inv(d)),M)])!=Gp.gen([delta,beta]): fail('F0_DeltaN',(mods,ab,N))
        for T in range(1,Tf+1):
            for cde in range(1<<T):
                lam=pc(cde); kap=Gp.mul(Gp.pw(a,T-2*lam),Gp.pw(bc,lam)); gd=gain(Gp,cde,T,abd)
                pred=Gp.mul(kap,gd) if not (cde>>(T-1))&1 else Gp.mul(Gp.mul(kap,bdd),gd)
                nw+=1
                if gain(Gp,cde,T,ab)!=pred: fail('F0',(mods,ab,T,cde))
    P('F0 group Z%s: all %d gain 4-tuples, all walks T<=%d, walk-gain comparisons=%d (independent of ring/line: gain depends on step sequence only); identities for N=1..8'%(mods,len(Gp.elts)**4,Tf,nw))
P('after F0: FAIL',dict(FAIL))
# ---------------- C1
for mods in ((7,),(12,),(9,),(2,8),(3,3)):
    Gp=G(mods); tried=0; qual=0; svals=Counter()
    for rep in range(400):
        ab=tuple(rng.choice(Gp.elts) for _ in range(4)); N=rng.choice([n for n in SAMPLES if SAMPLES[n]])
        bc,delta,B,beta,D,s=derived(Gp,ab,N); tried+=1; svals[s]+=1
        for j in range(2*s+1):
            for j2 in range(2*s+1):
                if (Gp.pw(beta,j-j2) in D)!=((j-j2)%s==0): fail('C1_cosetiff',(mods,ab,N,j,j2))
        if s<3: continue
        qual+=1; a,b,c,d=ab; M=Mof(N); bdd=Gp.mul(Gp.mul(b,delta),Gp.inv(d))
        for T,ev in rng.sample(SAMPLES[N],min(25,len(SAMPLES[N]))):
            byv=defaultdict(list)
            for w in ev: byv[vertex(w,T,N)].append(w)
            for y,ws in byv.items():
                l0=min(pc(w) for w in ws); k0=Gp.mul(Gp.pw(a,T-2*l0),Gp.pw(bc,l0))
                if y[1]: k0=Gp.mul(k0,bdd)
                cos=set()
                for w in ws:
                    j=(pc(w)-l0)//M; g=gain(Gp,w,T,ab)
                    if Gp.mul(g,Gp.inv(Gp.mul(k0,Gp.pw(beta,j)))) not in D: fail('C1_coset',(mods,ab,N,T,y,w))
                    cos.add(frozenset(Gp.mul(g,x) for x in D))
                CNT['C1_vertices']+=1
                if len(cos)>=3: CNT['C1_vertices_3+cosets_rail%s'%'RL'[y[1]]]+=1
                if len(ws)==3 and len(cos)==3: fail('C1_three',(mods,ab,N,T,y,ws))
    P('C1 group Z%s: gain tuples tried=%d, with s>=3 (qualify)=%d, s histogram=%s'%(mods,tried,qual,dict(sorted(svals.items()))))
P('after C1: CNT',{k:v for k,v in CNT.items() if k.startswith('C1')}); P('after C1: FAIL',dict(FAIL))
# ---------------- P prefixes
def run_masks(masks,N,start=None):
    ev=[0] if start is None else start
    for t,m in enumerate(masks): ev=extend(ev,t,m,N)
    return ev
def pre1(N): return [1<<((N-1)%N),1]
def pre2(N): return [1<<(k%N) for k in range(1,N+1)]
G1=G((1,))
for N in range(1,10):
    for name,pm in (('LR',pre1(N)),('N*R',pre2(N))):
        ev=run_masks(pm,N); T=len(pm)
        ok=len(ev)==1 and vertex(ev[0],T,N)==(0,0) and all(((ev[0]>>t)&3)!=3 for t in range(T-1))  # no LL arc => D_delta gain 1
        P('P N=%d prefix %s: walks=%d %s -> %s'%(N,name,len(ev),[bin(c)[2:].zfill(T)[::-1] for c in ev][:4],'single,(0,R),gain1' if ok else 'NOT single'))
        if N>=3 and not ok: fail('P',(N,name))
# ---------------- A  (W2a end to end)
negi=0
for mods in ((6,),(2,3),(4,),(12,),(3,3)):
    Gp=G(mods); cases=0; qual=0
    for rep in range(250):
        N=rng.randrange(3,9); T0=rng.randrange(1,10); masks=[]
        for t in range(T0):
            masks.append(sum(1<<x for x in range(N) if rng.random()<rng.choice([0.4,0.7,1.0])) or 1)
        ev=run_masks(masks,N); bys=defaultdict(list)
        for w in ev: bys[site(w,T0,N)].append(w)
        ab=tuple(rng.choice(Gp.elts) for _ in range(4)); a,b,c,d=ab
        bc,delta,B,beta,D,s=derived(Gp,ab,N); bdd=Gp.mul(Gp.mul(b,delta),Gp.inv(d)); abd=(Gp.e,Gp.e,Gp.e,delta)
        for x,ws in bys.items():
            cases+=1
            if len({pc(w) for w in ws})!=1: CNT['A_notqual_mixed_lambda']+=1; continue
            qual+=1; lam1=pc(ws[0]); x0=x+N*rng.randrange(0,4); mu0=rng.randrange(0,7)
            k0=Gp.mul(Gp.pw(a,x0),Gp.pw(bc,mu0))
            if (T0-2*lam1-x0)%N: fail('Ai',(N,T0,x,x0,lam1)); continue
            i=(T0-2*lam1-x0)//N; negi+= i<0
            p=(-i)%Gp.order(Gp.pw(a,N)); q=(mu0-lam1)%Gp.order(bc)
            full=pre1(N)*q+pre2(N)*p+masks; Tn=len(full); sh=2*q+N*p
            ev2=[w for w in run_masks(full,N) if site(w,Tn,N)==x]
            if sorted(w>>sh for w in ev2)!=sorted(ws) or len(ev2)!=len(ws): fail('Ap_bij',(mods,ab,N,masks,x,p,q)); continue
            for rail in (0,1):
                tr=k0 if rail==0 else Gp.mul(k0,bdd)
                tgt=Counter(Gp.mul(tr,gain(Gp,w,T0,abd)) for w in ws if (w>>(T0-1))&1==rail)
                got=Counter(gain(Gp,w,Tn,ab) for w in ev2 if (w>>(Tn-1))&1==rail)
                if tgt!=got: fail('Ap_multiset',(mods,ab,N,masks,x,p,q,rail))
                if any(Gp.mul(g,Gp.inv(tr)) not in D for g in got): fail('Ap_coset',(mods,ab,N,x))
    P('A group Z%s: (event,site) cases=%d, qualifying (common lambda)=%d'%(mods,cases,qual))
P('A: cases with negative i =',negi)
P('FINAL CNT',dict(CNT)); P('FINAL FAIL (kept, all predicates that failed)',dict(FAIL))
for o in OUTL: P('OUTLIER',o)
P('END')
