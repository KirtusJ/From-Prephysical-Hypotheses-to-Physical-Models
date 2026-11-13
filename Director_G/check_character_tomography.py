"""Tomography of a fixed counting/character mixture from signed-walk base ports.

Usage: python -B check_character_tomography.py OUTPUT_DIRECTORY.
All record and rank tests use integers; their cyclotomic comparisons are exact.
"""
import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def divide(p, divisor):
    """Integer long division by a monic polynomial in ascending degree."""
    r = list(p)
    q = [0]*max(1, len(r)-len(divisor)+1)
    while len(trim(r)) >= len(divisor):
        i = len(r)-len(divisor)
        q[i] = r[-1]
        for j, a in enumerate(divisor):
            r[i+j] -= q[i]*a
    return trim(q), r


@lru_cache(maxsize=None)
def cyclotomic(m):
    p = [-1]+[0]*(m-1)+[1]
    for d in range(1, m):
        if m % d == 0:
            p, remainder = divide(p, cyclotomic(d))
            assert remainder == [0]
    return tuple(p)


def reduced(p, m):
    return divide(p, cyclotomic(m))[1]


def scalar(a, m):
    return [a]+[0]*(m-1)


def step(counts, signed, m, g):
    base = 4*m
    nc, ns = Counter(), Counter()
    for (x,c), number in counts.items():
        for d in (1,-1):
            nc[(x+d)%base,d] += number
    for (x,c,j), amp in signed.items():
        for d in (1,-1):
            dest = ((x+d)%base, d, (j+g(x))%m)
            ns[dest] += -amp if c == d == -1 else amp
    return nc, {q:a for q,a in ns.items() if a}


def word_data(word, m, start=0, gain=None):
    g = gain if gain is not None else lambda x:x//2
    x,c,phase,sign = start,1,0,1
    for d in word:
        phase += g(x)
        if c == d == -1:
            sign = -sign
        x,c = x+d,d
    return (x%(4*m), c), phase, sign


def direct_words(m, t):
    counts, signed = Counter(), Counter()
    for directions in product((1,-1), repeat=t):
        (x,d),j,a = word_data(directions,m)
        counts[x,d] += 1
        signed[x,d,j%m] += a
    return counts,{k:v for k,v in signed.items() if v}


def one_left(m, n):
    # Move the unique left step through all n eligible positions, keeping
    # the last (n+1)-st step right. This calculation ignores sheet wrapping.
    terms = []
    for j in range(n):
        p, gain, a = word_data([1]*j+[-1]+[1]*(n-j),m)
        assert p == (n-1,1) and a == 1
        terms.append(gain)
    assert terms==list(range(terms[0],terms[0]+n))
    return terms


def correlate(v):
    m=len(v)
    return [sum(a*v[(j+h)%m] for j,a in enumerate(v)) for h in range(m)]


def affine_row(number, ac):
    # W = S + (N-S)c + sum_{h folded positive} row_h C(h).
    m=len(ac)
    return [number-ac[0]]+[ac[h]+(ac[-h] if 2*h!=m else 0) for h in range(1,m//2+1)]


class Rank:
    """Exact incremental integer row reduction; only independent rows are kept."""
    def __init__(self):
        self.rows={}
        self.witness=[]

    def enter(self, row, port):
        v=list(row)
        for j in range(len(v)):
            if not v[j]:
                continue
            if j not in self.rows:
                self.rows[j]=v
                self.witness.append(port)
                return
            b=self.rows[j]
            v=[b[j]*x-v[j]*y for x,y in zip(v,b)]
            divisor=math.gcd(*v)
            if divisor>1:
                v=[x//divisor for x in v]


def port_poly(number, ac, c, weights):
    # Numerator in the group ring, evaluated at the named primitive zeta_m.
    m=len(weights)
    p=scalar(c*number,m)
    for s,weight in enumerate(weights):
        for j,a in enumerate(ac):
            p[s*j%m]+=weight*a
    return p


def direct_lag(weights,h):
    m=len(weights)
    p=scalar(0,m)
    # Twice the real Fourier coefficient also for an oriented input.
    for j,a in enumerate(weights):
        p[j*h%m]+=a
        p[-j*h%m]+=a
    return p


def recover(m, ports, five, coefficients, label):
    c, weights=coefficients
    den=c+sum(weights)
    data=[scalar(0,m)]+[port_poly(n,ac,c,weights) for n,ac in ports]
    # D*W_n reconstructed from actual history counts. The observed P_n is
    # this polynomial divided by D*2^(n+1).
    twice_lags=[None]+[[a-2*b+e for a,b,e in zip(data[h+1],data[h],data[h-1])]
                        for h in range(1,m+1)]
    for h in range(1,m+1):
        assert reduced(twice_lags[h],m)==reduced(direct_lag(weights,h),m)
    cap=reduced(twice_lags[m],m)
    assert cap==[2*sum(weights)] and den*2-cap[0]==2*c

    # Apply inverse DFT to the recovered real profile at all M displacements.
    # This returns the conjugate-symmetrized weights. Delta_0 uses C(M).
    folded=[]
    for s in range(m//2+1):
        p=scalar(0,m)
        for h in range(m):
            for j,a in enumerate(twice_lags[h or m]):
                p[(j-s*h)%m]+=a
        normal=reduced(p,m)
        folded.append(str(Fraction(normal[0]*(1 if 2*s%m==0 else 2),2*m*den)))
        assert normal == [m*(weights[s]+weights[-s%m])]
    assert sum(map(Fraction,folded))+Fraction(c,den)==1

    # Independent short c: use only short one-left covariance lags actually
    # contributing to the five-tick signed pattern, folding aliases first.
    N,ac=five
    row=affine_row(N,ac); cross=scalar(0,m)
    for h,w in enumerate(row[1:],1):
        if w:
            assert h<=4
            cross=[x+w*y for x,y in zip(cross,twice_lags[h])]
    if row[0]:
        p=port_poly(N,ac,c,weights)
        residue=reduced([2*a-b for a,b in zip(p,cross)],m)
        assert residue==[2*(den*ac[0]+row[0]*c)]
        fast="five-tick (1,R) plus active folded lags at most four"
    else:
        assert m==4
        fast="one-left wrap at tick 6; the five-tick port has zero count coefficient"
    energies=[reduced(p,m) for p in data]
    return dict(label=label,count_weight=str(Fraction(2*den-cap[0],2*den)),recovered_folded=folded,
                short_count_method=fast,
                one_left_DW_coefficients_at_n_0_through_M_plus_1=energies,
                input_denominator=den,exact_dft_verified=True)


def scan(m):
    counts={(0,1):1}
    signed={(0,1,0):1}
    K=m//2
    full,positions,design=Rank(),Rank(),Rank()
    ranks=[];differences=[];ports=[];first=None
    for t in range(1,m+3):
        counts,signed=step(counts,signed,m,lambda x:x//2)
        assert sum(counts.values())==sum(v*v for v in signed.values())==1<<t
        if t<=7:
            dc,ds=direct_words(m,t)
            assert dc==counts and ds==signed
        vectors={port:scalar(0,m) for port in counts}
        for (x,c,j),w in signed.items():
            vectors[x,c][j]=w
        state_rows={}; contrasts=[]
        for port in sorted(counts):
            ac=correlate(vectors[port])
            row=affine_row(counts[port],ac)
            state_rows[port]=row
            full.enter(row,[t,*port])
            if row[0]:
                contrasts.append([*port,counts[port],ac[0]])
            if t==5 and port==(1,1):
                five=(counts[port],ac)
        for x in sorted({p[0] for p in counts}):
            z=[0]*(K+1)
            for c in (1,-1):
                if (x,c) in state_rows:
                    z=[v+w for v,w in zip(z,state_rows[x,c])]
            positions.enter(z,[t,x])
        if t>=2:
            n=t-1;port=(n-1,1);terms=one_left(m,n)
            assert counts[port]==n
            assert vectors[port]==[sum(j%m==h for j in terms) for h in range(m)]
            ac=correlate(vectors[port])
            ports.append((n,ac));design.enter(state_rows[port],[t,*port])
            assert ac[0]==(n if n<=m else n+2)
        tv=Fraction(sum(abs(n-s) for _,_,n,s in contrasts),2*(1<<t))
        if tv and first is None:first=dict(tick=t,tv=str(tv),ports=contrasts)
        ranks.append([t,len(full.rows),len(positions.rows),len(design.rows)])
        if t<=6:
            differences.append([t,str(tv)])
    assert len(full.rows)==len(design.rows)==K+1
    assert ranks[m][3]==K and ranks[K+1][3]==K
    assert first['tick']==(6 if m==4 else 5) and first['tv']==('5/16' if m==3 else '1/16')
    five_row=affine_row(*five)
    assert five[0]==6 and five[1][0]==(0 if m==3 else 6 if m==4 else 4)
    mixtures=[('mixed', (7,[1+(min(s,m-s)*3+1)%7 for s in range(m)])),
              ('count_only',(1,[0]*m)),('uniform_characters',(0,[1]*m)),
              ('oriented_input',(0,[int(s==m-1) for s in range(m)]))]
    return dict(M=m,ring_sites=4*m,folded_lag_count=K,
                short_count_vs_uniform_first=first,whole_base_tv_through_six=differences,
                five_tick_port=dict(count=five[0],signed_sheet_energy=five[1][0],affine_row=five_row),
                rank_by_tick=ranks,base_first_full_rank=next(t for t,a,b,e in ranks if a==K+1),
                position_only_first_full_rank=next((t for t,a,b,e in ranks if b==K+1),None),
                one_left_first_full_rank=next(t for t,a,b,e in ranks if e==K+1),
                whole_base_independent_rows=full.witness,position_only_independent_rows=positions.witness,
                one_left_pure_count_vs_uniform_first_gap=str(Fraction(2,2**(m+2))),
                magnitude_recoveries=[recover(m,ports,five,case,label) for label,case in mixtures])


def ruler_controls():
    # On the physical 4(R+1)-site ring prescribe comparison centres 2h
    # for h=0,...,R-1, and one balancing lag in the remaining centre.
    # g(2i+1)-g(2i-1) is the requested lag; every gain is local to a site.
    trials=[]
    for m in (3,4,5,8,9,16):
        settings=list(range(m//2+1))
        lags=settings+[(-sum(settings))%m]
        N=2*len(lags)
        g=[0]*N; running=0
        for i,h in enumerate(lags):
            running=(running+h)%m;g[2*i+1]=running
        assert running==0 and N>=6
        # Start each independent launch at the named centre with incoming R.
        # We do not rely on a dark-port truth: the data generator keeps counting
        # weights and signed histories separately.
        rows=[]
        for i,h in enumerate(settings):
            centre=2*i
            routes=Counter()
            for word in product((1,-1),repeat=3):
                x=centre;phase=0;c=1;sg=1
                for d in word:
                    phase+=g[x]
                    if c==d==-1:sg=-sg
                    x=(x+d)%N;c=d
                routes[x,c,phase%m,sg]+=1
            pure=group_totals(routes,m)
            for dark in (False,True):
                dest=((centre-1)%N,-1) if dark else ((centre+1)%N,1)
                cnt,v=pure[dest];assert cnt==2
                poly=correlate(v);polynomial_row=affine_row(cnt,poly)
                if h==0:
                    assert poly[0]==(0 if dark else 4)
                else:
                    assert poly[0]==2
                # For arbitrary input laws (c,lambda_s), H^3 denominator 8:
                # bright/dark W = 2 +/- 2 C(h), also when h=0.
                for s in range(m):
                    square=port_poly(2,poly,0,[int(j==s) for j in range(m)])
                    expected=scalar(2,m)
                    expected[s*h%m]+=(-1 if dark else 1)
                    expected[-s*h%m]+=(-1 if dark else 1)
                    assert reduced(square,m)==reduced(expected,m)
            assert sorted(q[0]for q in pure.values())==[1,1,1,1,2,2]
            rows.append(dict(setting=h,bright_port=[(centre+1)%N,1],dark_port=[(centre-1)%N,-1],
                             dark_count_coefficient=polynomial_row[0]))
        trials.append(dict(M=m,base_ring=N,departure_gains=g,settings=rows))
    return trials


def group_totals(routes,m):
    # Pair positive and negative histories only after collecting full ports.
    groups={}
    for (x,c,j,sign),amount in routes.items():
        if (x,c) not in groups:groups[x,c]=[0,scalar(0,m)]
        group=groups[x,c];group[0]+=amount;group[1][j]+=sign*amount
    return groups


def main(out):
    orders=[scan(m) for m in list(range(3,25))+[32,33,48,64]]
    assert all(r['base_first_full_rank']==r['position_only_first_full_rank'] for r in orders)
    result=dict(
        model="Use one physical 4M-site base ring, incoming R at x=0, and the same unobserved gain tags at every launch. A departure has unsigned sheet gain floor(x/2) mod M; representatives modulo 4M agree. H carries a minus exactly on L-to-L. Only final base position and direction are read (a separate cumulative rank tests position alone). No applicant state or detector weights are inferred outside the specified fixed homogeneous normalized G10 mixture.",
        characters="Denote gains by (sign,j) in {+,-} x Z_M, with character (sign,j) -> sign*zeta_M^(s*j). At odd M this is mu_2M; at even M sign remains independent and the direct product is not cyclic. This checker addresses that fixed family, not an automatic extension of Z17's cyclic classification to an arbitrary even-order block. b_s are nonnegative and fold into q_s=b_s+b_(M-s), except 0 and the even Nyquist M/2 stand alone. Define c+sum(b_s)=1 and C(h)=sum(b_s*cos(2pi*s*h/M)).",
        model_records="A port with N histories and signed residue counts D_j has 2^t P=cN+sum_s b_s |sum_j D_j zeta_M^(sj)|^2. Directed cyclic autocorrelations A_h=sum_j D_j D_(j+h) give 2^t P=A_0+(N-A_0)c+sum_{h>0} A_h C(h). The dynamic program computes N and D independently on the physical ring, checks both complete mass sums at every depth, and cross-checks every path and port through seven ticks.",
        one_left="At t=n+1 choose (x=n-1,R). Before any possible base wrap there are n words with a single L in one of the first n positions. Moving it one place later changes LR to RL in the prefix, changing only one intermediate departure and raising its gain by floor((x+1)/2)-floor((x-1)/2)=1. Every sign is positive. Sheet powers are n consecutive integers up to common translation. With W_n=2^(n+1) P_n and W_0=0, W_1=1, W_(h+1)-2W_h+W_(h-1)=2C(h). Collect h through M, set c=1-C(M), and invert the real cyclic transform. All readings are unconditional probabilities on separately launched ensembles.",
        exact_recovery="Each row recovers four different input mixtures by direct port-polynomial evaluation in Z[z]/Phi_M, not by feeding analytic W_n into the inverse. Twice-lags are inverted by an exact DFT in the same quotient. Odd and even M, pure count and pure uniform quadratic cases, and indistinguishable oriented input weights are included. Input_denominator is D; the polynomial row at each n gives D*W_n in the cyclotomic basis.",
        identifiability="The parameter vector is (c,C(1),...,C(floor(M/2))). With singleton normalization fixed these are independent affine coordinates: C(0)=1-c and the folded real Fourier map is invertible. The rational integer port rows in these coordinates give exact ranks. Full-dimensional nonnegative interiors make rank deficiency a genuine identifiability failure within the family. One-left n=1..floor(M/2)+1 captures all nonzero folded lags. Through n=M, count and uniform character squares agree on every one-left port because N=A_0; the first difference at n=M+1 is 2/2^(M+2). These statements concern only those nominated ports.",
        fast_count="At tick 5, (1,R), the six word terms with (integer gain,sign) in R-before-L order are (1,-),(0,+),(-1,-),(-1,+),(-2,+),(-3,-). Unwrapped signed autocorrelations at distances 0..4 are 4,-2,1,-2,1. With C extended periodically, 32P=4+2c-4C(1)+2C(2)-4C(3)+2C(4). For M>=5 the folded nonzero terms are obtained through <=6 ticks. At M=3 the lag 3 repeats C(0); solve the folded affine row instead, N-S=6. At M=4 N=S=6 and a six-tick one-left wrap supplies c. No terminal sheet pointer, filtered reference or independently assumed dark output enters any of these base-record reconstructions.",
        rank_schema="Entries are [depth, cumulative full x/coin rank, cumulative x-only rank, cumulative one-left rank]. Depth starts at 1 and includes all earlier complete base readouts. Stored witnesses [t,x,c] or [t,x] indicate ports selected by incremental exact integer row reduction. Direction is +/-1; x uses residues 0..4M-1. Some first TV numerators differ from the coefficient at one port; the TV sums all ports.",
        sampling="Inverting a rare one-left endpoint from unconditioned trials amplifies probability error by 2^(n+1). For the two-model first wrapped port the probabilities are (M+1)/2^(M+2) and (M+3)/2^(M+2). The signal-to-binomial-noise scale for comparable relative evidence grows on the order of M*2^M for this single event. At tick five the contrast for count vs uniform is 1/16 independent of M>=5 at (1,R). The enumerated full rank of the entire record guarantees identifiability at ideal frequencies and supplies no uniform conditioning guarantee.",
        routed_comparison="A changed, fixed menu of site gains supplies all lags h=0..floor(M/2) plus one balance lag. Each selected start location yields three-tick bright/dark probabilities (1 +/- C(h))/4, including C(0)=1-c, with four other distinct ports of probability 1/8. This follows from direct two-path polynomials for the same mixture, including counting. It uses a held response across the engineered gain menu, reproducible initialization at each chosen centre (or a verified distribution-preserving router), and independent repetitions. For Y=+1 at bright, -1 at dark, 0 elsewhere, E[Y]=C(h)/2. To get all estimated C within epsilon with failure <=alpha, n>=8*log(2K/alpha)/epsilon^2 separate trials per setting suffice by Hoeffding, K=floor(M/2)+1. The inverse folded DFT amplifies uniform lag error by at most 2 per recovered weight; simultaneous l1 accuracy would require smaller epsilon. This menu changes the original graph. On floor(x/2) the native two-path diamonds have only unit lag.",
        orders=orders,routed_physical_controls=ruler_controls())
    out.mkdir(parents=True,exist_ok=True)
    target=out/"character_tomography.json"
    target.write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())
    print(target,hashlib.sha256(target.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    main(parser.parse_args().directory)


