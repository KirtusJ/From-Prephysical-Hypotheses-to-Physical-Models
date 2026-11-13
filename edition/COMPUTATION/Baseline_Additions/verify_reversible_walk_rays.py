#!/usr/bin/env python3
"""Checks for paper G9, Section 6 (the signed arc digraph of a ring: weak limit, rays, uniform field, gains of small order) and the constructed trial GH-2.
Writes Reversible_Walk_Rays_Results.json.  Numeric values are double precision, not enclosures.  Seeds are fixed and reported."""
import itertools, json, math
import numpy as np
from reversible_walk_lib import ring_step, polar_structure, dispersion
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SQ2 = math.sqrt(2)

# ---------------- R6: weak limit of X_t/t against the group-velocity distribution
N = 1024; A = ring_step(N); U = A / SQ2
psi = np.zeros(2 * N); psi[2 * (N // 2) + 0] = 1.0                    # site 0, arriving from the left
xs = np.arange(N) - N // 2
ks = 2 * math.pi * (np.arange(4096) + 0.5) / 4096; pred1 = pred2 = 0.0
for kk in ks:                                                         # branches exp(-i w) and -exp(i w): velocities +v(k) and -v(k)
    Uk = np.array([[np.exp(-1j * kk), np.exp(-1j * kk)], [np.exp(1j * kk), -np.exp(1j * kk)]]) / SQ2
    lam, vec = np.linalg.eig(Uk); w1, v1 = dispersion(np.array(kk)); j1 = int(np.argmin(np.abs(lam - np.exp(-1j * w1))))
    for j, vel in ((j1, float(v1)), (1 - j1, -float(v1))):
        wt = abs(vec[0, j]) ** 2 / np.linalg.norm(vec[:, j]) ** 2
        pred1 += vel * wt / len(ks); pred2 += vel ** 2 * wt / len(ks)
rows = []; cur = psi.copy(); tcur = 0
for tt in (50, 100, 200, 400):
    for _ in range(tt - tcur): cur = U @ cur
    tcur = tt; p = cur[0::2] ** 2 + cur[1::2] ** 2
    rows.append(dict(t=tt, mean_over_t=float((p * xs).sum() / tt), second_moment_over_t2=float((p * xs ** 2).sum() / tt ** 2), norm=float(p.sum())))
ok("R6_weak_limit_moments_match_group_velocity_distribution", abs(rows[-1]["mean_over_t"] - pred1) < 5e-3 and abs(rows[-1]["second_moment_over_t2"] - pred2) < 5e-3 and abs(pred2 - (1 - 1 / SQ2)) < 1e-6,
   predicted_mean=float(pred1), predicted_second_moment=float(pred2), value_1_minus_1_over_sqrt2=1 - 1 / SQ2, rows=rows,
   first_run="the first version obtained the velocities by a finite difference of numerically matched eigenvalues; at the points where the two eigenvalues are close the matching failed and the predicted moments were -108 and 9.6e7. Failure of the checking program; the velocities are now the closed form on each branch",
   note="prediction: velocity cos k / sqrt(1 + cos^2 k) on either branch weighted by the squared component of the initial vector; Grimmett-Janson-Scudo")
# ---------------- R7: a wave packet follows the ray
def packet(N, k0, sigma, x0, field_shift=0.0):
    """real-space vector whose Fourier components lie on branch 1 of the dispersion, Gaussian in k around k0"""
    ks = 2 * math.pi * np.fft.fftfreq(N); psi_k = np.zeros((N, 2), dtype=complex)
    for i, kk in enumerate(ks):
        Uk = np.array([[np.exp(-1j * kk), np.exp(-1j * kk)], [np.exp(1j * kk), -np.exp(1j * kk)]]) / SQ2
        lam, vec = np.linalg.eig(Uk); w1 = math.asin(math.sin(kk) / SQ2); j = int(np.argmin(np.abs(lam - np.exp(-1j * w1))))
        u = vec[:, j] / np.linalg.norm(vec[:, j]); u = u * np.exp(-1j * np.angle(u[0] + 1e-30))
        d = (kk - k0 + math.pi) % (2 * math.pi) - math.pi
        psi_k[i] = math.exp(-d * d / (4 * sigma ** 2)) * np.exp(-1j * kk * x0) * u
    psi = np.fft.ifft(psi_k, axis=0); psi = np.roll(psi, N // 2, axis=0)       # sites -N/2..N/2-1 ; note sign conventions fixed by the check below
    out = psi.reshape(-1); return out / np.linalg.norm(out)
def centroid(vec, N):
    p = (np.abs(vec) ** 2).reshape(N, 2).sum(1); ang = 2 * math.pi * np.arange(N) / N
    return float(np.angle((p * np.exp(1j * ang)).sum()) * N / (2 * math.pi)) - N // 2          # circular mean
N = 2048; Ac = ring_step(N).astype(complex) / SQ2
rows = []
for k0 in (0.3, 1.0, 2.2, -0.8):
    psi = packet(N, k0, 0.03, 0.0); c0 = centroid(psi, N); cur = psi.copy(); T = 300
    for _ in range(T): cur = Ac @ cur
    c1 = centroid(cur, N); d = ((c1 - c0 + N / 2) % N) - N / 2
    # sign convention: with Fourier convention of ring_step (factor exp(-ik) on a right step) the ray velocity is dw/dk
    rows.append(dict(k0=k0, displacement_over_T=d / T, group_velocity=float(dispersion(np.array(k0))[1])))
sgn = np.sign(rows[0]["displacement_over_T"] / rows[0]["group_velocity"])
ok("R7_packet_velocity_equals_group_velocity", all(abs(r["displacement_over_T"] - sgn * r["group_velocity"]) < 2e-3 for r in rows), rows=rows, sign_convention=float(sgn), steps=300, sigma_k=0.03)
# ---------------- R8: uniform field: exact momentum law and the ray of H = w(k) + Phi x
def kdist(vec, N): return (np.abs(np.fft.fft(vec.reshape(N, 2), axis=0)) ** 2).sum(1)
rows = []; N = 2048
for M in (64, 128, 256):
    Phi = 2 * math.pi / M; Af = ring_step(N, field=Phi) / SQ2            # N divisible by M: the field is consistent round the ring
    psi = packet(N, 1.0, 0.03, 0.0); kd0 = kdist(psi, N); cur = psi.copy(); c0 = centroid(psi, N); T = M
    shift_err = 0.0; pos_err = 0.0; pred = 0.0; kk = 1.0; traj = []
    for s in range(1, T + 1):
        cur = Af @ cur
        m = s * (N // M); kd = kdist(cur, N)
        e_plus = np.abs(kd - np.roll(kd0, m)).max(); e_minus = np.abs(kd - np.roll(kd0, -m)).max(); shift_err = max(shift_err, min(e_plus, e_minus))
        if s == 1: direction = 1 if e_plus < e_minus else -1
        # ray: k advances by direction*Phi per step; position advances by sgn * w'(k) evaluated at the midpoint
        kmid = kk + direction * Phi / 2; pred += sgn * float(dispersion(np.array(kmid))[1]); kk += direction * Phi
        c = centroid(cur, N); d = ((c - c0 + N / 2) % N) - N / 2; pos_err = max(pos_err, abs(d - pred)); traj.append(d)
    # leakage out of branch 1 after one period: compare with the initial packet (k returns to k0)
    ret = abs(np.vdot(psi, cur)) ** 2
    rows.append(dict(period=M, field=Phi, momentum_shift_error=float(shift_err), k_direction_per_step=int(direction), max_position_error_sites=float(pos_err),
                     excursion_sites=float(max(traj) - min(traj)), predicted_excursion=float((math.pi / 2) / Phi), return_probability_after_one_period=float(ret)))
ok("R8_momentum_distribution_shifts_rigidly_by_the_field", all(r["momentum_shift_error"] < 1e-9 for r in rows), rows=rows)
ok("R8_centroid_follows_ray_of_w(k)+Phi_x", all(r["max_position_error_sites"] < 0.05 * r["excursion_sites"] for r in rows),
   note="ray integrated with the midpoint rule; excursion over one period is (w_max - w_min)/Phi = (pi/2)/Phi on branch 1")
# the residual of about 0.6 site does not shrink with the field.  Test: is it the change of the connection i<u|du/dk> of the branch eigenvector
# (in the phase convention of packet(): first component real and positive) between k0 and the current k?
def conn(kk, h=1e-6):
    def u(q):
        Uk = np.array([[np.exp(-1j * q), np.exp(-1j * q)], [np.exp(1j * q), -np.exp(1j * q)]]) / SQ2
        lam, vec = np.linalg.eig(Uk); j = int(np.argmin(np.abs(lam - np.exp(-1j * math.asin(math.sin(q) / SQ2))))); v = vec[:, j] / np.linalg.norm(vec[:, j]); return v * np.exp(-1j * np.angle(v[0]))
    return float(np.imag(np.vdot(u(kk), (u(kk + h) - u(kk - h)) / (2 * h))))
rows2 = []; N = 2048
for M in (64, 256):
    Phi = 2 * math.pi / M; Af = ring_step(N, field=Phi) / SQ2; psi = packet(N, 1.0, 0.03, 0.0); cur = psi.copy(); c0 = centroid(psi, N); kk = 1.0; pred = 0.0; e_plain = 0.0; e_corr = {+1: 0.0, -1: 0.0}
    for s_ in range(1, M + 1):
        cur = Af @ cur; pred += sgn * float(dispersion(np.array(kk + direction * Phi / 2))[1]); kk += direction * Phi
        d = ((centroid(cur, N) - c0 + N / 2) % N) - N / 2; e_plain = max(e_plain, abs(d - pred))
        for sg in (+1, -1): e_corr[sg] = max(e_corr[sg], abs(d - pred - sg * (conn(kk) - conn(1.0))))
    rows2.append(dict(period=M, max_error_without_offset=float(e_plain), max_error_with_offset=float(min(e_corr.values())), offset_sign=int(min(e_corr, key=e_corr.get))))
ok("R8_residual_below_0.02_site_after_connection_offset", all(r["max_error_with_offset"] < 0.02 for r in rows2), rows=rows2,
   note="criterion fixed before the run; it is not met (0.075 and 0.038 site) and the predicate is kept as failed. Observation: the change of the connection of the branch eigenvector accounts for 88 and 94 per cent of the residual, and the remainder is smaller for the weaker field")
# strong fields with gains of order 2, 3, 4, 6 (the orders for which the pair measure does not depend on the character)
rows = []; N = 240
for order in (2, 3, 4, 6, 12, 24):
    Phi = 2 * math.pi / order; Af = ring_step(N, field=Phi) / SQ2; psi = np.zeros(2 * N, dtype=complex); psi[2 * (N // 2)] = 1.0; cur = psi.copy(); rec = {}
    spread = 0.0
    for s in range(1, 4 * order + 1):
        cur = Af @ cur
        p = (np.abs(cur) ** 2).reshape(N, 2).sum(1); spread = max(spread, float(np.sqrt((p * (np.arange(N) - N // 2) ** 2).sum())))
        if s in (order, 2 * order, 4 * order): rec[s] = float(abs(np.vdot(psi, cur)) ** 2)
    rows.append(dict(gain_order=order, return_probability=rec, largest_rms_distance_within_4_periods=spread))
ok("R8_strong_field_revivals_recorded", True, rows=rows, note="recorded, not a predicate: localized start; return probability at m, 2m, 4m steps for field 2 pi/m")
# staircase of gains of order 4: V(x) = (pi/2) floor(x/L); mean slope pi/(2L)
rows = []; N = 4096
for L in (16, 64):
    V = (math.pi / 2) * np.floor((np.arange(N) - N // 2) / L); As = ring_step(N, potential=V) / SQ2
    psi = packet(N, 0.3, 0.03, 0.0); cur = psi.copy(); c0 = centroid(psi, N); Phi = math.pi / (2 * L)
    T = int(0.5 * (2 * math.pi / Phi) / 4)                  # an eighth of the Bloch period of the mean field
    for s in range(T): cur = As @ cur
    c = centroid(cur, N); d = ((c - c0 + N / 2) % N) - N / 2
    kk = 0.3; pred = 0.0
    for s in range(T): pred += sgn * float(dispersion(np.array(kk + direction * Phi / 2))[1]); kk += direction * Phi
    p = (np.abs(cur) ** 2).reshape(N, 2).sum(1); xs = np.arange(N) - N // 2
    # smooth comparison
    Asm = ring_step(N, field=Phi) / SQ2; cs = psi.copy()
    for s in range(T): cs = Asm @ cs
    ds = ((centroid(cs, N) - c0 + N / 2) % N) - N / 2
    rows.append(dict(step_length=L, steps=T, staircase_displacement=float(d), smooth_field_displacement=float(ds), ray_prediction=float(pred),
                     staircase_rms_width=float(np.sqrt((p * (xs - (c0 + d)) ** 2).sum())), fraction_left_of_start=float(p[xs < c0 - 5].sum())))
ok("R8_staircase_of_order_4_gains_recorded", True, rows=rows, note="recorded, not a predicate: whether gains of a rigid order reproduce the ray of the mean field")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seeds=[])
json.dump(R, open("Reversible_Walk_Rays_Results.json", "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
