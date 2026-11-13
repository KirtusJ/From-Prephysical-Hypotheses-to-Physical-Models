#!/usr/bin/env python3
"""Director Z cross-check of Director G's paper "Preparing the base walk and resolving two classical rays" (pull request 2, commit d4f6fea).
Nothing is imported from Director G's programs.  Model used here, this participant's reading of the paper: amplitudes a_R(x), a_L(x) on the
line; one step multiplies by exp(-i h x), applies the coin (r, l) -> ((r + l), (r - l))/sqrt 2 and moves R one site up and L one site down,
so that in momentum the free step is diag(e^{-ik}, e^{ik}) H.  Protocol: start at site 0 in direction R; blocks of two steps; after each
block keep one direction at all sites (first L, then alternately R, L, ...), unnormalized.
Predicates, fixed before the run:
 B0  a localized start has a flat momentum density after 37 steps with h = 0.01 (relative spread below 1e-10);
 B1  zero field, m = 4, 9, 16, 40: the probability of the retained word is binom(2m, m)/4^m to 1e-12 relative; the site amplitudes are
     binomial coefficients over 2^m in modulus, with alternating signs, on sites of spacing two centred at 0 (m even) or -1 (m odd), to
     1e-12; the conditional site variance is m^2/(2m - 1) to 1e-10 relative;
 B2  field on, (m, h) = (8, 0.03), (20, 0.01), (41, 0.004): the modulus of the momentum amplitude of the retained output is a constant
     times |prod_{j<m} sin(k + (2j+1) h)|, for one of the four sign conventions (k, h) -> (+-k, +-h), to 1e-9 of its maximum on 4096
     momenta; the convention found is recorded;
 B3  for m = 64, 256, 1024 and c = m^3 h^2 = 0.5, 0.125, 0.03125: the L2 distance between the normalized profiles
     prod sin(k + (2j+1) h) and sin^m(k + m h) is at most c, the ratio of their squared norms differs from 1 by at most c, and for each m
     the distance decreases with c;
 B4  two rays, F = 1, t = 2, delta = 0.2, 0.1, 0.05 (h = F delta^4, m the even integer nearest delta^(-5/2), then round(t/delta^3) free
     steps with the field on, Y = delta^2 x): the masses of Y < 0 and of Y > 0 are within 0.02 of 1/2; the conditional means of the two
     halves are within 15 percent of -+(F t^2/2 + t m h/delta), the ray with the momentum offset left by the preparation; and the residual
     of the conditional means against the central rays -+F t^2/2 decreases with delta.
Recorded without a predicate: distance/(m^2 h^2) in B3; the widths of the two halves in B4.
Writes Crosscheck_Director_G_Two_Rays_Results.json; refuses to overwrite."""
import json, math, os, sys
from math import comb
import numpy as np
OUT = "Crosscheck_Director_G_Two_Rays_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
RT2 = math.sqrt(2.0)
class Walk:
    def __init__(self, X, h):
        self.X = X; self.x = np.arange(-X, X + 1); self.r = np.zeros(2 * X + 1, dtype=complex); self.l = np.zeros(2 * X + 1, dtype=complex)
        self.r[X] = 1.0; self.ph = np.exp(-1j * h * self.x) if h else None
    def step(self):
        r, l = self.r, self.l
        if self.ph is not None: r = r * self.ph; l = l * self.ph
        a = (r + l) / RT2; b = (r - l) / RT2; self.r = np.zeros_like(a); self.l = np.zeros_like(b); self.r[1:] = a[:-1]; self.l[:-1] = b[1:]
    def block(self, keep):
        self.step(); self.step()
        if keep == "L": self.r[:] = 0
        else: self.l[:] = 0
    def prepare(self, m):
        keep = "L"
        for _ in range(m): self.block(keep); keep = "R" if keep == "L" else "L"
        return "R" if keep == "L" else "L"                      # the direction retained last
    def norm2(self): return float((np.abs(self.r) ** 2 + np.abs(self.l) ** 2).sum())
def momentum(v, x, ks): return np.array([np.sum(v * np.exp(-1j * k * x)) for k in ks])
# B0
w = Walk(60, 0.01)
for _ in range(37): w.step()
ks = np.linspace(-math.pi, math.pi, 257)[:-1]; dens = np.abs(momentum(w.r, w.x, ks)) ** 2 + np.abs(momentum(w.l, w.x, ks)) ** 2
ok("B0_flat_momentum_density_after_a_full_reading", float(dens.max() - dens.min()) / float(dens.mean()) < 1e-10, relative_spread=float(dens.max() - dens.min()) / float(dens.mean()))
# B1
rows = []; good = True
for m in (4, 9, 16, 40):
    w = Walk(2 * m + 4, 0.0); last = w.prepare(m); v = w.r if last == "R" else w.l; p = w.norm2(); pref = comb(2 * m, m) / 4 ** m
    c0 = 0 if m % 2 == 0 else -1; sites = c0 + 2 * (np.arange(m + 1) - m // 2) if m % 2 == 0 else c0 + 2 * (np.arange(m + 1) - (m + 1) // 2) + 1
    # expected support: m + 1 sites of spacing two, symmetric about c0
    sites = c0 - m + 2 * np.arange(m + 1); amp = v[sites + w.X]; ref = np.array([comb(m, j) for j in range(m + 1)]) / 2.0 ** m
    mod_ok = float(np.abs(np.abs(amp) - ref).max()) < 1e-12; off = float(np.abs(v).sum() - np.abs(amp).sum())
    ph = amp / np.abs(amp); alt = float(np.abs(ph[1:] / ph[:-1] + 1).max())                 # alternating signs: successive ratio -1
    prob = np.abs(amp) ** 2 / p; mean = float((prob * sites).sum()); var = float((prob * (sites - mean) ** 2).sum())
    row = dict(m=m, last_direction=last, probability=p, binomial_reference=pref, largest_modulus_error=float(np.abs(np.abs(amp) - ref).max()), amplitude_outside_support=off,
               alternation_defect=alt, centre=mean, variance=var, variance_reference=m * m / (2 * m - 1)); rows.append(row)
    good &= abs(p / pref - 1) < 1e-12 and mod_ok and abs(off) < 1e-12 and alt < 1e-9 and abs(mean - c0) < 1e-9 and abs(var / (m * m / (2 * m - 1)) - 1) < 1e-10
ok("B1_zero_field_word_gives_alternating_binomial_amplitudes", good, rows=rows)
# B2
rows = []; good = True; ks = np.linspace(-math.pi, math.pi, 4097)[:-1]
for m, h in ((8, 0.03), (20, 0.01), (41, 0.004)):
    w = Walk(2 * m + 4, h); last = w.prepare(m); v = w.r if last == "R" else w.l; A = np.abs(momentum(v, w.x, ks)); best = None
    for sk in (1, -1):
        for sh in (1, -1):
            P = np.abs(np.prod([np.sin(sk * ks + sh * (2 * j + 1) * h) for j in range(m)], axis=0)); cst = float(A @ P) / float(P @ P)
            err = float(np.abs(A - cst * P).max()) / float(A.max())
            if best is None or err < best[0]: best = (err, sk, sh, cst)
    rows.append(dict(m=m, h=h, largest_deviation_over_maximum=best[0], sign_of_k=best[1], sign_of_h=best[2], constant=best[3])); good &= best[0] < 1e-9
ok("B2_field_on_profile_is_the_product_of_shifted_sines", good, rows=rows)
# B3
rows = []; good = True; N = 1 << 17; kk = (np.arange(N) + 0.5) * (2 * math.pi / N) - math.pi
for m in (64, 256, 1024):
    prev = None
    for c in (0.5, 0.125, 0.03125):
        h = math.sqrt(c / m ** 3); logA = np.zeros(N); sgn = np.ones(N)
        for j in range(m):
            s = np.sin(kk + (2 * j + 1) * h); logA += np.log(np.abs(s) + 1e-300); sgn *= np.sign(s)
        A = sgn * np.exp(logA); s0 = np.sin(kk + m * h); B = np.sign(s0) ** m * np.abs(s0) ** m
        nA = float((A * A).sum()); nB = float((B * B).sum()); dist = float(np.sqrt(((A / math.sqrt(nA) - B / math.sqrt(nB)) ** 2).sum())); ratio = nA / nB
        rows.append(dict(m=m, c=c, h=h, distance=dist, norm_ratio=ratio, distance_over_m2h2=dist / (m * m * h * h)))
        good &= dist <= c and abs(ratio - 1) <= c and (prev is None or dist < prev); prev = dist
ok("B3_finite_field_filter_approaches_the_shifted_zero_field_filter", good, rows=rows)
# B4
rows = []; F = 1.0; t = 2.0
for delta in (0.2, 0.1, 0.05):
    h = F * delta ** 4; m = int(round(delta ** -2.5 / 2.0)) * 2; n = int(round(t / delta ** 3)); w = Walk(2 * m + n + 8, h); w.prepare(m); p_word = w.norm2()
    for _ in range(n): w.step()
    prob = (np.abs(w.r) ** 2 + np.abs(w.l) ** 2) / p_word; Y = delta ** 2 * w.x; neg = Y < 0; pos = Y > 0
    mn, mp = float(prob[neg].sum()), float(prob[pos].sum()); yn = float((prob[neg] * Y[neg]).sum()) / mn; yp = float((prob[pos] * Y[pos]).sum()) / mp
    sn = math.sqrt(float((prob[neg] * (Y[neg] - yn) ** 2).sum()) / mn); sp = math.sqrt(float((prob[pos] * (Y[pos] - yp) ** 2).sum()) / mp)
    central = F * t * t / 2; offset = central + t * m * h / delta
    rows.append(dict(delta=delta, m=m, h=h, free_steps=n, word_probability=p_word, word_probability_reference=delta ** 1.25 / math.sqrt(math.pi), total=float(prob.sum()),
                     mass_negative=mn, mass_positive=mp, mean_negative=yn, mean_positive=yp, width_negative=sn, width_positive=sp, central_ray=central, ray_with_preparation_offset=offset,
                     residual_against_central=(abs(yn + central) + abs(yp - central)) / 2, relative_error_against_offset_ray=max(abs(-yn / offset - 1), abs(yp / offset - 1))))
    print(rows[-1], flush=True)
ok("B4_two_rays_with_equal_masses", all(abs(r["mass_negative"] - 0.5) < 0.02 and abs(r["mass_positive"] - 0.5) < 0.02 and r["relative_error_against_offset_ray"] < 0.15 for r in rows)
   and rows[0]["residual_against_central"] > rows[1]["residual_against_central"] > rows[2]["residual_against_central"], rows=rows)
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
