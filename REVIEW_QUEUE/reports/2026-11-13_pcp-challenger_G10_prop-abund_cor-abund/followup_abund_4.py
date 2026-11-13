#!/usr/bin/env python3
"""Fourth follow-up.  K3e of followup_abund_3.py FAILED (dimension 4 for all three boxes; kept).

An exploratory script without predicates (explore_extra_no_predicate.py, kept beside this file) then showed that the
two extra solutions on the box ({-3..3}^4, {-2..2}^4) are concentrated on four unknowns, the moduli
|alpha|^2 = 132 +- 75 sqrt 3 and 150 +- 75 sqrt 3, which are the largest that occur (corner elements a + u b), all
other entries below 1e-3 of the largest.  The "support 712 of 714" recorded by K3d used a cut of 1e-8 and was a bad
diagnostic.  So the extra dimensions are unknowns at the corner of the box that too few equations determine.

PREDICATE K3h (fixed before this run): q0 = 12, multisets (0,1,6,7) and (0,2,6,8), box A = {-3..3}^4, B = {-2..2}^4.
Let W be the null space (eigenvalues of M^T M below 1e-9 of the largest) and W_in its restriction to the unknowns
that are moduli of elements of {-2..2}^4 (the inner unknowns; count reported).  The rank of W_in is 2, decided by its
singular values: third singular value below 1e-6 of the first; all four are recorded.
Result file followup_abund_4_results.json, never overwritten.
"""
import json, os, sys, itertools
import numpy as np
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "followup_abund_4_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
z = np.exp(2j * np.pi / 12); s3 = np.sqrt(3.0); Z1 = z ** np.arange(4); Z5 = z ** (5 * np.arange(4))
T = np.array([[0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0]], dtype=np.int64)
def mulz(c, e): return c @ np.linalg.matrix_power(T, e % 12).T
def key(c):
    n1 = np.abs(c @ Z1) ** 2; n5 = np.abs(c @ Z5) ** 2
    return np.rint((n1 + n5) / 2).astype(np.int64) * 100003 + np.rint((n1 - n5) / (2 * s3)).astype(np.int64)
A = np.array(list(itertools.product(range(-3, 4), repeat=4)), dtype=np.int64); B = np.array(list(itertools.product(range(-2, 3), repeat=4)), dtype=np.int64)
out = []
for es in ((0, 1, 6, 7), (0, 2, 6, 8)):
    cols = [key((A[:, None, :] + mulz(B, e)[None, :, :]).reshape(-1, 4)) for e in es]
    rows = np.unique(np.concatenate([np.sort(np.stack(cols, 1), 1), np.repeat(key(A), len(B))[:, None], np.tile(key(B), len(A))[:, None]], 1), axis=0)
    allk = np.unique(rows); ix = {int(k): i for i, k in enumerate(allk)}; n = len(allk); G = np.zeros((n, n))
    for r in rows:
        row = {}
        for k in r[:4]: row[ix[int(k)]] = row.get(ix[int(k)], 0) + 1
        for k in r[4:]: row[ix[int(k)]] = row.get(ix[int(k)], 0) - 4
        js = [j for j, v in row.items() if v]
        if js: vs = np.array([row[j] for j in js], float); G[np.ix_(js, js)] += np.outer(vs, vs)
    G[ix[0], ix[0]] += 1
    ev, U = np.linalg.eigh(G); dim = int((ev < 1e-9 * ev[-1]).sum()); W = U[:, :dim]
    inner = sorted({ix[int(k)] for k in key(B)}); sv = np.linalg.svd(W[inner, :], compute_uv=False)
    out.append(dict(exps=list(es), unknowns=n, inner_unknowns=len(inner), null_dim=dim, singular_values_inner=[float(s) for s in sv],
                    rank_inner=int((sv > 1e-6 * sv[0]).sum())))
res = dict(K3h=dict(cases=out, met=all(c["rank_inner"] == 2 for c in out)))
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res))
