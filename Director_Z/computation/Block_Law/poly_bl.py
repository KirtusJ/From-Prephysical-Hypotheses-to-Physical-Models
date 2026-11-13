#!/usr/bin/env python3
"""
Polynomial solutions of the block law (BL), no gauge invariance assumed.

For a block B (entries zeta^E, B*B = d) and a degree k, the unknown is a homogeneous
real polynomial P of degree k on V = R (x) reals, written in the integer coordinates
of R = Z[zeta].  (BL) is evaluated at integer points beta in [-3,3]^(d n) (seed 20261113),
3 * (number of monomials) + 10 points; each evaluation is a linear equation in the
coefficients of P, exact in integers.  The nullity (FLINT, exact) of the sampled
system is an UPPER bound for the dimension of the solutions of degree k.

PREDICATES (fixed before the first run; failures kept).
  H   B*B = d exactly (per case; cases failing H are not used).
  Q1  k = 2: nullity == dim of quadratic forms invariant under the group C_B generated
      by the entries of B (computed independently as symmetric S with M^T S M = S).
  Q2  k in {1,3,4,5,6}: nullity == 0.
  Q3  (control, H false on purpose: B = [[1,1],[1,1]]/, not a block) not evaluated.
  Q4  (control) for the two-input restriction (beta with at most two nonzero entries)
      of Fourier d=q=3, k=3: nullity == 0.  Expected to FAIL (a^3 survives); kept.
No tolerance; result file not overwritten.
"""
import sys, os, json, itertools
import numpy as np, flint
import gauge_bl as g

RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_poly_bl.json")

def monos(n, k):
    return [m for m in itertools.product(range(k + 1), repeat=n) if sum(m) == k]

def evalm(X, ms):
    # X: (K, n) object ints -> (K, len(ms))
    out = np.ones((X.shape[0], len(ms)), dtype=object)
    for j, m in enumerate(ms):
        for i, e in enumerate(m):
            if e:
                out[:, j] = out[:, j] * X[:, i] ** e
    return out

def nullity(q, E, k, rng, maxnz=None):
    n, Mk = g.ring(q); d = len(E)
    ms = monos(n, k)
    K = 3 * len(ms) + 10
    beta = rng.integers(-3, 4, size=(K, d, n))
    if maxnz is not None:
        for i in range(K):
            keep = rng.choice(d, size=maxnz, replace=False)
            for y in range(d):
                if y not in keep:
                    beta[i, y, :] = 0
    A = np.zeros((K, len(ms)), dtype=object)
    for z in range(d):
        o = np.zeros((K, n), dtype=np.int64)
        for y in range(d):
            o += beta[:, y, :] @ Mk[E[z][y] % q].T
        A = A + evalm(o.astype(object), ms)
    for y in range(d):
        A = A - d * evalm(beta[:, y, :].astype(object), ms)
    rk = flint.fmpz_mat(K, len(ms), [int(x) for x in A.ravel()]).rank()
    return len(ms) - rk, len(ms), K

def main():
    if os.path.exists(RESULT):
        sys.exit("refusing to overwrite " + RESULT)
    rng = np.random.default_rng(20261113)
    cases = [(nm, q, E) for nm, q, E, _ in g.CASES]
    out = []
    for nm, q, E in cases:
        n, Mk = g.ring(q)
        okH, qB = g.check_block(E, q, Mk)
        if not okH:
            out.append(dict(case=nm, H=False)); print(out[-1]); continue
        eB = len(g.invariant_forms(n, [Mk[q // qB]] if qB > 1 else []))
        for k in range(1, 7):
            nu, nm_, K = nullity(q, E, k, rng)
            exp = eB if k == 2 else 0
            rec = dict(case=nm, H=True, q=q, d=len(E), order_C_B=qB, k=k, monomials=nm_, points=K,
                       nullity=int(nu), expected=exp, predicate=("Q1" if k == 2 else "Q2"), passed=bool(nu == exp))
            out.append(rec); print(json.dumps(rec), flush=True)
    nu, nm_, K = nullity(3, g.fourier(3, 3), 3, rng, maxnz=2)
    rec = dict(case="Fourier d=q=3, two-input only", k=3, monomials=nm_, points=K, nullity=int(nu), expected=0,
               predicate="Q4", passed=bool(nu == 0))
    out.append(rec); print(json.dumps(rec))
    with open(RESULT, 'x') as f:
        json.dump(out, f, indent=1)
    print("FAILED:", [(r['case'], r.get('k'), r.get('predicate'), r.get('nullity')) for r in out if r.get('passed') is False])

if __name__ == '__main__':
    main()
