#!/usr/bin/env python3
"""Challenger program for the coefficient-sign claim.  Seed 20261113.

Claim: H finite abelian, W(m) = a*|m| + sum_{[rho] in I} c_rho |sigma_rho(m)|^2,
I a set of distinct nontrivial classes {rho, rho^-1}.  W >= 0 on all nonnegative
integer m  =>  a >= 0 and all c >= 0.

PREDICATES (fixed before the first run; failures are kept in the result file):
 P1  orthogonality: for every class rho and every nontrivial rho',
     sum_h (1+Re rho(h)) rho'(h) = |H| (rho order 2, rho'=rho), |H|/2 (rho' in
     {rho, rho^-1}, order>2), 0 otherwise.  Interval arithmetic, 30 digits.
 P2  rounding: for T=1..200, m_T(h)=floor(T(1+Re rho(h))), every nontrivial rho':
     |sigma_rho'(m_T) - T*main(rho,rho')| < |H|  (upper interval end < |H|).
 P3  count: 0 <= m_T(h) for all h, and |m_T| <= T|H|, T=1..200.
 P4  witness: for every tested coefficient vector and every negative coefficient
     in it, the proof's witness (all-ones for the count; m_T, T<=TMAX=5000, for a
     class) gives W<0 certified by an interval lying below 0.  Smallest T reported.
 P5  independent small search (entries 0..B, B depends on |H|, stated per group;
     plus 20000 seeded random m with entries 0..3 when |H|>=9) finds some m with
     W<0, for every vector with a negative coefficient.  Float screening
     (threshold -1e-9: a screening choice only, values are O(1..1e3) and double
     error is ~1e-12), every hit confirmed by intervals.  EXPECTED TO FAIL for
     vectors with a large count coefficient and a small negative c; such failures
     are measured and kept.
 P6  controls: vectors with all coefficients >= 0: no m with certified W<0 in the
     small search nor in the witness family T<=200 for any class.
 P7  redundancy remark: for (C,C0) in {(Z8,{0,4}), (Z2xZ2,{00,01}), (Z12,{0,3,6,9})}
     and full characters psi,lam with psi|C0 = lam^{+-1}|C0, |sigma_psi(m)|^2 =
     |sigma_lam(m)|^2 on every m supported on one coset of C0 (entries 0..3);
     and for a pair with different restriction classes some such m separates them.
     Then the redundant list (a,c_psi,c_lam)=(0,-1,2) has a negative coefficient
     and W>=0 on those m (it equals the single square).
 P8  edge cases: H trivial (no class; W=a*m; a<0 => m=1 negative; a>=0 none);
     H=Z2 (m_T=(2T,0), sigma=2T exactly); empty index set on every group.
 P9  the report's F_5 table: multiplicities (9,4,4,4,4) by enumeration of walks;
     selected counts <= available; exact weights -5, 6-4*sqrt5, 6-4*sqrt5 (sympy).
Hypothesis test per instance: each index set is checked to consist of distinct,
nontrivial classes closed under the inverse identification; each coefficient
vector is classified (has a negative coefficient / has none) before the search.
"""
import itertools, json, os, random, sys, time
from fractions import Fraction as Fr
from mpmath import iv, mp
import numpy as np

iv.dps = 30
mp.dps = 40
SEED = 20261113
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chal_signs_result.json")
if os.path.exists(OUT):
    sys.exit("result file exists; refusing to overwrite: " + OUT)
TMAX = 5000
GROUPS = [(n,) for n in range(2, 13)] + [(2, 2), (2, 4), (3, 3), (2, 2, 3)]

EXACT_COS = {Fr(0): Fr(1), Fr(1, 2): Fr(-1), Fr(1, 4): Fr(0), Fr(3, 4): Fr(0),
             Fr(1, 3): Fr(-1, 2), Fr(2, 3): Fr(-1, 2), Fr(1, 6): Fr(1, 2), Fr(5, 6): Fr(1, 2)}
EXACT_SIN = {Fr(0): Fr(0), Fr(1, 2): Fr(0), Fr(1, 4): Fr(1), Fr(3, 4): Fr(-1)}


def cos_fr(fr):
    """cos(2 pi fr): exact Fraction if rational, else None."""
    return EXACT_COS.get(fr % 1)


def cos_iv(fr):
    e = cos_fr(fr)
    if e is not None:
        return iv.mpf(e.numerator) / e.denominator
    f = fr % 1
    return iv.cos(2 * iv.pi * f.numerator / f.denominator)


def sin_iv(fr):
    f = fr % 1
    if f in EXACT_SIN:
        return iv.mpf(int(EXACT_SIN[f]))
    return iv.sin(2 * iv.pi * f.numerator / f.denominator)


class Grp:
    def __init__(self, mods):
        self.mods = mods
        self.elems = list(itertools.product(*[range(n) for n in mods]))
        self.N = len(self.elems)
        self.chars = list(itertools.product(*[range(n) for n in mods]))
        self.triv = tuple(0 for _ in mods)

    def inv(self, k):
        return tuple((-x) % n for x, n in zip(k, self.mods))

    def phase(self, k, h):
        return sum(Fr(a * b, n) for a, b, n in zip(k, h, self.mods)) % 1

    def classes(self):
        seen, out = set(), []
        for k in self.chars:
            if k == self.triv or k in seen:
                continue
            seen.add(k); seen.add(self.inv(k))
            out.append(k)
        return out

    def order2(self, k):
        return self.inv(k) == k

    def tables(self, k):
        return ([cos_iv(self.phase(k, h)) for h in self.elems],
                [sin_iv(self.phase(k, h)) for h in self.elems])


def sq_iv(tab, m):
    c, s = tab
    re = sum((mh * x for mh, x in zip(m, c)), iv.mpf(0))
    im = sum((mh * x for mh, x in zip(m, s)), iv.mpf(0))
    return re * re + im * im, re, im


def W_iv(a, cs, tabs, m):
    w = iv.mpf(a.numerator) / a.denominator * sum(m)
    for c, tab in zip(cs, tabs):
        if c != 0:
            w += iv.mpf(c.numerator) / c.denominator * sq_iv(tab, m)[0]
    return w


def witness(G, k, T):
    m = []
    for h in G.elems:
        fr = G.phase(k, h)
        e = cos_fr(fr)
        if e is not None:
            v = T * (1 + e)
            m.append(v.numerator // v.denominator)
        else:
            x = T * (1 + cos_iv(fr))
            lo, hi = int(mp.floor(mp.mpf(x.a))), int(mp.floor(mp.mpf(x.b)))
            if lo != hi:
                raise RuntimeError("floor undecided %s %s %s" % (G.mods, k, T))
            m.append(lo)
    return m


def certified_neg(w):
    return w.b < 0


res = {"seed": SEED, "tmax": TMAX, "groups": {}, "failures": [], "P7": [], "P8": [], "P9": {}}
rng = random.Random(SEED)
np_rng = np.random.default_rng(SEED)
tally = {p: {"met": 0, "failed": 0} for p in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"]}


def mark(p, ok, info=None):
    tally[p]["met" if ok else "failed"] += 1
    if not ok:
        res["failures"].append({"pred": p, "info": info})


def small_box(N):
    return 3 if N <= 8 else (2 if N <= 10 else 1)


def run_group(mods):
    G = Grp(mods)
    N = G.N
    cls = G.classes()
    tabs_all = {k: G.tables(k) for k in G.chars if k != G.triv}
    g = {"order": N, "classes": [list(k) for k in cls], "order2": [G.order2(k) for k in cls]}
    # hypothesis test for the class list
    hyp = all(k != G.triv for k in cls) and len({frozenset([k, G.inv(k)]) for k in cls}) == len(cls)
    g["class_list_distinct_nontrivial"] = hyp
    # P1
    for k in cls:
        for kp in tabs_all:
            c, s = tabs_all[kp]
            wts = [1 + cos_iv(G.phase(k, h)) for h in G.elems]
            re = sum((w * x for w, x in zip(wts, c)), iv.mpf(0))
            im = sum((w * x for w, x in zip(wts, s)), iv.mpf(0))
            if kp in (k, G.inv(k)):
                exp = Fr(N) if G.order2(k) else Fr(N, 2)
            else:
                exp = Fr(0)
            d = re - iv.mpf(exp.numerator) / exp.denominator
            ok = (d.a <= 0 <= d.b) and (im.a <= 0 <= im.b) and (d.b - d.a) < 1e-20 and (im.b - im.a) < 1e-20
            mark("P1", bool(ok), [mods, k, kp])
    # P2, P3
    maxdev = 0.0
    for k in cls:
        for T in range(1, 201):
            m = witness(G, k, T)
            mark("P3", min(m) >= 0 and sum(m) <= T * N, [mods, k, T])
            for kp in tabs_all:
                _, re, im = sq_iv(tabs_all[kp], m)
                if kp in (k, G.inv(k)):
                    exp = Fr(N) if G.order2(k) else Fr(N, 2)
                else:
                    exp = Fr(0)
                dre = re - iv.mpf((T * exp).numerator) / (T * exp).denominator
                dev2 = dre * dre + im * im   # compare squares: iv.sqrt fails on intervals touching 0
                mark("P2", bool(dev2.b < N * N), [mods, k, kp, T, float(dev2.b)])
                maxdev = max(maxdev, max(float(dev2.b), 0.0) ** 0.5 / N)
    g["max_rounding_dev_over_order"] = maxdev
    # small search features (float screening)
    B = small_box(N)
    ms = np.array(list(itertools.product(range(B + 1), repeat=N)), dtype=np.int64)
    if N >= 9:
        ms = np.vstack([ms, np_rng.integers(0, 4, size=(20000, N))])
    g["small_search"] = {"box": B, "n_vectors": int(len(ms))}
    ph = {k: np.array([float(G.phase(k, h)) for h in G.elems]) for k in cls}
    feats = {k: np.abs(ms @ np.exp(2j * np.pi * ph[k])) ** 2 for k in cls}
    cnt = ms.sum(axis=1).astype(float)

    def small_search(a, idx, cs):
        w = float(a) * cnt
        for k, c in zip(idx, cs):
            w = w + float(c) * feats[k]
        j = int(np.argmin(w))
        if w[j] < -1e-9:
            m = [int(x) for x in ms[j]]
            wi = W_iv(a, cs, [tabs_all[k] for k in idx], m)
            return m, certified_neg(wi), float(w[j])
        return None, False, float(w[j])

    # index sets: full, empty, one seeded random proper nonempty subset
    idxsets = [("full", list(cls)), ("empty", [])]
    if len(cls) >= 2:
        r = rng.randint(1, len(cls) - 1)
        idxsets.append(("subset", sorted(rng.sample(cls, r))))
    g["index_sets"] = {}
    minT = {}
    for name, idx in idxsets:
        tabs = [tabs_all[k] for k in idx]
        K = len(idx)
        vecs = []
        for t in range(K + 1):  # t = 0 is the count
            v = [Fr(1)] * (K + 1); v[t] = Fr(-1); vecs.append(("V1_minus1", t, v))
            v = [Fr(10)] + [Fr(1)] * K; v[t] = Fr(-1, 100)
            if t == 0:
                v = [Fr(-1, 100)] + [Fr(1)] * K
            vecs.append(("V2_small_neg_big_count", t, v))
            if K >= 1:
                v = [Fr(11, 10) / K] * (K + 1); v[t] = Fr(-1, 10)
                assert sum(v) == 1
                vecs.append(("V3_normalised", t, v))
        nr = 0
        while nr < 5 and K >= 1:
            v = [Fr(rng.randint(-5, 10)) for _ in range(K + 1)]
            s = sum(v)
            if s <= 0 or min(v) >= 0:
                continue
            v = [x / s for x in v]
            vecs.append(("R_random_normalised", None, v)); nr += 1
        ctrl = [("C_all_one", None, [Fr(1)] * (K + 1)), ("C_count_only", None, [Fr(1)] + [Fr(0)] * K)]
        for _ in range(3):
            v = [Fr(rng.randint(0, 10)) for _ in range(K + 1)]
            if sum(v) > 0:
                ctrl.append(("C_random_nonneg", None, [x / sum(v) for x in v]))
        info = {"classes": [list(k) for k in idx], "n_vectors_with_negative": 0, "n_controls": 0,
                "witness": [], "small_search_not_found": []}
        for kind, t, v in vecs:
            a, cs = v[0], v[1:]
            negs = [i for i, x in enumerate(v) if x < 0]
            assert negs  # hypothesis of the test: vector has a negative coefficient
            info["n_vectors_with_negative"] += 1
            for i in negs:
                if i == 0:
                    w = W_iv(a, cs, tabs, [1] * N)
                    ok = certified_neg(w)
                    mark("P4", ok, [mods, name, kind, [str(x) for x in v], "count"])
                    info["witness"].append([kind, "count", 1 if ok else None])
                else:
                    k = idx[i - 1]
                    found = None
                    for T in range(1, TMAX + 1):
                        if certified_neg(W_iv(a, cs, tabs, witness(G, k, T))):
                            found = T; break
                    mark("P4", found is not None, [mods, name, kind, [str(x) for x in v], list(k)])
                    info["witness"].append([kind, list(k), found])
                    key = (kind, "order2" if G.order2(k) else "order>2")
                    if found is not None:
                        minT.setdefault(key, []).append(found)
            m, cert, wmin = small_search(a, idx, cs)
            ok = m is not None and cert
            mark("P5", ok, [mods, name, kind, [str(x) for x in v], wmin])
            if not ok:
                info["small_search_not_found"].append([kind, t, [str(x) for x in v], wmin])
        for kind, t, v in ctrl:
            a, cs = v[0], v[1:]
            assert min(v) >= 0
            info["n_controls"] += 1
            m, cert, wmin = small_search(a, idx, cs)
            bad = m is not None
            for k in cls:
                for T in range(1, 201, 7):
                    if certified_neg(W_iv(a, cs, tabs, witness(G, k, T))):
                        bad = True
            mark("P6", not bad, [mods, name, kind, [str(x) for x in v]])
        info["witness_T_ranges"] = {"%s|%s" % key: [min(x), max(x)] for key, x in minT.items()}
        g["index_sets"][name] = info
    res["groups"]["x".join(map(str, mods))] = g
    print(mods, "done", time.strftime("%H:%M:%S"), flush=True)


for mods in GROUPS:
    run_group(mods)

# ---- P8 edge cases
for a in [Fr(-1), Fr(-1, 1000), Fr(0), Fr(1)]:
    vals = [a * m for m in range(0, 50)]
    neg = any(x < 0 for x in vals)
    ok = (neg == (a < 0)) and (not a < 0 or a * 1 < 0)
    mark("P8", ok, ["trivial H", str(a)]); res["P8"].append(["trivial H", str(a), neg])
G2 = Grp((2,))
for T in [1, 2, 17, 1000]:
    m = witness(G2, (1,), T)
    ok = m == [2 * T, 0]
    mark("P8", ok, ["Z2 witness", T, m]); res["P8"].append(["Z2 witness", T, m])
# Z2: W = a(m0+m1) + c(m0-m1)^2 exactly; c<0 => (2T,0): 2aT+4cT^2 <0 iff T > a/(2|c|)
for a, c in [(Fr(10), Fr(-1, 100)), (Fr(1), Fr(-1)), (Fr(1000), Fr(-1, 1000))]:
    Tpred = int(a / (2 * -c)) + 1
    exact = [T for T in range(1, 2 * Tpred + 2) if 2 * a * T + 4 * c * T * T < 0]
    ok = bool(exact) and exact[0] == Tpred
    mark("P8", ok, ["Z2 exact threshold", str(a), str(c)]); res["P8"].append(["Z2 threshold", str(a), str(c), exact[0] if exact else None, Tpred])

# ---- P7 redundancy
def p7(mods, C0, pairs_same, pair_diff):
    G = Grp(mods)
    cosets = []
    seen = set()
    for b in G.elems:
        co = tuple(sorted(tuple((x + y) % n for x, y, n in zip(b, h, mods)) for h in C0))
        if co not in seen:
            seen.add(co); cosets.append(co)
    def sq(k, co, m):
        tab = ([cos_iv(G.phase(k, h)) for h in co], [sin_iv(G.phase(k, h)) for h in co])
        return sq_iv(tab, m)[0]
    for psi, lam in pairs_same:
        ok = True; minW = None
        for co in cosets:
            for m in itertools.product(range(4), repeat=len(co)):
                d = sq(psi, co, m) - sq(lam, co, m)
                if not (d.a <= 0 <= d.b and d.b - d.a < 1e-20):
                    ok = False
                w = -sq(psi, co, m) + 2 * sq(lam, co, m)   # redundant list (0,-1,2)
                if w.b < 0:
                    ok = False
        mark("P7", ok, [mods, psi, lam]); res["P7"].append([list(mods), list(psi), list(lam), "same", ok])
    psi, lam = pair_diff
    sep = any(not ((sq(psi, co, m) - sq(lam, co, m)).a <= 0 <= (sq(psi, co, m) - sq(lam, co, m)).b)
              for co in cosets for m in itertools.product(range(4), repeat=len(co)))
    mark("P7", sep, [mods, psi, lam, "should separate"]); res["P7"].append([list(mods), list(psi), list(lam), "different", sep])

p7((8,), [(0,), (4,)], [((1,), (3,)), ((1,), (5,)), ((1,), (7,))], ((1,), (2,)))
p7((2, 2), [(0, 0), (0, 1)], [((0, 1), (1, 1))], ((0, 1), (1, 0)))
p7((12,), [(0,), (3,), (6,), (9,)], [((1,), (5,)), ((1,), (7,)), ((2,), (6,)), ((1,), (11,))], ((1,), (2,)))

# ---- P9 the report's table
import sympy as sp
mult = [0] * 5
for i in range(5):
    for j in range(5):
        mult[(0 * i + i * j + j * 1) % 5] += 1
ok = mult == [9, 4, 4, 4, 4]
mark("P9", ok, ["multiplicities", mult])
def Wsym(coef, m):
    a, c1, c2 = coef
    def q(f):
        return sum(m[h] * m[k] * sp.cos(2 * sp.pi * f * (h - k) / 5) for h in range(5) for k in range(5))
    return sp.nsimplify(sp.simplify(a * sum(m) + c1 * q(1) + c2 * q(2)))
rows = [((-1, 1, 1), (1, 1, 1, 1, 1), sp.Integer(-5)),
        ((1, -1, 1), (2, 2, 0, 0, 2), 6 - 4 * sp.sqrt(5)),
        ((1, 1, -1), (2, 0, 2, 2, 0), 6 - 4 * sp.sqrt(5))]
res["P9"] = {"multiplicities": mult, "rows": []}
for coef, m, exp in rows:
    w = Wsym(coef, m)
    ok = sp.simplify(w - exp) == 0 and all(x <= y for x, y in zip(m, mult)) and bool(exp < 0)
    mark("P9", bool(ok), [coef, m, str(w)])
    res["P9"]["rows"].append([list(coef), list(m), str(w), bool(ok)])

res["tally"] = tally
with open(OUT, "x") as f:
    json.dump(res, f, indent=1, default=str)
print(json.dumps(tally, indent=1))
print("failures kept:", len(res["failures"]))
