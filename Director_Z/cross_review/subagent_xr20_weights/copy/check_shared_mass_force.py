"""Run python -B check_shared_mass_force.py OUTPUT_DIRECTORY (Python standard library)."""
import argparse
import cmath
import json
import math
from collections import defaultdict
from pathlib import Path

from check_sheet_mass_coin import balanced, named_cycle, overlap, shift_sheet


def clean(value):
    return round(float(value), 12)


def odd_sign(k):
    assert k % 2 == 1
    return 1 if k % 4 == 1 else -1


def phase(angle):
    return cmath.exp(1j * angle)


def literal_flight():
    """One integer-valued real sheet experiment; compare every bin against independent rotations."""
    order, stride = 32, -3
    sectors = (1, -1, 3, -3, 5, -5, 7, -7, 15)
    starts = {-3: 1, 0: 2, 2: -1}
    power = sum(v * v for v in starts.values())
    signs = (1,) * 10
    # Physical H then D† prepares the odd sectors with the same apparatus.
    state = shift_sheet(balanced({(x, 1, 0): w for x, w in starts.items()}),
                        order, minus=-order // 4)
    waves = {
        k: {(x, d): w * (1 if d == 1 else 1j * odd_sign(k)) / math.sqrt(2 * power)
            for x, w in starts.items() for d in (1, -1)}
        for k in sectors
    }
    h = math.tau / order
    errors = []
    by_time = {}
    for n in range(len(signs) + 1):
        assert sum(v * v for v in state.values()) == 2 * power * 4**n
        if n:
            for k, old in waves.items():
                out = defaultdict(complex)
                angle = -h * k * stride * odd_sign(k)
                cs, sn = math.cos(angle), math.sin(angle)
                for (x, d), v in old.items():
                    v *= phase(-h * k * signs[n - 1] * x)
                    out[x + d, d] += cs * v
                    out[x - d, -d] += d * sn * v
                waves[k] = out
        row = {}
        for k, wave in waves.items():
            coefficients = overlap(state, order, k)
            norm = math.sqrt(2 * power) * 2**n
            largest = max(abs(coefficients.get(cell, 0) / norm - wave.get(cell, 0))
                          for cell in coefficients.keys() | wave.keys())
            errors.append(largest)
            assert largest < 3e-13
            start, end = min(starts) - n, max(starts) + n
            bins = [sum(abs(coefficients.get((x, d), 0) / norm)**2 for d in (1, -1))
                    for x in range(start, end + 1)]
            assert abs(sum(bins) - 1) < 2e-13
            row[k] = bins
        for k in (1, 3, 5, 7):
            assert max(abs(v - w) for v, w in zip(row[k], row[-k])) < 2e-14
        if n in (1, 4, 10):
            by_time[n] = {
                "first_site": min(starts) - n,
                "position_bins": {k: list(map(clean, p)) for k, p in row.items()},
                "TV_from_plus_one": {k: clean(sum(abs(v-w) for v, w in zip(row[1], p)) / 2)
                                     for k, p in row.items()},
                "integer_squared_norm": sum(v*v for v in state.values()),
            }
        if n < len(signs):
            state = named_cycle(state, order, stride, signs[n])
    assert by_time[10]["TV_from_plus_one"][3] > .1
    assert all(record["TV_from_plus_one"][15] < 2e-12 for record in by_time.values())
    return dict(order=order, stride=stride, launch_site_numerators=starts,
                physical_input_sheet="single site zero; Fourier projections are conditional diagnostics",
                maximum_complex_oracle_error=max(errors), complete_position_rows=by_time,
                adverse="The first trial incorrectly expected k=15 and k=1 at M=32 to differ. "
                        "They agree: conjugation followed by the M/2 alias preserves this eight-divisible "
                        "order's mass coin up to an overall sign and the force up to a clock/endpoint "
                        "parity sign. The additional one-stride ruler is a different instrument.")


def exact_alias_controls():
    """The half-shift changes the coin by a rail gauge and each departure by parity."""
    rows = []
    for order in (12,16,20,32):
        for stride in (-1,2):
            initial = {(0,1,0): 2,(1,1,0): 1,(2,1,0): -3}
            state = shift_sheet(balanced(initial),order,minus=-order//4)
            worst = 0.
            schedule = (1,-1,0,1,1,-1)
            for n in range(len(schedule)+1):
                if n == 3:
                    # Retain only an intermediate rail on every site. Do not renormalize.
                    state = {cell:v for cell,v in state.items() if cell[1] == -1}
                p = overlap(state,order,1)
                q = overlap(state,order,1+order//2)
                for (x,d), v in p.items():
                    exponent = n*stride + ((order//4) if d == -1 else 0)
                    exponent += sum(f*(x-n+t) for t,f in enumerate(schedule[:n]))
                    predicted = (-1 if exponent % 2 else 1)*v
                    worst = max(worst,abs(q[x,d]-predicted)/(2**n*math.sqrt(28)))
                if n < len(schedule):
                    state = named_cycle(state,order,stride,schedule[n])
            assert worst < 2e-13
            rows.append(dict(M=order,j=stride,rail_gauge_on_L=(-1)**(order//4),
                             filtered_tick=3,field_schedule=schedule,
                             maximum_phase_aware_amplitude_difference=worst))
    return rows


def readouts():
    rows = []
    for M, j in ((16,-1), (32,-3), (60,7), (32,4)):
        source = {(0,1,0): 1}
        # Two matched onsite H mixers with one known unit sheet delay on L.
        ruler = balanced(shift_sheet(balanced(source), M, minus=1))
        mass = named_cycle(source, M, j, 0)
        probs = []
        for k in range(M):
            pk = abs(overlap(ruler, M, k)[0,1] / 2)**2
            qk = abs(overlap(mass, M, k)[1,1] / 2)**2
            assert abs(pk - (1 + math.cos(math.tau * k / M)) / 2) < 2e-14
            assert abs(qk - math.cos(math.tau * k * j / M)**2) < 2e-14
            probs.append((pk,qk))
        same_square = [k for k in range(M) if abs(probs[k][1] - probs[1][1]) < 2e-14]
        same_cos = [k for k in range(M) if abs(probs[k][0] - probs[1][0]) < 2e-14]
        assert same_cos == [1,M-1]
        assert same_square == [k for k in range(M) if
                               ((2*j*(k-1)) % M == 0 or (2*j*(k+1)) % M == 0)]
        unity, p1, p3 = probs[0][0], probs[1][0], probs[3][0]
        w0 = (p1 - p3) / (unity - p3)
        assert abs(w0*unity + (1-w0)*p3 - p1) < 2e-15
        states = {"real_sheet_delta_uniform_sectors": sum(p for p, _ in probs)/M,
                  "weight_on_zero_in_nonordinary_0_3_mimic": w0,
                  "mimic_ruler_probability": w0*unity + (1-w0)*p3,
                  "two_read_correlation_retained_sector": w0*unity**2 + (1-w0)*p3**2,
                  "two_read_probability_after_independent_sheet_reset": p1**2}
        for time in (.1,1.,10.):
            weights = [math.exp(-2*time*(1-math.cos(math.tau*k/M))) for k in range(M)]
            states[f"heat_{time}_probability"] = sum(w*p for w,(p,_) in zip(weights,probs))/sum(weights)
        gap = p1 - p3
        # Hoeffding at the midpoint between simple Bernoulli laws, either-side error <= .05.
        shots = math.ceil(2*math.log(1/.05) / gap**2)
        # Angular infidelity near zero changes the *rare failures* by O(M^-2).
        # The likelihood-ratio test for equal priors obeys Bayes error <= BC^n/2.
        bc = math.sqrt(p1*p3) + math.sqrt((1-p1)*(1-p3))
        rare_aware = math.ceil(math.log(.1) / math.log(bc))
        rows.append(dict(M=M,stride=j,ordinary_squared_port=clean(probs[1][1]),
                         squared_port_aliases=same_square,unit_ruler_aliases=same_cos,
                         ruler_probabilities=list(map(lambda pair: clean(pair[0]),probs)),
                         ordinary_vs_three_ruler_gap=clean(gap),
                         sufficient_iid_shots_each_hypothesis_5pct=shots,
                         sufficient_iid_shots_equal_prior_average_5pct=rare_aware,
                         single_shot_Bhattacharyya=clean(bc),
                         mixture_controls={k:clean(v) for k,v in states.items()}))
    return rows


def two_setting_readouts():
    """Independent identically prepared replicas measured at strides one and two."""
    rows = []
    for M in (4,5,8,12,16,32,60,128):
        origin = {(0,1,0): 1}
        moments = []
        for d in (1,2):
            ports = balanced(shift_sheet(balanced(origin),M,minus=d))
            values = []
            for k in range(M):
                a = overlap(ports,M,k)
                pr, pl = abs(a[0,1]/2)**2, abs(a[0,-1]/2)**2
                assert abs(pr+pl-1) < 1e-14
                values.append(pr-pl)
            moments.append(values)
        x = [math.cos(math.tau*k/M) for k in range(M)]
        target = x[1]
        g = (1-target)**2
        assert set(k for k in range(M) if abs(x[k]-target)<1e-13) == {1,M-1}
        assert abs(g-min((x[k]-target)**2 for k in range(M) if k not in (1,M-1))) < 2e-14
        # Choose an undesired lower-response mode even when 3 is itself ordinary (M=4).
        nuisance = 3 if M >= 8 else 2
        w0 = (target-x[nuisance])/(1-x[nuisance])
        assert 0 < w0 < 1
        examples = {
            "pure_target": ({1:1.},0.),
            "trivial_mode_tight_gap": ({0:1.},0.),
            "one_read_mimic": ({0:w0,nuisance:1-w0},0.),
            "target_plus_five_percent_trivial": ({1:.95,0:.05},0.),
            "uniform_phase_sectors": ({k:1/M for k in range(M)},0.),
            "all_count": ({},1.),
            "twenty_percent_count": ({1:.8},.2),
        }
        tests = {}
        for name,(weights,count) in examples.items():
            assert abs(sum(weights.values())+count-1) < 1e-13
            m1,m2 = [sum(w*v[k] for k,w in weights.items()) for v in moments]
            variance = (1+m2)/2 - 2*target*m1 + target**2
            cost_count = .5+target**2
            square_reference = sum(w*(x[k]-target)**2 for k,w in weights.items()) + count*cost_count
            wrong_phase = sum(w for k,w in weights.items() if k not in (1,M-1))
            count_gap = min(g,cost_count)
            assert abs(variance-square_reference) < 5e-14
            assert variance + 5e-14 >= g*wrong_phase+count*cost_count
            assert count_gap*(wrong_phase+count) <= variance+5e-14
            if name == "one_read_mimic":
                assert abs(m1-target) < 1e-13 and variance > 0
                assert abs(m2-moments[1][1]) > 1e-9
            tests[name] = dict(m1=clean(m1),m2=clean(m2),weighted_square=clean(variance),
                               wrong_phase=clean(wrong_phase),count=count,
                               upper_wrong_including_count=clean(min(1.,max(0.,variance/count_gap))))
        assert abs(tests['all_count']['m1']-tests['uniform_phase_sectors']['m1'])<1e-13
        assert abs(tests['all_count']['m2']-tests['uniform_phase_sectors']['m2'])<1e-13
        rows.append(dict(M=M,target_x=clean(target),target_second_moment=clean(moments[1][1]),
                         wrong_phase_gap=g,count_gap=.5+target**2,
                         combined_wrong_gap=min(g,.5+target**2),
                         nuisance_mode=nuisance,nuisance_mixture_zero_weight=clean(w0),
                         second_setting_rows=tests))
    return dict(rows=rows,meaning="m_d=2 Pplus(d)-1 for one two-H ruler. The settings are "
                "run on matched fresh preparations. No joint simultaneous value is assigned. "
                "For phase weights and separately counted fraction c the nonnegative residual "
                "(1+m2)/2-2*x1*m1+x1^2 equals sum w_k*(x_k-x1)^2+c*(1/2+x1^2). "
                "Here counting gives 1/2 port probability in each setting by four equally "
                "counted two-H histories. A uniform phase mixture gives the same two moments. "
                "For M=4 counting has a smaller gap than any single wrong phase. "
                "For errors |delta m_d|<=eta_d add eta_2/2+2|x1|eta_1 to the measured "
                "residual before dividing by the applicable gap. The phase gap is (1-cos h)^2 "
                "since 1 is the nearest wrong cosine; its M^-4 scaling limits resolution.",
                calibration="If the order of the unit physical translation is known and "
                "independent pure-sector preparations exhaust its real spectral responses, its "
                "second-highest distinct cosine identifies the pair without a numerical phase "
                "table. An extremum over an incomplete set or arbitrary unknown mixtures can "
                "mislabel another value. This is relative to the chosen stroke, instrument "
                "and read law. Simultaneously relabel the whole sheet, preparations and ruler "
                "and every ordinal and moment is unchanged. These moments do not establish "
                "the assumed count-plus-character response law.")


def ordinal_selector():
    """Unknown folded class, one ensemble: zero cosine variance followed by rankings of powers."""
    rows = []
    tolerance = 2e-12
    for M in (4,5,8,12,16,32,60):
        ports = [balanced(shift_sheet(balanced({(0,1,0):1}),M,minus=d)) for d in range(M)]
        moments = []
        for k in range(M):
            row = []
            for port in ports:
                f = overlap(port,M,k)
                row.append((abs(f[0,1])**2 - abs(f[0,-1])**2)/4)
            moments.append(row)

        def classify(values):
            variance = (1+values[2])/2-values[1]**2
            high = max(values[1:])
            ties = [d for d in range(1,M) if high-values[d] < tolerance]
            accepted = (abs(variance)<tolerance and 1-values[1]>tolerance and 1 in ties)
            return dict(zero_target_variance=clean(variance),m1=clean(values[1]),
                        high=clean(high),maximizing_powers=ties,accepted=accepted)

        all_k = []
        for k, values in enumerate(moments):
            result = classify(values)
            assert result['accepted'] == (k in (1,M-1))
            g = math.gcd(k,M)
            order = M//g
            if g > 1:
                expected = list(range(order,M,order))
                assert abs(values[order]-1) < tolerance
            else:
                expected = [d for d in range(1,M) if (k*d)%M in (1,M-1)]
            assert result['maximizing_powers'] == expected
            all_k.append(dict(k=k,first_identity_power=order,**result))
        def mixture(weights):
            return [sum(weight*moments[k][d] for k,weight in weights.items()) for d in range(M)]
        other = 2 if M<8 else 3
        x,y = moments[1][1],moments[other][1]
        w = (x-y)/(1-y)
        controls = { "pure_count":classify([0.]*M),
                     "uniform":classify(mixture({k:1/M for k in range(M)})),
                     "one_read_mimic":classify(mixture({0:w,other:1-w})),
                     "folded_pair":classify(mixture({1:.4,M-1:.6})),
                     "one_percent_count":classify([.99*v for v in moments[1]])}
        assert controls['folded_pair']['accepted'] and not any(
            c['accepted'] for tag,c in controls.items() if tag!='folded_pair')
        rows.append(dict(M=M,all_pure_sectors=all_k,mixture_controls=controls))
    return dict(rows=rows,numeric_tolerance=tolerance,
                rule="On identically prepared copies use powers d=0..M-1 of one physical "
                     "primitive sheet translation. From d=1,2 form V=(1+m2)/2-m1^2. "
                     "V=0 excludes count and confines the ensemble to one folded pair "
                     "since the phase variance is nonnegative and count costs 1/2+m1^2. "
                     "Require m1<1 and equality with max(m1,...,m_{M-1}). A nonunit "
                     "produces identity response at nonzero d=M/gcd(k,M); for a unit "
                     "maximum occurs at kd=±1 precisely. Thus the noiseless rule accepts "
                     "exactly the fundamental conjugate pair relative to the physical stroke. "
                     "The implemented decision tolerance only checks floating point evaluation.",
                finite_accuracy="For measured |mhat_d-m_d|<=eta and mhat in [-1,1], "
                     "|Vhat-V|<=5*eta/2. The maximum-minus-one-stroke comparison has "
                     "error <=2*eta. Finite precision cannot prove exact sector purity: "
                     "small off-pair or count contamination changes all moments continuously. "
                     "Under the prior of a single folded class let Delta be the least spacing "
                     "of different cosine values at this order. Each wrong nontrivial class "
                     "fails the rank comparison by at least Delta, and the trivial class "
                     "has m1=1. In particular eta<Delta/4 allows a midpoint gap decision "
                     "under that prior. Simultaneous relabels of every apparatus "
                     "preserve all statistics.")


def band_and_rays():
    """Classical band integrals, independent of any finite-position probability fit."""
    force, mu, c, time = .8, 1., 1., .6
    rows = []
    common = -force*time**2 / (1 + math.hypot(1,force*time))
    for k in (1,-1,3,-3,5,-5,7,-7):
        branch = 1 if k > 0 else -1
        K = abs(k)
        f = k * force
        def ray(mass, p, b):
            return b*(math.hypot(c*p,mass)-math.hypot(c*(p-f*time),mass))/f
        rest = ray(K*mu, 0., branch)
        assert abs(rest-common) < 1e-14
        rows.append(dict(k=k,signed_mass=k*odd_sign(k)*mu,energy_band=branch,
                         force=f,rest=clean(rest),fixed_mass_control=clean(ray(mu,0.,branch)),
                         identical_nonzero_initial_momentum_control=clean(ray(K*mu,.3,branch)),
                         sector_scaled_initial_momentum=clean(ray(K*mu,k*.3,branch))))
    # Dispersion U(q)=diag(exp(-iq),exp(iq))R_y(alpha).
    # A characteristic at common scaled time carries q=-kFtc*tau/epsilon.
    disp = []
    for scale in (.12,.06,.03,.015):
        values = {}
        for k in (1, 3, 5, 7):
            alpha = k*odd_sign(k)*mu*scale
            q = -k*force*time*c*scale
            omega = math.acos(math.cos(alpha)*math.cos(q))
            velocity = c*math.cos(alpha)*math.sin(q)/math.sin(omega)
            assert abs(velocity) <= c
            values[k] = clean(velocity)
        disp.append(dict(tau_over_epsilon=scale,band_velocities=values))
    return dict(c=c,mu=mu,force=force,t=time,continuum_rows=rows,
                continuum_terminal_velocity=clean(-force*time/math.hypot(1,force*time)),
                finite_dispersion=disp)


def packet_flight():
    """Sparse, normalized finite momentum family on a periodized line, no full sheet allocation."""
    length, force = 48., 1.
    rows = []
    for eps in (.5,.25,.125):
        target = eps**3/4
        M = 4*round(math.tau*eps/target**2/4)
        tau = math.sqrt(math.tau*eps/M)
        h = math.tau/M
        stride = -round(1/tau)
        physical_time = round(.5/tau)*tau
        ticks = round(.5/tau)
        sites = round(length/tau)
        box = sites*tau
        dp = math.tau*eps/box
        B = math.ceil(math.sqrt(eps)/dp)-1
        us = [max(0.,1-(u*dp)**2/eps)**3 for u in range(-B,B+1)]
        power = sum(v*v for v in us)
        source = [v/math.sqrt(power*2) for v in us]
        k0 = [u*math.tau/sites for u in range(-B,B+1)]
        rows_k = {}
        for k in (1, -1, 3, -3, 5, -5, 7, -7):
            s = odd_sign(k)
            alpha = -k*s*h*stride
            cs, sn = math.cos(alpha), math.sin(alpha)
            z = [phase(-q) for q in k0]
            step = phase(k*h)
            R,L = source[:], [1j*s*v for v in source]
            for _ in range(ticks):
                z = [v*step for v in z]
                R,L = ([ph*(cs*r-sn*l) for ph,r,l in zip(z,R,L)],
                       [ph.conjugate()*(sn*r+cs*l) for ph,r,l in zip(z,R,L)])
            norm = sum(abs(v)**2 for v in R+L)
            assert abs(norm-1) < 8e-10
            harmonic = sum(a*b.conjugate() for rr in (R,L) for a,b in zip(rr,rr[1:]))
            ray = -physical_time**2/(1+math.hypot(1,physical_time))
            xi = math.tau/box
            rows_k[k] = dict(norm=clean(norm),first_position_harmonic=[clean(harmonic.real),clean(harmonic.imag)],
                             circular_centre=clean(cmath.phase(harmonic)/xi),
                             distance_from_shared_ray_harmonic=clean(abs(harmonic-phase(xi*ray))))
        for k in (1,3,5,7):
            assert abs(rows_k[k]['circular_centre']-rows_k[-k]['circular_centre']) < 1e-8
        rows.append(dict(epsilon=eps,tau=clean(tau),M=M,mass_stride=stride,
                         ticks=ticks,time=clean(physical_time),sites=sites,occupied_momenta=2*B+1,
                         actual_common_mass_scale=clean(-h*stride*eps/tau),
                         shared_rest_ray=clean(ray),sectors=rows_k))
    return rows


def main(out):
    result = dict(
        assumptions="Unit base speed and squared norms. The same quarter-sheet and negative "
                    "mass stride act in all sectors. Force, tick, site and the unit ruler are "
                    "fixed across comparisons. The limit uses each fixed odd k, a common "
                    "real, narrowing rest packet, small tau/epsilon and tau/epsilon^2, "
                    "and the phase-correlated quarter-rail preparation. Odd nonunits can "
                    "also be tested as representation sectors. A field embedding requires units.",
        sector_scope="Resolving a pure k in Fourier space requires an independent phase preparation "
                     "or read. For a physical real apparatus ±k are conjugate. The sheet-unresolved "
                     "distribution sums squared sector amplitudes with their actual preparation weights.",
        read_scope="Single-tick mass rail test starts in R, any packet, ignoring terminal base and sheet. "
                   "Unit-stride ruler has two onsite H operations around L-only T, matched base and "
                   "unread sheet. If a stream is compulsory after every H, physical refocusing is extra. "
                   "Pure sectors or mixtures solely of nonzero units can reach maximal unit ruler read "
                   "only at ±1. With zero/trivial sector admitted a mixture can mimic the one read. "
                   "The heat control uses normalized discrete circle heat-kernel eigenvalues as weights. "
                   "The two shot bounds concern only iid noiseless pure 1 versus pure 3. "
                   "Hoeffding gives a conservative guarantee under each hypothesis. "
                   "The Bhattacharyya bound uses O(M²) shots for fixed Bayes error when "
                   "false clicks and dark backgrounds are negligible; neither includes preparation.",
        finite_flights=literal_flight(),half_shift_alias_controls=exact_alias_controls(),
        calibrated_readouts=readouts(),two_setting_certificates=two_setting_readouts(),
        internal_power_rank=ordinal_selector(),
        band_limit=band_and_rays(),
        refined_packets=packet_flight(),
        limits="The finite rows retain all reported cases and do not prove convergence or alias "
               "every finite measurement. The shared ray at rest follows analytically for each "
               "fixed odd k from the band Hamiltonian with μ_k=k sin(πk/2)μ and f_k=kF. "
               "Keeping the mass calibrated independently, using mismatched input rails, or "
               "fixing nonzero input momentum across k changes that inference. High modes growing "
               "with M need uniform chart/gap control. The physical cost of large sheet translations "
               "and preparation is separate from the named base tick."
    )
    out.mkdir(parents=True, exist_ok=True)
    (out/'shared_mass_force.json').write_bytes((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory",type=Path)
    main(parser.parse_args().output_directory)
