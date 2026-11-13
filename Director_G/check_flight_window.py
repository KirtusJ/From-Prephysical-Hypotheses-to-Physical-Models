"""Run python -B check_flight_window.py OUTPUT_DIRECTORY (NumPy for the long panels).

At tick T copy one blank bit to 1 exactly on positions lo <= x <= hi.
Keep both bits in the output. A flight of S ticks ends at absolute tick T+S.
All probability predictions refer to a common score on complete tagged arrays.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import json
from math import ceil, floor, sqrt
import os
from pathlib import Path

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"
import numpy as np


def move(state):
    out = Counter()
    for (x, rail), a in state.items():
        out[x+1, 0] += a
        out[x-1, 1] += a if rail == 0 else -a
    return {key: value for key, value in out.items() if value}


def fly(state, steps):
    for _ in range(steps):
        state = move(state)
    return state


def squared(state):
    return {key: a*a for key, a in state.items()}


def resolved(prefix, steps, lo, hi, rail_read):
    """Retain a separate prefix label for each site, or for each site and rail."""
    groups = {}
    for (x, c), a in prefix.items():
        label = (x, c) if rail_read else x
        groups.setdefault(label, {})[x, c] = a
    mass = [Counter(), Counter()]
    for state in groups.values():
        x, _ = next(iter(state))
        tag = int(lo <= x <= hi)
        mass[tag].update(squared(fly(state, steps)))
    return mass


def passive(prefix, steps, lo, hi, t):
    """One admissible marker coupling: direction choice depends only on parent site.

    The subsequent signed totals include all prefixes; the tag is a passive log.
    """
    rows = [Counter(), Counter()]
    for (x, c), a in prefix.items():
        rows[int(lo <= x <= hi)][x, c] = F(a*a, 2**t)
    full = prefix
    for _ in range(steps):
        new_rows = [Counter(), Counter()]
        for x in {x for x, c in full}:
            r, l = full.get((x, 0), 0), full.get((x, 1), 0)
            right = F((r+l)**2, 2*(r*r+l*l))
            for tag in (0, 1):
                before = rows[tag][x, 0]+rows[tag][x, 1]
                new_rows[tag][x+1, 0] += before*right
                new_rows[tag][x-1, 1] += before*(1-right)
        rows, full = new_rows, move(full)
    return rows


def pack(row, ports):
    return [row.get(key, 0) for key in ports]


def exact_panel(t, s, lo, hi):
    prefix = fly({(0, 0): 1}, t)
    groups = [{k: a for k, a in prefix.items() if int(lo <= k[0] <= hi) == tag} for tag in (0, 1)]
    split = [fly(state, s) for state in groups]
    bare = fly(prefix, s)
    ports = [(x, c) for x in range(-t-s, t+s+1) for c in (0, 1)]
    den = 2**(t+s)
    score = [squared(state) for state in split]
    site, full_read = resolved(prefix, s, lo, hi, False), resolved(prefix, s, lo, hi, True)
    log = passive(prefix, s, lo, hi, t)
    weights = [F(sum(squared(state).values()), 2**t) for state in groups]
    assert sum(weights) == 1
    for key in ports:
        assert sum(state.get(key, 0) for state in split) == bare.get(key, 0)
        assert sum(branch.get(key, 0) for branch in log) == F(bare.get(key, 0)**2, den)
    for tag in (0, 1):
        assert all(F(sum(law[tag].values()), den) == weights[tag] for law in (score, site, full_read))
        assert sum(log[tag].values()) == weights[tag]
    def tv(other, denom):
        return sum(abs(F(score[tag].get(key, 0), den)-F(other[tag].get(key, 0), denom))
                   for tag in (0, 1) for key in ports)/2
    unmarked_tv = sum(abs(sum(F(row.get(key, 0), den) for row in score)-F(bare.get(key, 0)**2, den))
                      for key in ports)/2
    return dict(T=t, S=s, window=[lo, hi], bound=t+s, prefix_tag_mass=weights,
                prefix_raw=[prefix.get((x, c), 0) for x in range(-t, t+1) for c in (0, 1)],
                raw_by_tag=[pack(v, ports) for v in split], raw_without_copy=pack(bare, ports),
                denominator=den, site_resolved_numerators=[pack(v, ports) for v in site],
                site_rail_resolved_numerators=[pack(v, ports) for v in full_read],
                passive_joint_probabilities=[pack(v, ports) for v in log],
                joint_TV=dict(site_read=tv(site, den), site_rail_read=tv(full_read, den),
                              passive_marker=tv(log, 1)), unconditioned_TV_from_blank=unmarked_tv)


def spectral_flight(spinor, steps, k):
    """Apply U(k)^steps by its two distinct spectral roots, keeping both rails."""
    transformed = np.fft.fft(spinor, axis=1)
    er = np.exp(-1j*k)
    r, l = transformed
    single = np.stack(((r+l)*er, (r-l)*er.conj()))/sqrt(2)
    omega = np.arcsin(np.sin(k)/sqrt(2))
    positive, negative = np.exp(-1j*omega), -np.exp(1j*omega)
    plus = (single-negative*transformed)/(positive-negative)
    # Use explicit real phases to avoid feeding a large integer exponent to complex pow.
    final = (np.exp(-1j*steps*omega)*plus
             + (-1)**steps*np.exp(1j*steps*omega)*(transformed-plus))
    return np.fft.ifft(final, axis=1)


def spectral_check():
    max_error = 0.0
    n = 128
    k = 2*np.pi*np.fft.fftfreq(n)
    state = np.zeros((2, n))
    state[0, 0] = 1
    for t in (0, 1, 3, 6, 11):
        actual = spectral_flight(state, t, k)
        expected = np.zeros_like(state)
        for (x, c), a in fly({(0, 0): 1}, t).items():
            expected[c, x % n] = a/2**(t/2)
        max_error = max(max_error, float(np.max(np.abs(expected-actual))))
    assert max_error < 1e-12
    return max_error


def numerical_panel(inverse_delta, p0=1, flight_time=1, tolerance=0.5):
    delta = 1/inverse_delta
    pitch, tick = delta**2, delta**3
    center = delta*p0
    w = delta**1.1
    t = round(delta**-2.8)
    s = round(flight_time/tick)
    half_width = t*w
    horizon = t+s
    n = 1 << (2*horizon+2).bit_length()
    k = 2*np.pi*np.fft.fftfreq(n)
    x = np.arange(n)
    x = np.where(x < n//2, x, x-n)
    spinor = np.zeros((2, n))
    spinor[0, 0] = 1
    prefix = spectral_flight(spinor, t, k)
    lo, hi = ceil(t*center-half_width), floor(t*center+half_width)
    mask = (x >= lo) & (x <= hi)
    outputs = []
    combined = np.zeros_like(prefix)
    for bit in (0, 1):
        branch = prefix*(mask if bit else ~mask)
        source_weight = float(np.vdot(branch, branch).real)
        terminal = spectral_flight(branch, s, k)
        combined += terminal
        mass = np.sum(np.abs(terminal)**2, axis=0)
        total = float(mass.sum())
        assert abs(total-source_weight) < 2e-11
        velocity = (x-center*t)/(s*delta)
        outputs.append(dict(bit=bit, prefix_mass=source_weight, terminal_mass=total,
                            conditional_mean_physical_velocity=float(np.sum(mass*velocity)/total),
                            conditional_RMS_from_p0=float(np.sqrt(np.sum(mass*(velocity-p0)**2)/total)),
                            conditional_tail=float(mass[np.abs(velocity-p0) > tolerance].sum()/total)))
    assert abs(sum(b["prefix_mass"] for b in outputs)-1) < 2e-11
    superposition_error = float(np.linalg.norm(combined-spectral_flight(spinor, horizon, k)))
    assert superposition_error < 1e-10
    return dict(inverse_delta=inverse_delta, T=t, S=s, N=n, delta=delta, pitch=pitch,
                tick_duration=tick, release_time=t*tick, flight_duration=s*tick,
                predicted_release_position=pitch*t*center, predicted_terminal_position=pitch*horizon*center,
                target_physical_velocity=p0, window_center_lattice_velocity=center, velocity_half_width=w,
                position_half_width=half_width, inclusive_window=[lo, hi],
                lattice_sites_reachable_in_window=int(np.count_nonzero(mask & ((x-t) % 2 == 0) & (np.abs(x) <= t))),
                tolerance_physical_velocity=tolerance, outcomes=outputs,
                yes_mass_over_2w_pi=outputs[1]["prefix_mass"]/(2*w/np.pi),
                erased_tag_amplitude_error=superposition_error)


def main():
    # Predeclared panels. Store every case without selecting on numerical agreement.
    short = [(3, 1, 1, 1), (3, 4, 1, 1), (6, 8, 0, 2), (6, 8, 6, 6),
             (5, 4, 0, 0), (4, 4, -4, 4)]
    long = (4, 6, 8, 12, 16, 24, 32, 40)
    exact = [exact_panel(*args) for args in short]
    assert exact[0]["unconditioned_TV_from_blank"] == 0
    assert exact[1]["unconditioned_TV_from_blank"] > 0
    assert exact[2]["joint_TV"]["site_read"] > 0
    assert exact[1]["joint_TV"]["site_rail_read"] > 0
    assert exact[3]["prefix_tag_mass"][1] == F(1, 64)
    assert exact[4]["prefix_tag_mass"][1] == 0 and exact[5]["prefix_tag_mass"][1] == 1
    return dict(predicates_before_run=[
        "All short, unwrapped panels use exact signed integer paths. For each pointer value its probability at the prefix equals its full terminal mass. At each terminal cell the sum of the two signed branch amplitudes equals the blank-pointer amplitude.",
        "The passive route log marginalizes to the original untagged squared law; a nonzero change in its unconditioned endpoint law after a physical copy also excludes every passive logging of the same terminal marginals.",
        "The one-step singleton panel preserves unconditioned terminal marginals. The four-step singleton changes them. Resolving site at a two-site window and resolving rails in the singleton can change the full joint law. The rightmost path, parity-dark, and full windows have masses 1/64,0,1.",
        "Compare the Fourier implementation with full signed exact vectors before longer trials. Retain every postflight conditional tail, including large errors; enforce norm checks but no empirical monotonicity threshold."],
        exact_convention="bit order 0=outside,1=inside. Each vector uses every site in [-bound,bound] in increasing order, R then L. For prefix_raw, bound=T. No omitted zeros. Square raw_by_tag entries and divide by denominator to recover the joint terminal law; the site-dephased numerators already contain squares. Passive values are rational probabilities.",
        physics="Sharp (0,R), no field. Fourier convention exp(-ikx). Units epsilon=delta, pitch=delta², tick=delta³; target p0=1. Window |x/T-delta*p0|<=delta^(11/10); T=round(delta^(-14/5)), S=round(delta^(-3)), observed at absolute tick T+S. Physical displacement starts at the nominal release center. The tolerance in velocity is 1/2. The reference acceptance 2w/pi is asymptotic.",
        instrument="Extended complete detector law f(D)=D² applies to (bit,x,rail) and terminal resolution is additive. The XOR copies membership of the site in W and preserves rail/site coherence within each class; there is no repeated measurement during either flight. Passive coupling chooses the right daughter with probability (r+l)²/[2(r²+l²)] at each positive-mass site using the original untagged totals. Retaining per-site or per-site-and-rail records is a distinct operation.",
        exact=exact, spectral_error_against_integer_amplitudes=spectral_check(),
        numeric=[numerical_panel(j) for j in long],
        precision="Exact tables use integer or reduced rational entries. Floating diagnostics retain full binary64 round-trip precision, including small residuals. Exact zeros and measured numerical residuals are stored separately where specified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    directory = parser.parse_args().output
    directory.mkdir(parents=True, exist_ok=True)
    result = main()
    (directory/"flight_window.json").write_bytes((json.dumps(result, default=str, separators=(",", ":"))+"\n").encode("utf-8"))
    print(f'Checked {len(result["exact"])} exact pointer panels and {len(result["numeric"])} spectral flights.')
