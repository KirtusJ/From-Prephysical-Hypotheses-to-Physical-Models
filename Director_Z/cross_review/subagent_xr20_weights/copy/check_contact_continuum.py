"""Two-body contact defect on a compact momentum chart and finite ring tests.

Run python -B check_contact_continuum.py OUTPUT_DIRECTORY. Single-thread
NumPy; the largest dense object is a two-coordinate amplitude, not a propagator.
"""

import argparse
import json
import math
import os
from fractions import Fraction as F
from pathlib import Path

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from check_occupation_envelope import CA, CB, KAPPA, SA, SB, fourier, spectrum


def bondset(N, t):
    lo = np.arange(t, N, 2)
    hi = (lo + 1) % N
    twist = np.ones(len(lo))
    twist[hi == 0] = -1
    return lo, hi, twist


def one(u, t):
    """Antiperiodic one-particle layer along the last axis."""
    lo, hi, tw = bondset(u.shape[-1], t)
    diag, off = (CA, -1j * SA) if t == 0 else (CB, 1j * SB)
    out = np.empty_like(u)
    out[..., lo] = diag * u[..., lo] + off * tw * u[..., hi]
    out[..., hi] = diag * u[..., hi] + off * tw * u[..., lo]
    return out


def many(w, t, g):
    # W_ij=-W_ji, W_ij for i<j is the occupation amplitude.
    # det of an active one-body bond is +1. A direct conditional phase
    # on both occupied endpoints changes that amplitude to g times itself.
    out = one(one(w, t).T, t).T
    lo, hi, _ = bondset(w.shape[0], t)
    out[lo, hi] *= g
    out[hi, lo] *= g
    return out


def sq(w):
    return float(np.sum(abs(w) ** 2) / 2)


def wedge(orbitals):
    a, b = orbitals
    w = np.outer(a, b) - np.outer(b, a)
    return w / math.sqrt(sq(w))


def packet(N, L, eps, k, pole, q0, p0):
    # Prescribed periodized Gaussian, represented directly in the
    # antiperiodic lattice chart; scalar continuum width sqrt(eps).
    a = L / N
    p = eps * k / a
    envelope = np.exp(-((p - p0) ** 2) / (2 * eps) - 1j * p * q0 / eps)
    return fourier(envelope[:, None] * pole, True, True).ravel() / np.linalg.norm(envelope)


def observables(ref, alt, n, reach, contacts):
    p = abs(ref) ** 2
    q = abs(alt) ** 2
    ov = np.vdot(ref, alt) / 2
    return {
        "cycles": n,
        "free_contact_layer_norm_sum": reach,
        "zero_field_twisted_free_norm": sq(ref),
        "actual_contact_norm": sq(alt),
        "Hilbert_error_phase_held": math.sqrt(sq(ref - alt)),
        "best_global_phase_error": math.sqrt(max(0.0, 2 * (1 - abs(ov)))),
        "overlap": [float(ov.real), float(ov.imag)],
        "unordered_occupation_TV": float(np.sum(abs(p - q)) / 4),
        "free_and_alternate_contact_probability_by_bond": contacts,
    }


def run(N, L, eps, T, qsep, p0, glist, kind):
    a = L / N
    tau = KAPPA * a * a / eps
    n = max(1, round(T / tau))
    k, _, _, pole = spectrum(N, True)
    v = packet(N, L, eps, k, pole, -qsep, p0)
    h = packet(N, L, eps, k, pole, qsep, -p0)
    phi = np.array([v, h])
    initial_orbitals = phi.copy()
    w0 = wedge(phi)
    states = [w0.copy() for g in glist]
    selected = {0, n // 2, n}
    traces = [[] for g in glist]
    acc = 0.0
    peaks = [0.0, 0.0]
    contact_means = [0.0, 0.0]
    for tick in range(n + 1):
        ref = wedge(phi)
        if tick in selected:
            for j, w in enumerate(states):
                info = []
                for t in (0, 1):
                    lo, hi, _ = bondset(2 * N, t)
                    info.append(
                        [float(np.sum(abs(ref[lo, hi]) ** 2)), float(np.sum(abs(w[lo, hi]) ** 2))]
                    )
                row = observables(ref, w, tick, acc, info)
                row["Duhamel_bound_from_actual_free_amplitudes"] = abs(glist[j] - 1) * acc
                assert (
                    row["Hilbert_error_phase_held"]
                    <= row["Duhamel_bound_from_actual_free_amplitudes"] + 2e-10
                )
                assert abs(sq(w) - 1) < 2e-11 and np.max(abs(w + w.T)) < 1e-11
                traces[j].append(row)
        if tick == n:
            break
        for t in (0, 1):
            lo, hi, _ = bondset(2 * N, t)
            u, w = phi
            num = u[lo] * w[hi] - w[lo] * u[hi]
            E = 1 - abs(np.vdot(u, w)) ** 2
            pc = float(np.sum(abs(num) ** 2)) / E
            acc += math.sqrt(pc)
            peaks[t] = max(peaks[t], pc)
            contact_means[t] += pc / n
            phi = one(phi, t)
            states = [many(state, t, g) for state, g in zip(states, glist)]
    return {
        "kind": kind,
        "cells": N,
        "circumference": L,
        "epsilon": eps,
        "pitch": a,
        "cycle_time": tau,
        "target_time": T,
        "actual_time": n * tau,
        "cycles": n,
        "centres": [-qsep, qsep],
        "physical_centre_momenta": [p0, -p0],
        "initial_overlap_abs": float(abs(np.vdot(v, h))),
        "free_successive_layer_contact_probability_peaks": peaks,
        "free_successive_layer_contact_probability_means": contact_means,
        "Gaussian_chart_probability_abs_k_over_half": [
            float(np.sum(abs(fourier(vec.reshape(N, 2), True)[abs(k) > 0.5]) ** 2))
            for vec in initial_orbitals
        ],
        "trials": [
            {"g": [float(g.real), float(g.imag)], "snapshots": snap} for g, snap in zip(glist, traces)
        ],
    }


def spin(k):
    z = np.exp(-1j * k)
    U = np.array(
        [
            [CA * CB + SA * SB * z, -1j * SA * CB + 1j * CA * SB * z],
            [-1j * SA * CB + 1j * CA * SB * z.conjugate(), CA * CB + SA * SB * z.conjugate()],
        ]
    )
    omega = math.acos(CA * CB + SA * SB * math.cos(k))
    v = (np.exp(1j * omega) * np.array([1.0, 1.0]) - U @ np.array([1.0, 1.0])) / (2j * math.sin(omega))
    assert np.linalg.norm(U @ v - np.exp(-1j * omega) * v) < 1e-12
    return v / np.linalg.norm(v)


def plane_form(cells):
    k = math.pi / cells  # opposite allowed anti-periodic momenta, L=1
    s, r = spin(k), spin(-k)
    pre = s[0] * r[1] - s[1] * r[0]
    inside = np.array([[CA, -1j * SA], [-1j * SA, CA]])
    s, r = inside @ s, inside @ r
    mid = s[1] * r[0] * np.exp(-1j * k) - r[1] * s[0] * np.exp(1j * k)
    a = 1 / cells
    n = round(1 / (KAPPA * a * a))
    norms = [abs(pre) / math.sqrt(cells), abs(mid) / math.sqrt(cells)]
    return {
        "cells": cells,
        "k": k,
        "A_form_abs_per_2k": abs(pre) / (2 * k),
        "B_form_abs_per_2k": abs(mid) / (2 * k),
        "n_at_nominal_T_1_eps_1": n,
        "exact_Duhamel_bound_g_minus_one_at_n": 2 * n * sum(norms),
        "free_contact_norms": norms,
        "contact_norms_divided_by_a_to_3_over_2": [x / a**1.5 for x in norms],
    }


def direct_small():
    N = 4
    coords = [(i, j) for i in range(2 * N) for j in range(i + 1, 2 * N)]
    rows = []
    for phase in (1, -1, 1j):
        w = np.zeros((2 * N, 2 * N), complex)
        for i, j, z in ((0, 7, 1), (1, 2, -1j), (3, 6, 2)):
            w[i, j] = z / math.sqrt(6)
            w[j, i] = -w[i, j]
        d = {pos: w[pos] for pos in coords}
        mx = 0.0
        for layer in range(6):
            t = layer % 2
            lo, hi, _ = bondset(2 * N, t)
            diag, off = (CA, -1j * SA) if not t else (CB, 1j * SB)
            for i, j in zip(lo, hi):
                out = {z: 0j for z in coords}
                for occ, z in d.items():
                    bits = (i in occ, j in occ)
                    if bits[0] == bits[1]:
                        out[occ] += z * (phase if bits[0] else 1)
                    else:
                        dst = tuple(sorted(set(occ) ^ {i, j}))
                        out[occ] += diag * z
                        out[dst] += off * z
                d = out
            w = many(w, t, phase)
            mx = max(mx, max(abs(d[p] - w[p]) for p in coords))
        assert mx < 2e-14
        rows.append({"g": [complex(phase).real, complex(phase).imag], "max_amplitude_discrepancy": mx})
    return rows


def exact_threshold(N):
    # H_N=U_(N-1)(3)/(T_N(3)+1) for antiperiodic even N.
    tp, t, up, u = 1, 3, 0, 1
    for _ in range(1, N):
        tp, t = t, 6 * t - tp
        up, u = u, 6 * u - up
    H = F(u, t + 1)
    x = 1 - 4 * H
    A = F(3, 4) - F(75, 28) * x
    B = -F(4, 3) - F(100, 21) * x
    assert -A * B + (1 + F(24, 7) ** 2) * x * x == 1
    h = float(H)
    rho = math.sqrt(8) - 3
    assert abs(h - (1 - rho**N) / (math.sqrt(8) * (1 + rho**N))) < 1e-15
    matrix = np.array(
        [[1j * float(A), float(x) * (1 - 24j / 7)], [-float(x) * (1 + 24j / 7), 1j * float(B)]]
    )
    return A + B, H, matrix


def fiber(N, direct=False):
    """Total Bloch momentum zero, with antiperiodic one-body momenta."""
    forms = []
    spectrum0 = []
    basis = []
    inside = np.array([[CA, -1j * SA], [-1j * SA, CA]])
    for m in range(N // 2):
        k = (2 * m + 1) * math.pi / N
        u, v = spin(k), spin(-k)
        ubar = np.array([-u[1].conjugate(), u[0].conjugate()])
        vbar = np.array([-v[1].conjugate(), v[0].conjugate()])
        om = math.acos(CA * CB + SA * SB * math.cos(k))
        for i, x in enumerate((u, ubar)):
            for j, y in enumerate((v, vbar)):
                ex, ey = inside @ x, inside @ y
                c0 = x[0] * y[1] - x[1] * y[0]
                c1 = ex[1] * ey[0] * np.exp(-1j * k) - ey[1] * ex[0] * np.exp(1j * k)
                forms.append([np.conj(c0) / math.sqrt(N), np.conj(c1) / math.sqrt(N)])
                spectrum0.append(np.exp(-2j * (1 - i - j) * om))
                if direct:
                    left = np.outer(np.exp(1j * k * np.arange(N)), x).ravel() / math.sqrt(N)
                    right = np.outer(np.exp(-1j * k * np.arange(N)), y).ravel() / math.sqrt(N)
                    basis.append(wedge([left, right]))
    V = np.array(forms)
    U = np.array(spectrum0)
    assert np.max(abs(V.conj().T @ V - np.eye(2))) < 1e-12
    z = (complex(24, -7) / 25) ** 2
    G = V.conj().T @ ((U / (z - U))[:, None] * V)
    assert np.max(abs(G + G.conj().T + np.eye(2))) < 1e-10
    R = np.eye(2) + 2 * G
    minus_det = np.linalg.det(R)
    trace_coefficient, H, closed = exact_threshold(N)
    assert np.max(abs(closed - R)) < 2e-11
    for theta in (-2.1, -0.8, 0.0, 1.3, math.pi):
        g = np.exp(1j * theta)
        full = np.linalg.det(np.eye(2) - (g - 1) * G)
        assert abs(full - g * (math.cos(theta) + float(trace_coefficient) * math.sin(theta) / 2)) < 2e-11
    small_eigenvalues = np.linalg.eigvalsh((G - G.conj().T) / (2j))
    candidates = [1 + 1 / complex(-0.5, y) for y in small_eigenvalues]
    assert all(
        abs(abs(g) - 1) < 1e-12 and abs(np.linalg.det(np.eye(2) - (g - 1) * G)) < 1e-9
        for g in candidates
    )
    check = []
    if direct:
        upper = np.triu_indices(2 * N, 1)
        B = np.column_stack([w[upper] for w in basis])
        assert np.max(abs(B.conj().T @ B - np.eye(len(U)))) < 1e-12
        for g in (1, -1, 1j, *candidates):
            actual = np.column_stack([many(many(w, 0, g), 1, g)[upper] for w in basis])
            projected = B.conj().T @ actual
            matrix = U[:, None] * (np.eye(len(U)) + (g - 1) * (V @ V.conj().T))
            residual = float(np.max(abs(actual - B @ matrix)))
            span_residual = float(np.max(abs(actual - B @ projected)))
            offset = float(np.min(abs(np.linalg.eigvals(projected) - z)))
            assert max(residual, span_residual) < 1e-12
            if g in candidates:
                assert offset < 1e-12
            check.append(
                {
                    "g": [float(complex(g).real), float(complex(g).imag)],
                    "physical_vs_rank_two_full_amplitude_sup": residual,
                    "actual_eigenvalue_distance_to_threshold": offset,
                }
            )
    return {
        "cells": N,
        "mean_reciprocal_3_plus_cos_exact": str(H),
        "trace_of_I_plus_2G_divided_by_i_exact": str(trace_coefficient),
        "exact_minus_threshold_secular_determinant": 1,
        "band_sum_vs_closed_matrix_sup_error": float(np.max(abs(R - closed))),
        "fiber_dimension": len(U),
        "minus_threshold_secular_determinant": [float(minus_det.real), float(minus_det.imag)],
        "threshold_candidate_phase_angles_sorted": sorted(float(np.angle(g)) for g in candidates),
        "direct_coordinate_spectral_controls": check,
    }


def main():
    rows = []
    for N in (24, 40, 64, 96):
        a = 8 / N
        rows.append(
            run(
                N,
                8,
                1.0,
                1.5,
                0.75,
                1.0,
                [1, -1, 1j, np.exp(1j * a), np.exp(2j * math.asin(min(1, math.sqrt(a) / 2)))],
                "fixed_action_collision",
            )
        )
    rows.extend(
        [
            run(48, 8, 0.25, 1.5, 0.75, 1.0, [1, -1], "coarser_semiclassical_collision"),
            run(96, 8, 0.25, 1.5, 0.75, 1.0, [1, -1], "finer_semiclassical_collision"),
            run(64, 8, 1.0, 1.0, 2.25, -1.0, [1, -1], "separating_packets"),
            run(24, 8, 0.25, 1.0, 0.75, 2.0, [1, -1], "outside_low_chart"),
        ]
    )
    return {
        "direct_periodic_and_twist_checks": direct_small(),
        "cutoff_form_factors": [plane_form(n) for n in (16, 32, 64, 128, 256, 512, 1024)],
        "total_momentum_zero_secular_tests": [fiber(n, n == 8) for n in (8, 32, 128, 512)],
        "secular_scope": "On an even antiperiodic two-particle ring in total momentum zero, each active contact projector has rank one. The even contact vector and the pre-even-layer pullback of the odd contact vector are orthogonal: same-cell versus particles in neighboring distinct cells. Thus the full interaction in the free band basis is U0[I+(g-1)VV*], V carrying those two orthonormal columns. z*=exp(-2i gamma) is not an eigenvalue of these finite free fibers. The finite determinant lemma makes z* an eigenvalue exactly when det[I-(g-1)V*(z*-U0)^(-1)U0V]=0. Independent real-space matrices evaluated at eight cells check the two threshold-tuned phases and the complete rank-two action. The exact finite-ring threshold determinant at g=-1 equals one for all even N. The closed Chebyshev formula determines the two unit threshold phases and their thermodynamic limits. Contact_threshold_on_the_ring.md derives the matrix expression. This zero-total-momentum threshold diagnostic does not give a uniform scattering estimate, a limiting resolvent, or a continuum boundary condition for g=-1. Threshold-tuned finite roots are not automatically infinite-volume bound states.",
        "packet_tests": rows,
        "estimate": "Fix an isolated positive band at the rational angles. On a one-body momentum cutoff |k|,|l|<=K<<1, the two-body Slater contact form at the even bond is the antisymmetric determinant of the two spinors u(k),u(l). On the odd bond it uses s_alpha u(k), s_alpha u(l) and the one-cell phase for the second endpoint. Both are antisymmetric and bounded by C|k-l|, since the spinor chart has a bounded derivative. Holds by linearity for an arbitrary antisymmetric normalized two-band envelope supported on the product cutoff. At each total momentum take Cauchy-Schwarz over a relative momentum interval of length at most 2K; integrating the squared form yields <=C K^3 times the norm squared. Thus the total l2 norm of all active doubly occupied coordinates for a freely evolved state is <=C K^(3/2) independently at both required slices. Each layer multiplies the active double coordinates by g vs 1 leaving other entries unchanged; the projector commutes with the ideal layer. Unitarity plus a chronological product telescoping gives a Hilbert norm error <= |g-1| sum_j ||P_j psi_free(j)||. With K=aP/epsilon and tau=m kappa a^2/epsilon, this suffices for o(1) on fixed time and cutoff if |g-1| P^(3/2)=o(sqrt(a epsilon)); also require the original free-band continuum chart assumptions and control any discarded momentum tails separately by unitarity.",
        "strong_phase": "This triangle bound need not shrink for g=-1. The two antiperiodic plane waves k=+/-pi/N have N cells of size a=1/N, fixed physical momenta +/-pi and fixed action 1. Their exact free contact norm is order a^(3/2) on both half-layers, stationary up to a scalar per full cycle. Its sum across order a^(-2) cycles grows as a^(-1/2). This is an obstruction to this estimate, not a lower bound on the true state discrepancy. The simulated finite lattice does not resolve threshold resonances, band-changing scattering for all momenta, or a self-adjoint limiting contact condition for fixed g.",
        "scope": "Finite packet rows compare g on exactly the same normalized positive-band initial Slater. Born occupation TV, Hilbert and global-phase-minimized errors are distinct. Odd layer uses antiperiodic one-body cut for two particles but local occupation gates are periodic. Arrays have finite circumference; no infinite-volume limit or fair empirical test is inferred. Non-low-chart and outward-moving preparations are kept as controls. This is the fixed-gap Schroedinger scaling, not the separately retuned finite-speed Dirac chart.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "contact_continuum.json").write_bytes(
        (json.dumps(result, separators=(",", ":")) + "\n").encode()
    )
    print(
        len(result["packet_tests"]),
        "packet families and",
        len(result["cutoff_form_factors"]),
        "threshold form pairs.",
    )
