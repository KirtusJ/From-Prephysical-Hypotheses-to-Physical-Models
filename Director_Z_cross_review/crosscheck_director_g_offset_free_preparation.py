#!/usr/bin/env python3
"""Director Z, a variant of Director G's direction-switch preparation in which the momentum offset left by the field cancels.
In the paper the field acts with one sign through the m preparation blocks and the output momentum sits at the distance m h from the band
edge; the centres of the two rays are then displaced by t m h/delta at scaled time t, the leading finite-scale error found in the earlier
cross-check.  Proposal tested here: reverse the sign of the field over the middle half of the blocks (signs +, -, -, + over the four
quarters; m divisible by 4).  Counting back from the output, the momentum offsets of the blocks then have mean zero.
Model as in crosscheck_director_g_two_rays.py; F = 1, t = 2, h = delta^4, m the multiple of 4 nearest delta^(-5/2), flight with the field +.
Predicates, fixed before the run (delta = 0.1 and 0.05):
 P1  the conditional means of Y on the two halves are within 5 percent of -+F t^2/2;
 P2  the masses of the two halves differ by less than 0.01;
 P3  the probability of the retained word, over binom(2m, m)/4^m, is at least 0.95.
Recorded without a predicate: the widths of the two halves, and the same quantities for the unmodified preparation from the earlier run.
Writes Crosscheck_Director_G_Offset_Free_Preparation_Results.json; refuses to overwrite."""
import json, math, os, sys
import numpy as np
OUT = "Crosscheck_Director_G_Offset_Free_Preparation_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
RT2 = math.sqrt(2.0)
def run(delta, F=1.0, t=2.0):
    h = F * delta ** 4; m = int(round(delta ** -2.5 / 4.0)) * 4; n = int(round(t / delta ** 3)); X = 2 * m + n + 8; x = np.arange(-X, X + 1)
    ph = {1: np.exp(-1j * h * x), -1: np.exp(1j * h * x)}
    def step(r, l, s):
        r = r * ph[s]; l = l * ph[s]; a = (r + l) / RT2; b = (r - l) / RT2; r2 = np.zeros_like(a); l2 = np.zeros_like(b); r2[1:] = a[:-1]; l2[:-1] = b[1:]; return r2, l2
    r = np.zeros(2 * X + 1, dtype=complex); l = np.zeros(2 * X + 1, dtype=complex); r[X] = 1.0; keep = "L"
    for j in range(m):
        s = 1 if (j < m // 4 or j >= 3 * m // 4) else -1; r, l = step(*step(r, l, s), s)
        if keep == "L": r[:] = 0
        else: l[:] = 0
        keep = "R" if keep == "L" else "L"
    p_word = float((np.abs(r) ** 2 + np.abs(l) ** 2).sum())
    for _ in range(n): r, l = step(r, l, 1)
    prob = (np.abs(r) ** 2 + np.abs(l) ** 2) / p_word; Y = delta ** 2 * x; neg = Y < 0; pos = Y > 0
    mn, mp = float(prob[neg].sum()), float(prob[pos].sum()); yn = float((prob[neg] * Y[neg]).sum()) / mn; yp = float((prob[pos] * Y[pos]).sum()) / mp
    sn = math.sqrt(float((prob[neg] * (Y[neg] - yn) ** 2).sum()) / mn); sp = math.sqrt(float((prob[pos] * (Y[pos] - yp) ** 2).sum()) / mp)
    zero_field = math.exp(math.lgamma(2 * m + 1) - 2 * math.lgamma(m + 1) - 2 * m * math.log(2.0)); central = F * t * t / 2
    return dict(delta=delta, m=m, h=h, mass_negative=mn, mass_positive=mp, mean_negative=yn, mean_positive=yp, width_negative=sn, width_positive=sp, central_ray=central,
                relative_error_against_central_ray=max(abs(-yn / central - 1), abs(yp / central - 1)), word_probability_over_zero_field=p_word / zero_field)
rows = [run(0.1), run(0.05)]
for r in rows: print(r, flush=True)
ok("P1_means_on_the_central_rays", all(r["relative_error_against_central_ray"] < 0.05 for r in rows), rows=rows)
ok("P2_equal_masses", all(abs(r["mass_positive"] - r["mass_negative"]) < 0.01 for r in rows))
ok("P3_yield", all(r["word_probability_over_zero_field"] >= 0.95 for r in rows))
R["_unmodified_preparation_for_comparison"] = [dict(delta=0.1, mean_negative=-2.5536, mean_positive=2.6035, mass_difference=0.0316, yield_ratio=0.900), dict(delta=0.05, mean_negative=-2.4258, mean_positive=2.4454, mass_difference=0.0112, yield_ratio=0.928)]
R["_summary"] = dict(predicates=3, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
