#!/usr/bin/env python3
"""Challenger program for G10 Theorem 5.2 (label thm:power). Written from the paper text only.

Statement tested: D a gain digraph, gains of modulus one, A*A = d, d >= 2; two walks of equal
length from a common vertex end at distinct y1, y2 with a common successor.  Then
mu_p(S) = sum_y |v_S(y)|^p is consistent under continuation (mu_p(Ext S) = c mu_p(S) for all
events S, some c > 0) iff p = 2.

Conventions: A[z, y] = chi(gain of arc y -> z); v_ExtS = A v_S; a walk is a list of vertices;
gains are q-th roots of unity stored as exponents mod q; exact tests are done in Z[x]/(Phi_q).
Floating tolerance TOL = 1e-9: every float quantity is a sum of at most 2*d <= 60 terms, each at most
2^8 = 256 (p <= 8, moduli <= 2), so rounding is below 60*256*2.3e-16 < 4e-12; 1e-9 leaves a margin
of 250.  Strict inequalities are not decided by TOL: the smallest |gap| is recorded instead.

PREDICATES (fixed before the first run; none is edited afterwards):
 P1  hypothesis test, per carrier: A*A = d exactly (in Z[zeta_q]) and every column has d entries.
     Report number built / number qualifying.  Carriers that fail are excluded and counted.
 P2  hypothesis test, per carrier: a merging pair exists (two walks of equal length <= 6 from one
     vertex ending at y1 != y2 with a common successor).  Count qualifying.
 P3  on every qualifying (carrier, pair): mu_2(Ext S) = d * mu_2(S) exactly, S = {w1, w2}.
 P4  on every qualifying (carrier, pair), for every p in GRID_LOW = (1e-6, .25, .5, 1, 1.5, 1.9, 1.99):
     gap(p) = mu_p(Ext S) - d*mu_p(S) < 0; for every p in GRID_HIGH = (2.01, 2.1, 3, 4, 6, 8): gap(p) > 0.
     Recorded: the smallest |gap| over all instances and p (the separation).
 P5  the proof's two bounds hold on every instance within TOL:
     p<2: h(p) <= (1-p/2) h0 + p m ;  p>2: h(p) >= 2m + (p-2)(2m-h0)/2, with h, h0, m as in the proof,
     and sum_z u_z = 0 exactly (the orthogonality step).
 P6  single walks give c = d: for one walk w, mu_p(Ext{w}) = d for all p in both grids (within TOL).
 P7  abstract form of the convexity step, beyond realizable carriers: for 20000 random
     configurations (m in 2..9, unit u_z, sum u_z = 0 enforced by construction and re-tested
     per instance to 1e-12; count qualifying), h(p) - 2m < 0 on GRID_LOW and > 0 on GRID_HIGH.
 P8  the hypothesis is needed (paper's tree remark): on the directed binary tree of depth 7 with
     gains +1, restricted to events of length <= 6 from the root, mu_p(Ext S) = 2 mu_p(S) for all
     p in both grids, on 200 random events.  (Expected to HOLD; it is a check of the remark.)
 P9  boundary cases (micro-review): (a) d = 2 block [[1,1],[1,-1]]; (b) an instance with some
     u_z = -1 (h0 < m); (c) an instance with m < d; (d) an instance where every |1+u_z| = sqrt 2;
     each must exist among the instances and satisfy P4.  Report counts.
 P10 attempt at a counterexample by search: over all instances, the largest and smallest p in a
     fine grid (0.05 .. 8 step 0.05, excluding p=2) with |gap(p)| < TOL.  Predicate: none exists.
Seed 20261113.  Result file: challenge_thm_power_results.json (never overwritten).
"""
import json, os, sys, itertools, math, random
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenge_thm_power_results.json")
if os.path.exists(OUT):
    sys.exit("result file exists; refusing to overwrite")
random.seed(20261113); rng = np.random.default_rng(20261113)
TOL = 1e-9
GRID_LOW = (1e-6, .25, .5, 1, 1.5, 1.9, 1.99); GRID_HIGH = (2.01, 2.1, 3, 4, 6, 8)
x = symbols('x')
_phi = {}
def is_zero_cyc(coeffs, q):
    """coeffs[k] integer coefficient of zeta^k; exact test of sum = 0 in Z[zeta_q]."""
    if q not in _phi: _phi[q] = Poly(cyclotomic_poly(q, x), x)
    P = Poly(list(reversed([int(c) for c in coeffs])), x) if any(coeffs) else None
    if P is None: return True
    return P.rem(_phi[q]).is_zero

# a carrier: (name, q, E) with E[z][y] = exponent or None
def fourier(d, q, rho, kap):
    s = q // d
    return [[(rho[z] + kap[y] + s * z * y) % q for y in range(d)] for z in range(d)]
def from_signs(M, q):  # entries 0, +1, -1 ; q even
    return [[None if v == 0 else (0 if v == 1 else q // 2) for v in row] for row in M]
def switch(E, q, r, c):
    n = len(E)
    return [[None if E[z][y] is None else (E[z][y] + r[z] + c[y]) % q for y in range(n)] for z in range(n)]
def kron(E1, E2, q):
    n1, n2 = len(E1), len(E2)
    return [[None if (E1[a][c] is None or E2[b][e] is None) else (E1[a][c] + E2[b][e]) % q
             for c in range(n1) for e in range(n2)] for a in range(n1) for b in range(n2)]
def permute(E, perm):  # relabel rows: successor z -> perm[z]
    n = len(E); F = [[None] * n for _ in range(n)]
    for z in range(n):
        for y in range(n): F[perm[z]][y] = E[z][y]
    return F
W43 = [[0,1,1,1],[-1,0,1,-1],[-1,-1,0,1],[-1,1,-1,0]]
C6 = [[0,1,1,1,1,1],[1,0,1,-1,-1,1],[1,1,0,1,-1,-1],[1,-1,1,0,1,-1],[1,-1,-1,1,0,1],[1,1,-1,-1,1,0]]
W74c = [-1,1,1,0,1,0,0]
W74 = [[W74c[(j - i) % 7] for j in range(7)] for i in range(7)]
DELIBERATE_BAD = [[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,-1]]   # must be rejected by P1

carriers = []
for d in (2, 3, 4, 5, 6):
    for q in (d, 2 * d, 12 if 12 % d == 0 else 3 * d):
        for rep in range(3):
            rho = [random.randrange(q) for _ in range(d)]; kap = [random.randrange(q) for _ in range(d)]
            carriers.append((f"fourier d={d} q={q} #{rep}", q, fourier(d, q, rho, kap)))
for name, M in (("W(4,3)", W43), ("C6 conference", C6), ("W(7,4) circulant", W74), ("deliberately bad", DELIBERATE_BAD)):
    for q in (2, 4, 6, 10):
        E = from_signs(M, q)
        carriers.append((f"{name} q={q}", q, E))
        n = len(E)
        for rep in range(2):
            r = [random.randrange(q) for _ in range(n)]; c = [random.randrange(q) for _ in range(n)]
            perm = list(range(n)); random.shuffle(perm)
            carriers.append((f"{name} q={q} switched+permuted #{rep}", q, permute(switch(E, q, r, c), perm)))
H2 = [[0, 0], [0, 1]]  # exponents mod 2: [[1,1],[1,-1]]
carriers.append(("H2 block", 2, H2))
carriers.append(("H2 (x) W(4,3)", 2, kron(H2, from_signs(W43, 2), 2)))
carriers.append(("W(4,3) (x) W(4,3) q=4", 4, kron(from_signs(W43, 4), from_signs(W43, 4), 4)))
carriers.append(("fourier3 (x) H2 q=6", 6, kron(fourier(3, 6, [0, 1, 2], [3, 0, 5]), from_signs([[1, 1], [1, -1]], 6), 6)))
carriers.append(("fourier3 (x) W(4,3) q=6", 6, kron(fourier(3, 6, [0, 0, 0], [0, 0, 0]), from_signs(W43, 6), 6)))
# 8-cycle ring: signed arc digraph of a ring of 4 sites (text: "it holds on the ring")
def ring(N):
    idx = lambda s, t: 2 * (s % N) + t  # t=0 R, 1 L
    n = 2 * N; E = [[None] * n for _ in range(n)]
    for s in range(N):
        for t in (0, 1):
            E[idx(s + 1, 0)][idx(s, t)] = 0
            E[idx(s - 1, 1)][idx(s, t)] = 1 if t == 1 else 0
    return E
carriers.append(("signed arc digraph of ring N=5", 2, ring(5)))
carriers.append(("signed arc digraph of ring N=4", 2, ring(4)))

def check_norm_preserving(E, q):
    n = len(E); degs = set(sum(1 for z in range(n) if E[z][y] is not None) for y in range(n))
    if len(degs) != 1: return None
    d = degs.pop()
    for y1 in range(n):
        for y2 in range(y1 + 1, n):
            co = [0] * q
            for z in range(n):
                if E[z][y1] is not None and E[z][y2] is not None: co[(E[z][y2] - E[z][y1]) % q] += 1
            if not is_zero_cyc(co, q): return None
    return d

def find_pairs(E, q, maxlen=6, maxpairs=6):
    """merging pairs: (start, w1, w2) lists of vertices, equal length, distinct ends with a common successor."""
    n = len(E); succ = [[z for z in range(n) if E[z][y] is not None] for y in range(n)]
    res = []
    for start in range(n):
        walks = {start: [start]}  # one representative walk per end vertex at current length
        allw = [[start]]
        for L in range(1, maxlen + 1):
            allw = [w + [z] for w in allw for z in succ[w[-1]]]
            if len(allw) > 400: allw = random.sample(allw, 400)
            ends = {}
            for w in allw: ends.setdefault(w[-1], []).append(w)
            keys = sorted(ends)
            for y1, y2 in itertools.combinations(keys, 2):
                if set(succ[y1]) & set(succ[y2]):
                    res.append((random.choice(ends[y1]), random.choice(ends[y2])))
                    if len(res) >= maxpairs: return res
    return res

def gain_exp(E, q, w):
    return sum(E[w[i + 1]][w[i]] for i in range(len(w) - 1)) % q

def analyse(E, q, d, w1, w2):
    n = len(E); zeta = np.exp(2j * np.pi / q)
    a, b = gain_exp(E, q, w1), gain_exp(E, q, w2); y1, y2 = w1[-1], w2[-1]
    Z = [z for z in range(n) if E[z][y1] is not None and E[z][y2] is not None]; m = len(Z)
    # exact: sum u_z = 0 and mu_2(ExtS) = 2d
    co = [0] * q
    for z in Z: co[(b - a - E[z][y1] + E[z][y2]) % q] += 1
    sum_u_zero = is_zero_cyc(co, q)
    # mu_2(Ext S) - 2d = sum_{z in Z} 2 Re u_z  -> exact zero iff sum u + conj sum u = 0
    co2 = [0] * q
    for k in range(q): co2[k] += co[k]; co2[(-k) % q] += co[k]
    mu2_exact = is_zero_cyc(co2, q)
    # floats
    v = np.zeros(n, complex); v[y1] += zeta ** a; v[y2] += zeta ** b
    A = np.zeros((n, n), complex)
    for z in range(n):
        for y in range(n):
            if E[z][y] is not None: A[z, y] = zeta ** E[z][y]
    ext = np.abs(A @ v); ext[ext < 1e-13] = 0.0   # exact zeros: components are sums of <= 2 roots of unity
    u = np.array([zeta ** ((b - a - E[z][y1] + E[z][y2]) % q) for z in Z]); t = np.abs(1 + u); t[t < 1e-13] = 0.0
    h0 = int(np.sum(t > 0))
    def mu(vec, p): return float(np.sum(vec[vec > 0] ** p))
    gaps = {p: mu(ext, p) - d * 2.0 for p in GRID_LOW + GRID_HIGH}
    hval = {p: float(np.sum(t[t > 0] ** p)) for p in GRID_LOW + GRID_HIGH}
    bounds_ok = all(hval[p] <= (1 - p / 2) * h0 + p * m + TOL for p in GRID_LOW) and \
                all(hval[p] >= 2 * m + (p - 2) * (2 * m - h0) / 2 - TOL for p in GRID_HIGH)
    fine = [round(0.05 * k, 2) for k in range(1, 161) if k != 40]
    near = [p for p in fine if abs(mu(ext, p) - 2 * d) < TOL]
    single = np.abs(A[:, y1]); single_ok = all(abs(mu(single, p) - d) < TOL for p in GRID_LOW + GRID_HIGH)
    return dict(m=m, h0=h0, sum_u_zero=bool(sum_u_zero), mu2_exact=bool(mu2_exact), gaps=gaps,
                bounds_ok=bool(bounds_ok), near_zero_p=near, single_ok=bool(single_ok),
                all_sqrt2=bool(np.all(np.abs(t - math.sqrt(2)) < 1e-12)), len=len(w1) - 1)

res = dict(seed=20261113, predicates={}, carriers=[], notes=[])
n_built = len(carriers); n_np = 0; n_merge = 0; inst = []
for name, q, E in carriers:
    d = check_norm_preserving(E, q)
    rec = dict(name=name, q=q, n=len(E), d=d, norm_preserving=d is not None)
    if d is None or d < 2:
        rec["excluded"] = "hypothesis A*A=d, d>=2 not met"; res["carriers"].append(rec); continue
    n_np += 1
    pairs = find_pairs(E, q)
    rec["merging_pairs_found"] = len(pairs)
    if pairs: n_merge += 1
    rec["instances"] = []
    for w1, w2 in pairs:
        r = analyse(E, q, d, w1, w2); r["d"] = d; rec["instances"].append(r); inst.append(r)
    res["carriers"].append(rec)

P = res["predicates"]
bad_rejected = all(not c["norm_preserving"] for c in res["carriers"] if c["name"].startswith("deliberately bad"))
P["P1"] = dict(built=n_built, qualifying=n_np, deliberately_bad_rejected=bool(bad_rejected), met=bool(bad_rejected and n_np > 0))
P["P2"] = dict(norm_preserving=n_np, with_merging_pair=n_merge, instances=len(inst), met=n_merge > 0)
P["P3"] = dict(met=all(r["mu2_exact"] for r in inst), failures=sum(not r["mu2_exact"] for r in inst))
low_ok = all(r["gaps"][p] < 0 for r in inst for p in GRID_LOW); high_ok = all(r["gaps"][p] > 0 for r in inst for p in GRID_HIGH)
sep = min(abs(r["gaps"][p]) for r in inst for p in GRID_LOW + GRID_HIGH)
sep_no_tiny = min(abs(r["gaps"][p]) for r in inst for p in GRID_LOW[1:] + GRID_HIGH)
P["P4"] = dict(met=bool(low_ok and high_ok), smallest_abs_gap=sep, smallest_abs_gap_excluding_smallest_p=sep_no_tiny,
               note="gap at p=1e-6 tends to h0-2m+... , see instances")
P["P5"] = dict(met=all(r["bounds_ok"] and r["sum_u_zero"] for r in inst),
               sum_u_nonzero=sum(not r["sum_u_zero"] for r in inst), bound_failures=sum(not r["bounds_ok"] for r in inst))
P["P6"] = dict(met=all(r["single_ok"] for r in inst))
# P7
cnt = 0; qual = 0; fail7 = 0; minsep7 = 1e9
for _ in range(20000):
    m = int(rng.integers(2, 10)); parts = []; left = m
    while left > 0:
        k = int(rng.integers(2, min(left, 5) + 1)) if left >= 2 else 0
        if left - k == 1: k = left if left <= 5 else k + 1
        if k == 0: break
        th = rng.uniform(0, 2 * np.pi); parts += [np.exp(1j * (th + 2 * np.pi * i / k)) for i in range(k)]; left -= k
    u = np.array(parts); cnt += 1
    if len(u) != m or abs(u.sum()) > 1e-12: continue
    qual += 1; t = np.abs(1 + u); t = t[t > 1e-13]
    for p in GRID_LOW:
        g = float(np.sum(t ** p)) - 2 * m; minsep7 = min(minsep7, abs(g)); fail7 += g >= 0
    for p in GRID_HIGH:
        g = float(np.sum(t ** p)) - 2 * m; minsep7 = min(minsep7, abs(g)); fail7 += g <= 0
P["P7"] = dict(generated=cnt, qualifying=qual, sign_failures=int(fail7), smallest_abs_gap=minsep7, met=bool(fail7 == 0 and qual > 0))
# P8 binary tree depth 7
def tree_event_test():
    fails = 0
    for _ in range(200):
        L = random.randrange(0, 7); walks = set()
        for _ in range(random.randrange(1, 12)): walks.add(tuple(random.randrange(2) for _ in range(L)))
        # distinct walks end at distinct vertices: v_S has |S| components 1; Ext S has 2|S| components 1
        ext = {w + (b,) for w in walks for b in (0, 1)}
        for p in GRID_LOW + GRID_HIGH:
            if abs(len(ext) * 1.0 ** p - 2 * len(walks) * 1.0 ** p) > TOL: fails += 1
    return fails
f8 = tree_event_test(); P["P8"] = dict(failures=f8, met=f8 == 0, note="tree: A*A=2 because distinct vertices have disjoint successors; no merging pair")
# P9
ca = [r for c in res["carriers"] if c["name"] == "H2 block" for r in c.get("instances", [])]
cb = [r for r in inst if r["h0"] < r["m"]]; cc = [r for r in inst if r["m"] < r["d"]]; cd = [r for r in inst if r["all_sqrt2"]]
def ok4(rs): return all(all(r["gaps"][p] < 0 for p in GRID_LOW) and all(r["gaps"][p] > 0 for p in GRID_HIGH) for r in rs)
P["P9"] = dict(a_d2_block=len(ca), b_h0_lt_m=len(cb), c_m_lt_d=len(cc), d_all_sqrt2=len(cd),
               met=bool(all(len(s) > 0 for s in (ca, cb, cc, cd)) and ok4(ca) and ok4(cb) and ok4(cc) and ok4(cd)))
near = [(r["d"], r["m"], r["near_zero_p"]) for r in inst if r["near_zero_p"]]
P["P10"] = dict(instances_with_p_ne_2_and_gap_below_TOL=len(near), examples=near[:5], met=len(near) == 0)
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, sort_keys=True)
for k in sorted(P, key=lambda s: int(s[1:])): print(k, {a: b for a, b in P[k].items()})
print("all met:", res["all_met"])
