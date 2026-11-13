"""Second follow-up. B1' FAILED in xrev_followup_result.json (sup ratio 0.16666666666667458 > 1/6) and stays
recorded. Diagnosis offered before this run: at q=1e-12 the quantity q^4/6 ~ 1.7e-49 is a difference of
numbers of size 0.8 carried to 60 digits, so its relative rounding error is ~1e-11.

PREDICATES (fixed before the run)
 B1''  at 200 digits: |omega(k*+q)-omega(k*)-q^2/2| <= q^4/6 for the same 2000 seeded q, for q=10^-j,
       j=1..12, and for the 4000 nonzero grid points; and list which q failed at 60 digits.
 B1s   sympy series of -asin(cos q/sqrt2)+pi/4-q^2/2 about q=0 is -q^4/6 + c6 q^6 + O(q^8) with c6>0
       (so the remainder is strictly inside the bound for small q != 0).
"""
import json, os, sys, random
import mpmath as mp, sympy as sy
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xrev_followup2_result.json")
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
random.seed(20261113)
raw = [random.uniform(-1, 1) for _ in range(2000)]
def run(dps):
    mp.mp.dps = dps
    qs = [mp.mpf(x) for x in raw] + [mp.mpf(10)**(-j) for j in range(1, 13)] + \
         [mp.mpf(-1)+mp.mpf(2)*i/4000 for i in range(4001) if i != 2000]
    bad = []; worst = mp.mpf(0)
    for q in qs:
        v = abs(mp.asin(mp.sin(-mp.pi/2+q)/mp.sqrt(2)) + mp.pi/4 - q*q/2)
        worst = max(worst, v/q**4)
        if v > q**4/6: bad.append(mp.nstr(q, 6))
    return bad, mp.nstr(worst, 25)
bad60, w60 = run(60)
bad200, w200 = run(200)
q = sy.symbols("q")
ser = sy.series(-sy.asin(sy.cos(q)/sy.sqrt(2)) + sy.pi/4 - q**2/2, q, 0, 8).removeO()
c4, c6 = ser.coeff(q, 4), ser.coeff(q, 6)
res = {"failing_q_at_60_digits": bad60, "sup_ratio_60": w60, "failing_q_at_200_digits": bad200, "sup_ratio_200": w200,
       "series": str(ser), "predicates": {"B1pp": len(bad200) == 0, "B1s": bool(c4 == sy.Rational(-1, 6) and c6 > 0)}}
print(res)
json.dump(res, open(OUT, "x"), indent=1)
