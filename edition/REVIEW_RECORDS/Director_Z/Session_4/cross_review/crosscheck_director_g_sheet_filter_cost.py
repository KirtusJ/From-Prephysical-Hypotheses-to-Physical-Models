#!/usr/bin/env python3
"""Director Z, cost of the sheet preparation assumed in Director G's two-ray limit (pull request 2, commit d4f6fea).
The paper needs residual mass eta = o(delta^(5/4)) outside the two target sheet characters, with the field |h| = pi/M realized in the plane
of the characters r = (M -+ 1)/2 of an odd sheet order M, and says the three-step sheet instrument reaches any tolerance at each finite M
and that its cost must be counted separately.  This program counts it, for this participant's extension to M sheets of the five-sheet
word of the paper on native preparations: one destructive record and then s constructive records, integer sheet vector
(T + T^-1)^s (T - T^-1)|0>, joint probability C_s/8^(s+1) with C_s its squared length.  In characters,
C_s = (1/M) sum_r 4 sin^2(2 pi r/M) (2 cos(2 pi r/M))^(2s).
Predicates, fixed before the run:
 C1  for M = 5 and s = 0..10 the weight outside the planes r = 2, 3 equals 1/(1 + phi^(4s-2)), phi the golden ratio, to 1e-12
     (the formula of Director G; validates the model used here);
 C2  for M = 25, 45, 75, 135 the least s with weight at most 0.01 outside the planes r = (M -+ 1)/2, divided by M^2, is within 25 percent
     of ln(400)/(3 pi^2) = 0.2024;
 C3  for the same M the base-2 logarithm of the joint probability of that word, divided by that s, lies between -1.15 and -0.95.
Recorded without a predicate: the same quantities for M = 9, 15, and the value of s and of the logarithm for M = pi/delta^4 at
delta = 0.2 from the two fitted laws.  Writes Crosscheck_Director_G_Sheet_Filter_Cost_Results.json; refuses to overwrite."""
import json, math, os, sys
import numpy as np
OUT = "Crosscheck_Director_G_Sheet_Filter_Cost_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
def logweights(M, s):
    r = np.arange(1, M); ph = 2 * math.pi * r / M                      # r = 0 has weight zero
    return r, np.log(4 * np.sin(ph) ** 2) + 2 * s * np.log(np.abs(2 * np.cos(ph)))
def outside(M, s):
    r, lw = logweights(M, s); w = np.exp(lw - lw.max()); tgt = (r == (M - 1) // 2) | (r == (M + 1) // 2); return float(w[~tgt].sum() / w.sum())
def log2prob(M, s):
    r, lw = logweights(M, s); mx = lw.max(); return (mx + math.log(np.exp(lw - mx).sum()) - math.log(M)) / math.log(2) - 3 * (s + 1)
phi = (1 + math.sqrt(5)) / 2
ok("C1_five_sheet_formula_reproduced", all(abs(outside(5, s) - 1 / (1 + phi ** (4 * s - 2))) < 1e-12 for s in range(11)),
   largest_difference=max(abs(outside(5, s) - 1 / (1 + phi ** (4 * s - 2))) for s in range(11)))
rows = []
for M in (9, 15, 25, 45, 75, 135):
    s = 0
    while outside(M, s) > 0.01: s += 1
    rows.append(dict(M=M, least_s=s, s_over_M2=s / M ** 2, log2_joint_probability=log2prob(M, s), log2_over_s=log2prob(M, s) / s, weight_outside=outside(M, s))); print(rows[-1], flush=True)
ref = math.log(400) / (3 * math.pi ** 2); big = [r for r in rows if r["M"] >= 25]
ok("C2_records_needed_grow_as_the_square_of_the_sheet_order", all(abs(r["s_over_M2"] / ref - 1) < 0.25 for r in big), reference=ref, rows=rows)
ok("C3_joint_probability_halves_with_each_record", all(-1.15 <= r["log2_over_s"] <= -0.95 for r in big))
M02 = math.pi / 0.2 ** 4; s02 = ref * M02 ** 2
R["_extrapolation_not_a_predicate"] = dict(delta=0.2, F=1, sheet_order=M02, records_by_the_fitted_law=s02, log2_joint_probability_by_the_fitted_law=-s02,
                                           note="tolerance 0.01 only; the paper needs a tolerance that decreases with delta, which adds a logarithmic factor")
R["_summary"] = dict(predicates=3, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_extrapolation_not_a_predicate"]); print(R["_summary"])
