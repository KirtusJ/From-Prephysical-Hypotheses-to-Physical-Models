"""Follow-up to xrev_periodic.py. The original predicates A2, A3, B1 FAILED and stay recorded as failed
in xrev_periodic_result.json. Diagnosis offered before this run: the failures sit where the bound is
below the 60-digit resolution used (rho printed as ~1e-61 against bounds 1e-64..1e-77), and B1 at q=0
where a 1e-61 rounding residue is compared with 0. This program tests that diagnosis.

FOLLOW-UP PREDICATES (fixed before the run)
 A2'  as A2 (rho <= (N-3)(lambda2/lambda1)^m, N in {8,12,16,20,24,28,32,40}, four depths) at 400 digits.
      Basis for 400: smallest bound is ~1e-77; rho must be resolved far below it.
 A3'  as A3 (rho <= N^(1-3pi^2/ln2) at the note's depth) at 400 digits.
 A2'' same at 800 digits gives the same rho to 30 significant digits (precision is no longer the limit).
 B1'  as B1 at 60 digits on the same 4001 q, excluding q=0 exactly (where both sides are 0 analytically);
      plus 2000 seeded random q in (-1,1) and q=10^-j, j=1..12. Also report every q at which the
      ORIGINAL comparison fails.
"""
import json, os, sys, random
from fractions import Fraction
from math import ceil, log2
import mpmath as mp
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xrev_followup_result.json")
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
random.seed(20261113)
def counts(n, m):
    row = [1] + [0]*(n-1)
    for _ in range(m):
        row = [row[d-1] + 2*row[d] + row[(d+1) % n] for d in range(n)]
    return row
def rho_bound(n, m, dps):
    mp.mp.dps = dps
    c = counts(n, m); den = c[0]-c[n//2]
    rho = max(abs(mp.mpf(2*(c[0]-c[d]))/den - (1-mp.cos(2*mp.pi*d/n))) for d in range(n))
    r = (mp.cos(2*mp.pi/n)/mp.cos(mp.pi/n))**2
    return rho, (n-3)*r**m, mp.mpf(n)**(1-3*mp.pi**2/mp.log(2))
res = {"rows": [], "predicates": {}}
a2 = a3 = a2b = True
for n in (8, 12, 16, 20, 24, 28, 32, 40):
    mfull = n*n*ceil(log2(n))
    for m in (1, n, n*n, mfull):
        rho, bd, pw = rho_bound(n, m, 400)
        rho8, _, _ = rho_bound(n, m, 800)
        same = (rho8 == 0 and rho == 0) or abs(rho-rho8) <= abs(rho8)*mp.mpf(10)**(-30)
        row = {"N": n, "m": m, "rho": mp.nstr(rho, 10), "bound": mp.nstr(bd, 10), "ratio": mp.nstr(rho/bd, 8),
               "A2p": bool(rho <= bd), "stable_800": bool(same)}
        a2 &= row["A2p"]; a2b &= bool(same)
        if m == mfull:
            row["power_bound"] = mp.nstr(pw, 10); row["A3p"] = bool(rho <= pw); a3 &= row["A3p"]
        res["rows"].append(row); print(row)
res["predicates"]["A2p"] = a2; res["predicates"]["A3p"] = a3; res["predicates"]["A2pp_stable"] = a2b
mp.mp.dps = 60
def lhs(q): return abs(mp.asin(mp.sin(-mp.pi/2+q)/mp.sqrt(2)) + mp.pi/4 - q*q/2)
orig_fail = []; b1 = True; worst = mp.mpf(0)
qs = [mp.mpf(-1)+mp.mpf(2)*i/4000 for i in range(4001)]
for q in qs:
    if lhs(q) > q**4/6:
        orig_fail.append(mp.nstr(q, 5))
        if q != 0: b1 = False
extra = [mp.mpf(random.uniform(-1, 1)) for _ in range(2000)] + [mp.mpf(10)**(-j) for j in range(1, 13)]
for q in extra:
    v = lhs(q)
    worst = max(worst, v/q**4)
    if v > q**4/6: b1 = False
res["predicates"]["B1p"] = b1
res["B1_original_failing_q"] = orig_fail
res["B1_sup_ratio_extra"] = mp.nstr(worst, 20)
res["B1_value_at_q0"] = mp.nstr(lhs(mp.mpf(0)), 5)
print(res["predicates"], orig_fail, res["B1_sup_ratio_extra"], res["B1_value_at_q0"])
json.dump(res, open(OUT, "x"), indent=1)
