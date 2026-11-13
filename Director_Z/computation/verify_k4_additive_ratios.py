#!/usr/bin/env python3
"""Check of one sentence of paper G10, Section 4 (added at the comb after edition Z17).
Carrier: complete graph on four vertices, every edge in both directions, gain omega (order three) on the arc 0 -> 1, omega^-1 on 1 -> 0,
gain 1 elsewhere.  Additive switching-invariant rule: F(w) = a for a walk that does not end at its start, F_c(gain) for one that does.
Ratio of a walk w: (sum over arcs e leaving the end of w of F(we)) / F(w).
Predicates, fixed before the run:
 K1  with a = 1, F_c(1) = 2, F_c(omega) = F_c(omega^-1) = 1/2 the set of ratios over all walks of length two from each start vertex is
     {3/2, 5/2, 4};
 K2  with a = 1, F_c(1) = 1, F_c(omega) = 2, F_c(omega^-1) = 1/2 (the other reading of "weights 2 and 1/2") the set is NOT {3/2, 5/2, 4};
 K3  with F_c = a = 1 every ratio equals 3 (the count is consistent with factor d = 3).
Exact rational arithmetic.  Writes K4_Additive_Ratios_Results.json; refuses to overwrite."""
import json, os, sys
from fractions import Fraction as Fr
OUT = "K4_Additive_Ratios_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
def gain(x, y): return 1 if (x, y) == (0, 1) else 2 if (x, y) == (1, 0) else 0      # exponent of omega
def ratios(Fc, a, start):
    out = set()
    walks = [((start,), 0)]
    for _ in range(2): walks = [(w + (y,), (g + gain(w[-1], y)) % 3) for w, g in walks for y in range(4) if y != w[-1]]
    F = lambda w, g: Fc[g] if w[-1] == w[0] else a
    for w, g in walks:
        out.add(sum(F(w + (y,), (g + gain(w[-1], y)) % 3) for y in range(4) if y != w[-1]) / F(w, g))
    return out
R = {}
r1 = {s: sorted(ratios({0: Fr(2), 1: Fr(1, 2), 2: Fr(1, 2)}, Fr(1), s)) for s in range(4)}
r2 = {s: sorted(ratios({0: Fr(1), 1: Fr(2), 2: Fr(1, 2)}, Fr(1), s)) for s in range(4)}
r3 = {s: sorted(ratios({0: Fr(1), 1: Fr(1), 2: Fr(1)}, Fr(1), s)) for s in range(4)}
target = [Fr(3, 2), Fr(5, 2), Fr(4)]
st = lambda r: {str(s): [str(x) for x in v] for s, v in r.items()}
R["K1"] = dict(passed=all(v == target for v in r1.values()), ratios=st(r1))
R["K2"] = dict(passed=all(v != target for v in r2.values()), ratios=st(r2))
R["K3"] = dict(passed=all(v == [Fr(3)] for v in r3.values()), ratios=st(r3))
R["_summary"] = dict(predicates=3, passed=sum(1 for k in ("K1", "K2", "K3") if R[k]["passed"]))
json.dump(R, open(OUT, "w"), indent=1); print(json.dumps(R, indent=1))
