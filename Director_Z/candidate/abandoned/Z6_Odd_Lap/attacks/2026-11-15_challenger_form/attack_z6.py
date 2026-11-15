#!/usr/bin/env python3
"""Challenger program for candidate Z6 "Odd Lap" (own program; function/ not read).
Command: python3 attack_z6.py result_attack_z6_run1.json     (seed 20261115 fixed in file)
Exact integer arithmetic only. Groups written additively: A = Z_m1 x ... ; gains a,b,c,d.
delta=a+d-b-c, B=b+c-2a, beta=M*B, M=N/gcd(N,2).
O2 hypothesis (tested per carrier, numbers reported): ord(delta) even; beta not in <delta>;
2*beta = k*delta for some even k.
Rules: odd(m)=(e0-e1)^2, even(m)=(e0+e1)^2, with sign map on Delta=<delta,beta>:
  sgn_s(i*beta+n*delta)=s^i(-1)^n (asserted well defined), weight=(sum_g m(g) sgn(g-kappa))^2, kappa any element of m.
PREDICATES (fixed before first run):
P0 control: (2,-1) -> 1, 9, 5.
P1 (D2) per qualifying carrier: the event masks {-1},{-2,0},{-1},{0} has exactly one end vertex, two walks there,
   class sums (0,0) (odd weight 0 and even weight 0).
P2 (D3) per qualifying carrier: there is a position product event with exactly one end vertex carrying exactly two walks
   with |e0+e1|=2,|e0-e1|=0 ("(1,1)") and one with |e0+e1|=0,|e0-e1|=2 ("(1,-1)"). Events found by a search per ring
   (masks = sites of a pair of walks one level apart, lengths M+1..M+3), then evaluated on every carrier.
P3 algebra: q(e0^2+e1^2)+c e0 e1 == c+(e0+e1)^2+c-(e0-e1)^2 with c+=(2q+c)/4,c-=(2q-c)/4 on a grid of Fractions.
P4 (D4) per qualifying carrier, with S11 and S1m the events of P2: on the product multiset (gains added pairwise)
   (E0+E1)^2=(e0+e1)^2(e0'+e1')^2 and same for minus; for c+ in {0,1/4,1/2,3/4,1}, c-=1-c+, the rule is multiplicative on
   all four pairs from {S11,S1m} iff c+ in {0,1}.
P4b consistency: odd and even rule satisfy weight(Ext S)=2 weight(S) on sampled random events (per carrier, 6 events).
P5 (D6): on rings N in {3,4,5,6,9,16}: walks (L,R)^M and R^(2M) from (0,R) are closed, have gains M(b+c) and 2M a,
   quotient = beta; after switching by a random function on the 2N vertices (non-uniform arc gains) both gains and the
   quotient are unchanged. (All sampled carriers, qualifying or not; N<8.. are controls outside O1.)
P6 fork: per qualifying carrier, event masks A_t={t,-t} (t<=M), A_{M+1}={site of R^(M+1)}: exactly two walks at one
   vertex, odd weight != even weight; expected odd=0,even=4 for M odd and odd=4,even=0 for M even.
P7 (D7 part): per qualifying carrier, 20 random events of length <= M: odd weight == even weight.
P8 universality (challenger's own claim): for one ring, the odd weights of a fixed list of events (fork, P2 events,
   10 random events of length M+1..M+3) are the same on every qualifying carrier; same for even.
P9 one-class equivalence (challenger's own claim): the odd weights of P8 equal the weights of the single square on a
   one-class carrier (s=1, outside O2) with chi(beta)=-1: N odd: Z2, (a,b,c,d)=(0,1,0,0); N=16: Z16,(0,1,0,9);
   N=18: Z2,(0,1,0,0); N=20: Z4? (M=10: need 10B=delta odd multiple: Z4,(0,1,0,3): delta=2,B=1,beta=10=2) .
   Even weights equal the single square on Z2,(0,0,0,1) (beta=0).
P10 transformations, per qualifying carrier: T1 uniform switching (t with N t=0; u,v): a+t,b-t+v-u,c+t+u-v,d-t;
   T2 rail reflection a<->d,b<->c; T3 inversion g->-g; T4 power map g->u g (u odd, coprime to |A|);
   T5 (a,d)->(a+t,d-t) with 2M t an odd multiple of delta (if such t exists).
   For each: (i) image satisfies O2; (ii) sgn_odd of the ORIGINAL carrier evaluated on the image's beta (in the image's
   Delta if it lies in the original Delta) : -1 means the lap sign is unchanged, +1 exchanged; (iii) odd weights of the
   P8 event list unchanged. KILL predicate: some transformation with weights_odd(X) == weights_even(TX) on all events
   of the list.
P11 O2 census: for every group in a list and N in {9,16,18,20}, exhaustive over (a,b,c,d) with a=0 w.l.o.g.? NO:
   exhaustive over all quadruples when |A|^4<=70000, else 3000 random: count qualifying; cyclic groups expected 0.
   For every qualifying carrier both sign maps s=+1,-1 are well defined (asserted) .
Result file opened with mode 'x'. Failed predicates are kept in the file under "failures".
"""
import sys, json, random, itertools
from fractions import Fraction
from math import gcd
SEED=20261115
rng=random.Random(SEED)
fail=[]
def add(g,h,mod): return tuple((x+y)%m for x,y,m in zip(g,h,mod))
def neg(g,mod): return tuple((-x)%m for x,m in zip(g,mod))
def mul(n,g,mod): return tuple((n*x)%m for x,m in zip(g,mod))
def order(g,mod):
    n=1;h=g;z=tuple(0 for _ in mod)
    while h!=z: h=add(h,g,mod);n+=1
    return n
class Carrier:
    def __init__(s,N,mod,a,b,c,d):
        s.N=N;s.mod=mod;s.a,s.b,s.c,s.d=a,b,c,d
        s.M=N//gcd(N,2)
        s.delta=add(add(a,d,mod),neg(add(b,c,mod),mod),mod)
        s.B=add(add(b,c,mod),neg(mul(2,a,mod),mod),mod)
        s.beta=mul(s.M,s.B,mod)
        s.r=order(s.delta,mod)
        s.cyc=[mul(n,s.delta,mod) for n in range(s.r)]
    def O2(s):
        if s.r%2: return False
        if s.beta in s.cyc: return False
        b2=mul(2,s.beta,s.mod)
        if b2 not in s.cyc: return False
        k=s.cyc.index(b2)
        return k%2==0
    def sclass(s):  # s = min j: j*beta in <delta>
        j=1
        while mul(j,s.beta,s.mod) not in s.cyc: j+=1
        return j
    def sgnmap(s,sign):
        mp={}
        for i in range(2):
            for n in range(s.r):
                e=add(mul(i,s.beta,s.mod),s.cyc[n],s.mod); v=(sign**i)*(-1)**n
                if e in mp and mp[e]!=v: raise AssertionError("sign map not well defined")
                mp[e]=v
        return mp
    def step(s,rail,right):
        if rail==0: return s.a if right else s.b
        return s.c if right else s.d
def run(car,masks):
    """masks: list of sets of sites (mod N). returns dict vertex-> dict (gain,lam)->count"""
    z=tuple(0 for _ in car.mod)
    st={(0,0):{(z,0):1}}
    for A in masks:
        nw={}
        for (x,rail),ms in st.items():
            for right in (True,False):
                y=(x+1)%car.N if right else (x-1)%car.N
                if y not in A: continue
                g=car.step(rail,right); key=(y,0 if right else 1)
                d=nw.setdefault(key,{})
                for (e,l),n in ms.items():
                    k=(add(e,g,car.mod),l+(0 if right else 1)); d[k]=d.get(k,0)+n
        st=nw
    return st
def vsum(car,ms,mp):
    kappa=next(iter(ms))[0]; t=0
    for (e,l),n in ms.items():
        t+=n*mp[add(e,neg(kappa,car.mod),car.mod)]
    return t
def weight(car,st,mp): return sum(vsum(car,ms,mp)**2 for ms in st.values())
def nwalks(st): return sum(sum(ms.values()) for ms in st.values())
def walk_sites(N,w):
    x=0;out=[]
    for r in w:
        x=(x+1)%N if r else (x-1)%N; out.append(x)
    return out
def fork_masks(N):
    M=N//gcd(N,2)
    ms=[{t%N,(-t)%N} for t in range(1,M+1)]
    ms.append({(M+1)%N})
    return ms
def rand_masks(N,T):
    reach={0};ms=[]
    for t in range(T):
        cand=sorted({(x+1)%N for x in reach}|{(x-1)%N for x in reach})
        k=rng.randint(1,min(4,len(cand))); A=set(rng.sample(cand,k)); ms.append(A); reach=A
    return ms
def search_pairs(car):
    """find masks with single end vertex, two walks one level apart, of type (1,1) and (1,-1)"""
    N,M=car.N,car.M; mo=car.sgnmap(-1); me=car.sgnmap(1); found={}
    for T in range(M+1,M+4):
        lows=[w for w in itertools.product((True,False),repeat=T) if sum(1 for r in w if not r)<=T-M]
        for w1 in lows:
            l1=sum(1 for r in w1 if not r)
            if l1>3: continue
            s1=walk_sites(N,w1)
            for w2 in lows_hi(T,l1+M):
                if w2[-1]!=w1[-1]: continue
                s2=walk_sites(N,w2)
                if s2[-1]!=s1[-1]: continue
                masks=[{x,y} for x,y in zip(s1,s2)]
                st=run(car,masks)
                if len(st)!=1 or nwalks(st)!=2: continue
                ms=next(iter(st.values()))
                p=abs(vsum(car,ms,me)); m=abs(vsum(car,ms,mo))
                typ='11' if (p,m)==(2,0) else ('1m' if (p,m)==(0,2) else None)
                if typ and typ not in found: found[typ]=[sorted(A) for A in masks]
                if len(found)==2: return found
    return found
_hi={}
def lows_hi(T,l):
    if (T,l) not in _hi:
        _hi[(T,l)]=[tuple(i not in c for i in range(T)) for c in itertools.combinations(range(T),l)] if l<=T else []
    return _hi[(T,l)]
def product_ms(car,ms1,ms2):
    out={}
    for (e1,l1),n1 in ms1.items():
        for (e2,l2),n2 in ms2.items():
            k=(add(e1,e2,car.mod),0); out[k]=out.get(k,0)+n1*n2
    return out
def sample_carriers(N,mod,want,tries):
    els=list(itertools.product(*[range(m) for m in mod])); q=[];t=0
    while len(q)<want and t<tries:
        t+=1; g=[rng.choice(els) for _ in range(4)]; c=Carrier(N,mod,*g)
        if c.O2(): q.append(c)
    return q,t
def main():
    out=open(sys.argv[1],'x')
    R={"seed":SEED,"command":"python3 "+" ".join(sys.argv),"failures":fail}
    # P0
    e0,e1=2,-1; R["P0"]=[(e0+e1)**2,(e0-e1)**2,e0*e0+e1*e1]
    if R["P0"]!=[1,9,5]: fail.append("P0")
    # P3
    bad=0;tot=0
    for q in range(-3,4):
        for c in range(-5,6):
            cp=Fraction(2*q+c,4);cm=Fraction(2*q-c,4)
            for a0 in range(-4,5):
                for a1 in range(-4,5):
                    tot+=1
                    if q*(a0*a0+a1*a1)+c*a0*a1!=cp*(a0+a1)**2+cm*(a0-a1)**2: bad+=1
    R["P3"]={"cases":tot,"bad":bad}
    if bad: fail.append("P3")
    plan={9:[(2,2),(2,4),(4,4),(2,6)],16:[(2,16),(4,16),(2,48)],18:[(2,2),(2,4)],20:[(2,4),(4,4),(2,20)],11:[(2,2),(2,2,2)]}
    onecls={9:((2,),(0,),(1,),(0,),(0,)),11:((2,),(0,),(1,),(0,),(0,)),18:((2,),(0,),(1,),(0,),(0,)),
            16:((16,),(0,),(1,),(0,),(9,)),20:((4,),(0,),(1,),(0,),(3,))}
    R["rings"]={}
    for N,groups in plan.items():
        RN={"groups":{}}; R["rings"][str(N)]=RN
        cars=[]
        for mod in groups:
            q,t=sample_carriers(N,mod,10,3000)
            RN["groups"][str(mod)]={"tried":t,"qualify":len(q),"carriers":[[c.a,c.b,c.c,c.d] for c in q]}
            cars+=q
        if not cars: fail.append("no qualifying carrier N=%d"%N); continue
        M=cars[0].M
        found=search_pairs(cars[0]); RN["P2_events"]=found
        if len(found)<2: fail.append("P2 search N=%d found %s"%(N,list(found)))
        evlist=[fork_masks(N)]+[[set(A) for A in found[k]] for k in sorted(found)]+[rand_masks(N,rng.randint(M+1,M+3)) for _ in range(10)]
        short=[rand_masks(N,rng.randint(1,M)) for _ in range(20)]
        cnt={k:0 for k in ["P1","P2","P4","P4b","P6","P7","P8","P10_O2","P10_w"]}; n=len(cars)
        ref=None; t10={}
        d2=[{(-1)%N},{(-2)%N,0},{(-1)%N},{0}]
        for car in cars:
            mo=car.sgnmap(-1); me=car.sgnmap(1)
            st=run(car,d2)
            ok=len(st)==1 and nwalks(st)==2 and weight(car,st,mo)==0 and weight(car,st,me)==0
            cnt["P1"]+=ok
            if not ok: fail.append(["P1",N,car.mod,car.a,car.b,car.c,car.d])
            # P2/P4
            ok2=True; evs={}
            for typ,want in (('11',(2,0)),('1m',(0,2))):
                if typ not in found: ok2=False; continue
                st=run(car,[set(A) for A in found[typ]])
                if len(st)!=1 or nwalks(st)!=2: ok2=False; continue
                ms=next(iter(st.values())); evs[typ]=ms
                if (abs(vsum(car,ms,me)),abs(vsum(car,ms,mo)))!=want: ok2=False
            cnt["P2"]+=ok2
            if not ok2: fail.append(["P2",N,car.mod,car.a,car.b,car.c,car.d])
            if ok2:
                ok4=True; mult={}
                for cp in (Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1)):
                    cm=1-cp; allm=True
                    for x in evs:
                        for y in evs:
                            pm=product_ms(car,evs[x],evs[y])
                            Pp=vsum(car,pm,me)**2; Pm=vsum(car,pm,mo)**2
                            wx=(vsum(car,evs[x],me)**2,vsum(car,evs[x],mo)**2); wy=(vsum(car,evs[y],me)**2,vsum(car,evs[y],mo)**2)
                            if Pp!=wx[0]*wy[0] or Pm!=wx[1]*wy[1]: ok4=False
                            if cp*Pp+cm*Pm!=(cp*wx[0]+cm*wx[1])*(cp*wy[0]+cm*wy[1]): allm=False
                    mult[str(cp)]=allm
                if mult!={"0":True,"1/4":False,"1/2":False,"3/4":False,"1":True}: ok4=False
                cnt["P4"]+=ok4
                if not ok4: fail.append(["P4",N,car.mod,car.a,car.b,car.c,car.d,mult])
            # P4b
            okc=True
            for ms_ in evlist[3:9]:
                st=run(car,ms_); st2=run(car,ms_+[set(range(N))])
                for mp in (mo,me):
                    if weight(car,st2,mp)!=2*weight(car,st,mp): okc=False
            cnt["P4b"]+=okc
            if not okc: fail.append(["P4b",N,car.mod,car.a,car.b,car.c,car.d])
            # P6
            st=run(car,evlist[0]); wo,we=weight(car,st,mo),weight(car,st,me)
            exp=(0,4) if M%2 else (4,0)
            ok=len(st)==1 and nwalks(st)==2 and (wo,we)==exp
            cnt["P6"]+=ok
            if not ok: fail.append(["P6",N,car.mod,car.a,car.b,car.c,car.d,wo,we])
            # P7
            ok=all(weight(car,run(car,m_),mo)==weight(car,run(car,m_),me) for m_ in short)
            cnt["P7"]+=ok
            if not ok: fail.append(["P7",N,car.mod,car.a,car.b,car.c,car.d])
            # P8
            wl=[[weight(car,run(car,m_),mo) for m_ in evlist],[weight(car,run(car,m_),me) for m_ in evlist]]
            if ref is None: ref=wl
            ok=wl==ref; cnt["P8"]+=ok
            if not ok: fail.append(["P8",N,car.mod,car.a,car.b,car.c,car.d])
            # P10
            mod=car.mod; els=list(itertools.product(*[range(m) for m in mod]))
            ts=[t for t in els if mul(N,t,mod)==tuple(0 for _ in mod)]
            t=rng.choice(ts);u=rng.choice(els);v=rng.choice(els); vu=add(v,neg(u,mod),mod)
            T={}
            T["T1_switch"]=Carrier(N,mod,add(car.a,t,mod),add(add(car.b,neg(t,mod),mod),vu,mod),add(add(car.c,t,mod),neg(vu,mod),mod),add(car.d,neg(t,mod),mod))
            T["T2_reflect"]=Carrier(N,mod,car.d,car.c,car.b,car.a)
            T["T3_invert"]=Carrier(N,mod,*[neg(g,mod) for g in (car.a,car.b,car.c,car.d)])
            size=1
            for m in mod: size*=m
            us=[x for x in range(3,2*size) if gcd(x,size)==1]
            uu=rng.choice(us); T["T4_power"]=Carrier(N,mod,*[mul(uu,g,mod) for g in (car.a,car.b,car.c,car.d)])
            odd=[car.cyc[j] for j in range(1,car.r,2)]
            t5=[x for x in els if mul(2*car.M,x,mod) in odd]
            if t5:
                x=rng.choice(t5); T["T5_shift"]=Carrier(N,mod,add(car.a,x,mod),car.b,car.c,add(car.d,neg(x,mod),mod))
            for name,c2 in T.items():
                rec=t10.setdefault(name,{"n":0,"O2":0,"lap_sign_orig_char_-1":0,"lap_sign_orig_char_+1":0,"beta_outside_orig_Delta":0,"odd_weights_same":0,"KILL_odd_eq_even_image":0})
                rec["n"]+=1
                if not c2.O2(): continue
                rec["O2"]+=1
                sv=mo.get(c2.beta)
                if sv is None: rec["beta_outside_orig_Delta"]+=1
                elif sv==-1: rec["lap_sign_orig_char_-1"]+=1
                else: rec["lap_sign_orig_char_+1"]+=1
                mo2=c2.sgnmap(-1); me2=c2.sgnmap(1)
                w2o=[weight(c2,run(c2,m_),mo2) for m_ in evlist]; w2e=[weight(c2,run(c2,m_),me2) for m_ in evlist]
                rec["odd_weights_same"]+= (w2o==wl[0])
                rec["KILL_odd_eq_even_image"]+= (w2e==wl[0])
        RN["n_qualifying"]=n; RN["counts_pass"]=cnt; RN["P10"]=t10
        RN["P8_weights_odd"]=ref[0]; RN["P8_weights_even"]=ref[1]
        for k in ["P1","P2","P4","P4b","P6","P7","P8"]:
            if cnt[k]!=n: fail.append("%s N=%d %d/%d"%(k,N,cnt[k],n))
        # P9
        mod1,a1,b1,c1,d1=onecls[N]; c1c=Carrier(N,mod1,a1,b1,c1,d1)
        info={"s":c1c.sclass(),"r":c1c.r,"beta":c1c.beta,"delta":c1c.delta}
        mp1={c1c.cyc[n_]:(-1)**n_ for n_ in range(c1c.r)}
        w1=[weight(c1c,run(c1c,m_),mp1) for m_ in evlist]
        c0=Carrier(N,(2,),(0,),(0,),(0,),(1,)); mp0={c0.cyc[n_]:(-1)**n_ for n_ in range(c0.r)}
        w0=[weight(c0,run(c0,m_),mp0) for m_ in evlist]
        info["hyp_s1_beta_odd_power_of_delta"]= c1c.sclass()==1 and c1c.beta in [c1c.cyc[j] for j in range(1,c1c.r,2)]
        info["hyp_even_ctrl_beta_trivial"]= c0.beta==(0,)
        info["odd_eq_oneclass"]= w1==ref[0]; info["even_eq_plain_signed_ring"]= w0==ref[1]
        RN["P9"]=info
        if not (info["odd_eq_oneclass"] and info["even_eq_plain_signed_ring"] and info["hyp_s1_beta_odd_power_of_delta"]): fail.append(["P9",N,info])
    # P5
    P5=[]
    for N in (3,4,5,6,9,16):
        M=N//gcd(N,2)
        for mod in ((2,2),(2,4),(2,16),(3,6)):
            els=list(itertools.product(*[range(m) for m in mod]))
            for _ in range(5):
                g=[rng.choice(els) for _ in range(4)]; car=Carrier(N,mod,*g)
                th={(x,r):rng.choice(els) for x in range(N) for r in (0,1)}
                def walk(w,sw):
                    x,rail=0,0; tot=tuple(0 for _ in mod)
                    for right in w:
                        y=(x+1)%N if right else (x-1)%N; r2=0 if right else 1
                        gg=car.step(rail,right)
                        if sw: gg=add(add(gg,th[(y,r2)],mod),neg(th[(x,rail)],mod),mod)
                        tot=add(tot,gg,mod); x,rail=y,r2
                    return tot,(x,rail)
                w1=[False,True]*M; w2=[True]*(2*M)
                g1,e1_=walk(w1,False); g2,e2_=walk(w2,False); h1,_=walk(w1,True); h2,_=walk(w2,True)
                ok=(e1_==(0,0) and e2_==(0,0) and g1==mul(M,add(car.b,car.c,mod),mod) and g2==mul(2*M,car.a,mod)
                    and add(g1,neg(g2,mod),mod)==car.beta and h1==g1 and h2==g2)
                P5.append(ok)
                if not ok: fail.append(["P5",N,mod,g])
    R["P5"]={"cases":len(P5),"pass":sum(P5)}
    # P11
    P11={}
    for N in (9,16,18,20):
        for mod in ((2,),(4,),(8,),(16,),(6,),(12,),(32,),(2,2),(2,4),(4,4),(2,6),(2,8),(2,16),(3,3),(2,2,2),(2,10),(2,32)):
            els=list(itertools.product(*[range(m) for m in mod])); size=len(els)
            if size**4<=70000: quads=itertools.product(els,repeat=4); kind="exhaustive"
            else: quads=([rng.choice(els) for _ in range(4)] for _ in range(3000)); kind="random3000"
            tot=q=0
            for g in quads:
                tot+=1; c=Carrier(N,mod,*g)
                if c.O2():
                    q+=1; c.sgnmap(1); c.sgnmap(-1)
            P11["N=%d %s"%(N,mod)]=[kind,tot,q]
            if len(mod)==1 and q: fail.append(["P11 cyclic qualifies",N,mod])
    R["P11"]=P11
    R["n_failures"]=len(fail)
    json.dump(R,out,indent=1,default=str); out.close()
    print("failures",len(fail)); print(fail[:10])
main()
