"""Cross-review program for PR 52 (hidden-copy memory), written from the note text only.
Exact rationals. Result file opened with mode 'x'. Failed predicates are recorded, not raised.

Model from the note: a_j = C(2j,j)/4^j; W(word) = product of a over segments cut by copies
(word has m-1 internal bits for m passes). Regenerating detector: fresh interval length B,
P(B>=b)=2/(b(b+1)); stationary start: residual (current use included) R, P(R>=n)=1/n;
each interval repeats d iid Bernoulli(p) bits.
My word law: enumerate boundary positions explicitly (compositions), not the note's recursion.

Predicates (fixed before first run), per (d,p):
 H1 hypothesis: 0<p<1, d>=1 (counted).
 P1 stationarity: sum_x P(xw)=sum_x P(wx)=P(w) for all words w with len<=d+3.
 P2 window: P(w)=Bernoulli(p) for every word of len<=d.
 P2c control: some word of length d+1 differs from Bernoulli (the law is not iid).
 P3 S_m^mem = S_m^iid for 1<=m<=d+1.
 P4 S_{d+2}^mem - S_{d+2}^iid = pq/(d+1) * E[mixed difference] and >0.
 P5 every mixed difference over the 2^(d-1) middle words >0; no-middle value = a_d(d^2+d+1)/(4(d+1)(d+2)).
 P6 lower bound S_m^mem >= q^d a_m/(m-1) for 2<=m<=MMAX (measured ratio recorded).
 P7 (measured only) is S_m^mem >= S_m^iid for all m<=MMAX? recorded, not claimed by the note.
Four-pass panel at each p: range of S_4 over triple laws with product adjacent pairs by vertex
 enumeration of (c0,c1) box; P8 endpoints equal iid + (7q/128)c0+(p/64)c1 at box corners;
 P9 order-two chain built from the triple law keeps product pair law for 6 further steps;
 P10 at p=1/3: 37/216, 113/648, [1/6,13/72], cancellation at c0=1/126,c1=-1/18.
64-pass design: P11 numbers 5.0454e-9, 4.9655e-4, 6100*iid<1/32000, 6100*lower>3;
 P12 (measured) same design at other p: does 6100 launches still give both bounds?
"""
import json, sys
from fractions import Fraction as F
from itertools import product
from math import comb
from functools import lru_cache
from pathlib import Path

def a(j): return F(comb(2*j, j), 4**j)
def bern(w, p): return p**sum(w) * (1-p)**(len(w)-sum(w))
def W(word):
    out, run = F(1), 1
    for b in word:
        if b: out *= a(run); run = 1
        else: run += 1
    return out*a(run)
def pB(b): return F(4, b*(b+1)*(b+2))        # fresh length
def tB(b): return F(2, b*(b+1))              # fresh P(B>=b)
def pR(r): return F(1, r) - F(1, r+1)        # stationary residual
def tR(r): return F(1, r)
def compositions(n):
    if n == 0: yield (); return
    for first in range(1, n+1):
        for rest in compositions(n-first): yield (first, *rest)
def law(d, p):
    @lru_cache(None)
    def P(word):
        n = len(word); tot = F(0)
        for comp in compositions(n):
            pr = F(1); pos = 0; ok = True
            for i, L in enumerate(comp):
                last = (i == len(comp)-1)
                if i == 0: pr *= tR(L) if last else pR(L)
                else: pr *= tB(L) if last else pB(L)
                seg = word[pos:pos+L]; pos += L
                if any(seg[k] != seg[k % d] for k in range(L)): ok = False; break
                pr *= bern(seg[:d], p)
            if ok: tot += pr
        return tot
    return P
def iidS(m, p): return sum(bern(w, p)*W(w) for w in product((0, 1), repeat=m-1))
def iidS_dp(m, p):
    S = [F(1)]
    for n in range(1, m+1):
        # S_n = q-free renewal: last segment length l, preceded by a copy (p) unless l==n; no-copy factors q
        S.append(sum((p if l < n else 1) * (1-p)**(l-1) * a(l) * S[n-l] for l in range(1, n+1)))
    return S[m]
def memS_dp(m, d, p):
    """exact S_m^mem by summing over boundaries (dp over interval pieces) and motif bits."""
    n = m-1
    if n == 0: return a(1)
    # state: after position pos with current uncut run length; do DP over intervals
    @lru_cache(None)
    def go(pos, run, first):
        if pos == n: return a(run)
        tot = F(0)
        for L in range(1, n-pos+1):
            last = (pos+L == n)
            pr = (tR(L) if last else pR(L)) if first else (tB(L) if last else pB(L))
            for motif in product((0, 1), repeat=min(d, L)):
                r = run; w = F(1)
                for k in range(L):
                    if motif[k % d]: w *= a(r); r = 1
                    else: r += 1
                tot += pr*bern(motif, p)*w*go(pos+L, r, False)
        return tot
    return go(0, 1, True)
def mixed(mid):
    return W((0, *mid, 0)) - W((0, *mid, 1)) - W((1, *mid, 0)) + W((1, *mid, 1))

res = {"cases": [], "panel": [], "design": [], "failed": []}
def pred(name, ok, ctx):
    if not ok: res["failed"].append({"predicate": name, "context": ctx})
    return bool(ok)

CASES = [(d, F(*pq)) for d in (1, 2, 3, 4, 5, 6, 7) for pq in ((1, 3), (3, 7), (9, 10), (1, 50))]
MMAX = 13
for d, p in CASES:
    q = 1-p; ctx = f"d={d},p={p}"; row = {"d": d, "p": str(p), "H1": 0 < p < 1 and d >= 1}
    P = law(d, p)
    maxlen = min(d+3, 9)
    row["P1"] = pred("P1", all(P(w) == P((0, *w))+P((1, *w)) == P((*w, 0))+P((*w, 1))
                     for n in range(0, maxlen) for w in product((0, 1), repeat=n)), ctx)
    row["P2"] = pred("P2", all(P(w) == bern(w, p) for n in range(1, d+1) for w in product((0, 1), repeat=n)), ctx)
    row["P2c"] = pred("P2c", any(P(w) != bern(w, p) for w in product((0, 1), repeat=d+1)), ctx)
    mem = lambda m: sum(P(w)*W(w) for w in product((0, 1), repeat=m-1))
    row["P3"] = pred("P3", all(mem(m) == iidS(m, p) for m in range(1, d+2)), ctx)
    gap = mem(d+2)-iidS(d+2, p)
    Emix = sum(bern(y, p)*mixed(y) for y in product((0, 1), repeat=d-1))
    row["gap"] = str(gap); row["P4"] = pred("P4", gap == p*q*Emix/(d+1) and gap > 0, ctx)
    row["P5"] = pred("P5", all(mixed(y) > 0 for y in product((0, 1), repeat=d-1)) and
                     mixed((0,)*(d-1)) == a(d)*F(d*d+d+1, 4*(d+1)*(d+2)), ctx)
    if d <= 4:
        ok6 = True; ok7 = True; ratios = {}
        for m in range(2, MMAX+1):
            sm = memS_dp(m, d, p); si = iidS_dp(m, p)
            if m <= 9: assert sm == mem(m) and si == iidS(m, p)
            lb = q**d*a(m)/(m-1)
            ok6 &= sm >= lb; ok7 &= sm >= si
            if m in (d+2, MMAX): ratios[m] = dict(mem=float(sm), iid=float(si), lower=float(lb))
        row["P6"] = pred("P6", ok6, ctx); row["P7_measured_mem_ge_iid_all_m"] = ok7; row["at_m"] = ratios
    res["cases"].append(row)

for p in (F(1, 3), F(1, 5), F(3, 7), F(2, 3)):
    q = 1-p; ind = iidS(4, p); lo, hi = -min(p*p, q*q), p*q; vals = []
    ok8 = ok9 = True
    for c0, c1 in product((lo, hi), repeat=2):
        T = {(x, b, z): bern((b,), p)*(bern((x, z), p)+(1 if x == z else -1)*(c0, c1)[b])
             for x, b, z in product((0, 1), repeat=3)}
        ok8 &= all(v >= 0 for v in T.values())
        s4 = sum(T[w]*W(w) for w in T); vals.append(s4)
        ok8 &= s4 == ind + F(7, 128)*q*c0 + F(1, 64)*p*c1
        pair = {w: bern(w, p) for w in product((0, 1), repeat=2)}
        for _ in range(6):
            new = {w: F(0) for w in pair}
            for (x, b), pr in pair.items():
                for z in (0, 1):
                    new[b, z] += pr*T[x, b, z]/(T[x, b, 0]+T[x, b, 1])
            ok9 &= new == {w: bern(w, p) for w in new}; pair = new
    Pm = law(2, p); reg = sum(Pm(w)*W(w) for w in product((0, 1), repeat=3))
    ctx = f"panel p={p}"
    row = dict(p=str(p), iid=str(ind), regen_d2=str(reg), min=str(min(vals)), max=str(max(vals)),
               P8=pred("P8", ok8, ctx), P9=pred("P9", ok9, ctx),
               regen_inside=pred("regen_inside", min(vals) <= reg <= max(vals), ctx))
    if p == F(1, 3):
        canc = ind + F(7, 128)*q*F(1, 126) + F(1, 64)*p*F(-1, 18)
        row["P10"] = pred("P10", (ind, reg, min(vals), max(vals), canc) ==
                          (F(37, 216), F(113, 648), F(1, 6), F(13, 72), F(37, 216)) and lo <= F(-1, 18), ctx)
    res["panel"].append(row)

for p, d in ((F(1, 3), 2), (F(1, 5), 2), (F(1, 2), 2), (F(1, 3), 4), (F(1, 10), 2)):
    q = 1-p; ind = iidS_dp(64, p); lb = q**d*a(64)/63
    row = dict(p=str(p), d=d, iid=f"{float(ind):.5g}", lower=f"{float(lb):.5g}",
               null_bound_lt_1_32000=6100*ind < F(1, 32000), exponent_gt_3=6100*lb > 3)
    if (p, d) == (F(1, 3), 2):
        row["P11"] = pred("P11", row["iid"] == "5.0454e-09" and row["lower"] == "0.00049655"
                          and row["null_bound_lt_1_32000"] and row["exponent_gt_3"], "design")
    res["design"].append(row)
res["counts"] = dict(cases=len(res["cases"]), qualify_H1=sum(r["H1"] for r in res["cases"]),
                     failed=len(res["failed"]))
with Path(sys.argv[1]).open("x") as f: json.dump(res, f, indent=1)
print(json.dumps(res["counts"]), json.dumps(res["failed"]))
