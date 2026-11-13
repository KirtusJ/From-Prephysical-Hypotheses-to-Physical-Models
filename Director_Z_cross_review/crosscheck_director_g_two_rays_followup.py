#!/usr/bin/env python3
"""Follow-up to crosscheck_director_g_two_rays.py, whose predicate B4 failed and is kept: at delta = 0.2 the masses of the two halves were
0.456 and 0.544, outside the tolerance 0.02 of 1/2 that this participant had set.  Diagnosis, made from the three rows of that run: the
preparation leaves the momentum at the distance m h from the band edge, where the retained direction no longer has equal weight on the two
bands; the difference of the masses was 0.98, 1.00 and 1.00 times m h.  Predicates fixed before this run, on values of delta not used before
(delta = 0.14 and 0.07; F = 1, t = 2, same protocol and model):
 B4b  the mass of Y > 0 minus the mass of Y < 0 is within 5 percent of m h;
 B4c  the conditional means of the two halves are within 15 percent of -+(F t^2/2 + t m h/delta);
 B4d  the probability of the retained word, divided by binom(2m, m)/4^m, is within 0.01 of exp(-m^3 h^2/3).
Writes Crosscheck_Director_G_Two_Rays_Followup_Results.json; refuses to overwrite."""
import json, math, os, sys
from math import comb
import numpy as np
OUT = "Crosscheck_Director_G_Two_Rays_Followup_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
RT2 = math.sqrt(2.0)
def run(delta, F=1.0, t=2.0):
    h = F * delta ** 4; m = int(round(delta ** -2.5 / 2.0)) * 2; n = int(round(t / delta ** 3)); X = 2 * m + n + 8; x = np.arange(-X, X + 1)
    r = np.zeros(2 * X + 1, dtype=complex); l = np.zeros(2 * X + 1, dtype=complex); r[X] = 1.0; ph = np.exp(-1j * h * x)
    def step(r, l):
        r = r * ph; l = l * ph; a = (r + l) / RT2; b = (r - l) / RT2; r2 = np.zeros_like(a); l2 = np.zeros_like(b); r2[1:] = a[:-1]; l2[:-1] = b[1:]; return r2, l2
    keep = "L"
    for _ in range(m):
        r, l = step(*step(r, l))
        if keep == "L": r[:] = 0
        else: l[:] = 0
        keep = "R" if keep == "L" else "L"
    p_word = float((np.abs(r) ** 2 + np.abs(l) ** 2).sum())
    for _ in range(n): r, l = step(r, l)
    prob = (np.abs(r) ** 2 + np.abs(l) ** 2) / p_word; Y = delta ** 2 * x; neg = Y < 0; pos = Y > 0
    mn, mp = float(prob[neg].sum()), float(prob[pos].sum()); yn = float((prob[neg] * Y[neg]).sum()) / mn; yp = float((prob[pos] * Y[pos]).sum()) / mp
    offset = F * t * t / 2 + t * m * h / delta; zero_field = math.exp(math.lgamma(2 * m + 1) - 2 * math.lgamma(m + 1) - 2 * m * math.log(2.0))
    return dict(delta=delta, m=m, h=h, free_steps=n, mass_negative=mn, mass_positive=mp, mass_difference_over_mh=(mp - mn) / (m * h), mean_negative=yn, mean_positive=yp,
                ray_with_preparation_offset=offset, relative_error_against_offset_ray=max(abs(-yn / offset - 1), abs(yp / offset - 1)),
                word_probability_over_zero_field=p_word / zero_field, exp_minus_m3h2_over_3=math.exp(-m ** 3 * h * h / 3))
rows = [run(0.14), run(0.07)]
for r in rows: print(r, flush=True)
ok("B4b_mass_difference_is_m_times_h", all(abs(r["mass_difference_over_mh"] - 1) < 0.05 for r in rows), rows=rows)
ok("B4c_means_follow_the_ray_with_the_preparation_offset", all(r["relative_error_against_offset_ray"] < 0.15 for r in rows))
ok("B4d_word_probability_ratio", all(abs(r["word_probability_over_zero_field"] - r["exp_minus_m3h2_over_3"]) < 0.01 for r in rows))
R["_summary"] = dict(predicates=3, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
