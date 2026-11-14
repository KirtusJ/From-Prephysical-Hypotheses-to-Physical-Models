"""Ring criterion table.  PREDICATES FIXED BEFORE THE FIRST RUN.  Seed 20261113.  Exact integer/cyclotomic arithmetic.

Definitions (from the note): start (0,R); right step -> (x+1,R), left -> (x-1,L) on Z/N; arc gains RR=a, RL=b,
LR=c, LL=d; carrier a=c=1, b=g, d=z g in C2 x Cq (z order 2, g order q); B=bc/a^2, H=ad/(bc); D=N/gcd(N,2).
A character chi is "norm-preserving" iff chi(H)=-1.  An event = masks S_1..S_t (sets of wells retained at each tick).
Port probability = 2^-t |sum_w chi(G(w))|^2 at (t,x,rail); well probability = sum over the two rails.
omega(chi) = chi(B^D).  "Separates" = the two exact probabilities differ.
Groups: C2xC3 (the note's), C2xC4, C2xC12.  N = 1..12 (N=1,2 are boundary rows; the task range is 3..12).

H0  per group: count characters with chi(H)=-1 (computed from H=ad/(bc) in the group); only these are used.
P1  (invariance) for every event evaluated (exhaustive and random), every qualifying pair with
    Re omega0 = Re omega1 has equal probability at every port and every well.
P2  (lower bound) no port or well event of length t <= D separates any qualifying pair.
P3  (fork) for N>=3 the fork (wells {+j,-j} for 1<=j<D, {D}, then well D+1) has well probability
    2^-(D+1) * (2 + 2(-1)^(D-1) Re omega) for every qualifying chi, hence separates a pair iff Re omega differ.
P4  (minimal length) wherever the exhaustive enumeration reaches length D+1 (N>=3), every pair with
    Re omega0 != Re omega1 is separated by a well event of length exactly D+1 and by none shorter.
P5  (N=1,2) no well event separates any pair at any exhaustively enumerated length; the unmasked port (2,x,R)
    separates a pair iff Re chi0(B) != Re chi1(B).
P6  (identification) among the 60th roots of unity beta: pairs with Re beta^D equal for D in {2,3,5} are equal or
    conjugate; list non-conjugate pairs agreeing on {2,3} and on {2,5} (prediction made before run: primitive
    12th roots for {2,3}; primitive 20th roots for {2,5}).
P7  (fair count) fork probability equals the fair count 2^-D  iff  Re omega = 0.
Exhaustive range: all mask sequences (nonempty subsets of occupied wells at each tick), final mask a single well or
port (a larger final mask is a sum of these), up to the largest length T(N) at which the number of distinct
filtered states stays <= CAP (affordability only; reported per case) and T <= TMAX.
Random part: per (N>=3, group) NR events of length 2D+3, each tick a uniformly random nonempty subset of the
occupied wells with each well kept with probability 3/4; P1 tested at every tick.
"""
import json, sys, random, itertools
from math import gcd
SEED=20261113; CAP=int(sys.argv[1]) if len(sys.argv)>1 else 20000; TMAX=9; NR=200
OUT=sys.argv[2] if len(sys.argv)>2 else 'table_result.json'

def polydivmod(num,den):  # integer coefficient lists, low->high, den monic
    num=num[:]; dn=len(den)-1; qv=[0]*max(1,len(num)-dn)
    for i in range(len(num)-1,dn-1,-1):
        c=num[i]
        if c:
            qv[i-dn]=c
            for k in range(dn+1): num[i-dn+k]-=c*den[k]
    return qv,num[:dn]
_phi={}
def cyclo(n):
    if n in _phi: return _phi[n]
    p=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            p,r=polydivmod(p,cyclo(d)); assert not any(r)
            while len(p)>1 and p[-1]==0: p.pop()
    _phi[n]=p; return p
def red(vec,n):  # vec: length n, coefficient of zeta_n^k ; canonical tuple of length phi(n)
    return tuple(polydivmod(list(vec),cyclo(n))[1])

class Grp:
    def __init__(s,q):
        s.q=q; s.n=q*2//gcd(q,2); s.a=(0,0); s.b=(0,1); s.c=(0,0); s.d=(1,1)
        s.B=s.mul(s.mul(s.b,s.c),s.inv(s.mul(s.a,s.a))); s.H=s.mul(s.mul(s.a,s.d),s.inv(s.mul(s.b,s.c)))
        s.chars=[(si,r) for si in (0,1) for r in range(q)]
        s.qual=[ch for ch in s.chars if s.ev(ch,s.H)==s.n//2]   # chi(H) = -1 = zeta_n^(n/2)
        assert all(ch[0]==1 for ch in s.qual)
    def mul(s,x,y): return ((x[0]+y[0])%2,(x[1]+y[1])%s.q)
    def inv(s,x): return ((-x[0])%2,(-x[1])%s.q)
    def pw(s,x,k): return ((x[0]*k)%2,(x[1]*k)%s.q)
    def ev(s,ch,x): return (ch[0]*x[0]*(s.n//2)+ch[1]*x[1]*(s.n//s.q))%s.n   # exponent of zeta_n
    def omega(s,ch,D): return s.ev(ch,s.pw(s.B,D))
    def re2(s,e):  # 2 Re zeta_n^e as canonical tuple
        v=[0]*s.n; v[e%s.n]+=1; v[(-e)%s.n]+=1; return red(v,s.n)

def step(G,state,N):
    new={}
    for (x,rail),amp in state.items():
        for sdir in 'RL':
            g=G.arc[(rail,sdir)]; key=((x+1)%N if sdir=='R' else (x-1)%N, sdir)
            tgt=new.setdefault(key,{})
            for el,cf in amp.items():
                e2=G.mul(el,g); tgt[e2]=tgt.get(e2,0)+cf
    return {k:{e:c for e,c in v.items() if c} for k,v in new.items()}
def freeze(state): return tuple(sorted((k,tuple(sorted(v.items()))) for k,v in state.items()))
def autocorr(G,amp):   # qualifying chars have chi(z)=-1: fold z, then cyclic autocorrelation over C_q
    q=G.q; v=[0]*q
    for (i,j),cf in amp.items(): v[j]+= cf*(-1)**i
    return [sum(v[j]*v[(j+k)%q] for j in range(q)) for k in range(q)]
def pnum(G,A,ch):      # numerator of probability (times 2^t) for chi=(1,r): sum_k A_k zeta_q^(r k)
    vec=[0]*G.n
    for k,Ak in enumerate(A): vec[(ch[1]*k*(G.n//G.q))%G.n]+=Ak
    return red(vec,G.n)
def show(t,num):
    if not any(num[1:]):
        from fractions import Fraction; return str(Fraction(num[0],2**t))
    return '('+' + '.join('%d*z^%d'%(c,k) for k,c in enumerate(num) if c)+')/2^%d'%t

def eval_state(G,stepped,t):
    """returns {'port':{key:{ch:num}}, 'well':{x:{ch:num}}}"""
    ports={}; wells={}
    for key,amp in stepped.items():
        A=autocorr(G,amp); ports[key]={ch:pnum(G,A,ch) for ch in G.qual}
    for (x,rail),d in ports.items():
        w=wells.setdefault(x,{})
        for ch,num in d.items(): w[ch]=tuple(p+q_ for p,q_ in zip(w[ch],num)) if ch in w else num
    return ports,wells

def run_case(G,N,rng,res):
    D=N//gcd(N,2); qual=G.qual
    pairs=list(itertools.combinations(qual,2))
    reo={ch:G.re2(G.omega(ch,D)) for ch in qual}
    same={p:reo[p[0]]==reo[p[1]] for p in pairs}
    case={'N':N,'D':D,'q':G.q,'n_chars':len(G.chars),'n_qualifying':len(qual),'pairs':len(pairs),
          'pairs_same_Re_omega':sum(same.values()),'P1_viol':0,'P2_viol':0,'events_port':0,'events_well':0}
    firstsep_well={}; firstsep_port={}
    def check(ports,wells,t,masks):
        for kind,dd,first in (('port',ports,firstsep_port),('well',wells,firstsep_well)):
            for key,d in dd.items():
                case['events_'+kind]+=1
                for p in pairs:
                    if d[p[0]]!=d[p[1]]:
                        if same[p]: case['P1_viol']+=1; res['failures'].append(['P1',G.q,N,kind,str(key),masks,str(p)])
                        if t<=D: case['P2_viol']+=1; res['failures'].append(['P2',G.q,N,kind,str(key),masks,str(p)])
                        if p not in first: first[p]={'t':t,'masks':masks,'final':str(key),
                                                   'p0':show(t,d[p[0]]),'p1':show(t,d[p[1]])}
    # exhaustive
    level={freeze({(0,'R'):{(0,0):1}}):({(0,'R'):{(0,0):1}},[])}; T=0; nstates=[]
    for t in range(1,TMAX+1):
        nxt={}; stepped=[]
        for state,masks in level.values():   # v2: evaluate ALL events of length t before generating children
            st=step(G,state,N); ports,wells=eval_state(G,st,t); check(ports,wells,t,masks); stepped.append((st,masks))
        T=t
        for st,masks in stepped:
            occ=sorted({x for x,_ in st})
            for k in range(1,len(occ)+1):
                for sub in itertools.combinations(occ,k):
                    f={key:amp for key,amp in st.items() if key[0] in sub}
                    fz=freeze(f)
                    if fz not in nxt: nxt[fz]=(f,masks+[list(sub)])
            if len(nxt)>CAP: nxt=None; break
        if nxt is None:
            # v2: level t fully evaluated (T=t); only its children were not generated
            break
        nstates.append(len(nxt)); level=nxt
    case['T_exhaustive']=T; case['states_per_level']=nstates
    # NOTE: first-separation entries with t > T come from a partly evaluated level or random events; flagged below.
    # fork
    if N>=3:
        fm=[sorted({j%N,(-j)%N}) for j in range(1,D)]+[[D%N]]
        st={(0,'R'):{(0,0):1}}
        for j in range(1,D+1):
            st=step(G,st,N); st={k:v for k,v in st.items() if k[0] in fm[j-1]}
        st=step(G,st,N); ports,wells=eval_state(G,st,D+1); w=wells[(D+1)%N]
        okP3=True; okP7=True; forkp={}
        for ch in qual:
            vec=[0]*G.n; vec[0]+=2; e=G.omega(ch,D)+(G.n//2 if (D-1)%2 else 0)
            vec[e%G.n]+=1; vec[(-e)%G.n]+=1
            if red(vec,G.n)!=w[ch]: okP3=False
            fair=red([2]+[0]*(G.n-1),G.n)   # 2 words: 2/2^(D+1)=2^-D
            if (w[ch]==fair)!=(not any(reo[ch])): okP7=False
            forkp[str(ch)]=show(D+1,w[ch])
        for p in pairs:
            if (w[p[0]]!=w[p[1]])==same[p]: okP3=False
        case['fork_masks']=fm+[[(D+1)%N]]; case['fork_prob']=forkp; case['P3']=okP3; case['P7']=okP7
        if not okP3: res['failures'].append(['P3',G.q,N])
        if not okP7: res['failures'].append(['P7',G.q,N])
        # P4
        if T>=D+1:
            ok=all((p in firstsep_well and firstsep_well[p]['t']==D+1) for p in pairs if not same[p])
            case['P4']=ok
            if not ok: res['failures'].append(['P4',G.q,N])
        else: case['P4']='not reached (T=%d < D+1=%d)'%(T,D+1)
        # random deep events
        nsep=0; ntot=0
        for _ in range(NR):
            st={(0,'R'):{(0,0):1}}; masks=[]
            for t in range(1,2*D+4):
                st=step(G,st,N); ports,wells=eval_state(G,st,t)
                check(ports,wells,t,masks)
                if t==2*D+3:
                    for d in wells.values():
                        for p in pairs:
                            if not same[p]: ntot+=1; nsep+= d[p[0]]!=d[p[1]]
                occ=sorted({x for x,_ in st}); sub=[x for x in occ if rng.random()<0.75] or [rng.choice(occ)]
                st={k:v for k,v in st.items() if k[0] in sub}; masks=masks+[sub]
        case['random_events']=NR; case['random_len']=2*D+3
        case['random_final_well_pairs_with_Re_differ']=ntot; case['of_which_separated']=nsep
    else:
        okw=not firstsep_well
        st=step(G,step(G,{(0,'R'):{(0,0):1}},N),N); ports,_=eval_state(G,st,2)
        d=ports[(2%N,'R')]; reb={ch:G.re2(G.ev(ch,G.B)) for ch in qual}
        okp=all((d[p[0]]!=d[p[1]])==(reb[p[0]]!=reb[p[1]]) for p in pairs)
        case['P5_well_never']=okw; case['P5_port_t2']=okp
        if not (okw and okp): res['failures'].append(['P5',G.q,N])
    case['pair_table']=[{'pair':str(p),'omega_exponents_mod_n':[G.omega(p[0],D),G.omega(p[1],D)],
        'Re_omega_equal':same[p],'separated_by_fork':(not same[p]) if N>=3 else None,
        'smallest_separating_well_event_found':firstsep_well.get(p),
        'smallest_separating_port_event_found':firstsep_port.get(p)} for p in pairs]
    return case

def p6():
    n=60; out={'viol_235':[], 'agree_23_nonconj':[], 'agree_25_nonconj':[]}
    def re2(e):
        v=[0]*n; v[e%n]+=1; v[(-e)%n]+=1; return red(v,n)
    R={(e,D):re2(e*D) for e in range(n) for D in (2,3,5)}
    for e,f in itertools.combinations(range(n),2):
        conj=(e+f)%n==0
        a23=all(R[e,D]==R[f,D] for D in (2,3)); a25=all(R[e,D]==R[f,D] for D in (2,5))
        if a23 and R[e,5]==R[f,5] and not conj: out['viol_235'].append([e,f])
        if a23 and not conj: out['agree_23_nonconj'].append([e,f])
        if a25 and not conj: out['agree_25_nonconj'].append([e,f])
    orders=lambda L: sorted({n//gcd(n,e) for pr in L for e in pr})
    out['orders_23']=orders(out['agree_23_nonconj']); out['orders_25']=orders(out['agree_25_nonconj'])
    out['P6']=(not out['viol_235']) and out['orders_23']==[12] and out['orders_25']==[20]
    return out

def main():
    rng=random.Random(SEED); res={'seed':SEED,'CAP':CAP,'TMAX':TMAX,'failures':[],'H0':{},'cases':[]}
    for q in (3,4,12):
        G=Grp(q); G.arc={('R','R'):G.a,('R','L'):G.b,('L','R'):G.c,('L','L'):G.d}
        res['H0']['C2xC%d'%q]={'characters':len(G.chars),'qualifying_chi(H)=-1':len(G.qual),'H':G.H,'B':G.B}
        for N in range(1,13):
            res['cases'].append(run_case(G,N,rng,res)); print(q,N,res['cases'][-1]['T_exhaustive'],flush=True)
    res['P6']=p6()
    if not res['P6']['P6']: res['failures'].append(['P6'])
    res['summary']={'n_failures':len(res['failures']),
        'events_port':sum(c['events_port'] for c in res['cases']),'events_well':sum(c['events_well'] for c in res['cases'])}
    with open(OUT,'x') as f: json.dump(res,f,indent=1,sort_keys=True)
    print(json.dumps(res['summary']), res['failures'][:10], json.dumps(res['P6'])[:600])
main()
