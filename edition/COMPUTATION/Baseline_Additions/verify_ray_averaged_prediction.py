#!/usr/bin/env python3
"""Follow-up to verify_ray_error_scaling.py, whose predicate E1 failed: the residual after the connection offset fell to period 256 and then grew.
Hypothesis fixed before this run: the growth is the finite width of the packet in k (the ray was evaluated at the central k only), so the
prediction averaged over the packet's k-distribution, x(t) = sum_s <v(k - s Phi)> + <A(k - t Phi) - A(k)>, should have a residual that decreases
with the period.  Criterion fixed before the run: with the averaged prediction the residual decreases monotonically over the periods 64..2048 and
the fitted exponent against the period lies in (-2.3, -0.7).  Writes Ray_Averaged_Prediction_Results.json; refuses to overwrite."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reversible_walk_lib import dispersion
OUT = "Ray_Averaged_Prediction_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SQ2 = math.sqrt(2)
def step_factory(N, V):
    g = np.exp(-1j * V) / SQ2
    def step(psi):
        s = (psi[:, 0] + psi[:, 1]) * g; dlt = (psi[:, 0] - psi[:, 1]) * g
        out = np.empty_like(psi); out[:, 0] = np.roll(s, 1); out[:, 1] = np.roll(dlt, -1); return out
    return step
def branch_vector(q):
    Uk = np.array([[np.exp(-1j * q), np.exp(-1j * q)], [np.exp(1j * q), -np.exp(1j * q)]]) / SQ2
    lam, vec = np.linalg.eig(Uk); j = int(np.argmin(np.abs(lam - np.exp(-1j * math.asin(math.sin(q) / SQ2))))); v = vec[:, j] / np.linalg.norm(vec[:, j]); return v * np.exp(-1j * np.angle(v[0]))
def conn(kk, h=1e-6): return float(np.imag(np.vdot(branch_vector(kk), (branch_vector(kk + h) - branch_vector(kk - h)) / (2 * h))))
def packet(N, k0, sigma):
    ks = 2 * math.pi * np.fft.fftfreq(N); psi_k = np.zeros((N, 2), dtype=complex)
    for i, kk in enumerate(ks):
        d = (kk - k0 + math.pi) % (2 * math.pi) - math.pi
        psi_k[i] = math.exp(-d * d / (4 * sigma ** 2)) * branch_vector(kk)
    psi = np.fft.ifft(psi_k, axis=0); psi = np.roll(psi, N // 2, axis=0); return psi / np.linalg.norm(psi)
def centroid(psi):
    N = psi.shape[0]; p = (np.abs(psi) ** 2).sum(1); ang = 2 * math.pi * np.arange(N) / N
    return float(np.angle((p * np.exp(1j * ang)).sum()) * N / (2 * math.pi)) - N // 2
N = 8192; xs = np.arange(N) - N // 2
def run(sigma, periods, k0=1.0):
    rows = []
    # the packet's k-distribution (weights on the FFT grid) and tabulated v and A on a fine grid for the averages
    for M in periods:
        Phi = 2 * math.pi / M; st = step_factory(N, Phi * xs.astype(float)); psi = packet(N, k0, sigma); cur = psi.copy(); c0 = centroid(psi)
        kd0 = (np.abs(np.fft.fft(psi, axis=0)) ** 2).sum(1); kd0 = kd0 / kd0.sum(); ks = 2 * math.pi * np.fft.fftfreq(N)
        sel = kd0 > 1e-12; kw = kd0[sel]; kk_grid = ks[sel]
        cur = st(cur); kd = (np.abs(np.fft.fft(cur, axis=0)) ** 2).sum(1); m = N // M
        direction = 1 if np.abs(kd - np.roll(kd0 * kd0.sum(), m)).max() < np.abs(kd - np.roll(kd0 * kd0.sum(), -m)).max() else -1
        d1 = ((centroid(cur) - c0 + N / 2) % N) - N / 2; sgn = 1.0 if d1 * dispersion(np.array(k0))[1] > 0 else -1.0
        A0 = np.array([conn(q) for q in kk_grid]); A0m = float((kw * A0).sum())
        pred_c = 0.0; pred_avg = 0.0; e_central = {+1: 0.0, -1: 0.0}; e_avg = {+1: 0.0, -1: 0.0}; kc = k0
        for s in range(1, M + 1):
            if s > 1: cur = st(cur)
            pred_c += sgn * float(dispersion(np.array(kc + direction * Phi / 2))[1])
            pred_avg += sgn * float((kw * dispersion(kk_grid + direction * (s - 0.5) * Phi)[1]).sum()); kc += direction * Phi
            d = ((centroid(cur) - c0 + N / 2) % N) - N / 2
            offc = conn(kc) - conn(k0); offa = float((kw * np.array([conn(q + direction * s * Phi) for q in kk_grid])).sum()) - A0m if (s % max(1, M // 32) == 0 or s == M) else None
            for sg in (+1, -1):
                e_central[sg] = max(e_central[sg], abs(d - pred_c - sg * offc))
                if offa is not None: e_avg[sg] = max(e_avg[sg], abs(d - pred_avg - sg * offa))
        rows.append(dict(period=M, sigma_k=sigma, residual_central_ray_with_offset=float(min(e_central.values())), residual_averaged_ray_with_offset=float(min(e_avg.values())),
                         offset_sign=int(min(e_avg, key=e_avg.get)), return_probability=float(abs(np.vdot(psi, cur)) ** 2), averaged_residual_sampled_every=max(1, M // 32)))
        print(rows[-1], flush=True)
    return rows
rows = run(0.03, (64, 128, 256, 512, 1024, 2048))
res = np.array([r["residual_averaged_ray_with_offset"] for r in rows]); per = np.array([r["period"] for r in rows], dtype=float)
slope = float(np.polyfit(np.log(per), np.log(res), 1)[0])
ok("F1_averaged_ray_residual_decreases_with_period", all(res[i + 1] < res[i] for i in range(len(res) - 1)) and -2.3 < slope < -0.7, rows=rows, log_log_slope=slope,
   residual_times_period=[float(r * p) for r, p in zip(res, per)], note="criterion fixed before the run; the averaged residual is sampled at 32 points per period and at the end")
rows2 = run(0.015, (512, 2048))
ok("F2_narrower_k_packet_control_recorded", True, rows=rows2, note="recorded, not a predicate: a packet half as wide in k (twice as wide in x) for the two largest periods")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), ring=N, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
