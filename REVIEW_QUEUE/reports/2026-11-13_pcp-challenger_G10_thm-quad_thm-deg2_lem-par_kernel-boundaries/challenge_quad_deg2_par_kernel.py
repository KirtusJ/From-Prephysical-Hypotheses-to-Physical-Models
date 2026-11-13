#!/usr/bin/env python3
"""Challenger program for G10 Theorem 5.1 (thm:quad), Theorem 5.3 (thm:deg2), Lemma 5.4 (lem:par), and micro-review
of Theorem 5.8 (thm:kernel) at its boundaries.  Edition Z15 text, paper text only.  Uses REVIEW_QUEUE/lib/pcplib.py.

Conventions: E[z][y] gain of the arc y -> z; signed line = ring of 64 sites with walks of length <= 12 from (0,R),
which cannot wrap; vertex 2x+s, s = 0 for R; gain -1 on (x,L) -> (x-1,L).  Zero is counted as a non-negative integer
with phi(0) = 0 imposed.  Counting exact; ranks by singular values with the gap recorded.

PREDICATES (fixed before the first run):
 Q1  thm:quad, the proof's family: for a = 1..10 the event S of the a+1 walks with a steps right and one left has
     v_S = a at (a-1,R), 1 at (a-1,L), nothing else, and v_ExtS = a+1 at (a,R), a-1 at (a-2,L), nothing else. Exact.
 Q2  thm:quad "only if": equations mu(Ext S) = c mu(S) over 1500 random events (lengths 0..12, up to 14 walks) with
     c = 2; null space restricted to phi(n), n <= 6 has rank 1 and is proportional to n^2 (max deviation recorded,
     must be < 1e-8 relative; entries are O(1), eigenvector rounding ~1e-12).
 Q3  thm:quad, c: for c in (1, 1.5, 2.5, 3, 4) the same system has only the zero solution on the inner unknowns
     (rank 0), i.e. no rule with phi(1) != 0.  (Single walks already force c = 2; this is a check of that.)
 Q4  remark after thm:quad: with all gains +1 on the same digraph phi(t) = t solves the c = 2 system exactly.
 G0  thm:deg2 hypothesis per carrier: gains +-1, A*A = 2 exactly, underlying graph connected, finite.
     Carriers: 120 arc digraphs of random 2-in 2-out multidigraphs on 1..5 nodes with random signs; rings of 3..6 sites.
 G1  thm:deg2 proof steps on every qualifying carrier: strongly connected; in every block the two vertices lie in the
     same cyclic class of D; for n = 1..4 there is a length <= 40 with >= 2n-1 walks to x and >= 1 to x' (from vertex 0).
 G2  thm:deg2 conclusion through events: 500 random events from vertex 0 (lengths 0..10, up to 12 walks), c = 2:
     the inner null space (phi(n), n <= 4, restricted to those that occur; count reported) has rank 1 and is
     proportional to n^2.  Carriers where fewer than 4 inner unknowns occur are reported and not counted.
 G3  boundary: disconnected carrier (two disjoint 2-vertex blocks; hypothesis violated on purpose): recorded only.
 L1  lem:par on finite abelian groups Z_n (n = 1..12), Z2xZ2, Z2xZ4, Z3xZ3, Z4xZ4, Z2xZ2xZ2: exact rational null space
     (sympy) of the parallelogram law; for every basis solution f: f(0) = 0, f(-y) = f(y), f(2x) = 4 f(x),
     B symmetric, B(x,x) = f(x), B additive in the first argument.  The dimension of the solution space is reported
     per group (it may be zero; then the group is counted as vacuous).
 L2  lem:par on a box of Z^2 (f on {-6..6}^2, law imposed where all four points are in the box): every solution,
     restricted to {-2..2}^2, is a quadratic form (rank of inner null space = 3).
 K1  thm:kernel boundary d = 1, no two vertices with a common successor (directed cycle of 3, gains in Z3, each
     character): X(D) is the set of all characters; every event from a vertex has at most one walk; mu_f(S) = f(1);
     consistent with c = 1 for every kernel; conclusion of (ii) holds (every even real f is a combination of Re chi).
 K2  d = 1 with a merging pair (vertices 0,1 -> 2, 2 -> 0; gains trivial or in Z3): the hypothesis of (ii) FAILS
     (no start has walks of one length to both), X(D) is empty, yet mu_f with f(1) = 1 is consistent with c = 1:
     the conclusion of (ii) is false there, so the hypothesis is needed.  Expected; recorded PASS if so.
 K3  trivial group, d = 2, complete digraph with loops on 2 vertices: X(D) empty; hypothesis of (ii) holds; for
     f = 1 the rule (coincidence count) is not consistent for any c (single walks give c = 2, the pair event gives 3).
 K4  one vertex with one loop of gain g in Z4 (d = 1): no pairs; X(D) = all characters; mu_f(S) = f(1) for the one
     walk of each length; consistent with c = 1; conclusion of (ii) holds.
 K5  one vertex with a loop, trivial group: same, f constant.
Seed 20261113.  Result file challenge_quad_deg2_par_kernel_results.json, never overwritten.
"""
import json, os, sys, random, itertools
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", "..", "lib"), "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib"):
    if os.path.exists(os.path.join(p, "pcplib.py")): sys.path.insert(0, p); break
import pcplib as L
OUT = os.path.join(HERE, "challenge_quad_deg2_par_kernel_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
rng = random.Random(20261113); res = dict(seed=20261113, predicates={}); P = res["predicates"]
N = 64; E = L.ring_carrier(N); vid = lambda x, s: 2 * (x % N) + s
def vec(E, walks):
    v = {}
    for w in walks:
        g = sum(E[w[i + 1]][w[i]][0] for i in range(len(w) - 1)) % 2
        v[w[-1]] = v.get(w[-1], 0) + (1 if g == 0 else -1)
    return {k: x for k, x in v.items() if x}
def ext(E, walks): sD = L.succ(E); return [w + (z,) for w in walks for z in sD[w[-1]]]
ok = True
for a in range(1, 11):
    walks = []
    for pos in range(a + 1):
        steps = ['R'] * a; steps.insert(pos, 'L'); x = 0; w = [vid(0, 0)]
        for st in steps:
            x += 1 if st == 'R' else -1; w.append(vid(x, 0 if st == 'R' else 1))
        walks.append(tuple(w))
    ok &= vec(E, walks) == {vid(a - 1, 0): a, vid(a - 1, 1): 1} and vec(E, ext(E, walks)) == {k: v for k, v in {vid(a, 0): a + 1, vid(a - 2, 1): a - 1}.items() if v}
P["Q1"] = dict(met=bool(ok))
def solve(E, d, c, n_events, maxlen, maxwalks, inner_max, start=0, absval=False):
    sD = L.succ(E); rows = []; cols = {}
    for _ in range(n_events):
        Lw = rng.randrange(0, maxlen + 1); walks = set()
        for _ in range(rng.randrange(1, maxwalks + 1)):
            w = [start]
            for _ in range(Lw): w.append(rng.choice(sD[w[-1]]))
            walks.add(tuple(w))
        row = {}
        for val in vec(E, ext(E, list(walks))).values(): j = cols.setdefault(abs(val), len(cols)); row[j] = row.get(j, 0) + 1
        for val in vec(E, list(walks)).values(): j = cols.setdefault(abs(val), len(cols)); row[j] = row.get(j, 0) - c
        rows.append(row)
    n = len(cols); M = np.zeros((len(rows), n))
    for i, row in enumerate(rows):
        for j, v in row.items(): M[i, j] = v
    G = M.T @ M; ev, U = np.linalg.eigh(G); dim = int((ev < 1e-9 * ev[-1]).sum()); W = U[:, :dim]
    inner = sorted(k for k in cols if 1 <= k <= inner_max)
    if dim == 0: return dict(dim=0, inner=inner, rank=0, dev=None, exact_sq=None, exact_lin=None, sv=[])
    Wi = W[[cols[k] for k in inner], :]; sv = np.linalg.svd(Wi, compute_uv=False); rank = int((sv > 1e-6 * sv[0]).sum()) if sv[0] > 0 else 0
    dev = None
    if rank == 1:
        u = np.linalg.svd(Wi)[0][:, 0]; u = u / u[0] * inner[0] ** 2; dev = float(max(abs(u[i] - k * k) / (k * k) for i, k in enumerate(inner)))
    sq = np.array([float(k * k) for k in sorted(cols, key=cols.get)]); lin = np.array([float(k) for k in sorted(cols, key=cols.get)])
    return dict(dim=dim, inner=inner, rank=rank, dev=dev, exact_sq=float(np.abs(M @ sq).max()), exact_lin=float(np.abs(M @ lin).max()), sv=[float(s) for s in sv[:3]])
r = solve(E, 2, 2, 1500, 12, 14, 6); P["Q2"] = dict(result=r, met=bool(r["rank"] == 1 and r["dev"] is not None and r["dev"] < 1e-8 and len(r["inner"]) == 6 and r["exact_sq"] == 0))
q3 = {c: solve(E, 2, c, 600, 12, 14, 6)["rank"] for c in (1, 1.5, 2.5, 3, 4)}; P["Q3"] = dict(ranks=q3, met=all(v == 0 for v in q3.values()))
Eplus = [[None if v is None else (0,) for v in row] for row in E]; r4 = solve(Eplus, 2, 2, 600, 12, 14, 6)
P["Q4"] = dict(max_residual_of_phi_t=r4["exact_lin"], inner_rank=r4["rank"], met=r4["exact_lin"] == 0)
# deg2
def connected(E):
    n = len(E); adj = [set() for _ in range(n)]
    for z in range(n):
        for y in range(n):
            if E[z][y] is not None: adj[z].add(y); adj[y].add(z)
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for u in adj[v]:
            if u not in seen: seen.add(u); st.append(u)
    return len(seen) == n
M2 = [[(0,), (0,)], [(0,), (1,)]]
cands = [L.block_carrier(1 + i % 5, M2, (2,), rng) for i in range(120)] + [L.ring_carrier(k) for k in (3, 4, 5, 6)]
qual = [C for C in cands if L.norm_preserving(C, (2,), (1,)) == 2 and connected(C)]
P["G0"] = dict(built=len(cands), qualifying=len(qual), met=len(qual) > 0)
f1 = 0; g2_ok = g2_n = g2_short = 0; worst = 0.0
for C in qual:
    sD = [list(s) for s in L.succ(C)]; n = len(C)
    if not L.strongly_connected(sD): f1 += 1; continue
    r0, cls = L.period(sD); blocks = {}
    for y in range(n): blocks.setdefault(frozenset(sD[y]), []).append(y)
    if any(len(b) != 2 or cls[b[0]] != cls[b[1]] for b in blocks.values()): f1 += 1; continue
    wc = L.walk_counts(sD, 0, 40); good = True
    for b in blocks.values():
        for nn in range(1, 5):
            good &= any(cur.get(b[0], 0) >= 2 * nn - 1 and cur.get(b[1], 0) >= 1 for cur in wc)
    f1 += not good
    r = solve(C, 2, 2, 500, 10, 12, 4)
    if len(r["inner"]) < 4: g2_short += 1; continue
    g2_n += 1; okc = r["rank"] == 1 and r["dev"] is not None and r["dev"] < 1e-8 and r["exact_sq"] == 0; g2_ok += okc
    if r["dev"] is not None: worst = max(worst, r["dev"])
P["G1"] = dict(failures=f1, met=f1 == 0)
P["G2"] = dict(counted=g2_n, met_on=g2_ok, not_counted_too_few_inner_unknowns=g2_short, worst_relative_deviation=worst, met=g2_ok == g2_n and g2_n > 0)
two = [[None] * 4 for _ in range(4)]
for off in (0, 2):
    two[off][off] = (0,); two[off + 1][off] = (0,); two[off][off + 1] = (0,); two[off + 1][off + 1] = (1,)
r = solve(two, 2, 2, 400, 10, 12, 4); P["G3"] = dict(connected=connected(two), inner_rank=r["rank"], dev=r["dev"], met=True, note="hypothesis violated on purpose; recorded only")
# lem:par exact
def par_group(mod):
    G = L.group(mod); ix = {g: i for i, g in enumerate(G)}; rows = []
    for x in G:
        for y in G:
            row = [0] * len(G); row[ix[L.gadd(x, y, mod)]] += 1; row[ix[L.gsub(x, y, mod)]] += 1; row[ix[x]] -= 2; row[ix[y]] -= 2; rows.append(row)
    ns = sp.Matrix(rows).nullspace(); bad = 0
    for v in ns:
        f = {g: v[ix[g]] for g in G}; B = lambda x, y: sp.Rational(1, 4) * (f[L.gadd(x, y, mod)] - f[L.gsub(x, y, mod)])
        z = L.gzero(mod)
        ok = f[z] == 0 and all(f[L.gneg(y, mod)] == f[y] for y in G) and all(f[L.gadd(x, x, mod)] == 4 * f[x] for x in G)
        ok &= all(B(x, y) == B(y, x) for x in G for y in G) and all(B(x, x) == f[x] for x in G)
        ok &= all(B(L.gadd(u, w, mod), y) == B(u, y) + B(w, y) for u in G for w in G for y in G)
        bad += not ok
    return len(ns), bad
l1 = {}
for mod in [(n,) for n in range(1, 13)] + [(2, 2), (2, 4), (3, 3), (4, 4), (2, 2, 2)]:
    l1[str(mod)] = par_group(mod)
P["L1"] = dict(dimension_and_failures=l1, nonvacuous_groups=sum(1 for d, b in l1.values() if d > 0), met=all(b == 0 for d, b in l1.values()) and any(d > 0 for d, b in l1.values()))
pts = list(itertools.product(range(-6, 7), repeat=2)); ix = {p: i for i, p in enumerate(pts)}; rows = []
for x in pts:
    for y in pts:
        a = (x[0] + y[0], x[1] + y[1]); b = (x[0] - y[0], x[1] - y[1])
        if a in ix and b in ix:
            row = {}
            for k, c in ((a, 1), (b, 1), (x, -2), (y, -2)): row[ix[k]] = row.get(ix[k], 0) + c
            rows.append(row)
dim, W, ev = L.null_space(rows, len(pts)); inner = [ix[p] for p in itertools.product(range(-2, 3), repeat=2)]
sv = np.linalg.svd(W[inner, :], compute_uv=False); rk = int((sv > 1e-6 * sv[0]).sum())
quad = np.stack([[p[0] ** 2, p[0] * p[1], p[1] ** 2] for p in itertools.product(range(-2, 3), repeat=2)]).astype(float)
Qm, _ = np.linalg.qr(quad); resid = float(np.linalg.norm(W[inner, :] - Qm @ (Qm.T @ W[inner, :])))
P["L2"] = dict(null_dim_on_box=dim, inner_rank=rk, residual_outside_quadratic_forms=resid, met=rk == 3 and resid < 1e-8)
# kernel boundaries (exact, small)
def mu(E, mod, walks, f):
    tot = 0
    for w in walks:
        for w2 in walks:
            if w[-1] == w2[-1]:
                g1 = L.gzero(mod); g2 = L.gzero(mod)
                for i in range(len(w) - 1): g1 = L.gadd(g1, E[w[i + 1]][w[i]], mod)
                for i in range(len(w2) - 1): g2 = L.gadd(g2, E[w2[i + 1]][w2[i]], mod)
                tot += f[L.gsub(g2, g1, mod)]
    return tot
def all_events_consistent(E, mod, f, c, maxlen=4):
    sD = L.succ(E)
    for st in range(len(E)):
        ws = [(st,)]
        for Lw in range(maxlen):
            for k in range(1, min(len(ws), 3) + 1):
                for S in itertools.combinations(ws, k):
                    if mu(E, mod, [w + (z,) for w in S for z in sD[w[-1]]], f) != c * mu(E, mod, list(S), f): return False
            ws = [w + (z,) for w in ws for z in sD[w[-1]]]
    return True
def XD(E, mod): return [k for k in L.group(mod) if L.norm_preserving(E, mod, k) is not None]
K = {}
cyc = [[None] * 3 for _ in range(3)]
for y in range(3): cyc[(y + 1) % 3][y] = (rng.randrange(3),)
f = {(0,): sp.Rational(3), (1,): sp.Rational(-7, 2), (2,): sp.Rational(-7, 2)}
K["K1 d=1 cycle, Z3: X(D) all characters; arbitrary even kernel consistent with c=1"] = len(XD(cyc, (3,))) == 3 and all_events_consistent(cyc, (3,), f, 1)
mer = [[None] * 3 for _ in range(3)]; mer[2][0] = (0,); mer[2][1] = (1,); mer[0][2] = (2,)
K["K2 d=1 merging pair: X(D) empty, no common-length walks to both, yet f(1)=1 kernel consistent with c=1"] = \
    len(XD(mer, (3,))) == 0 and all_events_consistent(mer, (3,), {(0,): 1, (1,): 5, (2,): 5}, 1) and \
    all(not (0 in {w[-1] for w in ws} and 1 in {w[-1] for w in ws}) for st in range(3) for ws in [[(st,)]] + [[]] if ws) 
K2b = True
for st in range(3):
    cur = {st}
    for _ in range(12):
        K2b &= not ({0, 1} <= cur); cur = {z for y in cur for z in L.succ(mer)[y]}
K["K2b no start reaches both merging vertices at one length (12 lengths)"] = K2b
full = [[(0,), (0,)], [(0,), (0,)]]
c_single = 2; pair = [(0, 0), (0, 1)]
K["K3 trivial group, d=2: X(D) empty; coincidence count: single walk forces c=2, pair event gives ratio 3"] = \
    len(XD(full, (1,))) == 0 and mu(full, (1,), [w + (z,) for w in pair for z in (0, 1)], {(0,): 1}) == 3 * mu(full, (1,), pair, {(0,): 1}) and \
    mu(full, (1,), [(0, 0), (0, 1)], {(0,): 1}) == 2 * mu(full, (1,), [(0,)], {(0,): 1})
loop = [[(1,)]]
K["K4 one vertex, loop gain 1 in Z4: X(D) all four characters; any even kernel consistent with c=1"] = len(XD(loop, (4,))) == 4 and all_events_consistent(loop, (4,), {(0,): 2, (1,): -1, (2,): 7, (3,): -1}, 1)
K["K5 one vertex, loop, trivial group: consistent with c=1"] = len(XD([[(0,)]], (1,))) == 1 and all_events_consistent([[(0,)]], (1,), {(0,): 5}, 1)
P["K"] = dict(cases={k: ("PASS" if v else "FAIL") for k, v in K.items()}, met=all(K.values()))
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
for k, v in P.items(): print(k, str(v)[:600])
print("all met", res["all_met"])
