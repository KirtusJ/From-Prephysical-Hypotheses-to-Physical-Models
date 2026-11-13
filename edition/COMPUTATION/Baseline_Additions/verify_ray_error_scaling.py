#!/usr/bin/env python3
"""Fourth Director Z session: how the deviation of the packet centroid from the ray of w(k) + Phi x scales with the field,
with and without the connection offset of the branch eigenvector (paper G9, Table 4; OP-26).
Writes Ray_Error_Scaling_Results.json and refuses to overwrite it.  Double precision, not an enclosure."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reversible_walk_lib import dispersion
OUT = "Ray_Error_Scaling_Results.json"
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
N = 8192; xs = np.arange(N) - N // 2; k0 = 1.0; sigma = 0.03
# direction and sign conventions are determined from the first period, as in the third-session program
rows = []
for M in (64, 128, 256, 512, 1024, 2048):
    Phi = 2 * math.pi / M; st = step_factory(N, Phi * xs.astype(float)); psi = packet(N, k0, sigma); cur = psi.copy(); c0 = centroid(psi)
    kd0 = (np.abs(np.fft.fft(psi, axis=0)) ** 2).sum(1)
    cur = st(cur); kd = (np.abs(np.fft.fft(cur, axis=0)) ** 2).sum(1); m = N // M
    direction = 1 if np.abs(kd - np.roll(kd0, m)).max() < np.abs(kd - np.roll(kd0, -m)).max() else -1
    d1 = ((centroid(cur) - c0 + N / 2) % N) - N / 2; sgn = 1.0 if d1 * dispersion(np.array(k0))[1] > 0 else -1.0
    kk = k0; pred = 0.0; e_plain = 0.0; e_corr = {+1: 0.0, -1: 0.0}; worst_t = None
    for s in range(1, M + 1):
        if s > 1: cur = st(cur)
        pred += sgn * float(dispersion(np.array(kk + direction * Phi / 2))[1]); kk += direction * Phi
        d = ((centroid(cur) - c0 + N / 2) % N) - N / 2; e_plain = max(e_plain, abs(d - pred))
        for sg in (+1, -1):
            e = abs(d - pred - sg * (conn(kk) - conn(k0)))
            if e > e_corr[sg]: e_corr[sg] = e
    rows.append(dict(period=M, field=Phi, max_error_without_offset=float(e_plain), max_error_with_offset=float(min(e_corr.values())), offset_sign=int(min(e_corr, key=e_corr.get)),
                     excursion_predicted=float((math.pi / 2) / Phi), return_probability=float(abs(np.vdot(psi, cur)) ** 2)))
    print(rows[-1], flush=True)
res = np.array([r["max_error_with_offset"] for r in rows]); per = np.array([r["period"] for r in rows], dtype=float)
slope = float(np.polyfit(np.log(per), np.log(res), 1)[0]); const = float(np.mean(res * per))
ok("E1_residual_after_offset_scales_as_first_power_of_the_field", -1.3 < slope < -0.7, rows=rows, log_log_slope=slope, residual_times_period_mean_sites=const,
   residual_times_period=[float(r * p) for r, p in zip(res, per)], note="criterion fixed before the run: the fitted exponent of the residual against the period lies in (-1.3, -0.7); "
   "the residual without the offset is expected to tend to a constant (the connection change), the residual with it to vanish linearly in Phi")
ok("E2_residual_without_offset_tends_to_a_constant", np.std([r["max_error_without_offset"] for r in rows[2:]]) < 0.1 * np.mean([r["max_error_without_offset"] for r in rows[2:]]),
   values=[r["max_error_without_offset"] for r in rows])
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), ring=N, k0=k0, sigma=sigma, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
