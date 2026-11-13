"""Run python -B check_rational_phase_comparison.py OUTPUT_DIRECTORY (standard library)."""
import argparse
import cmath
import json
import math
from fractions import Fraction
from pathlib import Path

from check_rational_bypass import capacity, norm, walsh


def choose(q, denominator):
    """Rational stereographic approximation after an exactly implemented quarter turn."""
    # floor(.5+x) resolves the q=8 octant tie in favour of the upper quarter.
    quarter = math.floor(4/q+.5)
    residual = math.tau/q-quarter*math.pi/2
    m,n = denominator, round(denominator*math.tan(residual/2))
    a,b,c = m*m-n*n,2*m*n,m*m+n*n
    for _ in range(quarter%4):
        a,b = -b,a
    common = math.gcd(math.gcd(a,b),c)
    a,b,c = a//common,b//common,c//common
    error = abs(cmath.exp(1j*math.tau/q)-complex(a,b)/c)
    assert a*a+b*b==c*c and error <= 1/denominator+2e-15
    return a,b,c


def transform(state,a,b,c,K,adjoint=False):
    v = state.copy()
    walsh(v,K)
    u = [0]*len(v)
    for i,w in enumerate(v):
        block,label = divmod(i,K)
        junk,x = divmod(block,4)
        if x < 2:
            if label < abs(a):
                w *= 1 if a>=0 else -1
            elif label < abs(a)+abs(b):
                w *= (1 if b>=0 else -1)*(1 if x==0 else -1)*(-1 if adjoint else 1)
                x ^= 1
            else:
                junk ^= 1
        elif label >= c:
            junk ^= 1
        u[(4*junk+x)*K+label] = w
    walsh(u,K)
    return u


def anchor(state,K,passed):
    return [v if (i in (0,K,2*K,3*K))==passed else 0 for i,v in enumerate(state)]


def select4(raw,a,b,c):
    """Verify both success subspace and failure/recovery with the actual adjoint."""
    K = capacity(abs(a),abs(b))
    v = [0]*(8*K)
    for i,w in enumerate(raw):
        v[i*K] = w
    u = transform(v,a,b,c,K)
    got = [u[i*K] for i in range(4)]
    expected = [a*raw[0]-b*raw[1],b*raw[0]+a*raw[1],c*raw[2],c*raw[3]]
    assert got == expected and norm(u)==norm(raw)*K*K and norm(got)==norm(raw)*c*c
    assert transform(u,a,b,c,K,True) == [w*K*K for w in v]
    fail = anchor(u,K,False)
    back = transform(fail,a,b,c,K,True)
    log = []
    for intermediate_record in (True,False):
        final = transform(anchor(back,K,intermediate_record),a,b,c,K)
        success = [final[i*K] for i in range(4)]
        assert all(x*y0==x0*y for x,x0 in zip(success,expected) for y,y0 in zip(success,expected))
        log.append(Fraction(norm(success),norm(raw)*K**6))
    p = Fraction(c*c,K*K)
    assert sum(log) == 2*p*(1-p)**2
    return dict(K=K,coarse_success=str(Fraction(c*c,K*K)),acted_idle_anchor=got,
                all_complement_numerator=norm(u)-norm(got),input_squared_norm=norm(raw),
                first_failed_then_recovered_joint_by_middle_record=list(map(str,log)))


def apply_port(v,a,b,c,dark=False):
    """Unnormalized numerator of (T⊗I ± I⊗R)/2, spatially held on both arms."""
    sign = -1 if dark else 1
    q = len(v)
    return [(c*v[(y-1)%q][0]+sign*(a*x-b*z),
             c*v[(y-1)%q][1]+sign*(b*x+a*z)) for y,(x,z) in enumerate(v)]


def energy(v):
    return sum(x*x+y*y for x,y in v)


def all_spectra(q,a,b,c):
    # T eigenvalue exp(2πik/q), real plane J eigenvalues ±i. Correctness
    # depends on identifying these as *relative* phase orientations.
    return {(k,s):(1+(cmath.exp(1j*math.tau*k/q)*(complex(a,-s*b)/c)).real)/2
            for k in range(q) for s in (-1,1)}


def direct(q,a,b,c):
    v = [(1,0)]+[(0,0)]*(q-1)
    init = v.copy()
    rates = all_spectra(q,a,b,c)
    expected = [Fraction(1)]
    root_phase = cmath.exp(1j*math.tau/q)
    rows = []
    for r in range(1,13):
        dark = apply_port(v,a,b,c,True)
        bright = apply_port(v,a,b,c)
        denominator = (4*c*c)**r
        yes,no = Fraction(energy(bright),denominator),Fraction(energy(dark),denominator)
        assert yes+no == expected[-1]
        spectral = sum(p**r for p in rates.values())/(2*q)
        assert abs(float(yes)-spectral) < 1e-14
        if r <= 2:
            assert yes == (Fraction(1,2) if r==1 else Fraction(3,8))
        v = bright
        expected.append(yes)
        if r in (1,2,4,8,12):
            good = rates[(1,1)]**r/q
            rows.append(dict(all_bright=r,joint_bright=str(yes),first_dark_after_prefix=str(no),
                             conditional_relation=good/float(yes)))
    # Reversing the stipulated plane orientation conjugates the real rebit
    # and leaves its coordinate-bin probabilities identical for this launch.
    x = init
    for _ in range(4):
        x = apply_port(x,a,b,c)
    y = init
    for _ in range(4):
        y = apply_port(y,a,-b,c)
    assert y==[(l,-m) for l,m in x]
    # Folded-only prior (a pure conjugate pair on the sheet) without any
    # entanglement with the rebit: half correct chirality, half incorrect.
    assert abs((rates[(1,1)]+rates[(1,-1)])/2 -
               (1+a*root_phase.real/c)/2) < 1e-14
    return rows


def case(q):
    coarse = choose(q,8)
    a,b,c = coarse
    tests = [select4(x,a,b,c) for x in ([1,0,0,0],[0,1,0,0],[0,0,1,0],[2,-1,3,-4])]
    assert len(set(v['coarse_success'] for v in tests))==1
    physical = direct(q,a,b,c)
    bounds = []
    for r in (1,4,16,64,256,1024):
        # Choosing O(r) rational slope denominator makes angular error O(1/r).
        a,b,c = choose(q,max(16,r))
        K = capacity(abs(a),abs(b))
        delta = abs(math.atan2(b,a)-math.tau/q)
        assert delta < math.pi/q
        rates = all_spectra(q,a,b,c)
        good = rates[(1,1)]
        bad = max(v for (k,s),v in rates.items() if k != s%q)
        correct = sum(v**r for (k,s),v in rates.items() if k==s%q)/(2*q)
        wrong = sum(v**r for (k,s),v in rates.items() if k!=s%q)/(2*q)
        observed = correct+wrong
        ratio_upper = (q-1)*(bad/good)**r
        assert wrong/(correct+wrong) <= ratio_upper + 1e-13
        assert abs(good - (1+math.cos(delta))/2) < 2e-14
        assert abs(bad-(1+math.cos(math.tau/q-delta))/2)<2e-14
        p = Fraction(c*c,K*K)
        # The cap allows alternated W†/W coarse readbacks. The rank-balanced
        # anchor projector gives failure mass (1-p)[p²+(1-p)²]^N.
        # Tight p near 1 makes one retry pair inefficient; capture honest cap.
        cap = 0 if p==1 or 1-float(p)<=1/(r+1)**2 else math.ceil(
            math.log(1/((r+1)**2*(1-float(p))))/math.log1p(-2*float(p)*(1-float(p))))
        fail = (1-float(p))*(1-2*float(p)*(1-float(p)))**cap
        assert r*fail <= r/(r+1)**2+1e-12
        def contrast(d,axis):
            return sum(p0**r*math.cos(math.tau*k*d/q-s*axis) for (k,s),p0 in rates.items())/(2*q*observed)
        xy = [(contrast(d,0.),contrast(d,math.pi/2)) for d in (1,2)]
        for d,(x,y) in enumerate(xy,1):
            assert abs(x-math.cos(math.tau*d/q)) <= 2*wrong/observed + 3e-13
            assert abs(y-math.sin(math.tau*d/q)) <= 2*wrong/observed + 3e-13
        bounds.append(dict(reads=r,rational=[a,b,c],angle_error=delta,
                           guaranteed_chord_upper=1/max(16,r),walsh_capacity=K,
                           forward_walsh_H_layers=2*(K.bit_length()-1),
                           one_attempt_gate_success=str(p),expected_gate_calls=1+1/float(p) if p<1 else 1,
                           retry_pair_cap_per_gate=cap,per_gate_timeout=fail,
                           literal_one_gate_attempt_per_read_success_log10=r*math.log10(float(p)),
                           gate_completed_retained_yield=observed,
                           gate_completed_correct_mass=correct,
                           wrong_given_accepted=wrong/observed,
                           wrong_to_correct_upper=ratio_upper,
                           signed_relative_cos_sin_by_held_power=xy,
                           timed_joint_correct_lower=correct*max(0.,1-r*fail)))
    assert all(row['first_failed_then_recovered_joint_by_middle_record'] ==
               tests[0]['first_failed_then_recovered_joint_by_middle_record'] for row in tests)
    return dict(order=q,walsh_example=coarse,walsh_checks=tests,
                synchronized_integer_record_prefixes=physical,coherent_comparator=bounds)


def ambiguity(q):
    a,b,c = choose(q,32)
    z = complex(a,b)/c
    root = cmath.exp(1j*math.tau/q)
    values = {(k,s):(1+(root**k*(z.conjugate() if s==1 else z)).real)/2
              for k in range(q) for s in (-1,1)}
    assert all(abs(p-values[(-k%q,-s)])<1e-14 for (k,s),p in values.items())
    u = next(t for t in range(2,q) if math.gcd(t,q)==1)
    assert all(abs(values[(k,s)] - (1+((root**u)**((k*pow(u,-1,q))%q)*
               (z.conjugate() if s==1 else z)).real)/2)<1e-14
               for (k,s) in values)
    return dict(q=q,untransported_unit=u,
                correct_chirality_bright=values[1,1],wrong_chirality_bright=values[1,-1],
                simultaneous_generator_relabel_preserves_every_rate=True,
                full_real_conjugation_preserves_every_rate=True)


def joint_clock(q,n,flip):
    """q and n are given independent sheets, but they see the same real plane."""
    a,b,c = choose(q,64)
    A,B,C = choose(n,64)
    r,s = all_spectra(q,a,b,c),all_spectra(n,A,B,C)
    powers = []
    for copies in (8,32,128):
        w = {(k,l,t):r[k,t]**copies*s[l,t]**copies
             for k in range(q) for l in range(n) for t in (-1,1)}
        total = sum(w.values())
        good = sum(v for (k,l,t),v in w.items() if k==t%q and l==t%n)
        wrong = sum(v for (k,l,t),v in w.items() if k!=t%q or l!=t%n)/total
        profiles = []
        for axis in (0.,math.pi/2):
            contrast = sum(v*math.cos(math.tau*(k/q+flip*l/n)-t*axis)
                           for (k,l,t),v in w.items())/total
            target = math.cos(math.tau*(1/q+flip/n)-axis)
            assert abs(contrast-target)<=2*wrong+4e-13
            profiles.append(contrast)
        powers.append(dict(records_per_sheet=copies,herald_yield_given_gates=total/(2*q*n),
                           good_joint_mass=good/(2*q*n),wrong=wrong,
                           product_cos_sin=profiles))
    return dict(orders=[q,n],second_power=flip,held_same_plane=True,rows=powers)


def times(z,w):
    return (z[0]*w[0]-z[1]*w[1],z[1]*w[0]+z[0]*w[1])


def winding_certificate(q,a,b,c):
    """Trace q directed rational rotations and add their signed ray crossings exactly."""
    assert a>0 and b>0 and q>=5
    x,y = 1,0
    winding = 0
    for _ in range(q):
        u,v = times((x,y),(a,b))
        # Positive quadrant-step < π/2 makes y<0→v>=0 an increasing
        # crossing of the positive real ray when u>0, also at the endpoint.
        winding += int(y<0 and v>=0 and u>0)
        x,y = u,v
    scale = c**q
    if x<=0 or winding+int(y<0)!=1:
        return None
    # q*phi differs from 2π by signed principal endpoint arg. Since |arg|
    # < π/2 and |arg| <= π/2 |sin(arg)| < 2 |sin(arg)|, use rational enclosure.
    return Fraction(2*abs(y),q*scale)


def integer_search(q,den):
    """Finite search by integer tests alone; no trigonometric or phase table is needed."""
    feasible = []
    for num in range(1,den):
        a,b,c = den**2-num**2,2*den*num,den**2+num**2
        common = math.gcd(math.gcd(a,b),c)
        a,b,c = a//common,b//common,c//common
        bound = winding_certificate(q,a,b,c)
        if bound is None:
            continue
        feasible.append((bound,a,b,c))
    measured,a,b,c = min(feasible)
    assert abs(math.atan2(b,a)-math.tau/q) <= float(measured)+2e-15
    return dict(order=q,denominator_grid=den,selected=[a,b,c],
                winding_count=1,certified_angle_error=str(measured),
                search_only_used_integers=True)


def main(directory):
    results = dict(cases=[case(q) for q in (5,7,8,12)],
                   relabel_controls=[ambiguity(q) for q in (5,7,8,12)],
                   compositum=[joint_clock(q,n,sign) for q,n in ((5,7),(8,12))
                               for sign in (1,-1)],
                   integer_only_primitive_target=[integer_search(q,m) for q in (5,7,8,12)
                                                  for m in (16,64,128)],
                   theorem="On a retained cyclic sheet and a separate two-real-coordinate plane, "
                   "coherently route T of a fixed generator on one arm and the rational R=(aI+bJ)/c "
                   "on the other. Apply H to the arm before and after, accepting its plus output. "
                   "The complete port pair is (T⊗I±I⊗R)/2. The commuting operators share joint "
                   "sectors (k,s); T acts by exp(2πik/q), J by s i. Born conditioning multiplies "
                   "their weights by p_ks=(1+cos(2πk/q−sφ))/2. The localized real launch gives "
                   "weight 1/(2q) per sector. For |φ−2π/q|<π/q the maximizers are the two "
                   "correlated pairs k=s mod q. Put G=cos²(delta/2), B=cos²((2π/q−delta)/2) "
                   "for delta=absolute angle error. After r retained plus records wrong/correct "
                   "odds ≤(q−1)(B/G)^r, correct joint mass G^r/q. Choosing angle error O(1/r) "
                   "makes correct mass approach 1/q at this fixed order. At fixed nonzero "
                   "angle mismatch G<1, insisting on indefinitely many bright records kills yield. "
                   "For arbitrary input replace 1/q by its prior on the correlated subspace; "
                   "zero initial overlap cannot be created. A single fresh localized read always "
                   "has probability 1/2 and resetting every record gives 2^-r. A complete "
                   "ordinary folded sheet preparation uncorrelated with the rebit initially has "
                   "only half its weight in the wanted chiral relation.",
                   readout="After accepting, compare a held power T^d with I on the reference "
                   "arm to obtain cosine contrast, or with the real signed quarter-turn J "
                   "for sine contrast. Both survive global conjugation since s changes with k. "
                   "Both can be negative; neither is an absolute choice of complex square root "
                   "of -1. Two sheets calibrated on the SAME plane align their chiral signs "
                   "and powers of their product yield cosine and sine on the joint cyclotomic "
                   "order. Independent uncorrelated planes would not align those signs. "
                   "Conditioned wrong mass η perturbs any contrast by at most 2η. The "
                   "operational field generated by these limiting contrasts is the real "
                   "field Q(cos(2π/q),sin(2π/q)), the maximal real subfield of Q(zeta_lcm(q,4)); "
                   "it does not give arbitrary complex numbers as probabilities. Repeated "
                   "coherent synthesis and additional fields can extend the available apparatus.",
                   gate="For Pythagorean a²+b²=c², pad K=2^ceil(log2(|a|+|b|)). Reuse the "
                   "native Walsh-signed SELECT structure. Acted block: |a| labels implement "
                   "sign(a)I, |b| labels sign(b)J; idle block: c labels implement I; all other "
                   "labels flip the blank validity bit reversibly. Two full-index Walsh layers "
                   "and one common projector onto flag-zero/index-zero realize success Kraus "
                   "(c/K)(R direct-sum I). Full complement is retained as one outcome, never "
                   "reading a distinguishing data/name flag. All code input states have the same "
                   "pass probability p=c²/K²>1/8. For retry use the actual inverse W†, with J†=−J; "
                   "this SELECT need not be an involution. Alternating W†/W and coarse anchor reads "
                   "on a failed attempt gives residual (1−p)(1−2p(1−p))^N, expected 1+1/p calls "
                   "when 0<p<1. The sheet shift is separately applied only after a successful "
                   "rotation port, while the coherent comparison arms remain unread. Gate retries "
                   "and timeout are separate from subsequent plus/minus read. The two arms need "
                   "matched phase, timing and discarded-route information.",
                   finite_apparatus="Stereographic slope rounding with denominator m and an exact "
                   "signed quarter-turn gives rational orthogonals within 1/m chord distance, "
                   "including clocked idle blocks. A known finite circuit of L such plane rotations "
                   "and signed permutations, with ordinary common projectors, changes its "
                   "unconditional instrument probabilities by at most L/m in total variation "
                   "by telescoping contractive unitaries and retaining an outcome register. "
                   "General finite complex unitaries can be realified and decomposed into finitely "
                   "many real plane rotations and signed permutations; synthesis needs addressable "
                   "two-coordinate pairs and spectator matching. Finite rational programs give "
                   "exact rational laws on rational localized real input, even when the named target "
                   "limit has algebraic records. Conditional probabilities also need the original "
                   "herald mass bounded away from zero. Compilation alone does not establish "
                   "the probability law or choose an absolute field embedding.",
                   grounding="The fundamental angular target can be constructed as the smallest "
                   "positive order-q turn relative to a chosen oriented circle. A physical "
                   "synthesizer needs held addressable I,J and the fixed sheet stroke plus "
                   "coherent controlled use. For the examples an additional finite program "
                   "search uses only integer operations: enumerate rational rotations in the "
                   "first quadrant, count crossings of the positive real ray under q powers, "
                   "and require the nearest unwrapped return to have winding one. A final "
                   "point with positive real part bounds angular error by "
                   "2*abs(Im(R^q))/q. Refining the grid yields arbitrary accuracy by density "
                   "and the simple oriented order-q root. A finite grid and integer test "
                   "need no numerical sine/cosine input. The quarter orientation and order "
                   "are operational assumptions. Other instruments still require matched "
                   "controls or a calibrated operationally equivalent apparatus. "
                   "Only the relative sheet/reference chirality is measured. Complementing the "
                   "real plane or simultaneously relabeling the entire sheet apparatus leaves "
                   "the experiment invariant. Without the held comparison arm, native powers "
                   "give ordered folded cosines; they do not themselves supply this synchronized "
                   "reference or its heralded state preparation.")
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'rational_phase_comparison.json').write_bytes((json.dumps(results,indent=2,allow_nan=False)+'\n').encode())


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)
