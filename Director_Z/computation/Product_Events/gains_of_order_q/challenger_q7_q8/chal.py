#!/usr/bin/env python3
"""Challenger program for THEOREM_Q.tex (one-site equation, gain of order q). Own program; paper text only.
Convention: m is a tuple of length q, m[j] = multiplicity of h^j; (Tm)[j] = m[(j-step) % q], step=1 unless
stated (remark (c): h of order r in cyclic C of order q, step=q/r). Box = simplex: unknowns on multisets of
size <= n, equations for all pairs (U,V) with |U|+|V| <= n (so all four arguments lie in the box).
Arithmetic: ranks modulo p=2^61-1 (exact), plus Fraction ranks on small cases. Sandwich: rank_p <= rank_Q, so
nullity_Q <= nullity_p; the claimed solutions (checked exactly in integers, P2) give nullity_Q >= claimed; if
nullity_p == claimed then nullity_Q == claimed exactly. No tolerance anywhere. Seed 20261114.

PREDICATES (fixed before first run):
P0  control: q=2, F=(u0-u1)^2 satisfies Eq0 for all U,V in {0..6}^2.  expect True.
P1  for q=1..8 and every n in 2..NMAX[q]: nullity of Eq0 (two unknown functions, F_R(0)=F_L(0)=0) on the simplex
    box n equals claimed (1 for q odd, 2 for q even). Computed in 'reduced' form (V=0 and U=0 instances, which
    are in the box, substituted exactly: F_L=F_R, F(Tm)=F(m)); P1x cross-checks reduced==full system on small cases
    and mod-p==Fraction on small cases.
P2  claimed solutions |m| and (q even) eps(m)^2 satisfy every in-box equation exactly; they are independent.
P3  stability: nullity is the same at the last three n for each q.
P4  drop normalization (F_R(0),F_L(0) free): nullity == claimed (expected to FAIL: predicted claimed+1).
P5  drop the instances with U=0 or V=0: nullity == claimed (outcome not predicted).
P5b (added after the probe run, whose result is kept as probe_result.json; prediction fixed before running it):
    in the P5 system, the null space restricted to multisets of size <= n-1 has dimension claimed+1
    (extra = F_R=+b, F_L=-b on nonzero multisets); the further dimension seen in P5 lives on the top size only.
P6  factor k in {1,3} instead of 2: nullity == 0 (outcome not predicted).
P7  impose F_R=F_L beforehand: nullity == claimed.
P8  theorem (ii): rings N=1..8 and line, q=1..8, random events (sets of walks from (0,R), equal length and
    mixed length), F=3|m|+5 eps^2 (q even) or 3|m| (q odd): mu(Ext S)==2 mu(S) exactly; and the multiset
    identities m_Ext(x+1,R)=U_x+V_x, m_Ext(x-1,L)=U_x+T V_x. Hypothesis: none; count of instances reported.
P8c negative controls (expected to FAIL): F=eps (not squared), q even; F=m[0] (q>=2).
P10 remark (c): h of order r<q, r|q, q<=8: nullity == k + [r even] k(k+1)/2, k=q/r, at n=4,5 (6 where cheap).
Failed predicates are kept in the result file. Result file is never overwritten.
"""
import sys, os, json, time, random, hashlib
from fractions import Fraction
from itertools import product
P = (1 << 61) - 1
NMAX = json.loads(os.environ.get("NMAX", '{"1":16,"2":14,"3":12,"4":10,"5":9,"6":8,"7":8,"8":8}'))

def multisets(q, n):
    """by[s] = list of tuples of length q with sum s, s=0..n"""
    by = [[] for _ in range(n + 1)]
    def rec(pref, left, pos):
        if pos == q - 1:
            for s in range(left + 1):
                by[sum(pref) + s].append(tuple(pref) + (s,))
            return
        for v in range(left + 1):
            rec(pref + [v], left - v, pos + 1)
    rec([], n, 0)
    for b in by: b.sort()
    return by

def Tm(m, step=1):
    q = len(m)
    return tuple(m[(j - step) % q] for j in range(q))
def add(a, b): return tuple(x + y for x, y in zip(a, b))

class Elim:
    def __init__(self, frac=False):
        self.piv = {}; self.frac = frac
    def insert(self, row):
        piv = self.piv
        if self.frac:
            while row:
                v = max(row)
                pr = piv.get(v)
                if pr is None:
                    c = row[v]; piv[v] = {k: x / c for k, x in row.items()}; return True
                c = row[v]
                for k, x in pr.items():
                    y = row.get(k, 0) - c * x
                    if y == 0: row.pop(k, None)
                    else: row[k] = y
            return False
        while row:
            v = max(row)
            pr = piv.get(v)
            if pr is None:
                inv = pow(row[v], P - 2, P); piv[v] = {k: x * inv % P for k, x in row.items()}; return True
            c = row[v]
            for k, x in pr.items():
                y = (row.get(k, 0) - c * x) % P
                if y == 0: row.pop(k, None)
                else: row[k] = y
        return False

def nullity(q, n, mode="reduced", step=1, free0=False, skip_zero=False, k=2, tie=False, frac=False):
    by = multisets(q, n)
    zero = (0,) * q
    idx = {}
    def canon(m):
        best = m; x = m
        while True:
            x = Tm(x, step)
            if x == m: break
            if x < best: best = x
        return best
    ccache = {}
    def var(side, m):
        if mode == "reduced":
            c = ccache.get(m)
            if c is None: c = ccache[m] = canon(m)
            key = c
        else:
            key = (0 if tie else side, m)
        if not free0 and m == zero: return None
        i = idx.get(key)
        if i is None: i = idx[key] = None
        return key
    # fixed variable numbering: by size then lexicographic
    num = {}
    for s in range(n + 1):
        for m in by[s]:
            if m == zero and not free0: continue
            if mode == "reduced":
                c = canon(m); ccache[m] = c
                if c not in num: num[c] = len(num)
            else:
                for side in ((0,) if tie else (0, 1)):
                    num[(side, m)] = len(num)
    E = Elim(frac); seen = set(); neq = 0; Etop = Elim(frac); topvars = set()
    if mode != "reduced":
        topvars = {i for key, i in num.items() if sum(key[1]) == n}
    for su in range(n + 1):
        for U in by[su]:
            for sv in range(n - su + 1):
                for V in by[sv]:
                    if skip_zero and (su == 0 or sv == 0): continue
                    row = {}
                    for side, m, c in ((0, add(U, V), 1), (1, add(U, Tm(V, step)), 1), (0, U, -k), (1, V, -k)):
                        key = var(side, m)
                        if key is None: continue
                        i = num[key]
                        row[i] = row.get(i, 0) + c
                    row = {i: c for i, c in row.items() if c != 0}
                    if not row: continue
                    sig = tuple(sorted(row.items()))
                    if sig in seen: continue
                    seen.add(sig); neq += 1
                    if frac: row = {i: Fraction(c) for i, c in row.items()}
                    else: row = {i: c % P for i, c in row.items()}
                    if topvars:
                        tr = {i: c for i, c in row.items() if i in topvars}
                        if tr: Etop.insert(tr)
                    E.insert(row)
    nul = len(num) - len(E.piv)
    return {"unknowns": len(num), "distinct_eqs": neq, "rank": len(E.piv), "nullity": nul,
            "restricted_nullity": nul - (len(topvars) - len(Etop.piv)) if topvars else None}

def eps(m): return sum((-1) ** j * x for j, x in enumerate(m))
def check_claimed(q, n):
    by = multisets(q, n); ok = True; cnt = 0
    fs = [lambda m: sum(m)] + ([lambda m: eps(m) ** 2] if q % 2 == 0 else [])
    for su in range(n + 1):
        for U in by[su]:
            for sv in range(n - su + 1):
                for V in by[sv]:
                    cnt += 1
                    for f in fs:
                        if f(add(U, V)) + f(add(U, Tm(V))) != 2 * f(U) + 2 * f(V): ok = False
    indep = True
    if q % 2 == 0:
        e1 = tuple(1 if j == 0 else 0 for j in range(q)); e1h = tuple(1 if j < 2 else 0 for j in range(q))
        indep = (sum(e1) * eps(e1h) ** 2 - sum(e1h) * eps(e1) ** 2) != 0
    return ok and indep, cnt

def walks_test(rng):
    """P8, P8c. Ring N (N=0 means line)."""
    out = {"instances": 0, "fail_mu": 0, "fail_ident": 0, "neg_eps_fail": 0, "neg_eps_inst": 0, "neg_m0_fail": 0, "neg_m0_inst": 0, "fails": []}
    for q in range(1, 9):
        for N in list(range(1, 9)) + [0]:
            for trial in range(6):
                mixed = trial >= 4
                S = set()
                for _ in range(rng.randint(1, 40)):
                    t = rng.randint(0, 9) if mixed else (trial + 1) * 2 - 1 + (trial % 2)
                    S.add("".join(rng.choice("RL") for _ in range(t)))
                def info(w):
                    pos = sum(1 if c == "R" else -1 for c in w); l = sum(1 for i in range(1, len(w)) if w[i] == "L" and w[i - 1] == "L")
                    if N: pos %= N
                    return (pos, w[-1] if w else "R"), l % q
                def ms(Sx):
                    d = {}
                    for w in Sx:
                        y, g = info(w); v = d.setdefault(y, [0] * q); v[g] += 1
                    return {y: tuple(v) for y, v in d.items()}
                Ext = {w + c for w in S for c in "RL"}
                assert len(Ext) == 2 * len(S)
                a, b = ms(S), ms(Ext); z = (0,) * q
                # identities
                okid = True; sites = {y[0] for y in a}
                want = {}
                for x in sites:
                    U = a.get((x, "R"), z); V = a.get((x, "L"), z)
                    xp, xm = (x + 1, x - 1) if not N else ((x + 1) % N, (x - 1) % N)
                    want[(xp, "R")] = add(U, V); want[(xm, "L")] = add(U, Tm(V))
                want = {y: m for y, m in want.items() if any(m)}
                if want != b: okid = False
                F = (lambda m: 3 * sum(m) + 5 * eps(m) ** 2) if q % 2 == 0 else (lambda m: 3 * sum(m))
                mu = lambda d, f: sum(f(m) for m in d.values())
                out["instances"] += 1
                if mu(b, F) != 2 * mu(a, F):
                    out["fail_mu"] += 1; out["fails"].append([q, N, trial])
                if not okid:
                    out["fail_ident"] += 1; out["fails"].append([q, N, trial, "ident"])
                if q % 2 == 0:
                    out["neg_eps_inst"] += 1
                    if mu(b, eps) != 2 * mu(a, eps): out["neg_eps_fail"] += 1
                if q >= 2:
                    out["neg_m0_inst"] += 1
                    f0 = lambda m: m[0]
                    if mu(b, f0) != 2 * mu(a, f0): out["neg_m0_fail"] += 1
    return out

def main():
    resfile = sys.argv[1]
    if os.path.exists(resfile): sys.exit("refusing to overwrite " + resfile)
    rng = random.Random(20261114)
    R = {"seed": 20261114, "p": P, "NMAX": NMAX, "failed_predicates": []}
    t0 = time.time()
    def fail(name, detail): R["failed_predicates"].append({"predicate": name, "detail": detail})
    R["P0"] = all((u0 + v0 - u1 - v1) ** 2 + (u0 + v1 - u1 - v0) ** 2 == 2 * (u0 - u1) ** 2 + 2 * (v0 - v1) ** 2
                  for u0, u1, v0, v1 in product(range(7), repeat=4))
    if not R["P0"]: fail("P0", "control")
    R["P1"] = {}; R["P2"] = {}; R["P3"] = {}
    for q in range(1, 9):
        claimed = 1 if q % 2 else 2; row = {}
        for n in range(2, NMAX[str(q)] + 1):
            r = nullity(q, n); r["claimed"] = claimed; r["box_contains_1"] = n >= q; row[n] = r
            if r["nullity"] != claimed: fail("P1", {"q": q, "n": n, "nullity": r["nullity"], "claimed": claimed})
            print("P1", q, n, r, round(time.time() - t0, 1), flush=True)
        R["P1"][q] = row
        nn = min(NMAX[str(q)], 7); ok, cnt = check_claimed(q, nn); R["P2"][q] = {"n": nn, "pairs": cnt, "ok": ok}
        if not ok: fail("P2", {"q": q})
        last = [row[n]["nullity"] for n in sorted(row)[-3:]]; R["P3"][q] = {"last3": last, "stable": len(set(last)) == 1}
        if len(set(last)) != 1: fail("P3", {"q": q, "last3": last})
    # cross-checks and variants on smaller boxes, full two-function system
    SM = {1: 8, 2: 7, 3: 6, 4: 5, 5: 5, 6: 4, 7: 4, 8: 4}
    R["P1x"] = {}; R["P4"] = {}; R["P5"] = {}; R["P6"] = {}; R["P7"] = {}; R["P5b"] = {}
    for q in range(1, 9):
        claimed = 1 if q % 2 else 2
        for n in sorted({SM[q] - 1, SM[q]}):
            key = "%d,%d" % (q, n)
            red = nullity(q, n)["nullity"]; full = nullity(q, n, mode="full")["nullity"]
            fr = nullity(q, n, mode="full", frac=True)["nullity"] if q <= 5 else None
            R["P1x"][key] = {"reduced": red, "full_modp": full, "full_fraction": fr}
            if red != full or (fr is not None and fr != full): fail("P1x", {"q": q, "n": n, "red": red, "full": full, "frac": fr})
            v = nullity(q, n, mode="full", free0=True)["nullity"]; R["P4"][key] = v
            if v != claimed: fail("P4", {"q": q, "n": n, "nullity": v, "claimed": claimed})
            rr = nullity(q, n, mode="full", skip_zero=True); v = rr["nullity"]; R["P5"][key] = v
            if v != claimed: fail("P5", {"q": q, "n": n, "nullity": v, "claimed": claimed})
            R["P5b"][key] = rr["restricted_nullity"]
            if rr["restricted_nullity"] != claimed + 1: fail("P5b", {"q": q, "n": n, "restricted": rr["restricted_nullity"], "claimed_plus_1": claimed + 1})
            for k in (1, 3):
                v = nullity(q, n, mode="full", k=k)["nullity"]; R["P6"][key + ",k=%d" % k] = v
                if v != 0: fail("P6", {"q": q, "n": n, "k": k, "nullity": v})
            v = nullity(q, n, mode="full", tie=True)["nullity"]; R["P7"][key] = v
            if v != claimed: fail("P7", {"q": q, "n": n, "nullity": v, "claimed": claimed})
            print("variants", key, R["P1x"][key], R["P4"][key], R["P5"][key], R["P7"][key], round(time.time() - t0, 1), flush=True)
    w = walks_test(rng); R["P8"] = w
    if w["fail_mu"] or w["fail_ident"]: fail("P8", w["fails"][:20])
    if w["neg_eps_fail"] == 0: fail("P8c", "negative control eps never failed")
    if w["neg_m0_fail"] == 0: fail("P8c", "negative control m0 never failed")
    R["P10"] = {}
    for q in range(2, 9):
        for r in range(1, q):
            if q % r: continue
            k = q // r; pred = k + (k * (k + 1) // 2 if r % 2 == 0 else 0)
            for n in ((4, 5, 6) if q <= 4 else (4, 5) if q <= 6 else (4,)):
                v = nullity(q, n, mode="full", step=q // r)["nullity"]
                R["P10"]["q=%d,r=%d,n=%d" % (q, r, n)] = {"nullity": v, "formula": pred}
                if v != pred: fail("P10", {"q": q, "r": r, "n": n, "nullity": v, "formula": pred})
        print("P10", q, round(time.time() - t0, 1), flush=True)
    with open(resfile, "x") as f: json.dump(R, f, indent=1, sort_keys=True)
    print("failed predicates:", len(R["failed_predicates"]))
    for x in R["failed_predicates"]: print("  ", json.dumps(x))
    print("elapsed", round(time.time() - t0, 1))
if __name__ == "__main__": main()
