"""Run python -B check_string_motion.py OUTPUT_DIRECTORY. Requires NumPy.

Two hops layers then one complete string kick. Lengths use the two-mode cell
pitch. The independent continuum oracle evolves an odd scalar relative wave.
"""
import argparse
import json
import math
import os
from pathlib import Path

for variable in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ[variable] = "1"
import numpy as np
from check_occupation_envelope import CA, SA, CB, SB, KAPPA, GAMMA, fourier, spectrum


BOX = 16.
R0 = 1.6
P = .65
TIMES = (0., .65, 1.35, 2.07, 2.55, 3.1)


def norm(v):
    return float(np.linalg.norm(v))


def statistics(p, x):
    p = p.ravel()
    x = x.ravel()
    mu = float(p @ x)
    return mu, math.sqrt(max(0., float(p @ ((x-mu)**2))))


def bins(p, x):
    # Fixed physical bins of width 1/4, starting at -1/8 so the origin
    # lies in the middle of its bin. Last bin includes all overflow.
    idx = np.clip(np.floor(x*4+.5).astype(int), 0, 32).ravel()
    return np.bincount(idx, weights=p.ravel(), minlength=33)


def ray(t, sigma):
    sep = R0+2*P*t-sigma*t*t
    if sigma <= 0 or sep >= 0:
        return sep
    speed = math.sqrt(P*P+sigma*R0)
    hit = (P+speed)/sigma
    elapsed = (t-hit) % (2*speed/sigma)
    return 2*speed*elapsed-sigma*elapsed**2


def relative_source(r, eps):
    def lobe(x):
        return np.exp(-(x-R0)**2/(4*eps)+1j*P*(x-R0)/eps)
    f = lobe(r)-lobe(-r)
    return f/norm(f)


def continuum(times, eps, sigma, n, step):
    """Strang on [-8,8) by odd reflection. Walls at 0 and 8."""
    r = BOX*(np.arange(n)/n-.5)
    wave = relative_source(r, eps)
    k = 2*np.pi*np.fft.fftfreq(n, BOX/n)
    rows = []
    old = 0.
    for t in times:
        count = math.ceil((t-old)/step)
        if count:
            dt = (t-old)/count
            kick = np.exp(-.5j*dt*sigma*abs(r)/eps)
            drift = np.exp(-1j*dt*eps*k*k)
            for _ in range(count):
                wave = kick*np.fft.ifft(drift*np.fft.fft(kick*wave))
        assert abs(norm(wave)-1) < 1e-10 and abs(wave[n//2]) < 1e-12
        rows.append(wave.copy())
        old = t
    return r, rows


def open_axis(w, layer):
    out = w.copy()
    start = layer
    left, right = slice(start, w.shape[-1]-1, 2), slice(start+1, None, 2)
    c, off = (CA, -1j*SA) if layer == 0 else (CB, 1j*SB)
    out[..., left] = c*w[..., left]+off*w[..., right]
    out[..., right] = off*w[..., left]+c*w[..., right]
    return out


def open_cycle(w, kick):
    for layer in (0, 1):
        w = open_axis(open_axis(w, layer).T, layer).T
    return w*kick


def explicit_test():
    # Literal dressed hopping and phase on each switched link, on every
    # computational launch of an open eight-site graph. Strings are bitmasks.
    length = 8
    phase = np.exp(-.173j)
    sites = np.arange(length)
    kick = phase**abs(sites[:, None]-sites)
    worst = 0.
    for i in range(length):
        for j in range(i+1, length):
            initial = (i, j, (1 << j)-(1 << i))
            amps = {initial: 1.}
            w = np.zeros((length, length), complex)
            w[i, j], w[j, i] = 1., -1.
            for _ in range(3):
                for layer, (c, off) in enumerate(((CA, -1j*SA), (CB, 1j*SB))):
                    for lo in range(layer, length-1, 2):
                        nxt = {}
                        for (x, y, mask), val in amps.items():
                            mode = [h for h in (x, y) if h in (lo, lo+1)]
                            stationary = (x, y, mask)
                            if len(mode) == 1:
                                dest = tuple(sorted((2*lo+1-h if h == mode[0] else h) for h in (x, y)))
                                moved = (*dest, mask ^ (1 << lo))
                                nxt[moved] = nxt.get(moved, 0)+off*val
                                val *= c
                            nxt[stationary] = nxt.get(stationary, 0)+val
                        amps = nxt
                for bit in range(length-1):
                    for key in amps:
                        if key[2] & (1 << bit):
                            amps[key] *= phase
                w = open_cycle(w, kick)
                assert all(mask == (1 << y)-(1 << x) for x, y, mask in amps)
                for x in range(length):
                    for y in range(x+1, length):
                        worst = max(worst, abs(w[x,y]-amps.get((x,y,(1 << y)-(1 << x)),0)))
    assert worst < 2e-14
    return dict(sites=8, localized_basis_launches=28, cycles=3,
                link_phase_angle=-.173, maximum_coordinate_error=worst)


def cyclic(v, shift):
    w = np.roll(v, shift)
    w[0 if shift == 1 else -1] *= -1
    return w


def fiber_free(w):
    """F_d[s,t] with d=cell(second)-cell(first), antiperiodic in d."""
    inside = np.array([[CA, -1j*SA], [-1j*SA, CA]])
    w = inside @ w @ inside.T
    v = np.empty_like(w)
    for t in range(2):
        v[:,0,t] = CB*w[:,0,t]+1j*SB*cyclic(w[:,1,t], -1)
        v[:,1,t] = CB*w[:,1,t]+1j*SB*cyclic(w[:,0,t], 1)
    out = np.empty_like(w)
    for s in range(2):
        out[:,s,0] = CB*v[:,s,0]+1j*SB*cyclic(v[:,s,1], 1)
        out[:,s,1] = CB*v[:,s,1]+1j*SB*cyclic(v[:,s,0], -1)
    return out


def geometry(n):
    a = BOX/n
    r = (np.arange(n)-n//2)*a
    sub = (np.arange(2)[None,:]-np.arange(2)[:,None])*a/2
    physical = abs((r[:,None,None]+sub+BOX/2) % BOX-BOX/2)
    k, _, omega, u = spectrum(n, True)
    # k order is half-integer, so -k occurs at index n-1-index.
    pole = u[::-1,:,None]*u[:,None,:]
    return r, physical, k, omega, pole


def encode(scalar, pole):
    return fourier(fourier(scalar, True)[:,None,None]*pole, True, True)


def check_fiber():
    n = 8
    r, dist, k, omega, pole = geometry(n)
    w = encode(relative_source(r, .27), pole)
    spectral = fourier(fourier(w, True)*np.exp(-2j*omega)[:,None,None], True, True)
    err = norm(fiber_free(w)-spectral)
    # Compare a whole local open cycle in its interior against the translation
    # fiber. Both paths use the scalar-site kick including sublattice offsets.
    pos = np.arange(2*n)
    d = pos[None,:]//2-pos[:,None]//2
    index = (d+n//2) % n
    sign = (-1.)**((d+n//2)//n)
    def lift(v):
        return sign*v[index,pos[:,None]%2,pos[None,:]%2]
    angle = .31
    reduced = fiber_free(w)*np.exp(-1j*angle*dist)
    direct = open_cycle(lift(w), np.exp(-1j*angle*abs(pos[:,None]-pos)*BOX/(2*n)))
    mask = ((pos>1)&(pos<2*n-2))
    interior = mask[:,None]&mask& (abs(pos[:,None]-pos)<n)
    diff = float(np.max(abs((direct-lift(reduced))[interior])))
    assert err < 1e-13 and diff < 1e-13
    return dict(cells=n, free_fiber_vs_Bloch_norm=err,
                central_open_vs_fiber_kicked_maximum=diff, interior_entries=int(interior.sum()))


def fiber_trial(n, eps, sigma, times, name):
    a = BOX/n
    tau = KAPPA*a*a/eps
    ticks = sorted({round(t/tau) for t in times})
    actual = [m*tau for m in ticks]
    r, distance, k, _, pole = geometry(n)
    f = relative_source(r, eps)
    w = encode(f, pole)
    kick = np.exp(-1j*tau*sigma*distance/eps)
    _, coarse = continuum(actual, eps, sigma, 2*n, .02)
    fr, fine = continuum(actual, eps, sigma, 4*n, .01)
    max_edge = 0.
    rows = []
    for m in range(ticks[-1]+1):
        probability = abs(w)**2
        max_edge = max(max_edge, float(probability[distance>7].sum()))
        if m in ticks:
            h = ticks.index(m)
            t = actual[h]
            # Compare complete represented amplitudes on the same grid.
            # Downsample continuum rather than fitting the phase or the clock.
            fref = 2*fine[h][::4]
            coarse_on_matter_grid = math.sqrt(2)*coarse[h][::2]
            spectral = fourier(w, True)
            projection = np.einsum("kst,kst->k", pole.conj(), spectral)
            expected = ray(t, sigma)
            physical_marginal = bins(probability, distance)
            reference_marginal = bins(abs(fine[h])**2, abs(fr))
            mu, sd = statistics(probability, distance)
            fmu, fsd = statistics(abs(fine[h])**2, abs(fr))
            row = dict(tick=m, time=t, classical_separation=expected,
                       mean_separation=mu, sd_separation=sd, continuum_mean=fmu, continuum_sd=fsd,
                       rms_from_classical=math.hypot(mu-expected, sd),
                       continuum_rms_from_classical=math.hypot(fmu-expected, fsd),
                       norm=norm(w), rest_demodulated_Hilbert=norm(np.exp(2j*m*GAMMA)*w-encode(fref,pole)),
                       coarse_fine_reference_Hilbert_on_matter_grid=norm(fref-coarse_on_matter_grid),
                       reference_sampling_norm=norm(fref),
                       positive_pair_band_leakage=float(np.sum(abs(spectral-projection[:,None,None]*pole)**2)),
                       probability_abs_k_above_half=float(np.sum(abs(spectral[abs(k)>.5])**2)),
                       cumulative_max_mass_outer_unit_box=max_edge,
                       mass_separation_at_least_one=float(probability[distance>=1].sum()),
                       reference_mass_separation_at_least_one=float(np.sum(abs(fine[h][abs(fr)>=1])**2)),
                       actual_and_reference_separation_TV_quarter_bins=float(sum(abs(physical_marginal-reference_marginal))/2),
                       mean_cell_origin_distance=float(np.sum(probability*abs(r)[:,None,None])),
                       center_cell_double_occupation=float(probability[n//2].sum()))
            assert abs(row['norm']-1)<1e-10
            rows.append(row)
        if m < ticks[-1]:
            w = fiber_free(w)*kick
    return dict(name=name, cells=n, epsilon=eps, string_tension=sigma, cell_pitch=a,
                two_layer_duration=tau, source_relative_position=R0, source_relative_momentum=P,
                source_relative_sd_before_antisymmetrization=math.sqrt(eps),
                requested_times=list(times), relative_reference_cells=[2*n,4*n],
                reference_max_steps=[.02,.01], snapshots=rows)


def open_trial(n, sigma, target, name):
    eps, length = .25, 10.
    a = length/n
    tau = KAPPA*a*a/eps
    ticks = sorted({round(t/tau) for t in target})
    actual = [m*tau for m in ticks]
    vel = .37
    _, _, _, pole = spectrum(n, False)
    cells = -length/2 + np.arange(n)*a
    sites = -length/2 + np.arange(2*n)*a/2
    def orbital(q, p):
        env = np.exp(-(cells-q)**2/(2*eps)+1j*p*(cells-q)/eps)
        return fourier(fourier(env/norm(env),False)[:,None]*pole,False, True).ravel()
    u, v = orbital(-R0/2,vel-P), orbital(R0/2,vel+P)
    w = np.outer(u,v)-np.outer(v,u)
    w /= norm(w)
    sep = abs(sites[:,None]-sites)
    com = (sites[:,None]+sites)/2
    edge = (abs(sites)>4.5)
    kick = np.exp(-1j*tau*sigma*sep/eps)
    fr, fine = continuum(actual, eps, sigma, 768, .01)
    rows = []
    max_edge = 0.
    initial_com = float(np.sum(abs(w)**2*com))
    for m in range(ticks[-1]+1):
        prob = abs(w)**2
        max_edge = max(max_edge, float(prob[edge[:,None]|edge].sum()))
        if m in ticks:
            h = ticks.index(m)
            t = actual[h]
            cm, cmsd = statistics(prob, com)
            rm, rsd = statistics(prob, sep)
            pdf = abs(fine[h])**2
            refmean, refsd = statistics(pdf,abs(fr))
            rows.append(dict(tick=m, time=t, physical_norm=norm(w),
                             COM=cm, COM_sd=cmsd, ballistic_COM=vel*t,
                             COM_displacement_error_from_own_launch=abs(cm-initial_com-vel*t),
                             continuum_COM_sd=math.sqrt(eps*(1+t*t))/2,
                             separation_mean=rm, separation_sd=rsd,
                             classical_separation=ray(t,sigma),
                             continuum_separation_mean=refmean, continuum_separation_sd=refsd,
                             binned_TV_vs_relative_reference=float(sum(abs(bins(prob,sep)-bins(pdf,abs(fr))))/2),
                             cumulative_max_mass_within_half_unit_open_edge=max_edge))
            assert abs(norm(w)-1)<1e-10
        if m<ticks[-1]:
            w = open_cycle(w,kick)
    return dict(name=name, cells=n, box=length, action=eps, string_tension=sigma, cell_pitch=a,
                cycle_time=tau, initial_COM_velocity=vel,
                source_orbital_centers=[-R0/2,R0/2], source_orbital_momenta=[vel-P,vel+P],
                initial_positive_band_orbital_overlap_abs=float(abs(np.vdot(u,v))),
                requested_times=list(target), snapshots=rows)


def main():
    return dict(
        convention="m=1. Two matter layers in the complex hopping representation, then one link kick. Cell pitch a; scalar pitch a/2. Dressed hop toggles precisely the crossed link. Empty exterior flux on the open line. Product phase for i<j is exp(-i tau sigma (j-i)a/(2 epsilon)). The reduced wave represents joint Gauss-law amplitudes. Bare matter after tracing orthogonal link strings need not be in this pure state.",
        explicit_link_check=explicit_test(), fiber_implementations=check_fiber(),
        fiber_geometry="Total cell momentum zero, hence center delocalized. Antiperiodic one-body relative translation on the signed displacement interval [-8,8); the string length uses the short periodic extension of actual scalar-site distance, with both sublattice offsets. This is an auxiliary relative-coordinate box. The independently simulated open chain uses its unique non-wrapping string. Finite-box tail checks do not certify an infinite-volume error bound.",
        oracle="Continuum R=(x+y)/2 evolves freely, r=y-x has kinetic -epsilon^2 d^2/dr^2 and sigma |r|. Equal-width Gaussian Slater source factorizes into the COM packet and an odd relative combination. Strang reference uses the odd periodic extension and returns independent finite-grid, finite-step refinement differences. Positive-band sampling for the fiber Hilbert comparison omits a fitted global phase. All snapshots use actual rounded cycle times. TV bins have width 1/4 and last bin includes overflow.",
        turnaround_at_unit_tension=P, first_classical_contact_at_unit_tension=P+math.sqrt(P*P+R0),
        microscopic_scope="The check supplies the complex link phase and the Gaussian band-encoded preparations. It tests position laws of the stipulated circuit and provides finite comparisons, without establishing source costs, a continuum limit, or an empirical realization.",
        fiber_trials=[
            fiber_trial(128,.25,1.,TIMES,"coarse fixed action"),
            fiber_trial(256,.25,1.,TIMES,"medium fixed action"),
            fiber_trial(512,.25,1.,TIMES,"fine fixed action"),
            fiber_trial(512,.0625,1.,TIMES,"small action coarse chart"),
            fiber_trial(1024,.0625,1.,TIMES,"small action medium chart"),
            fiber_trial(2048,.0625,1.,TIMES,"small action fine chart"),
            fiber_trial(256,.25,0.,TIMES[:4],"force off"),
            fiber_trial(256,.25,-1.,TIMES[:3],"force reversed"),
        ],
        open_packet_trials=[
            open_trial(96,1.,TIMES[:3],"physical open coarse"),
            open_trial(192,1.,TIMES[:3],"physical open fine"),
            open_trial(96,0.,TIMES[:3],"open force off"),
            open_trial(96,-1.,TIMES[:3],"open force reversed"),
        ], predicates_scope="The fixed threshold gap>=1 was evaluated at every horizon, including the precontact, contact, rebound and control rows. Classical centers are not a field visibility predicate. The fixed-accuracy movement checks are finite diagnostics only.")


def validate(result):
    finer = result["fiber_trials"][5]["snapshots"]
    initial, turn, approach, near, after, rebound = finer
    assert turn["mean_separation"] > initial["mean_separation"]+.3
    assert near["mean_separation"] < approach["mean_separation"]-.8
    assert rebound["mass_separation_at_least_one"] > .9
    assert near["mass_separation_at_least_one"] < .15
    assert after["mean_separation"] > near["mean_separation"]+.3
    assert max(r["coarse_fine_reference_Hilbert_on_matter_grid"] for r in finer)<.003
    assert rebound["rest_demodulated_Hilbert"]>.8
    coarse = result["fiber_trials"][3]["snapshots"]
    assert max(r["probability_abs_k_above_half"] for r in coarse)>.9
    attractive, _, free, reversed_field = result["open_packet_trials"]
    # All three 96-cell settings are compared at the exact same clock time.
    settings = [tr["snapshots"][-1] for tr in (attractive, free, reversed_field)]
    assert len({s["time"] for s in settings})==1
    assert settings[0]["separation_mean"]+.5 < settings[1]["separation_mean"]
    assert settings[1]["separation_mean"]+.4 < settings[2]["separation_mean"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    result = main()
    validate(result)
    (directory/"string_motion.json").write_bytes((json.dumps(result,separators=(",",":"))+"\n").encode())
    print(len(result["fiber_trials"]), "relative-fiber trials,", len(result["open_packet_trials"]), "open packet trials")
