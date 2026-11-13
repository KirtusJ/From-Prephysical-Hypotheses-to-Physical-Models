#!/usr/bin/env python3
"""Follow-up to crosscheck_director_g.py, whose predicate X4 failed and is kept: the largest ratio of the band remainder
|w(k* + q) - w(k*) - q^2/2| to q^4/6 came out as 1.000114.  Diagnosis: in double precision the remainder at q = 0.001 is 1.7e-13 and is
formed by cancellation of numbers of order one, so its relative error is about 1e-3; the series of the integrand,
sin s / sqrt(1 + sin^2 s) = s - (2/3) s^3 + (19/30) s^5 - ..., gives a ratio below one that tends to one as q -> 0.
Predicates fixed before this run, in 60-digit arithmetic (mpmath):
 X4b  the ratio is at most 1 at every one of 4000 nonzero grid points of [-1, 1], and at q = 1e-3, 1e-2, 0.1, 0.5, 1 it is
      1 - (19/30) q^2 to within 5 q^4 (the next term of the series);
 X4c  the two other parts of X4 as computed before: section derivative at most 2; Bloch vector as stated (carried from the first result file).
Writes Crosscheck_Director_G_Followup_Results.json; refuses to overwrite."""
import json, os, sys
import mpmath as mp
OUT = "Crosscheck_Director_G_Followup_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
mp.mp.dps = 60
ks = -mp.pi / 2
w = lambda k: mp.asin(mp.sin(k) / mp.sqrt(2))
def ratio(q): q = mp.mpf(q); return abs(w(ks + q) - w(ks) - q * q / 2) / (q ** 4 / 6)
worst = mp.mpf(0)
for i in range(-2000, 2001):
    if i == 0: continue
    worst = max(worst, ratio(mp.mpf(i) / 2000))
# the remainder is q^4/6 - (19/180) q^6 + ..., so the ratio is 1 - (19/30) q^2 + O(q^4)
pts = {str(q): [float(ratio(q)), float(1 - mp.mpf(19) / 30 * mp.mpf(q) ** 2)] for q in ("0.001", "0.01", "0.1", "0.5", "1")}
series_ok = all(abs(v[0] - v[1]) <= 5 * float(q) ** 4 + 1e-30 for q, v in pts.items())
first = json.load(open("Crosscheck_Director_G_Results.json"))["X4_inputs_of_the_bound"]
R = {"X4b_band_remainder_at_most_q4_over_6": dict(passed=bool(worst <= 1 and series_ok), largest_ratio=mp.nstr(worst, 30), ratio_and_series_value=pts, digits=mp.mp.dps,
                                                   first_run="ratio 1.000114 in double precision at a grid point near q = 0.001: rounding in a difference of numbers of order one; the predicate of the first program failed through its arithmetic"),
     "X4c_section_derivative_and_bloch_vector": dict(passed=bool(first["largest_section_derivative"] <= 2 and first["bloch_vector_matches_up_to_axis_convention"]["residual"] < 1e-9),
                                                      largest_section_derivative=first["largest_section_derivative"], bloch=first["bloch_vector_matches_up_to_axis_convention"])}
R["_summary"] = dict(predicates=2, passed=sum(1 for v in R.values() if v["passed"]), mpmath=mp.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k, v.get("largest_ratio", ""), v.get("ratio_and_series_value", ""))
