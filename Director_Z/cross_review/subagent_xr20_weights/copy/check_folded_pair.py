"""Folded, field-off direction preparations and measured torus positions after an interaction.

Run python -B check_folded_pair.py results. Every flight uses the full four-component
state. Characteristic functions refer to a single terminal position read per flight.
"""

import argparse
import json
import os
import platform
from fractions import Fraction
from itertools import product
from math import ceil, comb, pi, sqrt
from pathlib import Path

for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np

from check_cycle_interaction import count_table
from check_walk import positive_eigenvector


OBSERVABLES = ((1, 0), (0, 1), (1, -1), (1, 1), (2, -1))
TARGETS = (0., 0.75, 1.5)


def norm(state):
    return float(np.sqrt(np.sum(abs(state)**2)))


def complex_pair(z):
    return [float(z.real), float(z.imag)]


def prepared_ring(size, blocks):
    # For even m the final direction is R; two literal steps and a coherent direction read
    # give integer counts before division by 2 per block.
    right, left = [1]+[0]*(size-1), [0]*size
    for j in range(blocks):
        for _ in range(2):
            right, left = ([right[(x-1) % size]+left[(x-1) % size] for x in range(size)],
                           [right[(x+1) % size]-left[(x+1) % size] for x in range(size)])
        if j % 2 == 0:
            right = [0]*size
        else:
            left = [0]*size
    counts = [0]*size
    for j in range(blocks+1):
        counts[(2*j-blocks) % size] += (-1)**j*comb(blocks, j)
    squared = sum(value*value for value in counts)
    alias_sum = sum(comb(2*blocks, blocks+q*size//2)
                    for q in range(-2*blocks//size-1, 2*blocks//size+2)
                    if 0 <= blocks+q*size//2 <= 2*blocks)
    ring = Fraction(squared, 4**blocks)
    line = Fraction(comb(2*blocks, blocks), 4**blocks)
    sites = np.arange(size)
    k = 2*pi*sites/size
    literal = np.array([value/2**blocks for value in counts])
    exact_fourier = (-1j)**blocks*np.sin(k)**blocks/np.sqrt(size)
    shell_error = norm(np.fft.fft(literal, norm="ortho")-exact_fourier)
    density = abs(exact_fourier)**2/float(ring)
    spectral_plus = abs(positive_eigenvector(k)[:, 0])**2
    # Sectors 0<=k<pi and pi<=k<2pi surround +pi/2 and -pi/2 respectively.
    labels = (("positive_edge", sites < size//2, -1),
              ("negative_edge", sites >= size//2, 1))
    chart_weights = []
    branch_weights = {1: 0., -1: 0.}
    for edge, mask, plus_curvature in labels:
        for band, probabilities, sign in (("plus", spectral_plus, plus_curvature),
                                          ("minus", 1-spectral_plus, -plus_curvature)):
            weight = float(density[mask] @ probabilities[mask])
            chart_weights.append(dict(edge=edge, band=band, curvature=sign, mass=weight))
            branch_weights[sign] += weight
    pair_weights = [{"curvatures": [u, v], "mass": branch_weights[u]*branch_weights[v]}
                    for u, v in product((1, -1), repeat=2)]
    data = dict(N=size, blocks=blocks, counts_equal_folded_binomials=(counts == right and not any(left)),
                exact_alias_sum_matches=(squared == alias_sum), ring_yield=str(ring), line_yield=str(line),
                ring_yield_decimal=float(ring), alias_relative_gain=float(ring/line-1),
                strict_alias_gain=bool(ring > line), pair_success=float(ring**2),
                fourier_yield=float(sum(abs(exact_fourier)**2)), unfitted_fourier_distance=shell_error,
                one_particle_chart_weights=chart_weights, pair_curvature_weights=pair_weights)
    return literal/sqrt(float(ring)), data


def count_gains(size, order):
    depth = ceil(0.4*size**2)
    counts = count_table(size, depth)
    den = counts[0]-counts[size//2]
    # M delta^2/(2 pi) = M/N exactly, and odd M precludes a tie for the choices below.
    scale = (2*order+size)//(2*size)
    gain = [(4*scale*(counts[0]-c)+den)//(2*den) for c in counts]
    a = 2*pi/size
    shape = 1-np.cos(a*np.arange(size))
    angles = (2*pi/order)*np.array(gain)
    return angles, dict(sheet_order=order, depth=depth, amplitude_scale=scale,
                        integer_gain=gain, count_sum_exact=(sum(counts) == 4**depth),
                        angle_error_vs_smooth=float(np.max(abs(angles-a*shape))))


def joint_walk_step(state, departure):
    # Physical site-space two-particle H tensor H, followed by both output shifts.
    coin = np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]])/2
    mixed = (state*departure[:, :, None]) @ coin.T
    result = np.empty_like(state)
    for channel, shifts in enumerate(product((1, -1), repeat=2)):
        result[:, :, channel] = np.roll(mixed[:, :, channel], shifts, axis=(0, 1))
    return result


def spectral_walk_step(state, departure):
    # Independently apply the two Fourier fibre matrices, including their output phases.
    n = state.shape[0]
    momenta = np.arange(n)*2*pi/n
    phase = np.exp(-1j*momenta)
    matrices = np.stack((phase, phase, phase.conj(), -phase.conj()), axis=-1).reshape(n, 2, 2)/sqrt(2)
    fourier = np.fft.fft2((state*departure[:, :, None]).reshape(n, n, 2, 2), axes=(0, 1))
    mixed = np.einsum("xai,ybj,xyij->xyab", matrices, matrices, fourier, optimize=True)
    return np.fft.ifft2(mixed, axes=(0, 1)).reshape(n, n, 4)


def branch_positions(time, kappa, count):
    # Both particles start at specified ring sites with zero canonical momentum.
    b = np.array(list(product((1, -1), repeat=2)))
    state = np.zeros((4, 4))
    state[:, :2] = np.array([pi/2, 0])
    dt = time/count

    def rhs(value):
        f = kappa*np.sin(value[:, 0]-value[:, 1])
        return np.column_stack((b[:, 0]*value[:, 2], b[:, 1]*value[:, 3], -f, f))

    for _ in range(count):
        k1 = rhs(state)
        k2 = rhs(state+dt*k1/2)
        k3 = rhs(state+dt*k2/2)
        k4 = rhs(state+dt*k3)
        state += dt*(k1+2*k2+2*k3+k4)/6
    return state[:, :2]


def record(state, sign, time, values, conjugation, spectral_error):
    density = np.sum(abs(state)**2, axis=2)
    fine = branch_positions(time, sign, 192)
    coarse = branch_positions(time, sign, 96)
    stats = []
    for (u, v), observable in zip(OBSERVABLES, values):
        walk = np.sum(density*observable)
        branch = np.mean(np.exp(1j*(u*fine[:, 0]+v*fine[:, 1])))
        stats.append(dict(frequencies=[u, v], walk=complex_pair(walk),
                          classical_equal_mixture=complex_pair(branch), distance=float(abs(walk-branch))))
    return dict(sheet_sign=sign, mass=float(density.sum()),
                conjugate_sector_unfitted_state_error=conjugation,
                spectral_vs_real_unfitted_state_error=spectral_error,
                classical_positions=fine.tolist(), classical_max_refinement=float(np.max(abs(fine-coarse))),
                characteristics=stats, maximum_characteristic_residual=max(x["distance"] for x in stats))


def flight(size):
    a = 2*pi/size
    delta = sqrt(a)
    tau = delta**3
    blocks = 2*round(delta**(-2.5)/2)
    base, prep = prepared_ring(size, blocks)
    targets = {round(t/tau): t for t in TARGETS}
    order = 200000*max(targets)+1
    angles, gains = count_gains(size, order)
    x = np.arange(size)
    field = np.exp(-1j*angles[(x[:, None]-x[None, :]) % size])
    # Each unnormalized retained R amplitude is real. Translate the first origin by N/4.
    start = np.zeros((size, size, 4), dtype=complex)
    start[:, :, 0] = np.roll(base, size//4)[:, None]*base[None, :]
    positive, negative = start.copy(), start.copy()
    spectral = start.copy() if size == 32 else None
    observables = [np.exp(1j*a*(u*x[:, None]+v*x[None, :])) for u, v in OBSERVABLES]
    rows = []
    for tick in range(max(targets)+1):
        if tick in targets:
            t = tick*tau
            conjugation_error = norm(positive-negative.conj())
            for sign, state in ((1, positive), (-1, negative)):
                # The independent Fourier solver follows the positive sector only.
                spect_err = norm(spectral-positive) if sign == 1 and spectral is not None else None
                row = record(state, sign, t, observables, conjugation_error, spect_err)
                row.update(ticks=tick, time=t, target_time=targets[tick])
                rows.append(row)
        if tick != max(targets):
            positive = joint_walk_step(positive, field)
            negative = joint_walk_step(negative, field.conj())
            if spectral is not None:
                spectral = spectral_walk_step(spectral, field)
    return dict(N=size, delta=delta, tau=tau, preparation=prep, count_interaction=gains, trials=rows)


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    flights = [flight(n) for n in (32, 48, 64, 96)]
    preparations = [f["preparation"] for f in flights]
    # Deliberately force aliases: two amplitudes of one position parity fold onto the same site.
    alias_controls = [prepared_ring(16, m)[1] for m in (8, 16, 32)]
    preparations += alias_controls
    rows = [r for f in flights for r in f["trials"]]
    checks = dict(
        exact_integer_preparations=all(p["counts_equal_folded_binomials"] and p["exact_alias_sum_matches"]
                                       for p in preparations),
        alias_positive_controls=all(p["strict_alias_gain"] for p in alias_controls),
        spectral_profile=all(p["unfitted_fourier_distance"] < 1e-12 and
                             abs(p["fourier_yield"]-p["ring_yield_decimal"]) < 1e-12 for p in preparations),
        curvature_masses=all(abs(w["mass"]-0.25) < 1e-12 for p in preparations
                             for w in p["pair_curvature_weights"]),
        count_mass=all(f["count_interaction"]["count_sum_exact"] for f in flights),
        mass=all(abs(r["mass"]-1) < 1e-12 for r in rows),
        conjugate_sectors=all(r["conjugate_sector_unfitted_state_error"] < 1e-12 for r in rows),
        real_vs_fourier_solver=all(r["spectral_vs_real_unfitted_state_error"] < 1e-12
                                   for r in rows if r["spectral_vs_real_unfitted_state_error"] is not None),
        classical_step_doubling=all(r["classical_max_refinement"] < 2e-8 for r in rows),
    )
    positive_rows = [r for r in rows if r["sheet_sign"] == 1]
    report = dict(checks=checks, runtime=dict(python=platform.python_version(), numpy=np.__version__),
                  centres=[pi/2, 0.], direction_state="R tensor R", preparation_field=0,
                  admissible_sizes="Four divides N, even m", branch_order=["++", "+-", "-+", "--"],
                  trials=len(rows), folded_yield_positive_controls=alias_controls, flights=flights,
                  finite_accuracy=dict(metric="Maximum of five complex joint-characteristic residuals below 0.1",
                                       count=sum(r["maximum_characteristic_residual"] < 0.1 for r in positive_rows),
                                       positive_sector_trials=len(positive_rows)),
                  scope="Unmeasured evolution before one time-slice read, conditional on both prepared base words "
                        "in a specified shared sector. No path measurement, full-sheet population or tracking rate inferred.")
    (out/"folded_pair.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print(checks, report["finite_accuracy"])
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
