#!/usr/bin/env python3
"""Second follow-up.  Predicate A1c of followup_A1_units.py FAILED and is kept.  Cause found by reading
its own code: the acceptance guard (value < -1e-6 * sum N) equals the tested weight eps = 1e-6, so
no value of about -eps*N could pass; the predicate was badly designed, it says nothing about the paper.

PREDICATE A1d (fixed before the run): as A1c (q = 8, 10, 12; units as there; exponents 0..12;
coefficient limit 1e9) but with c_k = -1e-4 and the unchanged guard 1e-6 (a factor 100 below the weight;
float error of the embedding sums for coefficients below 1e9 is below 1e-7 relative only if
coefficients stay below about 1e4, so additionally the element reported must have coefficients
below 1e4, else the case counts as not met).
Result file followup_A1_units_2_results.json, never overwritten.
"""
import json, os, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "followup_A1_units_2_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "followup_A1_units.py")).read()
import math, itertools
ns = {"__file__": __file__, "os": os, "math": math, "itertools": itertools}
exec(src[src.index("# reuse only"):src.index("res = {")], ns)
res = {"A1d": {q: ns["search"](q, uc, 1e-4, 12, 1e4) for q, uc in ((8, (0, 1, 2)), (10, (0, 1, 2)), (12, (0, 1)))}}
res["A1d_met"] = all(v["met"] for v in res["A1d"].values())
json.dump(res, open(OUT, "w"), indent=1, default=str); print(json.dumps(res, default=str))
