#!/usr/bin/env python3
"""Director Z cross-check of Director G's paper "What two sheet registers can tell each other" (pull request 2, commit 6bb2d14).
Nothing is imported from Director G's programs.  Level of this check: the sheet operators only.  The paper states that the destructive
record of a three-step block with gains v = (a, b) acts on the two sheet registers as D_v = S_v - S_v^-1 over sqrt 8 and the constructive
record as S_v + S_v^-1 over sqrt 8, with S_v the translation of (y, z) by (a, b); that statement is taken from the paper and is not tested
here.  Exact integer arithmetic.  Predicates, fixed before the run:
 R1  for p = 3, 5, 7, 11 and every unit u: after D_(0,1) and D_(1,-j) for every j != u, the integer vector on (Z/p)^2 from a localized start
     has p entries +1, p entries -1 and no others; the +1 entries form one coset of the line u y + z = constant and the -1 entries the
     coset whose constant differs by 2 or -2; the squared count is 2p (so the word has probability 2p/8^p);
 R2  for the same p and u and every j: the next destructive record with v = (1, -j) has conditional probability 0 if j = u, 3/8 if
     j = u + 1 or u - 1, and 1/4 otherwise; the constructive record has 1/2 minus that;
 R3  for M = 9, 15 (not prime) and all a, b: from a localized start, after a destructive record at (1, a) the destructive record at (1, b)
     has conditional probability 3/8 if a = b and 1/4 otherwise;
 R4  the identity prod_{k=1}^{p-1} (zeta^k - zeta^-k) = p for p = 3, 5, 7, 11, 13 to 1e-9.
Writes Crosscheck_Director_G_Relative_Transport_Results.json; refuses to overwrite."""
import cmath, json, math, os, sys
from fractions import Fraction
import numpy as np
OUT = "Crosscheck_Director_G_Relative_Transport_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
def shift(v, a, b): return np.roll(np.roll(v, a, axis=0), b, axis=1)                # entry (y, z) moves to (y + a, z + b)
def D(v, a, b): return shift(v, a, b) - shift(v, -a, -b)
def Cn(v, a, b): return shift(v, a, b) + shift(v, -a, -b)
sq = lambda v: int((v.astype(object) ** 2).sum())
rows1 = []; rows2 = []; g1 = g2 = True
for p in (3, 5, 7, 11):
    for u in range(1, p):
        v = np.zeros((p, p), dtype=np.int64); v[0, 0] = 1; v = D(v, 0, 1)
        for j in range(p):
            if j != u: v = D(v, 1, (-j) % p)
        plus = [(y, z) for y in range(p) for z in range(p) if v[y, z] == 1]; minus = [(y, z) for y in range(p) for z in range(p) if v[y, z] == -1]
        cp = {(u * y + z) % p for y, z in plus}; cm = {(u * y + z) % p for y, z in minus}
        good = (len(plus) == p and len(minus) == p and int(np.abs(v).sum()) == 2 * p and len(cp) == 1 and len(cm) == 1 and (min(cp) - min(cm)) % p in (2 % p, (-2) % p) and sq(v) == 2 * p)
        g1 &= good; rows1.append(dict(p=p, u=u, plus=len(plus), minus=len(minus), coset_of_plus=sorted(cp), coset_of_minus=sorted(cm), squared_count=sq(v)))
        for j in range(p):
            qd = Fraction(sq(D(v, 1, (-j) % p)), 8 * sq(v)); qc = Fraction(sq(Cn(v, 1, (-j) % p)), 8 * sq(v)); d = (u - j) % p
            want = Fraction(0) if d == 0 else (Fraction(3, 8) if d in (1, p - 1) else Fraction(1, 4))
            g2 &= qd == want and qc == Fraction(1, 2) - want; rows2.append(dict(p=p, u=u, j=j, destructive=str(qd), constructive=str(qc)))
ok("R1_word_prepares_two_opposite_cosets_of_one_line", g1, rows=rows1)
ok("R2_follow_up_probabilities", g2, cases=len(rows2), distinct_values=sorted({r["destructive"] for r in rows2}))
g3 = True; n3 = 0
for M in (9, 15):
    for a in range(M):
        for b in range(M):
            v = np.zeros((M, M), dtype=np.int64); v[0, 0] = 1; v = D(v, 1, a); q = Fraction(sq(D(v, 1, b)), 8 * sq(v)); n3 += 1
            g3 &= q == (Fraction(3, 8) if a == b else Fraction(1, 4))
ok("R3_two_block_control_at_composite_orders", g3, cases=n3)
rows4 = []
for p in (3, 5, 7, 11, 13):
    z = cmath.exp(2j * math.pi / p); pr = 1
    for k in range(1, p): pr *= z ** k - z ** (-k)
    rows4.append(dict(p=p, product_real=pr.real, product_imag=pr.imag))
ok("R4_cyclotomic_product_equals_p", all(abs(r["product_real"] - r["p"]) < 1e-9 and abs(r["product_imag"]) < 1e-9 for r in rows4), rows=rows4)
R["_summary"] = dict(predicates=4, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
