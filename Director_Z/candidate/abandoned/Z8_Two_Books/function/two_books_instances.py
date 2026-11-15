"""Candidate Z8 "Two Books": exact instances. STIPULATED CANDIDATE FOR DISPROOF; nothing here is a claim about the world.

Signed two-rail carrier (gain -1 on a left step that follows a left step), walks from (0,R), line (N = None) or ring.
At a vertex v after an event: eps(v) the signed sum, n(v) the number of walks. Book of chance: p(v) = eps(v)^2 / sum.
Book of heat: S(v) = log n(v). H = sum_v p(v) S(v).
PREDICATES fixed before the first run (15 November 2026):
 G1  (the theorem, exhaustively) for EVERY sequence of non-empty masks of length L <= Lmax on rings of 3, 4, 5 sites
     (Lmax = 5, 4, 3) with non-zero total weight, one free step does not lower H: the exact inequality
     prod over sites (n_R + n_L)^(w_R + w_L) >= prod n_R^(w_R) * n_L^(w_L)  (integers; w = eps^2), which is
     H(after) >= H(before) with both sides multiplied by the total weight and exponentiated; no logarithm is used.
 G2  equality in G1 holds exactly when every site with non-zero weight has all its weight on a rail that carries all
     the walks of the site, or, with weight on both rails, never (reported: the number of equality cases and whether
     each has, at every site of non-zero weight, the other rail empty of walks or of weight as stated in FORM T2).
 G3  additivity: for two events with weights and counts (w, n), (w', n'), H of the product event is H + H'
     (checked as an identity of exact fractions of logarithm coefficients on 200 random pairs from the exhaustive set).
 G4  a mask can lower H: at least one event and one further mask (not all sites) with H(after) < H(before) exists
     in the exhaustive set (so the law is about free continuation only).
Reported, no predicate: H(T) and T*log 2 - H(T) on the line for T = 1..64 (60-digit decimals).
Usage: python3 two_books_instances.py RESULT.json  (refuses to overwrite). Seed 20261115 for G3."""
import sys, os, json, itertools, random, collections
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
getcontext().prec = 60
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def stepf(st, N, mask=None):
    new = {}
    for (x, r), (sg, n) in st.items():
        for y, r2, flip in (((x + 1) if N is None else (x + 1) % N, 0, 1), ((x - 1) if N is None else (x - 1) % N, 1, -1 if r == 1 else 1)):
            if mask is not None and y not in mask: continue
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + sg * flip, b + n)
    return new
def sides(st):
    """integers (lhs, rhs) with lhs >= rhs  <=>  H(after one free step) >= H(before)."""
    by = collections.defaultdict(lambda: [(0, 0), (0, 0)])
    for (x, r), v in st.items(): by[x][r] = v
    lhs = rhs = 1; eq_ok = True
    for x, ((eR, nR), (eL, nL)) in by.items():
        wR, wL = eR * eR, eL * eL
        lhs *= (nR + nL) ** (wR + wL)
        rhs *= (nR ** wR if nR else 1) * (nL ** wL if nL else 1)
        if wR + wL and not ((wL == 0 and nL == 0) or (wR == 0 and nR == 0)): eq_ok = False
    return lhs, rhs, eq_ok
def Hlog(st):
    tot = sum(s * s for s, n in st.values())
    return {n: Fr(sum(s * s for s, m in st.values() if m == n), tot) for n in {n for s, n in st.values() if s}}   # coefficients of log n
rep = {"argv": sys.argv[1:]}
g1_cases = g1_fail = g2_eq = g2_bad = 0; pool = []; g4 = None
for N, Lmax in ((3, 5), (4, 4), (5, 3)):
    masks = [set(c) for k in range(1, N + 1) for c in itertools.combinations(range(N), k)]
    def rec(st, depth):
        global g1_cases, g1_fail, g2_eq, g2_bad, g4
        if depth and any(s for s, n in st.values()):
            lhs, rhs, eq_ok = sides(st); g1_cases += 1
            if lhs < rhs: g1_fail += 1
            if lhs == rhs:
                g2_eq += 1
                if not eq_ok: g2_bad += 1
            elif eq_ok: g2_bad += 1
            if len(pool) < 4000: pool.append(st)
            if g4 is None:
                for m in masks[:-1]:
                    nx = stepf(st, N, m)
                    if nx and any(s for s, n in nx.values()):
                        a, b = Hlog(st), Hlog(nx)
                        ha = sum(float(c) * __import__("math").log(n) for n, c in a.items()); hb = sum(float(c) * __import__("math").log(n) for n, c in b.items())
                        if hb < ha - 1e-9: g4 = {"N": N, "length": depth, "mask": sorted(m), "H_before": ha, "H_after": hb}; break
        if depth == Lmax: return
        for m in masks:
            nx = stepf(st, N, m)
            if nx: rec(nx, depth + 1)
    rec({(0, 0): (1, 1)}, 0)
rng = random.Random(20261115); g3_fail = 0
for _ in range(200):
    A, B = rng.choice(pool), rng.choice(pool); a, b = Hlog(A), Hlog(B)
    # product event: vertices (v, v'), weight w w', count n n'; H = sum p p' (log n + log n'): coefficients of log n are a, of log n' are b
    wa = sum(s * s for s, n in A.values()); wb = sum(s * s for s, n in B.values())
    coef = collections.defaultdict(Fr)
    for (s, n) in A.values():
        for (s2, n2) in B.values():
            if s and s2: coef[("A", n)] += Fr(s * s * s2 * s2, wa * wb); coef[("B", n2)] += Fr(s * s * s2 * s2, wa * wb)
    if any(coef[("A", n)] != c for n, c in a.items()) or any(coef[("B", n)] != c for n, c in b.items()): g3_fail += 1
line = []; st = {(0, 0): (1, 1)}; ln2 = Decimal(2).ln()
for T in range(1, 65):
    st = stepf(st, None); tot = sum(s * s for s, n in st.values())
    h = sum((Decimal(s * s) / Decimal(tot)) * Decimal(n).ln() for s, n in st.values() if s)
    line.append([T, str(h)[:24], str(T * ln2 - h)[:24]])
rep.update({"G1": {"cases": g1_cases, "failures": g1_fail}, "G2": {"equality_cases": g2_eq, "mismatches_with_the_stated_condition": g2_bad},
            "G3": {"pairs": 200, "failures": g3_fail}, "G4": g4, "line": line,
            "predicates": {"G1": g1_fail == 0, "G2": g2_bad == 0, "G3": g3_fail == 0, "G4": g4 is not None}})
json.dump(rep, open(OUT, "x"), indent=1); print(rep["predicates"], rep["G1"], rep["G2"], g4); print(line[7], line[31], line[63])
