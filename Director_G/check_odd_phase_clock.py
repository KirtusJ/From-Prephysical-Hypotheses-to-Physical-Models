"""Prepare and test the physical Fourier pair +/-1 on an odd nearest-hop cycle.

Run python -B check_odd_phase_clock.py OUTPUT_DIRECTORY. The finite circuit
uses integer amplitudes; a site's branch bit and motor direction are distinct.
"""
import argparse
import cmath
import hashlib
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


def least_signed(value, size):
    return (value + size // 2) % size - size // 2


def half_lift(size, shift):
    return least_signed(shift * ((size + 1) // 2), size)


def box_length(size):
    if size == 3:
        return 1
    return 1 << ((size // 4).bit_length() - 1)


def gate(state, flip):
    """A coin or motor XOR gate is a bijection of the complete mode labels."""
    out = {flip(x, b, motor): amp for (x, b, motor), amp in state.items()}
    assert len(out) == len(state)
    return out


def hadamard(state):
    out = {}
    for (x, b, motor), amp in state.items():
        for port in (0, 1):
            key = (x, port, motor)
            out[key] = out.get(key, 0) + (-amp if b == port == 1 else amp)
    return {key: a for key, a in out.items() if a}


def motor_hop(state, size, minus_if):
    # The clean motor starts right. Set its direction reversibly, stream
    # exactly one edge, then undo the XOR using the preserved branch bit.
    def toggle(x, b, m):
        return x, b, m ^ int(minus_if(b))

    assert all(m == 0 for _, _, m in state)
    routed = gate(state, toggle)
    moved = gate(routed, lambda x, b, m: ((x + 1 - 2*m) % size, b, m))
    restored = gate(moved, toggle)
    assert all(m == 0 for _, _, m in restored)
    return restored


def fixed_delay(state, size, lift, depth):
    steps = 2*abs(lift)
    assert steps <= depth and (depth - steps) % 2 == 0
    if lift:
        # First half sends the two arms oppositely. The common second
        # half returns arm 0 and advances arm 1 by exactly 2*lift.
        for _ in range(abs(lift)):
            state = motor_hop(state, size, lambda b: b == (0 if lift > 0 else 1))
        for _ in range(abs(lift)):
            state = motor_hop(state, size, lambda b: lift < 0)
    for _ in range((depth - steps)//2):
        state = motor_hop(state, size, lambda b: False)
        state = motor_hop(state, size, lambda b: True)
    return state


def box_seed(size):
    width = box_length(size)
    state = {(0, 0, 0): 1}
    for bit in reversed(range(width.bit_length() - 1)):
        gap = 1 << bit
        state = fixed_delay(hadamard(state), size, gap, 2*gap)
        # Each generated address is even and fits without wrapping.
        state = gate(state, lambda x, b, m: (x, b ^ ((x >> (bit+1)) & 1), m))
        assert all(b == m == 0 for _, b, m in state)
    assert state == {(2*j, 0, 0): 1 for j in range(width)}
    return tuple(int((x, 0, 0) in state) for x in range(size))


def probe(seed, shift):
    size = len(seed)
    state = {(x, 0, 0): a for x, a in enumerate(seed) if a}
    state = fixed_delay(hadamard(state), size, half_lift(size, shift), size-1)
    state = hadamard(state)
    ports = [tuple(state.get((x, b, 0), 0) for x in range(size)) for b in (0, 1)]
    for b, vector in enumerate(ports):
        assert vector == tuple(seed[x] + (1-2*b)*seed[(x-shift) % size] for x in range(size))
    assert sum(norm(v) for v in ports) == 4*norm(seed)
    return ports


def norm(seed):
    return sum(a*a for a in seed)


def weight(seed, k):
    size = len(seed)
    amplitude = sum(a*cmath.exp(-2j*math.pi*x*k/size) for x, a in enumerate(seed))
    return abs(amplitude)**2/(size*norm(seed))


def sign_mask(h, size):
    return 1 if abs(least_signed(h, size)) <= size//4 else -1


def means(size):
    length = 2*(size//4)+1
    values = [(2*length-size)/size]
    for k in range(1, size//2+1):
        values.append(2*math.sin(math.pi*k*length/size)/(size*math.sin(math.pi*k/size)))
    assert abs(values[1]-1/(size*math.sin(math.pi/(2*size)))) < 1e-13
    assert values[1] > 5/8 and all(abs(v) <= 1/3+1e-13 for k, v in enumerate(values) if k != 1)
    return values


def binomial_pass(p, count):
    # Aggregate independent +/-1 scores, accepting exactly if mean > 1/2.
    return math.fsum(math.comb(count, z)*p**z*(1-p)**(count-z)
                     for z in range(3*count//4+1, count+1))


def mean_checks(size):
    predicted = means(size)
    error = max(abs(mu - sum(sign_mask(h,size)*math.cos(math.tau*k*h/size)
                             for h in range(size))/size) for k,mu in enumerate(predicted))
    assert error < 1e-13
    return dict(M=size, interval_length=2*(size//4)+1, folded_score_means=predicted,
                direct_sum_max_abs_error=error)


def first_depths(size):
    # Independent enumeration of reachable displacements from a localized
    # cell, with no waiting edges, using every elapsed depth in order.
    rel = [None]*size
    fixed = [None]*size
    positions = {0}
    for t in range(size+1):
        for x in positions:
            if 0 in positions and fixed[x] is None:
                fixed[x] = t
            for y in positions:
                h = (y-x) % size
                if rel[h] is None:
                    rel[h] = t
        positions = {(x+step) % size for x in positions for step in (-1,1)}
    if size%2:
        expect = [abs(half_lift(size,h)) for h in range(size)]
        assert rel == expect and fixed == [2*u for u in expect]
    else:
        assert all((r is None) == bool(h%2) for h,r in enumerate(rel))
        assert all((r is None) == bool(h%2) for h,r in enumerate(fixed))
    return dict(M=size, relative_minimum_by_h=rel, fixed_minimum_by_h=fixed)


@lru_cache(maxsize=256)
def physical_tree(seed, remaining, score):
    # Identically zero amplitude histories have zero joint weight. Retain
    # their leaf multiplicity alongside live accepted and rejected histories.
    size = len(seed)
    if not norm(seed):
        return (0,0,(2*size)**remaining,0,0)
    if not remaining:
        passed = score > 0
        return (norm(seed) if passed else 0, 0 if passed else norm(seed),
                0, int(passed), int(not passed))
    totals = [0]*5
    for h in range(size):
        for b, output in enumerate(probe(seed,h)):
            # Add 2*X-1 each time, so final positivity gives mean X>1/2.
            res = physical_tree(output,remaining-1,score+2*(1-2*b)*sign_mask(h,size)-1)
            for i,v in enumerate(res):
                totals[i]+=v
    return tuple(totals)


def compare_tree(size, depths):
    seed = box_seed(size)
    prior = [weight(seed,k) for k in range(size)]
    mu = means(size)
    out = []
    for depth in depths:
        yes,no,zero,yes_count,no_count = physical_tree(seed,depth,0)
        den = norm(seed)*(4*size)**depth
        assert yes+no == den and zero+yes_count+no_count == (2*size)**depth
        prediction = sum(w*binomial_pass((1+mu[min(k,size-k)])/2,depth)
                         for k,w in enumerate(prior))
        assert abs(yes/den-prediction)<1e-13
        out.append(dict(M=size,reports=depth,accept=str(Fraction(yes,den)),reject=str(Fraction(no,den)),
                        live_accept_leaves=yes_count,live_reject_leaves=no_count,
                        zero_mass_leaves=zero,all_setting_port_histories=(2*size)**depth,
                        independent_spectral_accept=prediction))
    physical_tree.cache_clear()
    return out


def finite_spectra(size):
    width = box_length(size)
    def box_weight(k):
        if k == 0:
            return width/size
        return (math.sin(math.tau*k*width/size)/math.sin(math.tau*k/size))**2/(width*size)

    mu = means(size)
    wk = [box_weight(k) for k in range(size//2+1)]
    total = wk[0]+2*math.fsum(wk[1:])
    assert abs(total-1)<1e-12
    target = 2*wk[1]
    assert target >= 2/math.pi**2 - 1e-14
    rows=[]
    for probes in (1,7,63):
        passed = [binomial_pass((1+v)/2,probes) for v in mu]
        joint=target*passed[1]
        acc=wk[0]*passed[0]+2*math.fsum(w*t for w,t in zip(wk[1:],passed[1:]))
        rows.append(dict(probes=probes,accept=acc,target_and_accept=joint,
                         conditional_target=joint/acc,total_scheduled_hops=2*(width-1)+probes*(size-1)))
    return dict(M=size,box_width=width,preparation_hops=2*(width-1),target_prior=target,
                full_weight_sum=total,settings_per_probe=size,hop_depth_per_probe=size-1,reads=rows)


def check_ports(size):
    seeds={'localized':tuple(int(j==0) for j in range(size)),
           'box':box_seed(size),
           'signed':tuple((j%5)-2 for j in range(size))}
    rows={}
    for name,seed in seeds.items():
        data=[]
        for h in range(size):
            ports=probe(seed,h)
            den=4*norm(seed)
            spectral_plus=sum(weight(seed,k)*math.cos(math.pi*k*h/size)**2 for k in range(size))
            assert abs(spectral_plus-norm(ports[0])/den)<1e-13
            data.append(dict(h=h,even_lift=2*half_lift(size,h),
                             min_hops=2*abs(half_lift(size,h)),scheduled_hops=size-1,
                             plus=str(Fraction(norm(ports[0]),den)),
                             minus=str(Fraction(norm(ports[1]),den)),
                             plus_counts=list(ports[0]),minus_counts=list(ports[1])))
        rows[name]=dict(seed=list(seed),rows=data)
    return dict(M=size,inputs=rows)


def sampler(size):
    bits=(size-1).bit_length()
    level=1<<bits
    labels=[k for k in range(level) if k<size]
    assert labels==list(range(size))
    return dict(M=size,bits_per_draw=bits,accept_per_draw=str(Fraction(size,level)),
                expected_draws=str(Fraction(level,size)),
                pending_after_three_draws=str(Fraction(level-size,level)**3),
                fixed_bits_modulo_counts=[sum(v%size==h for v in range(level)) for h in range(size)])


def main(directory):
    direct=[check_ports(m) for m in (3,5,7,9,11,17)]
    trees=[row for m,steps in ((3,(1,2,3)),(5,(1,2,3)),(9,(1,2))) for row in compare_tree(m,steps)]
    rows=[finite_spectra(m) for m in (3,5,7,9,11,17,31,33,65,127,129,255,511,1025)]
    # A delocalized uniform input is purely k=0. A finite test can accept
    # this input. Its accepted ensemble still has exactly zero target weight.
    uniform=(1,)*5
    uniform_accept=sum(Fraction(norm(p),4*norm(uniform)*5)
                       for h in range(5) for b,p in enumerate(probe(uniform,h))
                       if (1-2*b)*sign_mask(h,5)>0)
    assert uniform_accept==Fraction(3,5)
    # A perfectly resolved which-arm tag prevents the two paths from adding
    # in a common coordinate. Equal total after either analyzer output.
    for h in range(5):
        which_arm = tuple(uniform[(x-h) % 5] for x in range(5))
        for sign in (1,-1):
            tagged = [(a,sign*b) for a,b in zip(uniform,which_arm)]
            assert Fraction(sum(a*a+b*b for a,b in tagged),4*norm(uniform))==Fraction(1,2)
    result=dict(
        assumptions="Odd periodic cycle, localized launch, real normalized squared coordinate law, balanced branch Hadamards, a clean transport direction bit, reversible control by the preserved branch and addressed reversible branch erasure. One microscopic motion tick streams every occupied cell by exactly one edge. Local gate, record and classical setting generation layers have separate costs.",
        fixed_frame="For u the least signed representative of h/2 modulo M, route 0 and 1 oppositely for |u| ticks, then both in sign(u) for |u| ticks. Branch 0 stays and branch 1 advances by 2u overall. XOR the clean motor before and after every hop. Add common (+1,-1) pairs to equalize the physical duration of every setting at M-1 hops. Analyze b with H and retain both final ports.",
        depth_proof="At n ticks each arm displacement lies in {-n,-n+2,...,n}. The two-arm displacement difference is even with magnitude at most 2n, giving n>=|u| up to a common translation. Opposite ballistic arms attain it. For fixed endpoints 0,h, even n allows the shortest even lift 2u, requiring n>=2|u|. An odd n reaching 0 on an odd ring requires n>=M, whereas 2|u|<=M-1. For an even ring odd relative shifts are impossible at any common elapsed time from one parity.",
        score="Each fresh, independent uniform h in Z/M multiplies the measured +/-1 port sign by +1 if |h|_M<=floor(M/4), else -1. Conditional on any character k, the Z expectation is cos(2*pi*k*h/M). The sheet persists and the likelihoods multiply on a character. Accept iff 2*sum(X)>n after n probes; this is the integer threshold mean >1/2. The guarantee is averaged over the random settings and ports; an arbitrarily selected recorded setting string need not separate any sectors.",
        gap_proof="Let L=2 floor(M/4)+1=(M +/-1)/2. The mean at k=0 is (2L-M)/M. At folded k>=1 it is 2*sin(pi*k*L/M)/(M*sin(pi*k/M)). Thus mu_1=1/(M*sin(pi/(2M)))>=2/pi>5/8. For k=2, the absolute mean is 1/(M*cos(pi/M))<1/3 when M>=5. For k>=3, M*sin(pi*k/M)>=2k for k<=M/2, giving absolute mean <=1/k<=1/3. At M=3 the sole distractor is k=0. Hoeffding for X in [-1,1] gives each-class error <= exp(-n/128). The alternative threshold 23/48 uses equal conservative margins 7/48 and yields exp(-49n/4608).",
        yield_bound="For prior W and per-class error eta, true joint acceptance >= W(1-eta); wrong joint acceptance <= (1-W)eta. For positive acceptance the posterior wrong fraction is <= (1-W)eta/[W(1-eta)+(1-W)eta] when the denominator is positive. A localized seed has W=2/M. Without a lower bound on W there is no positive uniform yield of correctly prepared target and no promised purity upon acceptance.",
        box_proof="For odd M>=5, B is the largest power of two <= M/4, hence M/8<B<=M/4. Put equal signed amplitudes on 0,2,...,2(B-1) using log2(B) Hadamards and addressed XOR erasure after each fixed-frame fanout at cost 2(B-1) motion ticks. For M=3 put B=1. The target pair weight is 2 sin^2(2*pi*B/M)/(M B sin^2(2*pi/M)). On [pi/4,pi/2] concavity gives sin^2(x)>=2x/pi; sin(2*pi/M)<=2*pi/M. Hence W>=2/pi^2 uniformly; M=3 gives 2/3 directly. The same ring and physical T read are used throughout. An untracked address-dependent phase or retained route tag changes the prepared spectrum.",
        setting_source="Draw b=ceil(log2(M)) independent fair bits. Reject candidate integers >=M and try again; each accepted label has probability 1/M. The number of attempts is geometric independent of the accepted label, with finite mean 2^b/M<2. Generate all settings before launch if fixed elapsed walk time matters. A cap retains a pending outcome; sampling by remainder alone is biased. Calibration, random settings and coherent controls are supplied physical premises.",
        cost="At fixed eta and target prior W>=2/pi^2 the scheduled motion depth 2(B-1)+n(M-1) is linear in M; each probe additionally needs two comparison Hadamards and motor/branch gates. Compiled motor toggles have bounded local depth per hop. Counting each motor control as time adds only a constant factor. Fresh independent launches may be needed for a specified eventual successful output; arbitrary input has no prior guarantee.",
        physical_ports=direct,all_record_trees=trees,exact_depths=[first_depths(m) for m in range(3,20)],
        direct_score_means=[mean_checks(m) for m in range(3,34,2)],spectral_orders=rows,
        fair_bit_samplers=[sampler(m) for m in (3,5,7,9,17)],
        adverse=dict(pure_constant_M5_one_probe_accept=str(uniform_accept),
                     pure_constant_M5_conditional_target="0",
                     force_setting_to_zero="At h=0 the + port has probability one for all inputs and the score is +1. The empirical gap needs uniform independent settings.",
                     leaked_route_tag="If a disjoint unread tag marks the two interfering routes, the split outcomes are 1/2 independent of k, and each full score has mean zero.",
                     modulo_sampling="The sampler rows include nonuniform counts when fixed-width random bits are reduced modulo M."))
    directory.mkdir(parents=True,exist_ok=True)
    target=directory/"odd_phase_clock.json"
    target.write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())
    print(target,hashlib.sha256(target.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)


