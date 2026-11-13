"""Check the cost and record yield of Fourier-pair preparation on a dyadic cycle.

Run python -B check_clock_bandwidth.py <output-directory>. All small physical
record counts use signed integer sheet amplitudes. The spectral expressions
use floating point only after the input, analyzer and clock have been defined.
"""

import argparse
import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path


def delays(M):
    assert M >= 4 and M & (M - 1) == 0
    return [M >> j for j in range(3, M.bit_length())]


def distribute(M):
    """One-bit addressed unitary fanout, with a signed initial high bit."""
    shift_count = 0
    split_count = 0
    # Tuple keys are (sheet coordinate, coin); the common amplitude scale
    # after s Hadamards is 2^(-s/2).
    modes = {(0, 0): 1}
    for bit in reversed(range(M.bit_length() - 1)):
        d = 1 << bit
        branches = {}
        for (x, coin), weight in modes.items():
            assert coin == 0 and x % (2*d) == 0
            for label in (0, 1):
                sign = -1 if bit == M.bit_length() - 2 and label else 1
                branches[x, label] = sign * weight
        for _ in range(d):
            branches = {((x+b) % M, b): w for (x,b),w in branches.items()}
        modes = {(x, b ^ ((x >> bit) & 1)): w for (x,b),w in branches.items()}
        assert len(modes) == 2**(split_count+1)
        assert all(coin == 0 for _,coin in modes)
        shift_count += d
        split_count += 1
    sheets = [modes[x, 0] for x in range(M)]
    assert sheets == [1]*(M//2) + [-1]*(M//2)
    assert shift_count == M-1 and 2**split_count == M
    return sheets


def weights(M, kind):
    if kind == "addressed":
        return [0.0 if k%2 == 0 else 4/(M*math.sin(math.pi*k/M))**2 for k in range(M)]
    if kind == "localized_odd":
        # The odd projector is itself a herald of unconditional probability 1/2.
        return [1/M if k%2 else 0.0 for k in range(M)]
    if kind == "localized_unfiltered":
        return [1/M]*M
    raise ValueError(kind)


def majority(p, r):
    return math.fsum(math.comb(r,h)*p**h*(1-p)**(r-h) for h in range(r//2+1, r+1))


def outcomes(M, r, kind="addressed", noise=0.0, extra_shift=0, grow_repeats=False):
    assert r >= 1 and r%2 and 0 <= noise <= 0.5
    clock = delays(M)
    initial = weights(M, kind)
    accepted = []
    for k, wk in enumerate(initial):
        prob = wk
        for i,d in enumerate(clock):
            if wk == 0:
                break
            pplus = math.cos(math.pi*(k*(d+extra_shift) % M)/M)**2
            count = r + 2*i if grow_repeats else r
            prob *= majority(noise+(1-2*noise)*pplus, count)
        accepted.append(prob)
    joint = accepted[1]+accepted[-1]
    total = math.fsum(accepted)
    return dict(initial_total=math.fsum(initial), initial_target=initial[1]+initial[-1],
                accepted=total, accepted_target=joint, accepted_wrong=total-joint,
                target_given_accepted=joint/total, target_acceptance=joint/(initial[1]+initial[-1]))


def integer_records(M, r, kind):
    # The plus and minus Kraus numerators commute at a scale. Group ordered
    # records by plus count h, retaining their exact binomial multiplicities.
    # All detectors are read at a common terminal time. Rejected groups stay
    # in the unconditional closure check.
    delta = [1]+[0]*(M-1)
    denom = 1
    if kind == "addressed":
        seed = distribute(M)
        denom = M
    elif kind == "localized_odd":
        seed = delta[:]
        seed[M//2] = -1
        denom = 4
    else:
        seed = delta

    def shifted_sum(x, d, sign):
        return [v+sign*x[(j-d)%M] for j,v in enumerate(x)]

    settings = delays(M)
    denom *= 4**(r*len(settings))
    accepted = rejected = 0
    empty_group_count = 0
    acc_target = 0.0
    for counts in product(range(r+1), repeat=len(settings)):
        x=seed
        multiplicity=1
        for d, h in zip(settings,counts):
            multiplicity *= math.comb(r,h)
            for sign,n in ((1,h),(-1,r-h)):
                for _ in range(n):
                    x = shifted_sum(x,d,sign)
        raw = multiplicity*sum(v*v for v in x)
        if raw == 0:
            empty_group_count += 1
        if all(h>r//2 for h in counts):
            accepted += raw
            # Independent direct Fourier projections of the signed terminal
            # sheet amplitudes, including every position and both orientations.
            c = math.fsum(x[j]*math.cos(2*math.pi*j/M) for j in range(M))
            s = math.fsum(x[j]*math.sin(2*math.pi*j/M) for j in range(M))
            acc_target += 2*multiplicity*(c*c+s*s)/(M*denom)
        else:
            rejected += raw
        # Anti-periodicity of every postmeasurement odd state.
        if kind != "localized_unfiltered":
            assert all(x[j] == -x[j+M//2] for j in range(M//2))
    accepted, rejected = Fraction(accepted,denom), Fraction(rejected,denom)
    assert accepted+rejected == (Fraction(1,2) if kind=="localized_odd" else 1)
    spectral = outcomes(M,r,kind)
    assert abs(float(accepted)-spectral["accepted"]) < 1e-12
    assert abs(acc_target-spectral["accepted_target"]) < 1e-12
    return dict(M=M,repeats_per_scale=r,initial=kind,accepted_exact=str(accepted),
                rejected_exact_after_initial_preparation=str(rejected),target_joint_direct_dft=acc_target,
                number_of_grouped_complete_records=(r+1)**len(settings),
                exactly_zero_mass_groups=empty_group_count)


def uniform_bounds(r):
    # For ±1, error of the majority decision at scale j is at most
    # (2 sqrt(p_j(1-p_j)))^r = sin(2*pi/2^j)^r. At each mistaken odd
    # residue's first conflicting scale, this bounds its acceptance instead.
    worst = 2**(-r/2)
    good_loss = worst + (math.pi/8)**r/(1-2**(-r))
    wmin = 8/math.pi**2
    accepted_target = wmin*max(0,1-good_loss)
    accepted_bad = (1-wmin)*worst
    return dict(odd_false_acceptance_upper=worst,target_rejection_upper=min(1,good_loss),
                target_joint_lower=accepted_target,acceptance_lower=accepted_target,
                conditional_target_lower=accepted_target/(accepted_target+accepted_bad))


def first_conflict(M):
    scale_count=M.bit_length()-1
    count=0
    for k in range(1,M,2):
        if k in (1,M-1):
            continue
        j=next(j for j in range(3,scale_count+1) if k%(1<<j) not in (1,(1<<j)-1))
        assert k%(1<<j) in ((1<<(j-1))-1,(1<<(j-1))+1)
        count+=1
    return count


def block_average(M, r):
    # One pass with binary delays 1,2,...,M/4 gives the coherent average
    # over a contiguous block of M/2 sites, on its all-plus report.
    B=M//2
    initial=weights(M,"addressed")
    tagged=[w*(1/(B*math.sin(math.pi*k/M)))**(2*r) if w else 0 for k,w in enumerate(initial)]
    y=math.fsum(tagged)
    pair=tagged[1]+tagged[-1]
    return dict(repeats=r,raw_acceptance=y,conditional_target=pair/y,
                analyzer_unit_steps=r*(B-1),single_target_pass=(1/(B*math.sin(math.pi/M)))**2)


def noisy_schedule():
    # Reusing the scale-specific Bernoulli probabilities avoids enumerating
    # full detector histories. Source preparation remains ideal throughout.
    examples = []
    limits = {}
    for noise in (0.0, 0.05, 0.2, 0.5):
        bad = noise + (1-2*noise)*math.sin(math.pi/8)**2
        beta = 2*math.sqrt(bad*(1-bad))
        r = 15
        if noise < 0.5:
            while beta**r/(1-beta*beta) > 0.05:
                r += 2
            loss = beta**r/(1-beta*beta)
            w = 8/math.pi**2
            joint_lower = w*(1-loss)
            limits[str(noise)] = dict(r=r,dark_upper=bad,beta=beta,
                    target_rejection_upper=loss,wrong_acceptance_upper=beta**r,
                    target_joint_lower=joint_lower,conditional_purity_lower=
                    joint_lower/(joint_lower+(1-w)*beta**r))
        else:
            limits[str(noise)] = dict(r=r,dark_upper=bad,beta=beta,
                    criterion="The reports are independent fair bits; sector likelihoods coincide.")
        for M in (8, 32, 4096):
            ds = delays(M)
            counts = [r+2*i for i in range(len(ds))]
            analyzer = sum(n*d for n,d in zip(counts,ds))
            probes = sum(counts)
            assert 4*analyzer <= M*(r+2)
            assert probes == len(ds)*(r+len(ds)-1)
            o = outcomes(M,r,noise=noise,grow_repeats=True)
            if noise < 0.5:
                assert o["target_acceptance"] >= 1-loss-1e-12
                assert o["accepted_wrong"] <= (1-o["initial_target"])*beta**r+1e-12
                assert o["target_given_accepted"] >= limits[str(noise)]["conditional_purity_lower"]-1e-12
            else:
                assert abs(o["accepted"]-2**(-len(ds))) < 1e-12
                assert abs(o["target_given_accepted"]-o["initial_target"]) < 1e-12
            examples.append(dict(M=M,flip_probability=noise,base_repeats=r,repeats=counts,
                    analyzer_unit_shifts=analyzer,total_unit_shifts=M-1+analyzer,
                    probes=probes,analyzer_hadamards=2*probes,**o))
    return dict(proof="Each ideal report is flipped independently with symmetric probability c. The true Kraus update is unchanged; only the recorded label can flip. For c<1/2 the target's unfavorable probability and each wrong residue's favorable probability at its first conflict are bounded by d'=c+(1−2c)sin²(pi/8)<1/2. Let beta=2 sqrt(d'(1−d')). With r_j=r+2(j−3) and odd r, the majority tail at that scale is at most beta^r_j. The target's total rejection is at most beta^r/(1−beta²), by the union bound. Each wrong odd residue has acceptance at most beta^r. This applies for every cycle size without independence between potential failures across settings once their conditional bounds hold. The Bernoulli calculation does require independent flips within a scale and the stated ideal instrument.",
        clock="For q=log2 M and s=q−2 scales, sum of r_j is s(r+s−1). Analyzer shifts cost at most M(r/4+1/2); the M−1 addressable preparation shifts are additional. At fixed c<1/2 and prescribed error this gives O(M) shift cost and O(r log M+log² M) readout, reset, and Hadamard overhead. The bounds deteriorate as c approaches 1/2. Pure phase errors, correlated flips, changes to the physical projection, and coherent gate errors require separate models.",
        uniform_examples=limits,finite_cases=examples)


def main():
    exact = [integer_records(M,r,kind) for M in (4,8,16,32) for r in (1,3)
             for kind in ("addressed","localized_odd","localized_unfiltered")]
    bounds={r:uniform_bounds(r) for r in (1,3,5,9,15)}
    tables=[]
    for M in (4,8,16,32,64,256,1024,4096):
        first=first_conflict(M)
        q=M.bit_length()-1
        assert first==M//2-2 and sum(delays(M))==M//4-1
        rows=[]
        for r in (1,3,5,9,15):
            o=outcomes(M,r)
            assert abs(o["initial_total"]-1)<2e-12
            assert o["initial_target"]+1e-13>=8/math.pi**2
            assert o["accepted_target"]+1e-13>=bounds[r]["target_joint_lower"]
            assert o["target_given_accepted"]+1e-13>=bounds[r]["conditional_target_lower"]
            shifts=M-1+r*(M//4-1)
            probes=r*(q-2)
            rows.append(dict(repeats_per_scale=r,**o,preparation_unit_shifts=M-1,
                        analyzer_unit_shifts=r*(M//4-1),total_unit_shifts=shifts,
                        split_hadamards=q,analyzer_hadamards=2*probes,analyzer_reads=probes,
                        expected_unit_shifts_per_accept=shifts/o["accepted"]))
        tables.append(dict(M=M,first_conflict_other_odd_residues=first,majority=rows,
                           all_plus_block=[block_average(M,r) for r in (1,3,9)]))
    controls=[]
    for M in (8,16,32,256):
        loc=outcomes(M,9,"localized_odd")
        raw=outcomes(M,9,"localized_unfiltered")
        # The lowest-bit input class bounds the prior log scale. At each
        # refinement the two lifts k and k+2^(j-1) have complementary plus
        # likelihoods, while all preceding scale likelihoods coincide.
        # Opposite majorities exhaust the ordered repetitions for odd r.
        assert abs(loc["accepted"]-2/M)<1e-13 and abs(raw["accepted"]-4/M)<1e-13
        bad=outcomes(M,3,extra_shift=1)
        half_drift=outcomes(M,3,extra_shift=M//2)
        baseline=outcomes(M,3)
        noisy=outcomes(M,3,noise=.1)
        assert loc["accepted_target"] <= 2/M+1e-12
        controls.append(dict(M=M,localized_odd_then_majority=loc,localized_accept_even_alias=raw,
                         addressed_without_drift=baseline,every_delay_one_site_too_long=bad,
                         every_delay_half_a_cycle_too_long=half_drift,independent_ten_percent_record_flip=noisy))
    return dict(scope="Fixed-coordinate clock preparation and discrimination of the unordered Fourier pair k=±1 using square-weight statistics. Coordinate-controlled erasure supplies an address resource. Once initialized the analyzer uses only integer translations and balanced real coins.",
        cycle="M=2^q, q>=2. M=4 has only the desired odd pair and no analyzer probes. M=2 has one self-conjugate frequency and is outside the pair construction.",
        protocol="Initialize sheet 0 and coin 0. For d=M/2,...,1 use a single balanced split, add a minus to the upper half at the first split, and conditionally move forward d unit ticks with the other arm held. At the endpoints coherently XOR the known address bit into the coin to uncompute it. The resulting signed sheet is +1 then -1 on the two halves, divided by sqrt(M). At scale j=3,...,q use controlled shift d=M/2^j between two Hadamards, read the coin and reset it. Repeat r odd times per scale and accept its majority-plus at every scale. A real state leaves conjugate orientations equally populated.",
        clock="Every microscopic sheet displacement is <=1, including the controlled stationary arm. Preparation uses M−1 unit shifts, q Hadamards, q address-conditioned local XOR layers and one sign flip. Analyzer uses r(M/4−1) unit shifts, 2r(q−2) balanced ticks and r(q−2) report/reset operations, scheduled equally for all histories. Read/reset and local address decoding must be priced separately if not single layers. No position measurement is made during fanout. The runtime resource is one coherent coin qubit along with the M-site clock and a classical record/counter. A free guess of an absolute clock site is not entailed by an unaddressed walk.",
        spectrum="For odd k the initial mass is 4/[M^2 sin^2(pi k/M)]; even k have zero. Desired pair total 8/[M^2 sin^2(pi/M)] is >=8/pi^2. Conditional on a character, the plus probability at scale j is cos^2(pi k/2^j). Orthogonality of characters makes complete-record likelihoods a mixture of independent Bernoulli likelihoods at fixed k.",
        guarantee="Every other odd k has a first j where it ceases to be ±1 mod 2^j. At that j it equals 2^(j−1)±1 mod 2^j. Its plus probability is the target’s minus probability. The majority tail bound [2 sqrt(p(1-p))]^r follows from Markov on the binomial generating function (with the trivial p=0 limit). The remaining target rejection series is bounded by sin x<=x. Hence at fixed r time O(Mr), and as r increases acceptance tends uniformly to the initial target mass while conditional purity tends uniformly to 1. For a prescribed error e, r=O(log(1/e)) and finite expected retries; exponent, confidence bounds and all tabulated resources concern ideal gates only.",
        translation_only="With a localized sheet and initially uncorrelated auxiliary registers, a complete translation-commuting instrument preserves sector populations when all outcomes are included. The prior mass of ±1 is 2/M. A herald whose conditional target weight is >=1−e can therefore have yield at most 2/[M(1−e)], also for adaptive multi-outcome selection. The deterministic addressed erasures in the preparation break that symmetry. A minus half-turn projector on a localized seed consumes M/2 unit shifts and has yield 1/2; localized control probabilities below include that success. For uniform odd prior each majority scale halves the surviving mass exactly: the residues k and k+2^(j−1) within every lift at scale j agree at prior scales and have complementary plus probabilities. Their majority probabilities sum to one for odd r. Thus the absolute yield from the localized seed with the preliminary odd herald is exactly 2/M including all target-report histories, for every r. Omitting that herald gives 4/M including even aliases.",
        alternate_filter="The all-plus block-of-length M/2 average uses M/2−1 unit shifts per pass. At odd k its amplitude magnitude is 1/[(M/2)sin(pi k/M)]. For M>=8 each undesired odd sector is suppressed relative to target by at most [sin(pi/8)/sin(3pi/8)]^2 per pass. Target acceptance per pass >=4/pi^2, and repeated all-plus herald yield tends to zero for fixed M>=8. The majority analyzer instead collects many accepted records.",
        adverse="The addressable protocol assumes aligned integer translations, a coherent stationary arm, reliable record readouts, and ideal address masks. Bare balanced steps forced to move on every sublattice need not implement the control. A persistent readout-flip floor makes all-scale acceptance of a target vanish at fixed r as log M grows. If flips are independent with probability c>0, every scale has false-rejection probability >=Pr(Bin(r,c)>r/2). Different clock-origin labeling or gain direction changes the named reference; the construction concentrates an unordered pair relative to the supplied geometry.",
        finite_integer_checks=exact,uniform_guarantees=bounds,finite_spectral_tables=tables,
        adverse_readouts=controls,independent_readout_noise=noisy_schedule())


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    out=parser.parse_args().output_directory
    out.mkdir(parents=True,exist_ok=True)
    result=main()
    target=out/"clock_bandwidth.json"
    target.write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())
    print(target)
