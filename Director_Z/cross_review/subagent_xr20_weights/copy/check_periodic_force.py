"""Finite periodic two-body walks against phase-sensitive periodic Schrödinger references.

Run python -B check_periodic_force.py results. All quantities are dimensionless.
The discrete ring Fourier convention is exp(+i*l*Y) in the inverse transform.
"""

import argparse
import csv
import json
import os
import platform
from itertools import product
from math import ceil, pi, sqrt
from pathlib import Path

# These checks run in one process. Keep FFT and vector-library worker pools bounded.
for variable in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np


EDGE = -pi/2
CARRIER_FREQUENCY = -pi/4
TARGET_TIME = 0.75
CENTRES = (1.2, -0.6)


def modes(size):
    return np.rint(np.fft.fftfreq(size)*size).astype(int)


def vector_norm(values):
    return float(sqrt(np.sum(abs(values)**2)))


def field_shape(size):
    y = 2*pi*np.arange(size)/size
    return 1 - np.cos(y[:, None] - y[None, :])


def initial_fourier(size, eps, regime):
    ell = modes(size)
    if regime == "quantum":
        # Product of two explicit, low-degree trigonometric polynomials.
        first = (ell == 0) + 0.65*np.exp(-1.2j)*(ell == 1) + 0.3j*(ell == -2)
        second = (ell == 0) + 0.6*np.exp(0.5j)*(ell == -1)
    else:
        # Periodized Gaussian amplitudes with zero mean momentum, angular width O(sqrt(eps)).
        gaussian = np.exp(-eps*ell**2/2)
        first, second = (gaussian*np.exp(-1j*ell*centre) for centre in CENTRES)
    pair = first[:, None]*second[None, :]
    return pair/vector_norm(pair)


def plus_section(size):
    # The normalized first column of the plus-band projector of diag(e^-ik,e^ik) H.
    k = EDGE + 2*pi*modes(size)/size
    c, s = np.cos(k), np.sin(k)
    r = np.sqrt(1 + c*c)
    section = np.stack((r + c, c + 1j*s), axis=-1)
    section /= np.linalg.norm(section, axis=-1, keepdims=True)
    return section


def encode(coefficients, section):
    return (coefficients[:, :, None, None]*section[:, None, :, None]*
            section[None, :, None, :])


def exact_walk(size, eps, steps, kappa, order, regime, relative_gains=None):
    a = 2*pi/size
    shape = field_shape(size)
    ideal_angle = (a/eps)**2 * kappa * shape
    if order == 0:
        departure = np.exp(-1j*ideal_angle)
        angle_error = 0.
        max_gain = None
    else:
        if relative_gains is None:
            gains = np.rint(order*ideal_angle/(2*pi)).astype(np.int64)
        else:
            sites = np.arange(size)
            gains = np.asarray(relative_gains)[(sites[:,None]-sites[None,:]) % size]
        angle = (2*pi/order)*gains
        departure = np.exp(-1j*angle)
        angle_error = float(np.max(abs(angle - ideal_angle)))
        max_gain = int(np.max(abs(gains)))
    section = plus_section(size)
    spinor = encode(initial_fourier(size, eps, regime), section)
    # Multiply the position state by the spatial carrier exp(i*k* (x1+x2)).
    spinor = np.fft.ifft2(np.roll(spinor, (-size//4, -size//4), axis=(0, 1)),
                          axes=(0, 1), norm="ortho")
    for _ in range(steps):
        scattered = spinor*departure[:, :, None, None]
        first = (scattered[:, :, 0, :] + scattered[:, :, 1, :])/sqrt(2)
        second = (scattered[:, :, 0, :] - scattered[:, :, 1, :])/sqrt(2)
        for coin1, row in enumerate((first, second)):
            right = (row[:, :, 0] + row[:, :, 1])/sqrt(2)
            left = (row[:, :, 0] - row[:, :, 1])/sqrt(2)
            shift = 1 if coin1 == 0 else -1
            spinor[:, :, coin1, 0] = np.roll(right, (shift, 1), axis=(0, 1))
            spinor[:, :, coin1, 1] = np.roll(left, (shift, -1), axis=(0, 1))
    expectation = float(np.sum(abs(spinor)**2*shape[:, :, None, None]))
    fourier = np.fft.fft2(spinor, axes=(0, 1), norm="ortho")
    fourier = np.roll(fourier, (size//4, size//4), axis=(0, 1))
    fourier *= np.exp(2j*steps*CARRIER_FREQUENCY)
    projection = np.sum(fourier*np.conj(encode(np.ones((size, size)), section)), axis=(2, 3))
    residual = fourier - encode(projection, section)
    return fourier, dict(walk_norm_error=abs(vector_norm(fourier)-1),
                         walk_relative_separation_observable=expectation, max_abs_integer_gain=max_gain,
                         leakage_probability=vector_norm(residual)**2,
                         maximum_step_rounding_error=angle_error)


def strang(size, steps, time, eps, kappa, regime):
    """Symmetric potential--kinetic--potential split of the scalar PDE."""
    ell = modes(size)
    shape = field_shape(size)
    dt = time/steps
    half = np.exp(-0.5j*dt*kappa/eps*shape)
    full = half*half
    kinetic = np.exp(-0.5j*dt*eps*(ell[:, None]**2 + ell[None, :]**2))
    state = np.fft.ifft2(initial_fourier(size, eps, regime), norm="ortho")*half
    for index in range(steps):
        coeff = np.fft.fft2(state, norm="ortho")*kinetic
        state = np.fft.ifft2(coeff, norm="ortho")
        state *= half if index == steps-1 else full
    expectation = float(np.sum(abs(state)**2*shape))
    return np.fft.fft2(state, norm="ortho"), expectation


def truncate(fine, size):
    indices = modes(size) % fine.shape[0]
    coarse = fine[np.ix_(indices, indices)]
    outside = fine.copy()
    outside[np.ix_(indices, indices)] = 0
    return coarse, vector_norm(outside)


def scalar_distance(coarse, fine):
    retained, tail = truncate(fine, coarse.shape[0])
    return float(np.hypot(vector_norm(coarse-retained), tail))


def reference_solutions(size, time, eps, kappa, regime):
    # Spatial grid size and time resolution are refined separately.
    count = max(24, ceil(time/0.015))
    medium, _ = strang(2*size, count, time, eps, kappa, regime)
    small, _ = strang(size, count, time, eps, kappa, regime)
    fine, expectation = strang(2*size, 2*count, time, eps, kappa, regime)
    stats = dict(ref_space_difference=scalar_distance(small, medium),
                 ref_time_difference=vector_norm(medium-fine),
                 ref_steps=2*count, ref_grid=2*size, ref_norm_error=abs(vector_norm(fine)-1),
                 ref_observable=expectation)
    if kappa == 0:
        ell = modes(2*size)
        free = initial_fourier(2*size, eps, regime)*np.exp(
            -0.5j*time*eps*(ell[:, None]**2 + ell[None, :]**2))
        stats["ref_free_exact_distance"] = vector_norm(fine-free)
    else:
        stats["ref_free_exact_distance"] = None
    return fine, stats


def position_flow(time, kappa):
    # Classical relative coordinate r obeys r''=-2*kappa*sin(r). Initial speed is zero.
    def solve(count):
        state = np.array([CENTRES[0]-CENTRES[1], 0.])
        dt = time/count

        def rhs(v):
            return np.array([v[1], -2*kappa*np.sin(v[0])])

        for _ in range(count):
            k1 = rhs(state)
            k2 = rhs(state+dt*k1/2)
            k3 = rhs(state+dt*k2/2)
            k4 = rhs(state+dt*k3)
            state += dt*(k1+2*k2+2*k3+k4)/6
        return float(1-np.cos(state[0]))

    fine = solve(192)
    return fine, abs(fine-solve(96))


def compare(spinor, reference):
    size = spinor.shape[0]
    section = plus_section(size)
    retained, tail = truncate(reference, size)
    encoded = encode(retained, section)
    edge = np.broadcast_to(section[0], section.shape)
    frozen = encode(retained, edge)
    return dict(spinor_distance=float(np.hypot(vector_norm(spinor-encoded), tail)),
                constant_edge_distance=float(np.hypot(vector_norm(spinor-frozen), tail)),
                continuum_outside_walk_square_norm=tail,
                overlap_real=float(np.vdot(encoded, spinor).real),
                overlap_imag=float(np.vdot(encoded, spinor).imag))


def experiment(size, regime):
    a = 2*pi/size
    eps = 1. if regime == "quantum" else sqrt(a)
    delta = a/eps
    tau = eps*delta**2
    steps = round(TARGET_TIME/tau)
    time = steps*tau
    accurate_order = 2*ceil(1e5*steps)+1
    specs = [(0., accurate_order, "free"), (1., accurate_order, "attractive"),
             (1., 3, "coarse_sheet"), (1., 0, "continuous_phase"),
             (-1., accurate_order, "repulsive")]
    exact = {}
    rows = []
    fine_initial = initial_fourier(2*size, eps, regime)
    initial_tail = truncate(fine_initial, size)[1]
    initial_difference = scalar_distance(initial_fourier(size, eps, regime), fine_initial)
    accurate_attractive = None
    for kappa in (0., 1., -1.):
        exact[kappa] = reference_solutions(size, time, eps, kappa, regime)
    for kappa, order, label in specs:
        spinor, walk = exact_walk(size, eps, steps, kappa, order, regime)
        observed_rounding = None
        rounding_budget = None
        if label == "attractive":
            accurate_attractive = spinor
        if label == "continuous_phase":
            observed_rounding = vector_norm(spinor-accurate_attractive)
            rounding_budget = steps*pi/accurate_order
        comparisons = [(kappa, label)]
        if label == "repulsive":
            comparisons.append((1., "wrong_force_against_attractive"))
        for ref_kappa, category in comparisons:
            fine, stats = exact[ref_kappa]
            row = dict(N=size, regime=regime, case=category, walk_kappa=kappa,
                       reference_kappa=ref_kappa, sheet_order=order, a=a, eps=eps,
                       delta=delta, tau=tau, steps=steps, time=time,
                       initial_reference_outside_square_norm=initial_tail,
                       initial_grid_difference=initial_difference,
                       accurate_vs_unrounded_distance=observed_rounding,
                       accurate_vs_unrounded_bound=rounding_budget,
                       telescoped_rounding_bound=steps*pi/order if order else 0.,
                       **walk, **stats, **compare(spinor, fine))
            row["quantum_observable_abs_error"] = abs(walk["walk_relative_separation_observable"] -
                                                       stats["ref_observable"])
            row["classical_point_observable"] = None
            row["classical_point_abs_error"] = None
            row["classical_step_refinement"] = None
            if regime == "semiclassical":
                classical, diff = position_flow(time, ref_kappa)
                row.update(classical_point_observable=classical, classical_step_refinement=diff,
                           classical_point_abs_error=abs(walk["walk_relative_separation_observable"]-classical))
            rows.append(row)
    return rows


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    all_rows = []
    for size, regime in product((32, 48, 64), ("quantum", "semiclassical")):
        all_rows.extend(experiment(size, regime))
    with (output/"periodic_force_trials.csv").open("w", encoding="utf8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=all_rows[0])
        writer.writeheader()
        writer.writerows(all_rows)
    groups = [(regime, size) for regime in ("quantum", "semiclassical") for size in (32, 48, 64)]
    pairs = [{r["case"]: r for r in all_rows if (r["regime"], r["N"]) == key} for key in groups]
    checks = dict(
        norm=all(max(r["walk_norm_error"], r["ref_norm_error"]) < 2e-12 for r in all_rows),
        certified_phase_rounding=all(r["maximum_step_rounding_error"] <= pi/r["sheet_order"] + 1e-14
                                     for r in all_rows if r["sheet_order"]),
        observed_rounding_within_bound=all(r["accurate_vs_unrounded_distance"] <=
                                           r["accurate_vs_unrounded_bound"] + 2e-12 for r in all_rows
                                           if r["case"] == "continuous_phase"),
        coarse_integer_gain_vanishes=all(r["max_abs_integer_gain"] == 0 for r in all_rows
                                         if r["case"] == "coarse_sheet"),
        free_scalar_oracle=all(r["ref_free_exact_distance"] < 2e-12 for r in all_rows if r["case"] == "free"),
        space_difference=all(r["ref_space_difference"] < 1e-8 for r in all_rows),
        time_difference=all(r["ref_time_difference"] < 1e-4 for r in all_rows),
        attractive_beats_wrong_sign=all(p["attractive"]["spinor_distance"] <
                                        p["wrong_force_against_attractive"]["spinor_distance"] for p in pairs),
        attractive_beats_coarse_order=all(p["attractive"]["spinor_distance"] <
                                          p["coarse_sheet"]["spinor_distance"] for p in pairs),
    )
    report = dict(checks=checks, rows=len(all_rows), runtime=dict(python=platform.python_version(), numpy=np.__version__),
                  target_time=TARGET_TIME, semiclassical_packet_centres=CENTRES,
                  observable="1-cos(Y1-Y2)", sheet_order_zero="Unrounded continuous departure control.",
                  norm_comparison="Absolute unfitted norm after both temporal carriers and spatial momenta are removed. "
                                  "Full reference includes every resolved Fourier coefficient on its larger grid.",
                  reference_limit="Changes on doubling grid and time resolution are observed differences, "
                                  "not certified bounds on the continuum solution.",
                  cases=all_rows)
    (output/"periodic_force.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf8")
    print(len(all_rows), checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    main(parser.parse_args().output)
