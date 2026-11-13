#!/usr/bin/env python3
"""Follow-up to three FAILED predicates of challenge_quad_deg2_par_kernel.py (kept, not edited).  All three failed
through the reviewer's expectations, none through the paper:
 Q2 required six inner unknowns phi(1..6); the 1500 sampled events reached moduli 1..5 only (rank 1, n^2 to 3e-15).
 L1 required a finite group with a non-zero solution of the parallelogram law; there is none (f(nx) = n^2 f(x) and
    nx = 0 force f = 0), so on finite groups the lemma is vacuous.  L2 (a box of Z^2) is the non-vacuous test.
 K3 expected the ratio 3 for the pair event on the complete two-vertex digraph with trivial group; the reviewer's
    arithmetic was wrong: mu(S) = 2 and mu(Ext S) = 2 * 2^2 = 8.

PREDICATES (fixed before this run):
 Q2b thm:quad on the signed line with events built to reach larger moduli: 1500 random events of lengths 6..12 with
     up to 60 walks; the inner null space on phi(n), 1 <= n <= 8, all eight occurring, has rank 1 and equals n^2 to 1e-8.
 L1b on every group of L1 the solution space of the parallelogram law is {0} (dimension 0), exact.
 K3b trivial group, complete digraph with loops on two vertices: mu(Ext{w}) = 2 mu({w}) for a single walk and
     mu(Ext S) = 4 mu(S) for S = {0->0, 0->1}; hence no factor c is consistent for the constant kernel.
Seed 20261114 (a new seed: this is a new sample).  Result file followup_z13_results.json, never overwritten.
"""
import json, os, sys, random
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "followup_z13_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
for p in (os.path.join(HERE, "..", "..", "lib"), "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib"):
    if os.path.exists(os.path.join(p, "pcplib.py")): sys.path.insert(0, p); break
import pcplib as L
rng = random.Random(20261114); E = L.ring_carrier(64); sD = L.succ(E)
def vec(walks):
    v = {}
    for w in walks:
        g = sum(E[w[i + 1]][w[i]][0] for i in range(len(w) - 1)) % 2; v[w[-1]] = v.get(w[-1], 0) + (1 if g == 0 else -1)
    return v
rows = []; cols = {}
for _ in range(1500):
    Lw = rng.randrange(6, 13); walks = set()
    for _ in range(rng.randrange(1, 61)):
        w = [0]
        for _ in range(Lw): w.append(rng.choice(sD[w[-1]]))
        walks.add(tuple(w))
    row = {}
    for val in vec([w + (z,) for w in walks for z in sD[w[-1]]]).values():
        if val: j = cols.setdefault(abs(val), len(cols)); row[j] = row.get(j, 0) + 1
    for val in vec(walks).values():
        if val: j = cols.setdefault(abs(val), len(cols)); row[j] = row.get(j, 0) - 2
    rows.append(row)
dim, W, ev = L.null_space(rows, len(cols)); inner = [k for k in range(1, 9) if k in cols]
Wi = W[[cols[k] for k in inner], :]; sv = np.linalg.svd(Wi, compute_uv=False); rank = int((sv > 1e-6 * sv[0]).sum())
u = np.linalg.svd(Wi)[0][:, 0]; u = u / u[0]; dev = float(max(abs(u[i] - k * k) / (k * k) for i, k in enumerate(inner)))
res = dict(Q2b=dict(inner=inner, null_dim=dim, rank=rank, dev=dev, largest_modulus=max(cols), met=bool(inner == list(range(1, 9)) and rank == 1 and dev < 1e-8)))
old = json.load(open(os.path.join(HERE, "challenge_quad_deg2_par_kernel_results.json")))
dims = {k: v[0] for k, v in old["predicates"]["L1"]["dimension_and_failures"].items()}
res["L1b"] = dict(dimensions=dims, met=all(v == 0 for v in dims.values()), note="read from the first run's exact null spaces (sympy)")
def coincidence(walks):
    ends = {}
    for w in walks: ends[w[-1]] = ends.get(w[-1], 0) + 1
    return sum(c * c for c in ends.values())
S1 = [(0,)]; S2 = [(0, 0), (0, 1)]; ext = lambda S: [w + (z,) for w in S for z in (0, 1)]
res["K3b"] = dict(single=[coincidence(S1), coincidence(ext(S1))], pair=[coincidence(S2), coincidence(ext(S2))],
                  met=coincidence(ext(S1)) == 2 * coincidence(S1) and coincidence(ext(S2)) == 4 * coincidence(S2))
res["all_met"] = all(v["met"] for v in res.values())
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res))
