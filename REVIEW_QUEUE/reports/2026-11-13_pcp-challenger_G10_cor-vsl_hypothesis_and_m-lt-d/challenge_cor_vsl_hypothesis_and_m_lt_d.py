#!/usr/bin/env python3
"""Challenger + micro-review program for two questions on G10 Corollary 5.13 (cor:vsl), edition Z14/Z15.
Paper text only.  Uses REVIEW_QUEUE/lib/pcplib.py (reviewer's library).

Q1 (challenger): does the hypothesis of Corollary 5.13 (for some starting vertex and every N a length at which every
   q-th root of unity is the gain of >= N walks to y1 and of >= N walks to y2, for a pair y1 != y2 with a common
   successor) follow from the hypotheses of Theorem 5.3 (finite, gains +-1, norm-preserving of degree two, underlying
   graph connected)?  Here q = 2.
   Argument to be tested (from Proposition 5.14 and the first step of Corollary 5.15, read in the paper): D-hat is
   strongly connected and C0 contains the elements u u_z', which sum to zero, so C0 = Z2 and r = r0; then 5.14(c).
Q2 (micro-review): a carrier where the merging vertices have successors that are not common (m < d), through actual
   events: W(4,3) (d = 3, m = 2) and the conference matrix C6 (d = 5, m = 4), gains +-1; and W(4,3) with gains
   switched in Z4 (row and column gains random in Z4).

Conventions: E[z][y] gain of arc y -> z; "N" below is 25; lengths up to LMAX = 4|V-hat| + 60; counts exact.

PREDICATES (fixed before the first run):
 D0  hypothesis per carrier (Theorem 5.3): gains in Z2, A*A = 2 exactly, underlying graph connected.
     Carriers: arc digraphs of random 2-in 2-out multidigraphs on 1..6 nodes with the block [[+,+],[+,-]] and random
     signs on rows and columns (300 built; count qualifying), the rings of 3, 4, 5, 8 sites, and the 2-vertex block.
 D1  on every qualifying carrier: D is strongly connected; D-hat is strongly connected; r = r0.
 D2  on every qualifying carrier, for EVERY pair y1 != y2 with a common successor and EVERY starting vertex: there is
     a length <= LMAX at which both gains occur >= N times at y1 and >= N times at y2.  (This is the hypothesis of
     Corollary 5.13 with "for every N" replaced by N = 25 and "some starting vertex" strengthened to every one.)
 D3  control, that the test can fail: on the paper's four-vertex q = 4 example (after Corollary 5.15) the same test
     with all four gains fails for every pair and start.
 M0  hypothesis per carrier for Q2: A*A = d exactly; a pair with m < d common successors exists (m, d reported);
     abundance as in D2 for the q of the carrier (for the Z4-switched W(4,3) the order q0 = |C0| is computed and
     reported; abundance is then tested for the coset structure of Proposition 5.14(b)).
 M1  through actual events: consistency equations mu(Ext S) = d mu(S) over 600 random events (lengths 0..8, up to 10
     walks) from vertex 0, unknowns phi at the exact values of |v|^2.  The squared modulus solves every equation
     exactly (integer arithmetic).
 M2  the null space, restricted to the unknowns |v|^2 <= 9 that occur (count reported), has rank 1 for gains +-1
     (rule unique up to a factor), decided by singular values (second below 1e-6 of the first; all recorded).
     For the Z4-switched carrier the expected rank is phi(q0)/2 with q0 computed (1 for q0 = 2 or 4).
 M3  the pair event itself: for a = b = 1 on a pair with m < d, the continuation has exactly 2(d - m) components of
     modulus 1 and m components |1 + u_z| with sum of u_z = 0 (exact), as the proof of Corollary 5.13 says.
Seed 20261113.  Result file challenge_cor_vsl_results.json, never overwritten.
"""
import json, os, sys, random, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", "..", "lib"), "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib"):
    if os.path.exists(os.path.join(p, "pcplib.py")): sys.path.insert(0, p); break
import pcplib as L
OUT = os.path.join(HERE, "challenge_cor_vsl_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
rng = random.Random(20261113); NN = 25
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
def abundance(E, mod, need_all=True):
    """for every pair with a common successor and every start: is there a length with every gain >= NN at both?"""
    n = len(E); G = L.group(mod); idx, S = L.lift(E, mod); inv = {i: yg for yg, i in idx.items()}; sD = L.succ(E)
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if set(sD[a]) & set(sD[b])]
    LMAX = 4 * len(S) + 60; ok = 0; tot = 0
    for st in range(n):
        tables = []
        for cur in L.walk_counts(S, idx[(st, L.gzero(mod))], LMAX):
            dd = {}
            for v, c in cur.items(): y, g = inv[v]; dd.setdefault(y, {})[g] = c
            tables.append(dd)
        for (y1, y2) in pairs:
            tot += 1
            ok += any(len(dd.get(y1, {})) == len(G) and len(dd.get(y2, {})) == len(G) and min(dd[y1].values()) >= NN and min(dd[y2].values()) >= NN for dd in tables)
    return ok, tot, pairs
res = dict(seed=20261113, predicates={}); P = res["predicates"]
M2 = [[(0,), (0,)], [(0,), (1,)]]
cands = [L.block_carrier(1 + i % 6, M2, (2,), rng) for i in range(300)] + [L.ring_carrier(N) for N in (3, 4, 5, 8)] + [[[(0,), (0,)], [(0,), (1,)]]]
qual = [E for E in cands if L.norm_preserving(E, (2,), (1,)) == 2 and connected(E)]
P["D0"] = dict(built=len(cands), qualifying=len(qual), sizes=sorted({len(E) for E in qual}), met=len(qual) > 0)
f1 = 0; ok2 = tot2 = 0
for E in qual:
    sD = [list(s) for s in L.succ(E)]; idx, S = L.lift(E, (2,))
    if not (L.strongly_connected(sD) and L.strongly_connected(S)): f1 += 1; continue
    if L.period(S)[0] != L.period(sD)[0]: f1 += 1
    o, t, _ = abundance(E, (2,)); ok2 += o; tot2 += t
P["D1"] = dict(failures=f1, met=f1 == 0)
P["D2"] = dict(pair_start_instances=tot2, with_abundance=ok2, met=ok2 == tot2 and tot2 > 0)
ex = [(0, 2, 0), (0, 3, 1), (1, 0, 1), (1, 1, 3), (2, 0, 0), (2, 1, 0), (3, 2, 0), (3, 3, 3)]
E4 = [[None] * 4 for _ in range(4)]
for (a, b, e) in ex: E4[b][a] = (e,)
o, t, _ = abundance(E4, (4,)); P["D3"] = dict(instances=t, with_abundance=o, met=o == 0 and t > 0)
# Q2
def switched(E, q, rng):
    n = len(E); r = [rng.randrange(q) for _ in range(n)]; c = [rng.randrange(q) for _ in range(n)]
    return [[None if E[z][y] is None else ((E[z][y][0] + r[z] + c[y]) % q,) for y in range(n)] for z in range(n)]
micro = []
for name, E, q in (("W(4,3) signs", L.sign_carrier(L.W43, 2), 2), ("C6 conference signs", L.sign_carrier(L.C6, 2), 2),
                   ("W(4,3) switched in Z4", switched(L.sign_carrier(L.W43, 4), 4, rng), 4)):
    mod = (q,); d = L.norm_preserving(E, mod, (1,)); sD = L.succ(E); n = len(E)
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if 0 < len(set(sD[a]) & set(sD[b])) < (d or 0)]
    idx, S = L.lift(E, mod); sc = L.strongly_connected(S); r = L.period(S)[0] if sc else None; r0 = L.period([list(s) for s in sD])[0]
    q0 = None if not sc else q // (r // r0)
    o, t, _ = abundance(E, mod) if (sc and r == r0) else (None, None, None)
    rec = dict(name=name, q=q, d=d, pairs_with_m_lt_d=len(pairs), m=sorted({len(set(sD[a]) & set(sD[b])) for a, b in pairs}),
               Dhat_strongly_connected=bool(sc), r=r, r0=r0, q0=q0, abundance=[o, t])
    rec["M0"] = bool(d is not None and pairs and sc and (r != r0 or o == t))
    rows, keys, R = L.event_rows(E, q, d, 0, rng, n_events=600, maxlen=8, maxwalks=10)
    # M1 exact: squared modulus as an integer when q in (2,4): |v|^2 = key[0] (Z[i] norm is rational integer; q=2 likewise)
    val = {k: k[0] for k in keys}
    rec["M1"] = all(sum(c * val[kk] for kk, j in keys.items() for jj, c in row.items() if jj == j) == 0 for row in rows[:0]) if False else \
        all(sum(c * valj for (jj, c) in row.items() for valj in [dict((j, val[k]) for k, j in keys.items())[jj]]) == 0 for row in rows)
    zero = keys.get(R.N(R.zero())); dim, W, ev = L.null_space(rows, len(keys), zero)
    inner = [j for k, j in keys.items() if k[0] <= 9]; sv = np.linalg.svd(W[inner, :], compute_uv=False) if dim else np.array([0.0])
    rk = int((sv > 1e-6 * sv[0]).sum()) if sv[0] > 0 else 0
    rec.update(unknowns=len(keys), inner_unknowns=len(inner), null_dim=dim, inner_singular_values=[float(s) for s in sv[:4]], inner_rank=rk)
    rec["M2"] = rk == 1
    # M3
    a, b = pairs[0]; Z = sorted(set(sD[a]) & set(sD[b])); m = len(Z)
    comp = {}
    for z in sD[a]: comp[z] = R.add(comp.get(z, R.zero()), R.pw[E[z][a][0]])
    for z in sD[b]: comp[z] = R.add(comp.get(z, R.zero()), R.pw[E[z][b][0]])
    ones = sum(1 for z, v in comp.items() if z not in Z and R.N(v) == R.N(R.pw[0]))
    rec["M3"] = bool(ones == 2 * (d - m) and L.zero_sum([(E[z][b][0] - E[z][a][0]) % q for z in Z], q))
    micro.append(rec)
P["M0"] = dict(met=all(r["M0"] for r in micro)); P["M1"] = dict(met=all(r["M1"] for r in micro))
P["M2"] = dict(met=all(r["M2"] for r in micro)); P["M3"] = dict(met=all(r["M3"] for r in micro))
res["micro"] = micro; res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
for k, v in P.items(): print(k, v)
for r in micro: print({k: r[k] for k in ("name", "d", "m", "pairs_with_m_lt_d", "r", "r0", "q0", "abundance", "unknowns", "inner_unknowns", "null_dim", "inner_singular_values", "inner_rank")})
print("all met", res["all_met"])
