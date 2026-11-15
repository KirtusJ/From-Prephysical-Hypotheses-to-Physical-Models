"""Kill test KZ10 of the candidate sprint, predicate as fixed in 00_PLAN.md before this program and before c* was
computed. Signed line, sharp start. Usage: python3 kill_test_z10.py RESULT.json (refuses to overwrite)."""
import sys, os, json, math
from decimal import Decimal, getcontext
getcontext().prec = 60
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def h(x): return 0.0 if x <= 0 or x >= 1 else -(x * math.log2(x) + (1 - x) * math.log2(1 - x))
def g(t): return h((1 + math.sin(t) / math.sqrt(2)) / 2) / (1 - math.sin(t) ** 2 / 2)
def simpson(f, a, b, n):
    hh = (b - a) / n; s = f(a) + f(b)
    for i in range(1, n): s += (4 if i % 2 else 2) * f(a + i * hh)
    return s * hh / 3
cstar = simpson(g, -math.pi / 2, math.pi / 2, 200000) / (math.pi * math.sqrt(2))
cstar_half = simpson(g, -math.pi / 2, math.pi / 2, 100000) / (math.pi * math.sqrt(2))
norm = simpson(lambda t: 1 / (1 - math.sin(t) ** 2 / 2), -math.pi / 2, math.pi / 2, 200000) / (math.pi * math.sqrt(2))
LN2 = Decimal(2).ln(); EPS = Decimal(10) ** -40
st = {(0, 0): (1, 1)}; lq = {}; lc = {}
for T in range(1, 1201):
    new = {}
    for (x, r), (sg, n) in st.items():
        for y, r2, flip in ((x + 1, 0, 1), (x - 1, 1, -1 if r == 1 else 1)):
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + sg * flip, b + n)
    st = new
    wq = sum(s * s for s, n in st.values()); wc = sum(n for s, n in st.values())
    lq[T] = sum((Decimal(s * s) / wq) * (Decimal(n).ln() / LN2) for s, n in st.values() if s)
    lc[T] = sum((Decimal(n) / wc) * (Decimal(n).ln() / LN2) for s, n in st.values())
C = Decimal(repr(cstar)); r = {T: lq[T] / T for T in (300, 600, 1200)}
eq = [T for T in range(1, 1201) if abs(lq[T] - lc[T]) <= EPS]; gt = [T for T in range(1, 1201) if lq[T] > lc[T] + EPS]
P = {"a": 0 < cstar < 1, "b": all(r[T] < C for T in r), "c": (C - r[600] < C - r[300]) and (C - r[1200] < C - r[600]),
     "d": C - r[1200] < Decimal("0.01"), "e": (not gt) and eq == [1, 2, 3, 4], "f": 1 - lc[1200] / 1200 < Decimal("0.01")}
rep = {"argv": sys.argv[1:], "c_star": cstar, "c_star_with_half_the_panels": cstar_half, "normalisation_of_the_weight": norm,
       "rates": {str(T): str(r[T])[:14] for T in r}, "gaps": {str(T): str(C - r[T])[:14] for T in r}, "counting_rate_1200": str(lc[1200] / 1200)[:14],
       "equal_lengths": eq[:10], "lengths_where_interfering_age_is_larger": gt[:10], "predicates": P, "predicate": all(P.values())}
rep["verdict"] = "STANDS" if rep["predicate"] else "KILLED"
json.dump(rep, open(OUT, "x"), indent=1); print(rep["verdict"], P); print(cstar, cstar_half, norm, rep["rates"], rep["gaps"], rep["counting_rate_1200"], eq, gt[:5])
