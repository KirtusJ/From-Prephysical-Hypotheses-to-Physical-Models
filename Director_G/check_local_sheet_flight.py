"""Fixed-action Gaussian after a successful localized-sheet and base preparation.

Run python -B check_local_sheet_flight.py NEW_OUTPUT_DIRECTORY with NumPy.
The output directory may exist but the result file must be new. The exact
selector-yield checks are in the companion routed and addressed checkers.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np


def require(test, message):
    if not test:
        raise ValueError(message)


def staircase_loop(magnitude, start):
    """Evaluate two actual routes before translating the whole base packet."""
    signs = [-1]*magnitude + [1]*(2*magnitude) + [-1]*magnitude
    gains = []
    for outward in (1, -1):
        directions = [outward]*(2*magnitude) + [-outward]*(2*magnitude)
        position = start
        gain = 0
        for field, direction in zip(signs, directions):
            gain += field*(position // 2)
            position += direction
        require(position == start, "loop return")
        gains.append(gain)
    return gains[0] - gains[1]  # first arm ends on L, second on R


def flight(order, charge, read, m, n, delta, q, x):
    size = 4*order
    source = np.sin(q)**m
    source /= np.linalg.norm(source)
    b = round(math.sqrt(order/8))
    gap = staircase_loop(b, 0)
    for start in (-5, -2, 1, 4):
        require(staircase_loop(b, start) == gap, "site-dependent rail phase")
    require(gap == 2*b*b, "compensated staircase gain")
    if read == "loop":
        relative = np.exp(-2j*np.pi*charge*gap/order)
        right = source/np.sqrt(2)
        left = relative*right
    else:
        right = source.copy()
        left = np.zeros_like(right)

    initial_momentum = abs(right)**2 + abs(left)**2
    stream_r = np.exp(-1j*q)
    for _ in range(n):
        # With exp(-i*h*x) at departure, psi_new(q)=U(q) psi_old(q+h).
        shifted_r = np.roll(right, -2*charge)
        shifted_l = np.roll(left, -2*charge)
        right = stream_r*(shifted_r+shifted_l)/np.sqrt(2)
        left = stream_r.conj()*(shifted_r-shifted_l)/np.sqrt(2)
    momentum = abs(right)**2 + abs(left)**2
    density = size*(abs(np.fft.ifft(right))**2 + abs(np.fft.ifft(left))**2)
    mass_error = abs(float(density.sum()) - 1)
    chart_error = float(np.max(np.abs(momentum-np.roll(initial_momentum, -2*charge*n))))
    parity_leak = float(density[(x % 2) != n % 2].sum())
    require(max(mass_error, chart_error, parity_leak) < 1e-10, "mass, parity or exact kick")

    lam = m*delta**2
    time = n*delta**2
    variance = (lam + time**2/lam)/2
    gaussian = np.exp(-variance/2)
    if read == "loop":
        predicted_position_cf = gaussian*np.exp(-1j*time**2/2)
    else:
        predicted_position_cf = gaussian*np.cos(charge*time**2/2)
    actual_position_cf = np.sum(density*np.exp(1j*delta*x))
    j = 2*round(0.85/(2*delta))
    distance = j*delta
    contrast = float(((-1)**(j//2)*np.sum(momentum*np.exp(1j*j*q))).real)
    predicted_contrast = math.exp(-distance**2/(4*lam))*math.cos(charge*time*distance)
    row = dict(M=order, charge=charge, source=read, m=m, flight_ticks=n,
               delta=delta, effective_lambda=lam, elapsed=time, normal_variance=variance,
               x0=0, position_wavenumber=1, loop_b=b if read == "loop" else None,
               position_cf=[float(actual_position_cf.real), float(actual_position_cf.imag)],
               predicted_cf=[float(predicted_position_cf.real), float(predicted_position_cf.imag)],
               position_cf_error=float(abs(actual_position_cf-predicted_position_cf)),
               even_translation=j, separation=distance,
               contrast=contrast, predicted_contrast=predicted_contrast,
               contrast_error=abs(contrast-predicted_contrast), norm_error=mass_error,
               opposite_parity_mass=parity_leak, exact_momentum_bin_max_error=chart_error)
    return row, density


def run():
    rows = []
    conjugation = []
    for order in (128, 512, 2048, 8192):
        size = 4*order
        delta = (math.pi/order)**(1/3)
        m = 2*round(1/(2*delta**2))
        n = round(0.75/delta**2)
        q = 2*np.pi*np.arange(size)/size
        x = np.arange(size)
        x[x >= size//2] -= size
        for read in ("rail_R", "loop"):
            positive = None
            for charge in (1, -1, 0):
                if charge == 0 and read == "loop":
                    continue
                row, density = flight(order, charge, read, m, n, delta, q, x)
                rows.append(row)
                if charge == 1:
                    positive = density
                elif charge == -1:
                    tv = float(np.abs(density-positive).sum()/2)
                    require(tv < 1e-10, "conjugate position distributions")
                    conjugation.append(dict(M=order, source=read, tv=tv))
    return dict(scope="Full two-rail final position and coherent translation after successful base "
                      "preparation, with F=1 and eps=1. Asymptotic Gaussian predictions are "
                      "compared at actual m*delta^2 and n*delta^2, with no finite error cutoff.",
                rows=rows, conjugation=conjugation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    output = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/"local_sheet_flight.json").open("x", encoding="utf8", newline="\n") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")
