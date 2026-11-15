"""Director's test of the forward prediction R7 of candidate Z10 "Slow Clock" (STIPULATED CANDIDATE FOR DISPROOF).
The two sub-agents assigned to attack the candidate were stopped by the account's usage limit before writing
anything, so the director runs R7 himself. The predicate was fixed in FUNCTION.md and BRAND.md before this run:
 R7  gap(2400) = c* - Lambda(2400)/2400 lies strictly between 0.0020 and 0.0035.
 Also checked: Lambda(T) <= Lambda_c(T) for every T to 2400 with equality exactly for T <= 4 (E6 extended), and
 Lambda(T)/T < c* for every T to 2400.
c* by Simpson's rule with 200,000 panels (as in KZ10); logarithms in 60-digit decimals; margin 10^-40.
Usage: python3 r7.py RESULT.json (refuses to overwrite)."""
import sys, os, json, math
from decimal import Decimal, getcontext
getcontext().prec = 60
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def h(x): return 0.0 if x <= 0 or x >= 1 else -(x * math.log2(x) + (1 - x) * math.log2(1 - x))
def g(t): return h((1 + math.sin(t) / math.sqrt(2)) / 2) / (1 - math.sin(t) ** 2 / 2)
n_ = 200000; a_, b_ = -math.pi / 2, math.pi / 2; hh = (b_ - a_) / n_
cstar = (g(a_) + g(b_) + sum((4 if i % 2 else 2) * g(a_ + i * hh) for i in range(1, n_))) * hh / 3 / (math.pi * math.sqrt(2))
C = Decimal(repr(cstar)); LN2 = Decimal(2).ln(); EPS = Decimal(10) ** -40
st = {(0, 0): (1, 1)}; eq = []; gt = []; above = []; rates = {}
for T in range(1, 2401):
    new = {}
    for (x, r), (sg, n) in st.items():
        for y, r2, flip in ((x + 1, 0, 1), (x - 1, 1, -1 if r == 1 else 1)):
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + sg * flip, b + n)
    st = new; two = Decimal(2) ** T
    lq = sum((Decimal(s * s) / two) * (Decimal(n).ln() / LN2) for s, n in st.values() if s)
    lc = sum((Decimal(n) / two) * (Decimal(n).ln() / LN2) for s, n in st.values())
    if abs(lq - lc) <= EPS: eq.append(T)
    if lq > lc + EPS: gt.append(T)
    if not lq / T < C: above.append(T)
    if T in (300, 600, 1200, 2400): rates[T] = (lq / T, lc / T)
gap = C - rates[2400][0]
rep = {"argv": sys.argv[1:], "c_star": cstar, "rates": {str(T): [str(a)[:14], str(b)[:14]] for T, (a, b) in rates.items()},
       "gaps": {str(T): str(C - a)[:14] for T, (a, b) in rates.items()}, "gap_2400": str(gap)[:16],
       "R7_strictly_between_0.0020_and_0.0035": Decimal("0.0020") < gap < Decimal("0.0035"),
       "E6_extended": (not gt) and eq == [1, 2, 3, 4], "equal_lengths": eq, "lengths_with_interfering_age_larger": gt[:5], "lengths_with_rate_not_below_c_star": above[:5]}
rep["verdict_for_Z10"] = "STANDS" if rep["R7_strictly_between_0.0020_and_0.0035"] and rep["E6_extended"] and not above else "KILLED"
json.dump(rep, open(OUT, "x"), indent=1); print(json.dumps(rep, indent=1))
