"""Run python -B check_common_ray_source.py OUTPUT_DIRECTORY (standard library)."""
import argparse
import cmath
import json
import math
from pathlib import Path

from check_clock_bandwidth import distribute


def crest(M, B, k):
    """Unit-norm signed box on sites [0,B), [B,2B), using the unitary DFT."""
    if k % M == 0 or (k*B) % M == 0:
        return 0.
    t = min(k % M, (-k) % M)
    return 2*math.sin(math.pi*((t*B) % M)/M)**4 / (M*B*math.sin(math.pi*t/M)**2)


def folded_sum(weights, K):
    M = len(weights)
    return math.fsum(w for k,w in enumerate(weights) if min(k,M-k) > K)


def direct_spectra():
    rows = []
    for M,B in ((16,4),(32,4),(64,16),(128,16),(256,64)):
        length = 2*B
        block = distribute(length)
        assert sum(block) == 0 and len(block) <= M
        literal = []
        for k in range(M):
            a = sum(w*cmath.exp(-1j*math.tau*((k*y)%M)/M) for y,w in enumerate(block))
            literal.append(abs(a)**2/(M*length))
        w = [crest(M,B,k) for k in range(M)]
        error = max(abs(v-u) for v,u in zip(w,literal))
        assert error < 1e-14 and abs(math.fsum(w)-1) < 1e-13 and literal[0]==0
        for k in range(1,M):
            assert w[k] <= M/(2*B*min(k,M-k)**2)+1e-14
        assert abs(sum(w[0::2])-.5)<1e-13
        if B == M//4:
            assert w[2]+w[-2] > 4/math.pi**2
        K = min(8,M//2-1)
        tail = folded_sum(w,K)
        assert tail <= M/(B*K)
        rows.append(dict(M=M,B=B,nonzero_sites=length,integer_numerators=block,
                         coherent_success=1,unit_conditional_shifts=length-1,
                         balanced_split_layers=length.bit_length()-1,cleared_address_bits=True,
                         largest_literal_weight_error=error,folded_weights=
                         [w[0]]+[w[k]+w[-k] for k in range(1,M//2)]+[w[M//2]],
                         even_weight=sum(w[0::2]),K=K,tail=tail,tail_upper=min(1.,M/(B*K))))
    return rows


def escape_controls():
    out = []
    for e in (5,7,9,11,13):
        M = 2**e
        K = 4
        for name,B in (("fixed_two_site_dipole",1),("sublinear_dipole",2**(e//2)),
                       ("half_of_circumference",M//4)):
            low = sum(crest(M,B,k) for k in range(-K,K+1))
            out.append(dict(M=M,B=B,source=name,low_window=K,weight_in_window=low,
                            zero_weight=crest(M,B,0),support_bound=(2*K+1)*2*B/M))
        # The unfiltered delta and unsigned uniform source have completely different limits.
        out.append(dict(M=M,source="localized_sheet_delta",low_window=K,
                        weight_in_window=(2*K+1)/M,zero_weight=1/M))
        out.append(dict(M=M,source="whole_cycle_positive_constant",low_window=K,
                        weight_in_window=1.,zero_weight=1.))
    return out


def rate_table():
    """Exact integer scale sizes; analytical error bounds up to fixed constants."""
    out = []
    for r in range(1,9):
        M,B,K = 1<<(16*r),1<<(14*r),1<<(3*r)
        eps,theta = 1/math.sqrt(M),math.tau/M
        tau = theta*eps
        assert K*K * tau/eps**2 < 2*math.pi and 2*B <= M
        out.append(dict(r=r,M=M,B=B,K=K,epsilon=eps,tau=tau,
                        support_fraction=2*B/M,unit_preparation_hops=2*B-1,
                        unit_preparation_time=(2*B-1)*tau,
                        preparation_time_over_epsilon=(2*B-1)*theta,
                        tail_upper=M/(B*K),max_split_scale=K*K*tau/eps**2,
                        dither_endpoint_scale=K*theta,dither_commutator_scale=K*K*theta**2/tau,
                        scaled_largest_momentum_angle=K*tau/eps,
                        minimum_continuum_gap=2.,rest_initial_momentum_width=math.sqrt(eps)))
    return out


def impulse_word(ticks,tau):
    # System c=mu=F=1, θ=τ/ε, ideal per-tick vector setting at t_n=nτ.
    Q = [math.floor(tau*n*(n+1)/2+.5) for n in range(ticks+1)]
    assert all(abs(q-tau*n*(n+1)/2) <= .5+2e-12 for n,q in enumerate(Q))
    return [new-old for new,old in zip(Q[1:],Q)]


def finite_ensemble(M,source,physical_target=.6):
    """All Fourier sectors and a compact rest momentum packet. Both parities of k are kept."""
    eps = 1/math.sqrt(M)
    theta = math.tau/M
    tau = eps*theta
    ticks = round(physical_target/tau)
    duration = ticks*tau
    qword = impulse_word(ticks,tau)
    circumference = 32.
    sites = round(circumference/tau)
    circumference = sites*tau
    xi = math.tau/circumference
    dp = xi*eps
    width = math.sqrt(eps)
    Q = math.ceil(width/dp)-1
    g = [max(0.,1-(i*dp/width)**2)**3 for i in range(-Q,Q+1)]
    norm = math.sqrt(2*sum(w*w for w in g))
    g = [w/norm for w in g]
    ell = [i*math.tau/sites for i in range(-Q,Q+1)]
    B = M//4
    if source == "half_ring_dipole":
        weights = [crest(M,B,k) for k in range(M)]
    elif source == "two_site_dipole":
        weights = [crest(M,1,k) for k in range(M)]
    elif source == "localized_delta":
        weights = [1/M]*M
    else:
        raise ValueError(source)
    # The paired sectors are conjugates of the physical real-space wave.
    # An even real rest envelope lets the momentum labels reverse under conjugation.
    numerator = 0j
    rows = []
    largest_norm_error = 0.
    for k in range(M//2+1):
        folded = weights[k] if k in (0,M//2) else weights[k]+weights[-k]
        if folded == 0:
            continue
        spin_R,spin_L = [z for z in g],[z for z in g]
        alpha = theta*k
        co, si = math.cos(alpha), -1j*math.sin(alpha)
        phases = {q:[cmath.exp(-1j*(u-k*theta*q)) for u in ell] for q in set(qword)}
        for q in qword:
            ph = phases[q]
            spin_R,spin_L = (
                [z*(co*r+si*l) for z,r,l in zip(ph,spin_R,spin_L)],
                [z.conjugate()*(si*r+co*l) for z,r,l in zip(ph,spin_R,spin_L)])
        total = sum(abs(x)**2 for x in spin_R+spin_L)
        assert abs(total-1) < 3e-12
        largest_norm_error = max(largest_norm_error,abs(total-1))
        harmonic = sum(v*w.conjugate() for rail in (spin_R,spin_L) for v,w in zip(rail,rail[1:]))
        if k in (0,M//2):
            launch_harmonic = 2*sum(v*w for v,w in zip(g,g[1:]))
            ballistic = launch_harmonic*math.cos(ticks*math.tau/sites)
            assert abs(harmonic-ballistic) < 3e-12
        numerator += folded*harmonic
        rows.append(dict(fold=k,weight=folded,position_harmonic=[harmonic.real,harmonic.imag]))
    assert abs(sum(d['weight'] for d in rows)-1) < 2e-13
    target = -duration**2/(1+math.hypot(1,duration))
    return dict(M=M,source=source,epsilon=eps,tau=tau,ticks=ticks,physical_time=duration,
                base_sites=sites,occupied_modes=2*Q+1,ruler_winding=1,
                max_sheet_vector_stride=max(map(abs,qword)),
                phase_word=qword,position_harmonic=[numerator.real,numerator.imag],
                circular_centre=cmath.phase(numerator)/xi,shared_rest_ray=target,
                harmonic_distance=abs(numerator-cmath.exp(1j*xi*target)),
                maximum_norm_error=largest_norm_error,all_populated_folds=rows)


def half_alias_controls():
    rows = []
    for M in (8,12,16,32,64):
        theta = math.tau/M
        maximum = 0.
        for k in range(M//2):
            for q in (-2,-1,0,1,2):
                def coefficients(mode):
                    a = mode*theta
                    ph = cmath.exp(-1j*(.47-mode*theta*q))
                    return [ph*math.cos(a),ph*(-1j*math.sin(a)),
                            ph.conjugate()*(-1j*math.sin(a)),ph.conjugate()*math.cos(a)]
                one,two = coefficients(k),coefficients(k+M//2)
                sign = -1 if (q+1)%2 else 1
                maximum = max(maximum,*(abs(b-sign*a) for a,b in zip(one,two)))
            assert abs(crest(M,1,k)+crest(M,1,k+M//2)-2/M)<2e-14
        assert maximum < 3e-14
        rows.append(dict(M=M,largest_matrix_error=maximum,
                         dipole_and_delta_joint_weight_per_half_shift_pair=2/M))
    return rows


def main(dest):
    result = dict(source="Real ±1 block of length 2B, zero elsewhere, shared denominator √(2B). "
                  "One H-fed balanced base coin prepares |+x>. Coherent addressed dyadic fanout "
                  "starts at localized sheet and cleans the routing bit at every stage by reading "
                  "the occupied address bit coherently. The source difference can be implemented "
                  "by a Z sign on the most significant split; this changes no success probabilities. "
                  "The apparatus can start the flight clock after source construction.",
                  exact_weights=direct_spectra(),escaping_controls=escape_controls(),
                  growing_window=rate_table(),half_shift_alias=half_alias_controls(),
                  finite_flights=[finite_ensemble(M,s) for M in (16,32,64) for s in
                                  ("half_ring_dipole","two_site_dipole","localized_delta")],
                  later_flights=[finite_ensemble(32,s,1.2) for s in
                                 ("half_ring_dipole","two_site_dipole","localized_delta")],
                  time_costs="One addressed-sheet preparation entails log2(2B) local H/signed "
                  "splits and address cleanups, and 2B-1 conditional unit translations. The "
                  "computed duration counts one sheet-edge translation per τ; if the H and "
                  "address operations also take one such tick each, add O(τ log B). This "
                  "requires synchronous address-dependent local gates and retained relative "
                  "phase. It prepares the sheet, not the independent narrowing base packet.",
                  limit="Put θ=2π/M, τ=εθ, c=μ=F=1; DFT of T^1 uses exp(-ikθ). The onsite "
                  "coin H diag(T,T^-1) H gives exp(-ikθ X). A common real |+x> "
                  "spinor at rest belongs to energy branch sign(k) of cp Z+kμ X for "
                  "every fixed k≠0, including even k. Along p(t)=-kFt, the group velocity "
                  "λ c²p/sqrt(c²p²+k²μ²) is independent of k for either sign. This is the "
                  "bare X model with its own common source. Identifying it with the original "
                  "D gauge and the ZH launch requires the corresponding sheet-sector constraint.",
                  uniform_estimates="For continuum rest chart |p0|<=sqrt(eps), 1<=|k|<=K, "
                  "launch band error O(sqrt(eps)/|k|), gap error O(eps/|k|), endpoint "
                  "sampling O(K*tau/eps), Lie split remainder O(K²*tau/eps²) for fixed time. "
                  "Rounded cumulative vector-angle counts have residual ≤|k|θ/2 and a "
                  "per-tick commutator ≤2|sin(kθ)| sin(|k|θ/2) while |k|θ is small. "
                  "Total dither error O(Kθ+TK²θ²/τ). Momentum support stays on small charts "
                  "when Kτ/eps→0. In the scalar comparison the group velocity differs from "
                  "the common ray by O(sqrt(eps)/|k|), and the smooth rest packet initially "
                  "has position width O(sqrt(eps)); bounded-position characteristic "
                  "convergence suffices. Combine uniform low-window errors with total "
                  "high-window weight ≤M/(BK); no individual high-index limit is inferred.",
                  adverse="An unfiltered sheet delta or a fixed-width source has no tight "
                  "folded spectrum as M grows. In this integer-stride vector walk even M gives "
                  "U(k+M/2)=(-1)^(1+q_n)U(k) per tick. The adjacent signed dipole has "
                  "pairwise weights w_k+w_{k+M/2}=2/M exactly like the delta, so their "
                  "complete sheet-unread flight statistics agree for all times under the "
                  "same common base preparation and sector-independent base instruments. "
                  "The antipode is a ballistic copy of k=0. The broad dipole kills both. "
                  "A whole positive uniform sheet has only the massless, unforced k=0 sector. "
                  "The finite fully mixed "
                  "position statistics and controls do not decide their continuum behavior. "
                  "The spectral mixture here is Parseval from a real coherent wavefunction; "
                  "a separate incoherent path-count sector is not addressed.")
    dest.mkdir(parents=True,exist_ok=True)
    (dest/'common_ray_source.json').write_bytes((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())


if __name__ == "__main__":
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument("output_directory",type=Path)
    main(arg.parse_args().output_directory)
