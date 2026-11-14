"""Challenger program for two_rail_start FINDINGS.md and RAIL_WEIGHT.md. Written from the definitions only.
Exact arithmetic in Z[zeta_12] (basis 1,x,x^2,x^3 mod x^4-x^2+1), integer starts (unnormalised; formulas are
used in their homogeneous form with n=|alpha|^2+|beta|^2). Seed 20261115. Result file never overwritten.
Convention: a datum = (N, start (alpha,beta), exponents (ea,eb,ec,ed) of chi on the gains, chi(g)=zeta^e).
Probabilities compared WITHOUT the common factor 2^-t (same t on both sides).
Signature of a datum = sha256 over all port values |amp|^2 at every (tick, site, rail) of: every mask sequence
(exhaustive, nonempty subsets of Z/N) up to length TEX[N]; the named events of B1,B2,B3, rail weight; RND random
mask sequences of length 2D+3 (fixed per N). Equal digests are taken as equal statistics (collision ignored).

PREDICATES (fixed before first run)
L0   Lemma 0 as an identity in the free abelian group Z^4 on a,b,c,d: every word of length 1..7 from rail L.
X0   simulator against brute word enumeration with individual arc gains (random masks). must agree.
RW1  eta=-1, N=3..12 and line: unmasked P(3,1,R) = |alpha|^2/2 (brute words).   RW2: P(3,-1,L) = |beta|^2/2.
RWc  control eta=+1: RW1 as a universal statement, expected to fail.
RW12 N=1,2, eta=-1: 8P(3,1 mod N,R) = |alpha(1+2u-u^2)+beta gamma(1+u^2)|^2 (my own derivation), and count how
     often it equals |alpha|^2/2 (statement excludes N=1,2; expected to differ).
A1   same N, eta in {+1,-1}: equal Q=(|a|^2,|b|^2,eta,Re w,Re k,Im w Im k) => equal signature.
B1   eta=-1,N>=3: 2P(1,1,R) = n+2Re k ; 2P(1,-1,L) = n-2Re k.
B2a  2^(D+2) P(read well D+2) = (n+2Re k)(2+2s Re w).   B2b mirror with (n-2Re k), read well -D-2.
B2c  for start != 0, at least one of n+2Re k, n-2Re k is nonzero (count cases with exactly one zero).
B3   2^(D+1) P(fork, well D+1) = 2n + 2s(|a|^2-|b|^2)Re w + 4s Im w Im k.
IFF1 eta=-1,N>=3: equal five (|a|^2,|b|^2,Re w,Re k,Im w Im k) => equal signature.
IFF2 different five => different signature.
K1   control: four-tuple without Im w Im k determines signature (expected to fail).
K2   control: (Re w,Re k,Im w Im k) without the weights determines signature (expected to fail).
K3   control: equal signature => equal gamma (expected to fail).  K4: => equal omega (expected to fail).
C    eta=-1,N>=3: sig(chi)=sig(conj chi)  iff  Im(conj(alpha)beta)=0 or (gamma=+-1 and omega=+-1). both directions,
     with counts at the boundaries gamma=+-1, omega=+-1.
D1   sharp start (0,R), eta=+-1, N>=1 and line: the list over all visited (mask history, tick, site) of
     (|psi_R|^2,|psi_L|^2, conj(psi_R) psi_L gamma) is the same for data with equal (eta,omega) (gamma, u differ).
D2   that list for omega is the conjugate of the list for conj omega.
D3   count of non-real kappa' (information).
D4   unstated direction: sharp-start signature (all events, several sites retained, wrapping, both rails read)
     is a function of (eta, Re omega) alone; in particular independent of gamma.
LINE line, eta=+-1: equal (|a|^2,|b|^2,eta,Re k) => equal signature (masks exhaustive over reachable sites, T=4).
"""
import sys, os, json, random, hashlib, itertools
from collections import defaultdict
random.seed(20261115)
OUT='chal_result.json'
if os.path.exists(OUT): print('refuse to overwrite'); sys.exit(3)
def mul(p,q):
    r=[0]*7
    for i in range(4):
        if p[i]:
            for j in range(4): r[i+j]+=p[i]*q[j]
    # x^4=x^2-1, x^5=x^3-x, x^6=-1
    return (r[0]-r[4]-r[6], r[1]-r[5], r[2]+r[4], r[3]+r[5])
ONE=(1,0,0,0); ZERO=(0,0,0,0)
Z=[ONE]
for k in range(11): Z.append(mul(Z[-1],(0,1,0,0)))
def add(p,q): return tuple(x+y for x,y in zip(p,q))
def sub(p,q): return tuple(x-y for x,y in zip(p,q))
def sc(c,p): return tuple(c*x for x in p)
def conj(p):
    r=ZERO
    for i in range(4): r=add(r,sc(p[i],Z[(-i)%12]))
    return r
def nrm(p): return mul(p,conj(p))
def re2(p): return add(p,conj(p))           # 2 Re
def im2i(p): return sub(p,conj(p))          # 2 i Im
def el(c,k): return sc(c,Z[k%12])
ARC={('R','R'):0,('R','L'):1,('L','R'):2,('L','L'):3}
def step(st,N,e):
    new={}
    for (x,r),amp in st.items():
        for s,dx in (('R',1),('L',-1)):
            y=x+dx if N is None else (x+dx)%N
            v=mul(amp,Z[e[ARC[(r,s)]]%12])
            if (y,s) in new: new[(y,s)]=add(new[(y,s)],v)
            else: new[(y,s)]=v
    return new
def mask(st,S): return {k:v for k,v in st.items() if k[0] in S}
def start_state(al,be):
    st={}
    if al!=ZERO: st[(0,'R')]=al
    if be!=ZERO: st[(0,'L')]=be
    return st
def run(N,al,be,e,masks):
    """returns list of states after each tick (after masking)"""
    st=start_state(al,be); out=[]
    for S in masks:
        st=step(st,N,e)
        if S is not None: st=mask(st,S)
        out.append(st)
    return out
def P(st,x,r): return nrm(st.get((x,r),ZERO))
def wellP(st,x): return add(P(st,x,'R'),P(st,x,'L'))
def brute(N,al,be,e,masks,port):
    t=len(masks); tot=ZERO
    for r0,c in (('R',al),('L',be)):
        for w in itertools.product('RL',repeat=t):
            x=0;prev=r0;ex=0;ok=True
            for j,s in enumerate(w):
                ex+=e[ARC[(prev,s)]]; x+=1 if s=='R' else -1; prev=s
                xx=x if N is None else x%N
                if masks[j] is not None and xx not in masks[j]: ok=False;break
            if ok and (xx,prev)==port: tot=add(tot,mul(c,Z[ex%12]))
    return nrm(tot)
def subsets(sites):
    out=[]
    for m in range(1,1<<len(sites)): out.append(frozenset(s for i,s in enumerate(sites) if m>>i&1))
    return out
def Dof(N): return N//(2 if N%2==0 else 1)
TEX={1:5,2:5,3:4,4:3,5:2,6:2,7:2,8:2}
RND=12
def fork(N):
    D=Dof(N); return [frozenset({j%N,(-j)%N}) for j in range(1,D)]+[frozenset({D%N}),frozenset({(D+1)%N})]
def fork_t(N):
    D=Dof(N); return [frozenset({1})]+[frozenset({(1+j)%N,(1-j)%N}) for j in range(1,D)]+[frozenset({(1+D)%N}),frozenset({(D+2)%N})]
def fork_m(N):
    D=Dof(N); return [frozenset({(-1)%N})]+[frozenset({(-1-j)%N,(-1+j)%N}) for j in range(1,D)]+[frozenset({(-1-D)%N}),frozenset({(-D-2)%N})]
RNDEV={}
def rnd_events(N):
    if N not in RNDEV:
        D=Dof(N); ev=[]
        for _ in range(RND):
            m=[]
            for j in range(2*D+3):
                S=frozenset(x for x in range(N) if random.random()<0.7) or frozenset({random.randrange(N)})
                m.append(S)
            ev.append(m)
        RNDEV[N]=ev
    return RNDEV[N]
def signature(N,al,be,e,collect=False):
    h=hashlib.sha256(); hd=hashlib.sha256(); hdc=hashlib.sha256(); nonreal=0; nsite=0
    gam=Z[(e[2]-e[0])%12]
    def rec(st):
        nonlocal nonreal,nsite
        sites=sorted(set(k[0] for k in st))
        for x in sites:
            pr=st.get((x,'R'),ZERO); pl=st.get((x,'L'),ZERO)
            h.update(repr((x,nrm(pr),nrm(pl))).encode())
            if collect:
                kp=mul(mul(conj(pr),pl),gam); v=(x,nrm(pr),nrm(pl),kp)
                hd.update(repr(v).encode()); hdc.update(repr((x,nrm(pr),nrm(pl),conj(kp))).encode())
                nsite+=1
                if kp!=conj(kp): nonreal+=1
        h.update(b'|'); hd.update(b'|'); hdc.update(b'|')
    def dfs(st,t,T):
        if t==T: return
        st2=step(st,N,e)
        if N is None: allm=subsets(sorted(set(k[0] for k in st2))) if st2 else []
        else: allm=SUBS[N]
        for S in allm:
            s3=mask(st2,S); rec(s3)
            if s3: dfs(s3,t+1,T)
            else: h.update(b'0')
    st0=start_state(al,be)
    dfs(st0,0,4 if N is None else TEX[N])
    if N is not None:
        evs=[[None]*3]
        if N>=3: evs+= [fork(N),fork_t(N),fork_m(N)]
        evs+=rnd_events(N)
        for m in evs:
            for st in run(N,al,be,e,m): rec(st)
            h.update(b'#'); hd.update(b'#'); hdc.update(b'#')
    return h.hexdigest(),hd.hexdigest(),hdc.hexdigest(),nonreal,nsite
SUBS={N:subsets(list(range(N))) for N in range(1,9)}
RES={}; 
def pred(name,q,p,f,ex=None,note=''):
    RES[name]={'qualify':q,'pass':p,'fail':f,'examples':(ex or [])[:5],'note':note}
    print(name,q,p,f,note,(ex or [])[:2]); sys.stdout.flush()
    with open('NOTES.md','a') as fh: fh.write('  %s qualify=%d pass=%d fail=%d %s %s\n'%(name,q,p,f,note,(ex or [])[:2]))
# ---------- L0 (free abelian group) ----------
def vec(i): v=[0,0,0,0]; v[i]=1; return v
q=p=0; ex=[]
for t in range(1,8):
    for w in itertools.product('RL',repeat=t):
        g=[0,0,0,0]; prev='L'; l=0; m=0
        for s in w:
            g[ARC[(prev,s)]]+=1
            if s=='L': l+=1
            if prev=='L' and s=='L': m+=1
            prev=s
        e_=1 if prev=='L' else 0
        # (c/a) a^t (a/c)^e B^l H^m ; B=bc/a^2 ; H=ad/(bc)
        f=[ -1+t+e_-2*l+m, l-m, 1-e_+l-m, m]
        q+=1
        if f==g: p+=1
        else: ex.append(''.join(w))
pred('L0',q,p,q-p,ex)
# ---------- starts and characters ----------
def E(c,k): return el(c,k)
STARTS=[(E(1,0),ZERO),(ZERO,E(1,0)),(E(1,0),E(1,0)),(E(1,0),E(-1,0)),(E(1,0),E(1,3)),(E(1,0),E(-1,3)),
        (E(3,0),E(4,3)),(E(4,0),E(3,3)),(E(3,0),E(4,0)),(E(1,0),E(1,1)),(E(2,0),E(1,5)),(E(4,3),E(3,0)),
        (E(5,0),ZERO),(ZERO,E(5,0)),(E(3,1),E(4,4)),(E(1,0),E(1,2)),(E(3,0),E(-4,0)),(E(4,0),E(3,9))]
def rand_group_char():
    k=random.randint(1,3); orders=[random.choice([2,3,4,6,12]) for _ in range(k)]
    gains=[[random.randrange(n) for n in orders] for _ in range(4)]
    ch=[random.randrange(n) for n in orders]
    e=tuple(sum(12//n*r*g for n,r,g in zip(orders,ch,gg))%12 for gg in gains)
    return e,orders
def chars(structured_b):
    out={}; drawn=0; ncy=0
    for eb in structured_b:
        for ec in range(12):
            out[(0,eb,ec,(6+eb+ec)%12)]=1
    for eb in (0,1,3,4):
        for ec in (0,2,3,6): out[(0,eb,ec,(eb+ec)%12)]=1        # eta=+1
    for _ in range(400):
        e,orders=rand_group_char(); drawn+=1
        if (e[0]+e[3]-e[1]-e[2])%12 in (0,6):
            out[e]=1
            if len(orders)>1: ncy+=1
    return list(out),drawn,ncy
def inv(N,al,be,e):
    eta=Z[(e[0]+e[3]-e[1]-e[2])%12]
    if N is None: w=ONE; D=None
    else: D=Dof(N); w=Z[((e[1]+e[2]-2*e[0])*D)%12]
    gam=Z[(e[2]-e[0])%12]; k=mul(mul(conj(al),be),gam)
    A=nrm(al); B=nrm(be)
    imim=sc(-1,mul(im2i(w),im2i(k)))    # 4 Im w Im k
    return dict(A=A,B=B,eta=eta,rw=re2(w),rk=re2(k),imim=imim,w=w,gam=gam,k=k,D=D)
MONE=sc(-1,ONE)
# ---------- X0 ----------
q=p=0; ex=[]
for _ in range(300):
    N=random.choice([1,2,3,4,5,6,None]); e=tuple(random.randrange(12) for _ in range(4)); al,be=random.choice(STARTS)
    t=random.randint(1,6)
    if N is None: ms=[frozenset(x for x in range(-j,j+1) if random.random()<0.75) for j in range(1,t+1)]
    else: ms=[frozenset(x for x in range(N) if random.random()<0.75) for j in range(t)]
    st=run(N,al,be,e,ms)[-1]
    xs=range(-t,t+1) if N is None else range(N)
    for x in xs:
        for r in 'RL':
            q+=1
            if P(st,x,r)==brute(N,al,be,e,ms,(x,r)): p+=1
            else: ex.append((N,e,t))
pred('X0',q,p,q-p,ex)
# ---------- rail weight ----------
allch=[(ea,eb,ec,ed) for ea in (0,1,4) for eb in range(12) for ec in range(12) for ed in range(12)]
cnt=defaultdict(lambda:[0,0,0,[]]); rw12vals=[]
for N in [1,2,3,4,5,6,7,8,9,10,11,12,None]:
    for e in allch:
        h=(e[0]+e[3]-e[1]-e[2])%12
        if h not in (0,6): continue
        for al,be in STARTS[:10]:
            ms=[None]*3
            pR=brute(N,al,be,e,ms,(1 if N is None else 1%N,'R')); pL=brute(N,al,be,e,ms,(-1 if N is None else (-1)%N,'L'))
            A=nrm(al); B=nrm(be)
            if N in (1,2):
                if h==6:
                    u=Z[(e[1]+e[2]-2*e[0])%12]; g=Z[(e[2]-e[0])%12]; u2=mul(u,u)
                    f=add(mul(al,sub(add(ONE,sc(2,u)),u2)),mul(mul(be,g),add(ONE,u2)))
                    c=cnt['RW12_formula']; c[0]+=1; c[1 if pR==nrm(f) else 2]+=1
                    c=cnt['RW12_equals_alpha2_over_2']; c[0]+=1
                    if pR==sc(4,A): c[1]+=1
                    else:
                        c[2]+=1
                        if len(c[3])<3: c[3].append((N,e,al,be,'8P=',pR,'4|a|^2=',sc(4,A)))
                    c=cnt['RW12L_equals_beta2_over_2']; c[0]+=1; c[1 if pL==sc(4,B) else 2]+=1
                continue
            key='' if h==6 else 'c'
            for nm,val,tgt in (('RW1',pR,A),('RW2',pL,B)):
                c=cnt[nm+key+('_N%s'%N if h==6 and N in (3,4,None) else '')]; c[0]+=1
                if val==sc(4,tgt): c[1]+=1      # 8P = 4|alpha|^2
                else:
                    c[2]+=1
                    if len(c[3])<3: c[3].append((N,e,al,be))
                if h==6 and N in (3,4,None):
                    c=cnt[nm]; c[0]+=1; c[1 if val==sc(4,tgt) else 2]+=1
for k in sorted(cnt): pred(k,cnt[k][0],cnt[k][1],cnt[k][2],cnt[k][3],'N=3..12 and line; chi values all 12th roots, chi(a) in {1,z,z^4}' if k in('RW1','RW2') else '')
# ---------- main ----------
def classes(data,keyf,sigf):
    """returns (#pairs with equal key, of which equal sig), (#pairs different key, of which different sig), examples"""
    bykey=defaultdict(list)
    for d in data: bykey[keyf(d)].append(d)
    eqk=eqk_ok=0; bad=[]
    for k,L in bykey.items():
        c=defaultdict(int)
        for d in L: c[sigf(d)]+=1
        n=len(L); eqk+=n*(n-1)//2; eqk_ok+=sum(v*(v-1)//2 for v in c.values())
        if len(c)>1 and len(bad)<3:
            s=list({sigf(d):d for d in L}.values())[:2]; bad.append([x['id'] for x in s])
    n=len(data); tot=n*(n-1)//2
    bysig=defaultdict(list)
    for d in data: bysig[sigf(d)].append(d)
    eqs=sum(len(L)*(len(L)-1)//2 for L in bysig.values())
    # pairs different key & equal sig = eqs - eqk_ok
    dk=tot-eqk; dk_bad=eqs-eqk_ok; bad2=[]
    if dk_bad:
        for s,L in bysig.items():
            ks={}
            for d in L: ks.setdefault(keyf(d),d)
            if len(ks)>1 and len(bad2)<3: bad2.append([x['id'] for x in list(ks.values())[:2]])
    return eqk,eqk_ok,bad,dk,dk-dk_bad,bad2
agg=defaultdict(lambda:[0,0,0,[]])
def acc(name,q,p,ex=None):
    a=agg[name]; a[0]+=q; a[1]+=p; a[2]+=q-p
    if ex: a[3]+=ex
drawn_tot=0; qual={'eta-1':0,'eta+1':0,'noncyclic_random':0}
for N in [3,4,5,6,7,8,1,2,None]:
    Nn=N if N is not None else 0
    chs,drawn,ncy=chars(range(12) if Nn in (3,4) else (0,1,2,3,4,6,9))
    drawn_tot+=drawn; qual['noncyclic_random']+=ncy
    data=[]
    for e in chs:
        for si,(al,be) in enumerate(STARTS):
            if N in (1,2,None) and si not in (0,2,4,6,9): continue
            iv=inv(N,al,be,e); sharp=(si==0)
            sg=signature(N,al,be,e,collect=sharp)
            d=dict(id=(N,e,si),N=N,e=e,si=si,al=al,be=be,sig=sg[0],**iv)
            if sharp: d.update(hd=sg[1],hdc=sg[2],nonreal=sg[3],nsite=sg[4])
            data.append(d)
    m1=[d for d in data if d['eta']==MONE]; p1=[d for d in data if d['eta']==ONE]
    qual['eta-1']+=len(m1); qual['eta+1']+=len(p1)
    with open('NOTES.md','a') as fh: fh.write(' N=%s data=%d eta-1=%d eta+1=%d\n'%(N,len(data),len(m1),len(p1)))
    Q=lambda d:(d['A'],d['B'],d['eta'],d['rw'],d['rk'],d['imim'])
    five=lambda d:(d['A'],d['B'],d['rw'],d['rk'],d['imim'])
    sig=lambda d:d['sig']
    if N is None:
        r=classes(data,lambda d:(d['A'],d['B'],d['eta'],d['rk']),sig); acc('LINE',r[0],r[1],r[2])
        r=classes(m1,lambda d:(d['A'],d['B'],d['rk']),sig); acc('LINE_converse_eta-1 (not claimed; information)',r[3],r[4],r[5])
    else:
        r=classes(data,Q,sig); acc('A1' if Nn>=3 else 'A1_N12',r[0],r[1],r[2])
    if Nn>=3:
        r=classes(m1,five,sig); acc('IFF1',r[0],r[1],r[2]); acc('IFF2',r[3],r[4],r[5])
        r=classes(m1,lambda d:(d['A'],d['B'],d['rw'],d['rk']),sig); acc('K1',r[0],r[1],r[2])
        r=classes(m1,lambda d:(d['rw'],d['rk'],d['imim']),sig); acc('K2',r[0],r[1],r[2])
        r=classes(m1,sig,lambda d:d['gam']); acc('K3',r[0],r[1],r[2])
        r=classes(m1,sig,lambda d:d['w']); acc('K4',r[0],r[1],r[2])
        # degenerate sub-searches for IFF2
        for nm,sel in (('IFF_sub_alpha0_or_beta0',lambda d:d['A']==ZERO or d['B']==ZERO),
                       ('IFF_sub_omega_pm1',lambda d:d['w'] in (ONE,MONE)),
                       ('IFF_sub_|2Re k|=n',lambda d:d['rk'] in (add(d['A'],d['B']),sc(-1,add(d['A'],d['B'])))),
                       ('IFF_sub_Im_omega0_Im_kappa_differs',lambda d:d['w'] in (ONE,MONE) and im2i(d['k'])!=ZERO)):
            sub_=[d for d in m1 if sel(d)]
            r=classes(sub_,five,sig); acc(nm+'_eq',r[0],r[1],r[2]); acc(nm+'_ne',r[3],r[4],r[5])
        D=Dof(N); s=1 if (D-1)%2==0 else -1
        bysig={d['id']:d for d in m1}
        for d in m1:
            al,be,e=d['al'],d['be'],d['e']; n=add(d['A'],d['B']); twos=add(sc(2,ONE),sc(s,d['rw']))
            st=run(N,al,be,e,[None]); 
            acc('B1',1,int(sc(2,P(st[0],1,'R'))==add(n,d['rk']) and sc(2,P(st[0],N-1,'L'))==sub(n,d['rk'])),[d['id']])
            if sc(2,P(st[0],1,'R'))!=add(n,d['rk']) or sc(2,P(st[0],N-1,'L'))!=sub(n,d['rk']): pass
            else: agg['B1'][3].pop()
            # also well = port at tick 1
            acc('B1_well_equals_port',1,int(wellP(st[0],1)==P(st[0],1,'R') and wellP(st[0],N-1)==P(st[0],N-1,'L')))
            st=run(N,al,be,e,fork_t(N)); ok=sc(2,wellP(st[-1],(D+2)%N))==mul(add(n,d['rk']),twos)
            acc('B2a',1,int(ok),None if ok else [d['id']])
            st=run(N,al,be,e,fork_m(N)); ok=sc(2,wellP(st[-1],(-D-2)%N))==mul(sub(n,d['rk']),twos)
            acc('B2b',1,int(ok),None if ok else [d['id']])
            z1=add(n,d['rk'])==ZERO; z2=sub(n,d['rk'])==ZERO
            acc('B2c',1,int(not(z1 and z2)))
            if z1!=z2: agg['B2c_exactly_one_prefactor_zero (count)'][0]+=1; agg['B2c_exactly_one_prefactor_zero (count)'][1]+=1
            st=run(N,al,be,e,fork(N))
            rhs=add(add(sc(2,n),sc(s,mul(sub(d['A'],d['B']),d['rw'])) ), sc(s,d['imim']))
            # 2*[2n + 2s(A-B)Re w + 4 s Im w Im k] = 4n + 2s(A-B)(2Re w) + 2s(4ImIm) ; compare 2*P
            rhs2=add(add(sc(4,n),sc(2*s,mul(sub(d['A'],d['B']),d['rw']))),sc(2*s,d['imim']))
            ok=sc(2,wellP(st[-1],(D+1)%N))==rhs2
            acc('B3',1,int(ok),None if ok else [d['id']])
            # Corollary C
            ec=tuple((-x)%12 for x in e)
            sgc=signature(N,al,be,ec)[0] if (N,ec,d['si']) not in bysig else bysig[(N,ec,d['si'])]['sig']
            same=(sgc==d['sig'])
            cond=(im2i(mul(conj(al),be))==ZERO) or (d['gam'] in (ONE,MONE) and d['w'] in (ONE,MONE))
            acc('C_unreadable_side' if cond else 'C_readable_side',1,int(same==cond),None if same==cond else [d['id']])
            if d['gam'] in (ONE,MONE) or d['w'] in (ONE,MONE): acc('C_boundary(gamma or omega = +-1)',1,int(same==cond))
            if im2i(mul(conj(al),be))!=ZERO and d['gam'] in (ONE,MONE) and d['w'] in (ONE,MONE): acc('C_boundary(complex ratio, gamma=+-1, omega=+-1 -> unreadable)',1,int(same))
            if im2i(mul(conj(al),be))!=ZERO and (d['gam'] in (ONE,MONE)) != (d['w'] in (ONE,MONE)): acc('C_boundary(complex ratio, exactly one of gamma, omega real -> readable)',1,int(not same))
    # Theorem D
    sh=[d for d in data if d['si']==0]
    tag='' if Nn>=3 else ('_N12' if N else '_line')
    r=classes(sh,lambda d:(d['eta'],d['w']),lambda d:d['hd']); acc('D1'+tag,r[0],r[1],r[2])
    r=classes(sh,lambda d:(d['eta'],d['w']),lambda d:d['gam']); agg['D1%s_pairs_same_omega_different_gamma (count)'%tag][0]+=r[0]-r[1]
    byw={}
    for d in sh: byw.setdefault((d['eta'],d['w']),d)
    for (eta,w),d in byw.items():
        if (eta,conj(w)) in byw: acc('D2'+tag,1,int(byw[(eta,conj(w))]['hd']==d['hdc']),[d['id']] if byw[(eta,conj(w))]['hd']!=d['hdc'] else None)
    agg['D3%s_nonreal_kappa_prime (count of site-states)'%tag][0]+=sum(d['nsite'] for d in sh); agg['D3%s_nonreal_kappa_prime (count of site-states)'%tag][1]+=sum(d['nonreal'] for d in sh)
    r=classes(sh,lambda d:(d['eta'],d['rw']),sig); acc('D4'+tag,r[0],r[1],r[2])
    r=classes(sh,lambda d:(d['eta'],d['rw']),lambda d:d['gam']); agg['D4%s_pairs_different_gamma (count)'%tag][0]+=r[0]-r[1]
for k in agg: pred(k,agg[k][0],agg[k][1],agg[k][2],agg[k][3])
RES['_meta']={'seed':20261115,'drawn_random_group_characters':drawn_tot,'qualifying_data':qual,'TEX':{str(k):v for k,v in TEX.items()},'RND':RND,
 'starts':len(STARTS)}
with open(OUT,'x') as fh: json.dump(RES,fh,indent=1,sort_keys=True,default=str)
expected_fail={'RW1c','RW2c','K1','K2','K3','K4','RW12_equals_alpha2_over_2','RW12L_equals_beta2_over_2'}
bad=[k for k,v in RES.items() if k!='_meta' and v['fail'] and k not in expected_fail and 'information' not in k]
print('UNEXPECTED FAILS:',bad)
sys.exit(1 if bad else 0)
