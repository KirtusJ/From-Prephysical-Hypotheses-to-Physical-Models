#!/usr/bin/env python3
"""Second follow-up.  K3b of followup_abund.py FAILED for q0 = 12 on the multisets with exponents (0,1,6,7), (0,2,6,8),
(0,4,6,10), (0,5,6,11): dimension 4 against 2 (kept).  The other eight multisets met it.

Two explanations are possible: (i) the box is still too small (Theorem 5.12 concerns all of R); (ii) the theorem fails
for these multisets.  They are separated as follows.

PREDICATE K3c (fixed before the run): for q0 = 12 and the multisets (0,1,6,7) and (0,2,6,8) (the other two are their
images under zeta -> zeta^5), with a AND b in {-2..2}^4 (390625 pairs), the solution space has dimension 2.
PREDICATE K3d (diagnostic, fixed before the run; evaluated whatever K3c gives): let W be the solution space found.
Every solution that is a polynomial of degree <= 4 in the four real coordinates of V restricted to the box norms ...
is not tested; instead: the two functions N_1, N_5 lie in W (residual below 1e-9), and if dim W > 2 the program
records, for a basis vector of W orthogonal to N_1 and N_5, the number of unknowns on which it is non-zero
(above 1e-8 of its maximum) and whether those unknowns include norms of elements with all coefficients in -1..1.
A solution supported only on norms that occur near the boundary of the box indicates (i).
Same rank rule as K3b.  Expected run time about two minutes per multiset (stated reason for exceeding the usual size:
the smaller box left the question open).  Result file followup_abund_2_results.json, never overwritten.
"""
import json, os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", "..", "lib"), "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib"):
    if os.path.exists(os.path.join(p, "pcplib.py")): sys.path.insert(0, p); break
import pcplib as L
OUT = os.path.join(HERE, "followup_abund_2_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
R = L.Ring(12); A = [tuple(t) for t in itertools.product(range(-2, 3), repeat=4)]
Ncache = {}
def N(a):
    if a not in Ncache: Ncache[a] = R.N(a)
    return Ncache[a]
out = []
for es in ((0, 1, 6, 7), (0, 2, 6, 8)):
    keys = {}; rows = set(); sh = {e: {b: R.mulz(b, e) for b in A} for e in set(es)}
    for a in A:
        for b in A:
            row = {}
            for e in es:
                j = keys.setdefault(N(R.add(a, sh[e][b])), len(keys)); row[j] = row.get(j, 0) + 1
            for t in (a, b):
                j = keys.setdefault(N(t), len(keys)); row[j] = row.get(j, 0) - 4
            rows.add(tuple(sorted((j, v) for j, v in row.items() if v)))
    rows.discard(()); n = len(keys); G = np.zeros((n, n))
    for row in rows:
        js = [j for j, _ in row]; vs = np.array([v for _, v in row], float); G[np.ix_(js, js)] += np.outer(vs, vs)
    G[keys[N(R.zero())], keys[N(R.zero())]] += 1
    ev, U = np.linalg.eigh(G); dim = int((ev < 1e-9 * ev[-1]).sum())
    vecs = {j: np.array([R.emb(k, j).real for k in sorted(keys, key=keys.get)]) for j in R.J}
    resid = {j: float(np.sqrt(max(vecs[j] @ G @ vecs[j], 0)) / np.linalg.norm(vecs[j])) for j in R.J}
    rec = dict(exps=list(es), unknowns=n, distinct_equations=len(rows), dim=dim, kept=float(ev[dim]) if dim < n else None,
               null_max=float(ev[dim - 1]) if dim else None, conjugate_rule_residuals=resid)
    if dim > 2:
        W = U[:, :dim]; Q, _ = np.linalg.qr(np.stack([vecs[j] for j in R.J], 1)); extra = W - Q @ (Q.T @ W)
        u, s, _ = np.linalg.svd(extra, full_matrices=False); v = u[:, 0]; sup = np.abs(v) > 1e-8 * np.abs(v).max()
        small = {N(t) for t in itertools.product(range(-1, 2), repeat=4)}
        inv = sorted(keys, key=keys.get)
        rec["extra"] = dict(support=int(sup.sum()), support_on_norms_of_small_elements=int(sum(1 for i in range(n) if sup[i] and inv[i] in small)), singular=[float(t) for t in s[:4]])
    out.append(rec)
res = dict(K3c=dict(cases=out, met=all(c["dim"] == 2 for c in out)), K3d=dict(met=all(max(c["conjugate_rule_residuals"].values()) < 1e-9 for c in out)))
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res, indent=0))
