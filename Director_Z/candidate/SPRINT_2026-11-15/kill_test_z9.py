"""Kill test KZ9 of the candidate sprint (third batch), predicate as fixed in 00_PLAN.md before this program.
Signed line, sharp start. Usage: python3 kill_test_z9.py RESULT.json (refuses to overwrite)."""
import sys, os, json
from decimal import Decimal, getcontext
getcontext().prec = 60
OUT = sys.argv[1]; assert not os.path.exists(OUT)
LN2 = Decimal(2).ln(); EPS = Decimal(10) ** -40
st = {(0, 0): (1, 1)}; rows = []; lq = {}; lc = {}
for T in range(1, 301):
    new = {}
    for (x, r), (sg, n) in st.items():
        for y, r2, flip in ((x + 1, 0, 1), (x - 1, 1, -1 if r == 1 else 1)):
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + sg * flip, b + n)
    st = new
    wq = sum(s * s for s, n in st.values()); wc = sum(n for s, n in st.values())
    lq[T] = sum((Decimal(s * s) / wq) * (Decimal(n).ln() / LN2) for s, n in st.values() if s)
    lc[T] = sum((Decimal(n) / wc) * (Decimal(n).ln() / LN2) for s, n in st.values())
fa = [T for T in range(3, 301) if not lq[T] < lc[T] - EPS]
fb = [T for T in range(3, 299) if not lq[T + 2] / (T + 2) > lq[T] / T + EPS]
fc = [T for T in range(3, 301) if not lq[T] / T < 1 - EPS]
rep = {"argv": sys.argv[1:], "a_failures": fa[:10], "b_failures": fb[:10], "c_failures": fc[:10], "counts": [len(fa), len(fb), len(fc)],
       "samples": [[T, str(lq[T])[:20], str(lc[T])[:20], str(lq[T] / T)[:12], str(lc[T] / T)[:12]] for T in (3, 4, 5, 6, 8, 16, 32, 64, 128, 200, 300)],
       "predicate": not fa and not fb and not fc}
rep["verdict"] = "STANDS" if rep["predicate"] else "KILLED"
json.dump(rep, open(OUT, "x"), indent=1); print(rep["verdict"], rep["counts"], fa[:5], fb[:8], fc[:5]); [print(s) for s in rep["samples"]]
