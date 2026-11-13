#!/usr/bin/env python3
"""Third follow-up.  K3c of followup_abund_2.py FAILED (dimension 4 against 2 for q0 = 12, multisets (0,1,6,7) and
(0,2,6,8), a and b in {-2..2}^4), and the extra solutions have support on 712 of 714 unknowns, so "support near the
boundary of the box" does not explain it.  K3d's residual threshold 1e-9 also failed (2.9e-8, 9.9e-8); that threshold
was applied to a square root of a rounded quadratic form and is not a finding about the conjugate rules.

Question: box effect or counterexample to Theorem 5.12?  The unknowns are indexed by the exact value of |alpha|^2, so
the condition "f depends only on |alpha|" is enforced only through pairs alpha, beta in the box with equal modulus.
Besides beta = unit * alpha and conjugates there are other such pairs in R (products pi_a pi_b and pi_a conj(pi_b)),
which need larger coefficients.

PREDICATES (fixed before the run):
 K3e  vectorised recomputation, q0 = 12, multiset (0,1,6,7): for the boxes (A, B) = ({-2..2}^4, {-2..2}^4) [must
      reproduce 714 unknowns and dimension 4, as a check of the new code], ({-3..3}^4, {-2..2}^4) and
      ({-4..4}^4, {-2..2}^4): record the dimension.  Predicate: the dimension is 2 for the largest box.
      Exact keys: |alpha|^2 = p + q sqrt 3 with integers p, q obtained by rounding from the two embeddings; the
      rounding distance is recorded and must be below 1e-6 (values are below 1e3, float error below 1e-12).
 K3f  for each box: the number of unordered pairs of box elements (elements a + u b that occur) with equal |alpha|^2
      that are NOT related by multiplication by a 12th root of unity or complex conjugation ("non-trivial collisions").
      No predicate; recorded to see whether the drop in dimension comes with their appearance.
 K3g  whatever the dimension: N_1 and N_5 satisfy every equation exactly in integer arithmetic on (p, q):
      N_1 -> p + q sqrt 3, N_5 -> p - q sqrt 3, i.e. the two integer vectors p and q are both solutions.
Rank rule as before (eigenvalues of M^T M below 1e-9 of the largest).  Stated reason for a run above three minutes,
if it happens: the largest box has 6561 * 625 pairs.  Result file followup_abund_3_results.json, never overwritten.
"""
import json, os, sys, itertools, time
import numpy as np
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "followup_abund_3_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
z = np.exp(2j * np.pi / 12); s3 = np.sqrt(3.0)
Z1 = z ** np.arange(4); Z5 = z ** (5 * np.arange(4))
def key(coef):      # coef: (..., 4) int array -> (p, q) ints and rounding distance
    x1 = coef @ Z1; x5 = coef @ Z5; n1 = np.abs(x1) ** 2; n5 = np.abs(x5) ** 2
    p = (n1 + n5) / 2; q = (n1 - n5) / (2 * s3); pr = np.rint(p); qr = np.rint(q)
    return pr.astype(np.int64), qr.astype(np.int64), float(max(np.abs(p - pr).max(), np.abs(q - qr).max()))
# multiplication by zeta^e on coefficient vectors (basis 1, z, z^2, z^3; z^4 = z^2 - 1)
T = np.array([[0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0]], dtype=np.int64)   # columns: images of basis
def mulz(coef, e):
    M = np.linalg.matrix_power(T, e % 12); return coef @ M.T
es = (0, 1, 6, 7); res = dict(cases=[])
for ra, rb in ((2, 2), (3, 2), (4, 2)):
    t0 = time.time()
    A = np.array(list(itertools.product(range(-ra, ra + 1), repeat=4)), dtype=np.int64)
    B = np.array(list(itertools.product(range(-rb, rb + 1), repeat=4)), dtype=np.int64)
    cols = []; maxd = 0.0; occ = []
    for e in es:
        ub = mulz(B, e); S = A[:, None, :] + ub[None, :, :]; p, q, dd = key(S.reshape(-1, 4)); maxd = max(maxd, dd)
        cols.append(p * 100003 + q); occ.append(S.reshape(-1, 4))
    pa, qa, d1 = key(A); pb, qb, d2 = key(B); maxd = max(maxd, d1, d2)
    ka = np.repeat(pa * 100003 + qa, len(B)); kb = np.tile(pb * 100003 + qb, len(A))
    K = np.sort(np.stack(cols, 1), axis=1); rows = np.unique(np.concatenate([K, ka[:, None], kb[:, None]], 1), axis=0)
    allk = np.unique(rows); n = len(allk); ix = {int(k): i for i, k in enumerate(allk)}
    G = np.zeros((n, n))
    for r in rows:
        row = {}
        for k in r[:4]: row[ix[int(k)]] = row.get(ix[int(k)], 0) + 1
        for k in r[4:]: row[ix[int(k)]] = row.get(ix[int(k)], 0) - 4
        js = [j for j, v in row.items() if v]
        if js:
            vs = np.array([row[j] for j in js], float); G[np.ix_(js, js)] += np.outer(vs, vs)
    G[ix[0], ix[0]] += 1
    ev = np.linalg.eigvalsh(G); dim = int((ev < 1e-9 * ev[-1]).sum())
    pvec = np.array([np.floor_divide(k + 50000, 100003) for k in allk]); qvec = allk - pvec * 100003
    def exact_ok(vec):
        tot = 0
        for r in rows:
            tot = max(tot, abs(sum(vec[ix[int(k)]] for k in r[:4]) - 4 * vec[ix[int(r[4])]] - 4 * vec[ix[int(r[5])]]))
        return int(tot)
    g_ok = exact_ok(pvec) == 0 and exact_ok(qvec) == 0
    # non-trivial collisions among occurring elements
    elems = np.unique(np.concatenate(occ + [A, B]), axis=0); pe, qe, _ = key(elems); ke = pe * 100003 + qe
    orbit = {}
    conjM = np.array([[1, 0, 0, 0], [0, 0, 0, -1], [0, 0, -1, 0], [0, -1, 0, 0]])  # placeholder, replaced below
    def canon(c):
        best = None; x = c.copy()
        for cj in (0, 1):
            y = x if cj == 0 else conj(x)
            for e in range(12):
                t = tuple(int(v) for v in mulz(y[None, :], e)[0])
                if best is None or t < best: best = t
        return best
    # conjugation: zeta -> zeta^-1 = zeta^11 ; images of basis 1, z, z^2, z^3 are z^0, z^11, z^10, z^9
    basis = np.eye(4, dtype=np.int64); Cm = np.stack([mulz(basis[:1], 0)[0], mulz(basis[:1], 11)[0], mulz(basis[:1], 10)[0], mulz(basis[:1], 9)[0]], 1)
    def conj(c): return Cm @ c
    classes = {}
    for c, k in zip(elems, ke): classes.setdefault(int(k), set()).add(canon(c))
    nontriv = sum(len(s) - 1 for s in classes.values() if len(s) > 1)
    res["cases"].append(dict(box_a=ra, box_b=rb, unknowns=n, distinct_equations=int(len(rows)), dim=dim,
                             null_max=float(ev[dim - 1]) if dim else None, kept=float(ev[dim]), rounding_distance=maxd,
                             p_and_q_are_exact_solutions=bool(g_ok), moduli_with_nontrivial_collisions=int(sum(1 for s in classes.values() if len(s) > 1)),
                             extra_orbits_from_collisions=int(nontriv), seconds=round(time.time() - t0, 1)))
    print(res["cases"][-1], flush=True)
res["K3e_met"] = res["cases"][-1]["dim"] == 2 and res["cases"][0]["dim"] == 4 and res["cases"][0]["unknowns"] == 714
res["K3g_met"] = all(c["p_and_q_are_exact_solutions"] for c in res["cases"])
json.dump(res, open(OUT, "w"), indent=1); print(res["K3e_met"], res["K3g_met"])
