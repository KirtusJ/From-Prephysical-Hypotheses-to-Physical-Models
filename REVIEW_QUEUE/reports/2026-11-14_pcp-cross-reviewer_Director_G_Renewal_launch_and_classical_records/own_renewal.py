"""Own check of Director G's note 'Recycling failed direction records prepares a classical launch'.
Written from the note's definitions only. Run: OMP_NUM_THREADS=1 python3 -B own_renewal.py OUTDIR
Seed 20261113. Result file opened with mode 'x' (never overwritten).

CONVENTIONS. Tick U=SH on unnormalised integer amplitudes: (x,R)->(x+1,R)+(x-1,L); (x,L)->(x+1,R)-(x-1,L);
one tick carries 1/sqrt2, so a block (two ticks) divides intensities by 4. Block j passes iff the rail at the
end of the block is opposite to the rail at its start (start rail R for j odd). Zero return distance (x=0)
costs zero route slots. Slot schedule (note, last section): 3 slots per block, 1 per returned link, 2 per
failure. A branch counts as released at deadline t iff its total slot count is <= t.
HYPOTHESIS tested per instance: m even (note requires it for the release formula/rail R). m odd instances are
run and reported separately as non-qualifying.

PREDICATES (fixed before first run), for m in 1..20 (note reports 2,4,6,8,12):
P1  survival after j passes = C(2j,j)/4^j, exact.                               [all m]
P2  first-failure mass at block j = p_{j-1}-p_j and every failure site has |x|<=2j, exact. [all m]
P3  A_m=sum_{j<m} p_j = 2 m p_m ; sum j(p_{j-1}-p_j)= m p_m, exact.             [all m]
P4  E[|x|;failure] <= 2 m p_m, exact (also record whether strict).              [all m]
P5  release amplitudes = (-1)^(m-l) C(m,l) at x=2l-m, rail R.                   [m even only]
P6  site variance of release law = m^2/(2m-1), mean 0, exact.                   [m even]
P7  E sin^2 q = 1/(2m+2) for decoded field, computed exactly in position space as
    (1 - sum c_l c_{l+1}/sum c_l^2)/2 with c_l the decoded amplitudes i^x * raw (real up to global i^-m). [m even]
P8  E q^2 <= (pi/2)^2/(2m+2), numerical quadrature on [-pi/2,pi/2) density cos^(2m) q; tolerance: none
    needed, the measured gap bound-minus-value is reported (must be >0).         [m even]
P9  mean number of failures 1/p_m-1; ratio to sqrt(m) reported (claim O(sqrt m): ratio bounded, limit sqrt(pi)). [all m]
P10 mean total slots = 6m + E|x|/p + 2(1/p-1) (Wald), compared with a direct sum over an explicit
    enumeration of failure sequences truncated at depth K; the truncated sum must be <= the closed form and
    the remainder bounded by the geometric tail; done for m=2 only (exactness by tail bound). [m=2]
P11 m=2: yield 3/8, mean ticks 8, mean return 2, mean slots 52/3, released(24)=393/512, released(5)=0,
    released(6)=3/8, where released(t) is obtained by enumerating explicit failure sequences (tuples), not by the
    recursion.                                                                    [m=2]
P12 Markov: (1-released(t))*t <= mean slots for every t in 0..12m (recursion, own code). [all m<=12]
P13 Monte Carlo (seed 20261113, N=200000 runs each, m=2,4,10): sample mean of slots, ticks and timeout
    fraction at t=12m agree with exact values within 5 standard errors (basis: CLT, 5 sigma two-sided
    false alarm 6e-7 per test). m=10 is not in the note's panel.                 [m=2,4,10]
P14 full coordinate read yield: each block from a sharp input flips rail with prob 1/2 -> 2^-m < p_m for m>=2
    (m=1: equality 1/2).                                                          [all m]
P15 symbolic: |offdiag U(k)^2| = |sin k| ; folded Fourier sum of decoded amplitudes = i^-m (2cos q)^m (m=2,4,6).
P16 scale limit numbers, eps in {1e-2,1e-3,1e-4,1e-6}, delta=eps^1.5 (so delta/eps->0), m = even integer
    nearest delta^-2 eps^-1/2: report sigma_Y/eps^(3/4), sigma_p bound/eps^(1/4), Markov bound with the
    checker's schedule (slot=tau): (8m + 2(1/p_m -1))*tau/d, d=eps^(1/4); predicate: ratios bounded
    (monotone approach to constants), Markov bound -> 0. p_m by log-gamma.
"""
import sys, json, math, random
from fractions import Fraction as Fr
from math import comb
from pathlib import Path
import numpy as np, sympy as sp

def tick(st):
    out = {}
    for (x, r), a in st.items():
        out[(x+1,'R')] = out.get((x+1,'R'),0) + a
        out[(x-1,'L')] = out.get((x-1,'L'),0) + (a if r=='R' else -a)
    return {k:v for k,v in out.items() if v}

def attempt(m):
    st = {(0,'R'):1}; start='R'; fails=[]; surv=[Fr(1)]
    for j in range(1,m+1):
        want = 'L' if start=='R' else 'R'
        b = tick(tick(st))
        st = {k:v for k,v in b.items() if k[1]==want}
        fails.append({x: Fr(v*v,4**j) for (x,r),v in b.items() if r!=want})
        surv.append(Fr(sum(v*v for v in st.values()),4**j)); start=want
    return st, fails, surv

def pj(j): return Fr(comb(2*j,j),4**j)

def run(m, res):
    st, fails, surv = attempt(m); p = surv[m]; R = {}
    R['P1'] = all(surv[j]==pj(j) for j in range(m+1))
    R['P2'] = all(sum(f.values())==pj(j-1)-pj(j) and all(abs(x)<=2*j for x in f) for j,f in enumerate(fails,1))
    R['P3'] = (sum(pj(j) for j in range(m))==2*m*p) and (sum(j*(pj(j-1)-pj(j)) for j in range(1,m+1))==m*p)
    Eabs = sum(abs(x)*w for f in fails for x,w in f.items())
    R['P4'] = Eabs <= 2*m*p
    even = (m%2==0)
    info = {'m':m,'hypothesis_m_even':even,'p':str(p),'E_abs_x_failure':str(Eabs),'mean_return':str(Eabs/p),
            'P4_slack_ratio_Eabs_over_2mp':float(Eabs/(2*m*p)),'max_abs_failure_site':max(abs(x) for f in fails for x in f)}
    final_rails = sorted({r for (_,r) in st})
    info['final_rail']=final_rails
    if even:
        R['P5'] = st == {(2*l-m,'R'):(-1)**(m-l)*comb(m,l) for l in range(m+1)}
        N = sum(v*v for v in st.values())
        mean = Fr(sum(x*v*v for (x,_),v in st.items()),N); var = Fr(sum(x*x*v*v for (x,_),v in st.items()),N)-mean**2
        R['P6'] = (mean==0 and var==Fr(m*m,2*m-1))
        # decoded: i^x * raw, x=2l-m -> i^-m * (-1)^l * raw ; drop global i^-m
        c = [(-1)**l*st[(2*l-m,'R')] for l in range(m+1)]
        es2 = (1-Fr(sum(c[l]*c[l+1] for l in range(m)),sum(v*v for v in c)))/2
        R['P7'] = es2==Fr(1,2*m+2); info['E_sin2_q']=str(es2)
        q = np.linspace(-np.pi/2,np.pi/2,400001); w = np.cos(q)**(2*m)
        eq2 = float(np.trapezoid(q*q*w,q)/np.trapezoid(w,q)); bnd=(math.pi/2)**2/(2*m+2)
        R['P8'] = eq2 < bnd; info['E_q2']=eq2; info['E_q2_bound']=bnd; info['P8_gap']=bnd-eq2
    else:
        for k in ('P5','P6','P7','P8'): R[k]='not_applicable_hypothesis_fails'
        info['odd_m_release_matches_formula_in_rail_L'] = st == {(2*l-m,'L'):(-1)**(m-l)*comb(m,l) for l in range(m+1)}
        info['odd_m_release_abs_match'] = sorted((x,abs(v)) for (x,_),v in st.items())==[(2*l-m,comb(m,l)) for l in range(m+1)]
    info['mean_failures']=str(1/p-1); info['mean_failures_over_sqrt_m']=float((1/p-1)/math.sqrt(m)); R['P9']=float((1/p-1)/math.sqrt(m))<math.sqrt(math.pi)
    costs={}
    for j,f in enumerate(fails,1):
        for x,w in f.items(): costs[3*j+abs(x)+2]=costs.get(3*j+abs(x)+2,0)+w
    mean_slots = 6*m+Eabs/p+2*(1/p-1); info['mean_slots']=str(mean_slots)
    info['mean_blocks']=str(sum(pj(j) for j in range(m))/p); info['mean_ticks']=str(2*sum(pj(j) for j in range(m))/p)
    if m<=12:
        cdf=[]
        for t in range(12*m+1):
            s = p if t>=3*m else Fr(0)
            s += sum(w*cdf[t-c] for c,w in costs.items() if c<=t); cdf.append(s)
        R['P12']=all((1-cdf[t])*t<=mean_slots for t in range(12*m+1))
        info['released_at_3m_4m_6m_12m']=[str(cdf[t]) for t in (3*m,4*m,6*m,12*m)]
        info['markov_tightest_ratio']=float(max((1-cdf[t])*t/mean_slots for t in range(12*m+1)))
        info['_cdf12m']=cdf[12*m]
    R['P14'] = (Fr(1,2**m)<p) if m>=2 else (Fr(1,2**m)==p)
    two_ok = all(sum(v*v for (x,r),v in tick(tick({(0,a):1})).items() if r==b)==2 for a,b in (('R','L'),('L','R')))
    R['P14']=R['P14'] and two_ok
    if m==2:
        # explicit failure sequences as tuples
        def seqs(t, prefix_cost, weight, depth, acc):
            if prefix_cost+3*m<=t: acc[0]+=weight*p
            for c,w in costs.items():
                if prefix_cost+c+3*m<=t: seqs(t,prefix_cost+c,weight*w,depth+1,acc)
        rel={}
        for t in (5,6,8,12,24):
            acc=[Fr(0)]; seqs(t,0,Fr(1),0,acc); rel[t]=acc[0]
        info['released_enumerated']={str(t):str(v) for t,v in rel.items()}
        R['P11']=(p==Fr(3,8) and info['mean_ticks']=='8' and Eabs/p==2 and mean_slots==Fr(52,3) and rel[24]==Fr(393,512) and rel[5]==0 and rel[6]==Fr(3,8) and 1-rel[24]==Fr(119,512))
        # P10 truncated enumeration of mean slots
        K=40; tot=Fr(0); mass=Fr(0)
        from itertools import product
        # distribution of (number of failures k, cost sum) via convolution (explicit sum over sequences grouped by cost)
        dist={0:Fr(1)}
        for k in range(K+1):
            for c0,w0 in dist.items(): tot+=w0*p*(c0+3*m); mass+=w0*p
            nd={}
            for c0,w0 in dist.items():
                for c,w in costs.items(): nd[c0+c]=nd.get(c0+c,0)+w0*w
            dist=nd
        info['P10_truncated_mean']=float(tot); info['P10_missing_mass']=float(1-mass); info['P10_closed']=float(mean_slots)
        R['P10']= tot<=mean_slots and float(mean_slots-tot)<1e-3 and float(1-mass)==float((1-p)**(K+1))
    info['predicates']=R; info['costs']={str(c):str(w) for c,w in sorted(costs.items())}
    res.append(info); return p,costs,mean_slots,info

def mc(m,costs,p,N,rng,deadline):
    cs=list(costs); ws=[float(costs[c]) for c in cs]; fp=float(p)
    # sample each attempt: success w.p. p else failure cost by weight; ticks via block index not tracked here ->
    # simulate blocks directly instead for ticks
    slots=np.empty(N); ticks=np.empty(N)
    st,fails,surv=attempt(m)
    out=[(float(w),j,x) for j,f in enumerate(fails,1) for x,w in f.items()]
    probs=[o[0] for o in out]+[fp]
    for i in range(N):
        s=0;tk=0
        while True:
            k=rng.choices(range(len(probs)),weights=probs)[0]
            if k==len(out): s+=3*m; tk+=2*m; break
            _,j,x=out[k]; s+=3*j+abs(x)+2; tk+=2*j
        slots[i]=s; ticks[i]=tk
    return slots,ticks

def main():
    outdir=Path(sys.argv[1]); outdir.mkdir(parents=True,exist_ok=True)
    f=(outdir/'own_renewal.json').open('x')
    res=[]; keep={}
    for m in range(1,21): keep[m]=run(m,res)
    rng=random.Random(20261113); mcout=[]
    for m in (2,4,10):
        p,costs,ms,info=keep[m]; N=200000
        slots,ticks=mc(m,costs,p,N,rng,12*m)
        to=float((slots>12*m).mean()); exact_to=float(1-info['_cdf12m'])
        se_s=float(slots.std(ddof=1)/math.sqrt(N)); se_t=float(ticks.std(ddof=1)/math.sqrt(N)); se_to=math.sqrt(exact_to*(1-exact_to)/N)
        z=[(float(slots.mean())-float(ms))/se_s,(float(ticks.mean())-4*m)/se_t,(to-exact_to)/se_to]
        mcout.append({'m':m,'N':N,'mean_slots':float(slots.mean()),'exact_slots':float(ms),'mean_ticks':float(ticks.mean()),'exact_ticks':4*m,
                      'timeout_12m':to,'exact_timeout_12m':exact_to,'z_scores':z,'P13':all(abs(v)<5 for v in z)})
    for r in res: r.pop('_cdf12m',None)
    # P15
    k,q=sp.symbols('k q',real=True); a=sp.exp(sp.I*k)
    U=sp.Matrix([[a,a],[1/a,-1/a]])/sp.sqrt(2); U2=sp.simplify(U*U)
    p15a=all(sp.simplify(sp.expand(sp.expand_complex(U2[i,j]*sp.conjugate(U2[i,j]))-sp.sin(k)**2).rewrite(sp.cos))==0 for i,j in ((0,1),(1,0)))
    p15b=True
    for m in (2,4,6):
        expr=sum(sp.I**(2*l-m)*(-1)**(m-l)*comb(m,l)*sp.exp(-sp.I*q*(2*l-m)) for l in range(m+1))-sp.I**(-m)*(2*sp.cos(q))**m
        p15b = p15b and sp.simplify(sp.expand(expr.rewrite(sp.exp)))==0
    # numeric cross-check of P15a at high precision
    hp=[abs(sp.N((U2[0,1]*sp.conjugate(U2[0,1])-sp.sin(k)**2).subs(k,sp.Rational(v,7)),50)) for v in (1,3,10)]
    # P16
    sc=[]
    for eps in (1e-2,1e-3,1e-4,1e-6):
        d=eps**1.5; m=int(round(d**-2*eps**-0.5/2))*2; a_=eps*d; tau=eps*d*d
        pm=(1-1/(8*m))/math.sqrt(math.pi*m)  # run-3 fix: lgamma cancels catastrophically at m>=1e7; Stirling, rel. error O(m^-2)
        sY=a_*m/math.sqrt(2*m-1); spb=math.pi/(2*d*math.sqrt(2*m+2)); mark=(8*m+2*(1/pm-1))*tau/eps**0.25
        sc.append({'eps':eps,'delta':d,'m':m,'sigmaY_over_eps34':sY/eps**0.75,'sigma_p_bound_over_eps14':spb/eps**0.25,
                   'markov_bound':mark,'markov_over_eps14':mark/eps**0.25,'deadline_over_min_success_time_3m_tau':eps**0.25/(3*m*tau)})
    p16=all(abs(s['sigmaY_over_eps34']-1/math.sqrt(2))<0.01 for s in sc) and sc[-1]['markov_bound']<sc[0]['markov_bound']
    allp={}
    for r in res:
        for kx,v in r['predicates'].items(): allp.setdefault(kx,[]).append((r['m'],v))
    summary={kx:{'pass':[m for m,v in vs if v is True],'fail':[m for m,v in vs if v is False],'na':[m for m,v in vs if v not in (True,False)]} for kx,vs in allp.items()}
    summary['P13']=[(x['m'],x['P13']) for x in mcout]; summary['P15']=[bool(p15a),bool(p15b),[str(h) for h in hp]]; summary['P16']=p16
    out={'seed':20261113,'qualifying_m_even':[m for m in range(1,21) if m%2==0],'non_qualifying':[m for m in range(1,21) if m%2],
         'summary':summary,'monte_carlo':mcout,'scale':sc,'instances':res}
    f.write(json.dumps(out,indent=1)+'\n'); f.close()
    print(json.dumps({'summary':summary,'mc':mcout,'scale':sc},indent=1))
    for r in res: print(r['m'],r['p'],r['mean_return'],r['mean_slots'],r['P4_slack_ratio_Eabs_over_2mp'],r['mean_failures_over_sqrt_m'],r.get('released_enumerated'),r.get('P8_gap'),r.get('odd_m_release_matches_formula_in_rail_L'),r.get('markov_tightest_ratio'))
main()
