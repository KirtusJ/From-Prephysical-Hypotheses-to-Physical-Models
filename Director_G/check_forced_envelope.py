"""Propagate exact two-channel fibres and compare with the forced scalar envelope."""

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from check_walk import fibre_step, omega, positive_eigenvector


EDGE = -np.pi / 2


def edge_spinor(momentum):
    """Choose the section obtained by projecting the central eigenvector."""
    v = positive_eigenvector(momentum)
    centre = positive_eigenvector(np.array([EDGE]))[0]
    overlap = v.conj() @ centre
    return v * (overlap / np.abs(overlap))[:, None]


def trial(sheet_order, scale_exponent, force, p, t_max):
    delta = (np.pi / sheet_order)**(1/scale_exponent)
    eps = delta if scale_exponent == 4 else 1.0
    radius = float(max(abs(p)))
    momentum = EDGE + delta*p
    state = edge_spinor(momentum)
    phase_sum = np.zeros_like(p)
    for n in range(1, math.floor(t_max/(eps*delta**2)) + 1):
        t = n*eps*delta**2
        current_p = p - force*t
        current_k = EDGE + delta*current_p
        state = fibre_step(state, current_k)
        phase_sum += omega(current_k) - omega(EDGE)
        action = (t*p**2/2 - force*t*t*p/2 + force**2*t**3/6)/eps
        readout = edge_spinor(current_k)
        exact = np.exp(1j*n*omega(EDGE))*state
        comparison = np.exp(-1j*action)[:, None] * readout
        residual = np.linalg.norm(exact-comparison, axis=1)
        transport = np.linalg.norm(exact-np.exp(-1j*phase_sum)[:, None]*readout, axis=1)
        leakage = np.abs(readout[:, 0]*state[:, 1]-readout[:, 1]*state[:, 0])**2
        max_p = radius + abs(force)*t
        frame_bound = 2*abs(force)*t*delta
        dispersion_bound = t*delta**2*max_p**4/(6*eps)
        quadrature_bound = t*abs(force)*max_p*delta**2/2
        bound = frame_bound + dispersion_bound + quadrature_bound
        for j, initial_p in enumerate(p):
            yield (sheet_order, scale_exponent, force, delta, eps, n, t, initial_p, residual[j], bound,
                   transport[j], frame_bound, leakage[j], abs(phase_sum[j]-action[j]), dispersion_bound+quadrature_bound,
                   abs(np.linalg.norm(state[j])-1))


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    p = np.linspace(-0.75, 0.75, 17)
    rows = 0
    summaries = []
    checks = dict(frame=True, dispersion=True, envelope=True, norm=True)
    with (out / "forced_envelope_trials.csv").open("w", encoding="utf8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("M", "field_scale_exponent", "force", "delta", "eps", "step", "time", "initial_p",
                         "spinor_distance", "distance_bound", "frame_error", "frame_bound", "band_leakage_probability",
                         "unwrapped_phase_error", "phase_bound", "norm_error"))
        for m in (65, 257, 1025, 4097, 16385):
            for exponent in (3, 4):
                for force in (-1, 0, 1):
                    maximum = 0.
                    for row in trial(m, exponent, force, p, 0.75):
                        writer.writerow(row)
                        rows += 1
                        maximum = max(maximum, row[8])
                        checks["envelope"] &= bool(row[8] <= row[9]+2e-12)
                        checks["frame"] &= bool(row[10] <= row[11]+2e-12)
                        checks["dispersion"] &= bool(row[13] <= row[14]+2e-12)
                        checks["norm"] &= bool(row[15] < 2e-12)
                    summaries.append(dict(M=m, field_scale_exponent=exponent, force=force,
                                          max_spinor_distance=maximum))
    report = dict(checks=checks, rows=rows, summaries=summaries, scope="Deterministic binary64 fibre samples on the line.")
    (out / "forced_envelope.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n", encoding="utf8")
    print(checks, rows)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    main(parser.parse_args().out)
